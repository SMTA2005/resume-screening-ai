import os
import sys

# Project paths set karein taake modules mil jayein
sys.path.append(os.getcwd())

from src.features.pdf_resume_parser import parse_resume_pdf
from src.features.skill_extractor import extract_skills, clean_text

# APNE RESUME KA PATH YAHAN LIKHEIN
test_resume = "D:/png2pdf.pdf" 

def test_everything():
    print("--- 🛠️ STARTING DEBUG TEST ---")
    
    if not os.path.exists(test_resume):
        print(f"❌ Error: File nahi mili is path par: {test_resume}")
        return

    # 1. Test PDF Parsing
    print("\n1. Parsing PDF...")
    raw_text = parse_resume_pdf(test_resume)
    print(f"Raw Text Length: {len(raw_text)} characters")
    
    # AGAR RAW TEXT KHALI HAI YA BOHAT KAM HAI TO TESSERACT KA MASLA HAI
    print("\n--- FIRST 500 CHARACTERS OF EXTRACTED TEXT ---")
    print(raw_text[:500])
    print("----------------------------------------------")

    # 2. Test Cleaning
    print("\n2. Cleaning Text...")
    cleaned = clean_text(raw_text)
    
    # 3. Test Skill Extraction
    print("\n3. Extracting Skills...")
    skills = extract_skills(cleaned)
    print(f"Skills Found: {skills}")

    if "python" in skills and len(skills) == 1:
        print("\n⚠️ WARNING: Sirf 'python' mila. Iska matlab baqi skills text mein nazar nahi aa rahe.")
    elif len(skills) > 3:
        print("\n✅ SUCCESS: Multiple skills mil gaye! Masla API ya Score logic mein tha.")

if __name__ == "__main__":
    test_everything()