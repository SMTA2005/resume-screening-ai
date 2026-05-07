import os
from pathlib import Path
import logging
import tempfile
import time
import uuid
from fastapi import BackgroundTasks
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Resume Screening API")
app.state.limiter = app.add_exception_handler(429, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import modules
from src.features.pdf_resume_parser import parse_resume_pdf
from src.features.skill_extractor import AdvancedSkillExtractor
from src.models.hybrid_matcher import HybridMatcher
from src.utils.file_parser import extract_text_from_docx_bytes  # naya import

skill_extractor = AdvancedSkillExtractor()
matcher = HybridMatcher()

# ---------- Conversion function for images and txt only (DOCX ab alag) ----------
def convert_to_pdf(file_bytes: bytes, original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    
    if ext == '.pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file_bytes)
            return tmp.name
    
    elif ext == '.txt':
        from fpdf import FPDF
        text = file_bytes.decode('utf-8', errors='replace')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            try:
                pdf.cell(0, 10, txt=line[:200], ln=True)
            except:
                safe = line.encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(0, 10, txt=safe[:200], ln=True)
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
        pdf.output(temp_pdf)
        return temp_pdf
    
    elif ext in ['.png', '.jpg', '.jpeg']:
        import img2pdf
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as img_tmp:
            img_tmp.write(file_bytes)
            img_path = img_tmp.name
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
        with open(temp_pdf, 'wb') as f:
            f.write(img2pdf.convert(img_path, dpi=300))
        os.unlink(img_path)
        return temp_pdf
    
    else:
        raise ValueError(f"Unsupported format for conversion: {ext}")

# ------------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.2f}s)")
    return response

# In-memory store
jobs = {}

# ---------- Background processing (works for both PDF and direct text) ----------
async def process_resume_background(job_id: str, text: str):
    """Direct text se processing karega (PDF conversion already done or direct text)"""
    try:
        logger.info(f"Processing job {job_id}, text length: {len(text)}")
        if not text or len(text.strip()) == 0:
            jobs[job_id] = {"status": "failed", "error": "No text extracted"}
            return
        
        skills = skill_extractor.extract(text)
        matches = matcher.match(skills, text)
        jobs[job_id] = {
            "status": "completed",
            "result": {
                "matches": matches,
                "skills": skills[:10] if skills else []
            }
        }
        logger.info(f"Job {job_id} completed with {len(matches)} matches")
    except Exception as e:
        logger.exception(f"Job {job_id} failed")
        jobs[job_id] = {"status": "failed", "error": str(e)}

# ---------- Async upload endpoint ----------
@app.post("/upload_resume_async")
async def upload_resume_async(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_bytes = await file.read()
    job_id = str(uuid4())
    jobs[job_id] = {"status": "processing"}
    
    file_ext = Path(file.filename).suffix.lower()
    
    # DOCX: direct text extraction (no PDF conversion)
    if file_ext == '.docx':
        text = extract_text_from_docx_bytes(file_bytes)
        if not text:
            jobs[job_id] = {"status": "failed", "error": "Could not extract text from DOCX"}
            return {"job_id": job_id}
        background_tasks.add_task(process_resume_background, job_id, text)
        return {"job_id": job_id}
    
    # PDF, TXT, PNG, JPG: convert to PDF first, then parse
    try:
        pdf_path = convert_to_pdf(file_bytes, file.filename)
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": f"Conversion failed: {str(e)}"}
        return {"job_id": job_id}
    
    # Parse PDF to get text
    try:
        text = parse_resume_pdf(pdf_path)
        os.unlink(pdf_path)  # cleanup
        if not text:
            jobs[job_id] = {"status": "failed", "error": "No text extracted from PDF"}
            return {"job_id": job_id}
        background_tasks.add_task(process_resume_background, job_id, text)
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
    
    return {"job_id": job_id}

# ---------- Status check ----------
@app.get("/job_status/{job_id}")
async def job_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job

# ---------- Health ----------
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Resume Screening API"}