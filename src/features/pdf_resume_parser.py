import fitz  # PyMuPDF
import easyocr
import numpy as np
import PyPDF2
import logging

logger = logging.getLogger(__name__)

# Ek baar EasyOCR reader load karo (global)
try:
    reader = easyocr.Reader(['en'], gpu=False)
    logger.info("EasyOCR reader loaded successfully")
except Exception as e:
    logger.error(f"EasyOCR load failed: {e}")
    reader = None

def parse_resume_pdf(file_path: str) -> str:
    """
    PDF file se text extract karta hai.
    Pehle PyPDF2 try karega (text-based PDFs ke liye).
    Agar fail ho to EasyOCR se scanned/image PDF read karega.
    """
    # ---------- STEP 1: Try normal text extraction (PyPDF2) ----------
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                logger.info(f"Extracted {len(text)} chars using PyPDF2")
                return text
    except Exception as e:
        logger.warning(f"PyPDF2 failed: {e}")

    # ---------- STEP 2: Fallback to OCR (EasyOCR) ----------
    if reader is None:
        logger.error("EasyOCR not available, cannot process scanned PDF")
        return ""

    logger.info("Scanned PDF detected. Running EasyOCR...")
    try:
        # Open PDF with PyMuPDF for high-quality rendering
        doc = fitz.open(file_path)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Render page to image (zoom factor 2 for ~144 DPI)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            # Run EasyOCR
            result = reader.readtext(img, detail=0, paragraph=True)
            full_text += " ".join(result) + "\n"
        doc.close()
        logger.info(f"EasyOCR extracted {len(full_text)} chars")
        return full_text
    except Exception as e:
        logger.error(f"EasyOCR failed: {e}")
        return ""

def parse_resume_image(image_path: str) -> str:
    """Direct image file (PNG/JPG) ke liye OCR"""
    if reader is None:
        return ""
    try:
        result = reader.readtext(image_path, detail=0, paragraph=True)
        return " ".join(result)
    except Exception as e:
        logger.error(f"Image OCR failed: {e}")
        return ""