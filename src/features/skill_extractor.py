# import spacy

# nlp = spacy.load("en_core_web_sm")

# SKILLS_DB = [
# "python","java","aws","docker","kubernetes",
# "machine learning","pandas","tensorflow",
# "html","css","javascript","react",
# "nodejs","sql","mongodb","django","flask"
# ]

# def clean_text(text):

#     return text.lower()


# def extract_skills(text):

#     doc = nlp(text)

#     found_skills = []

#     for token in doc:

#         if token.text.lower() in SKILLS_DB:
#             found_skills.append(token.text.lower())

#     return list(set(found_skills))














import logging
import re

logger = logging.getLogger(__name__)

# General skill list – har field ke liye
COMMON_SKILLS = [
    # IT & Programming
    "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "swift", "kotlin",
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "spring",
    "sql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp", "docker", "kubernetes",
    "git", "jenkins", "ci/cd", "rest api", "graphql", "microservices",
    
    # Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy",
    "data analysis", "data visualization", "tableau", "power bi",
    
    # Management & Soft Skills
    "project management", "agile", "scrum", "jira", "leadership", "communication",
    "teamwork", "problem solving", "critical thinking", "time management",
    
    # Marketing & Sales
    "digital marketing", "seo", "social media", "content writing", "google analytics",
    "sales", "negotiation", "crm", "lead generation",
    
    # HR & Finance
    "recruitment", "onboarding", "hr policies", "payroll", "accounting", "tally", "gst",
    "financial reporting", "excel", "quickbooks",
    
    # Design
    "photoshop", "illustrator", "figma", "ui/ux", "adobe xd",
]

class AdvancedSkillExtractor:
    def __init__(self):
        self.skills_set = set([s.lower() for s in COMMON_SKILLS])
    
    def extract(self, text):
        if not text:
            return []
        text_lower = text.lower()
        found = set()
        for skill in self.skills_set:
            # Word boundary check for single words
            if ' ' not in skill:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    found.add(skill)
            else:
                if skill in text_lower:
                    found.add(skill)
        logger.info(f"Extracted {len(found)} skills: {list(found)[:10]}")
        return list(found)