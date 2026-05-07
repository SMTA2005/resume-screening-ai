import pandas as pd
from datasets import load_dataset
from pathlib import Path
import re
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common skills ki comprehensive list (configs/skills_list.txt se bhi le sakte ho)
COMMON_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "swift", 
    "kotlin", "go", "rust", "scala", "perl", "r", "matlab",
    
    # Web Frameworks
    "django", "flask", "fastapi", "spring", "spring boot", "node.js", "express", 
    "react", "angular", "vue", "jquery", "bootstrap", "tailwind",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", 
    "terraform", "ansible", "puppet", "chef", "ci/cd", "github actions",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "elasticsearch",
    "cassandra", "dynamodb", "firebase", "mariadb",
    
    # Data Science & ML
    "machine learning", "deep learning", "ai", "nlp", "tensorflow", "pytorch",
    "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
    "data analysis", "data visualization", "tableau", "power bi",
    
    # Mobile Development
    "android", "ios", "flutter", "react native", "xamarin", "swiftui",
    
    # Testing
    "selenium", "junit", "pytest", "mockito", "cucumber", "testng",
    
    # Version Control
    "git", "github", "gitlab", "bitbucket", "svn",
    
    # Soft Skills
    "communication", "leadership", "team management", "project management",
    "agile", "scrum", "kanban", "jira", "confluence",
    
    # Others
    "rest api", "graphql", "microservices", "design patterns", "tdd",
    "excel", "powerpoint", "word", "outlook"
]

def extract_skills(text):
    text_lower = text.lower()
    skills_found = []
    for skill in COMMON_SKILLS:
        # Word boundary check
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills_found.append(skill)
    return skills_found

def build_categories():
    # Load dataset
    logger.info("Loading dataset...")
    dataset = load_dataset("AzharAli05/Resume-Screening-Dataset")
    df = pd.DataFrame(dataset['train'])
    logger.info(f"Dataset loaded with {len(df)} rows")
    
    # Dictionary to store skills per role
    role_skills = {}
    
    for idx, row in df.iterrows():
        role = row['Role']
        job_desc = row.get('Job_Description', '')
        resume = row.get('Resume', '')
        combined_text = job_desc + " " + resume
        
        skills = extract_skills(combined_text)
        
        if role not in role_skills:
            role_skills[role] = []
        role_skills[role].extend(skills)
    
    # For each role, get top 10 most frequent skills
    categories = []
    for role, skills in role_skills.items():
        skill_counts = Counter(skills)
        top_skills = [skill for skill, _ in skill_counts.most_common(10)]
        categories.append({
            "category": role,
            "skills": ", ".join(top_skills)
        })
    
    # Save to CSV
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "job_categories.csv"
    pd.DataFrame(categories).to_csv(output_file, index=False)
    logger.info(f"Saved {len(categories)} job categories to {output_file}")
    
    # Also save a readable format
    print("\n=== Generated Job Categories ===")
    for cat in categories:
        print(f"{cat['category']}: {cat['skills']}")

if __name__ == "__main__":
    build_categories()