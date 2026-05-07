# import re


# def clean_text(text: str):

#     if text is None:
#         return ""

#     text = text.lower()

#     text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# def parse_job_description(jd_text):

#     cleaned = clean_text(jd_text)

#     return cleaned



import re
from typing import List, Dict, Optional

def extract_skills_from_jd(text: str) -> List[str]:
    """
    Extract skills from job description text.
    Yeh ek basic implementation hai. Aap chahein to skill extractor feature use kar sakte hain.
    """
    # Common skills ki list (aap isko alag file se bhi le sakte hain)
    common_skills = [
        "python", "java", "javascript", "react", "angular", "node.js", "django", "flask",
        "sql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp", "docker", "kubernetes",
        "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "pandas", "numpy",
        "tableau", "power bi", "excel", "communication", "leadership", "project management",
        "agile", "scrum", "jira", "git", "jenkins", "ci/cd", "terraform", "ansible"
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        # Simple word boundary check
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return found_skills

def extract_min_experience(text: str) -> Optional[float]:
    """
    Extract minimum years of experience from job description.
    Examples: "5+ years", "minimum 3 years", "3-5 years"
    """
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience',
        r'minimum\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)[-\s]+\d+\s*(?:years?|yrs?)',  # for ranges like 3-5 years, take minimum
        r'experience\s*[:\-]?\s*(\d+)\+?\s*(?:years?|yrs?)'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return float(match.group(1))
    
    return None

def extract_education_req(text: str) -> List[str]:
    """
    Extract education requirements from job description.
    Returns list of education levels mentioned.
    """
    education_keywords = [
        "bachelor", "b.s.", "b.tech", "master", "m.s.", "m.tech", "ph.d", "phd",
        "associate", "diploma", "high school", "graduate", "postgraduate"
    ]
    
    text_lower = text.lower()
    found_education = []
    
    for edu in education_keywords:
        pattern = r'\b' + re.escape(edu) + r'\b'
        if re.search(pattern, text_lower):
            found_education.append(edu)
    
    return found_education

def parse_job_description(text: str) -> Dict:
    """Extract structured info from job description."""
    skills = extract_skills_from_jd(text)
    experience = extract_min_experience(text)
    education = extract_education_req(text)
    
    return {
        "skills": skills,
        "min_experience": experience,
        "education": education,
        "full_text": text
    }

def parse_job_description(text: str) -> Dict:
    """Extract structured info from job description."""
    # Extract required skills, experience, education
    skills = extract_skills_from_jd(text)
    experience = extract_min_experience(text)
    education = extract_education_req(text)
    
    return {
        "skills": skills,
        "min_experience": experience,
        "education": education,
        "full_text": text
    }