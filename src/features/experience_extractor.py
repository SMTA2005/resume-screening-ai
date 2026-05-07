# import re

# def extract_experience(text):

#     text = text.lower()

#     pattern = r'(\d+)\+?\s*(years|yrs)\s*(of)?\s*(experience)?'

#     matches = re.findall(pattern, text)

#     years = []

#     for m in matches:
#         years.append(int(m[0]))

#     if len(years) == 0:
#         return 0

#     return max(years)



import re
from typing import Optional

def extract_total_experience(text: str) -> Optional[float]:
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience',
        r'experience\s*[:\-]?\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'total\s+experience\s*[:\-]?\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)\s+in\s+(?:\w+\s+)?(?:development|engineering|it|software)'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return float(match.group(1))
    
    # Agar specific number na mile to common phrases check karo
    if any(word in text_lower for word in ['fresher', 'entry level', '0 years']):
        return 0.0
    elif any(word in text_lower for word in ['senior', 'lead', '10+']):
        return 8.0  # default senior
    
    return None