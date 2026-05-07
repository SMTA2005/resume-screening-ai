import tempfile
import os
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from docx import Document
import io
import PyPDF2

def extract_text_from_bytes(file_bytes, filename):
    ext = filename.split('.')[-1].lower()
    
    if ext == 'pdf':
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = " ".join([page.extract_text() or "" for page in reader.pages])
            if text.strip():
                return text
        except:
            pass
        # Agar normal PDF se nahi mila to OCR
        return ocr_pdf(file_bytes)
    
    elif ext == 'docx':
        doc = Document(io.BytesIO(file_bytes))
        return " ".join([para.text for para in doc.paragraphs])
    
    elif ext == 'txt':
        return file_bytes.decode('utf-8')
    
    elif ext in ['png', 'jpg', 'jpeg']:
        img = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(img)
    
    else:
        return ""

def ocr_pdf(pdf_bytes):
    images = convert_from_bytes(pdf_bytes, dpi=200)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text