# import pandas as pd

# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from src.features.experience_extractor import extract_experience

# from src.features.skill_extractor import extract_skills


# DATA_PATH = "data/processed/processed_dataset.parquet"


# def skill_overlap(resume, jd):

#     r = set(extract_skills(resume))
#     j = set(extract_skills(jd))

#     if len(j) == 0:
#         return 0

#     return len(r.intersection(j)) / len(j)

# def experience_score(resume, jd):

#     r_exp = extract_experience(resume)
#     j_exp = extract_experience(jd)

#     if j_exp == 0:
#         return 0.5

#     return min(r_exp / j_exp, 1)


# def main():

#     df = pd.read_parquet(DATA_PATH)

#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     resumes = df["resume_clean"].tolist()
#     jds = df["jd_clean"].tolist()

#     resume_emb = model.encode(resumes)
#     jd_emb = model.encode(jds)

#     final_scores = []

#     for i in range(len(df)):

#         semantic = cosine_similarity(
#             [resume_emb[i]],
#             [jd_emb[i]]
#         )[0][0]

#         skill_score = skill_overlap(
#             resumes[i],
#             jds[i]
#         )

#         exp_score = experience_score(resumes[i], jds[i])

#         final = (0.6 * semantic +0.25 * skill_score + 0.15 * exp_score)

#         final_scores.append(final)

#     df["final_score"] = final_scores

#     print("\nTop Matches:\n")

#     print(
#         df[["Role","final_score"]]
#         .sort_values(by="final_score",ascending=False)
#         .head(10)
#     )


# if __name__ == "__main__":
#     main()
















import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import logging
import pandas as pd
from src.features.experience_extractor import extract_total_experience

logger = logging.getLogger(__name__)

# Core skills (double weight)
CORE_SKILLS = {
    "python", "java", "javascript", "react", "angular", "vue",
    "django", "spring", "node.js", "flask",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "sql", "mongodb", "postgresql", "mysql",
    "tensorflow", "pytorch", "machine learning", "deep learning",
    "android", "ios", "flutter", "react native"
}

class HybridMatcher:
    def __init__(self):
        self.jobs = []
        self.load_job_categories()
    
    def load_job_categories(self):
        csv_path = Path("data/processed/job_categories.csv")
        if not csv_path.exists():
            logger.error(f"Job categories file not found: {csv_path}")
            logger.info("Please run src.data.build_categories first")
            self.jobs = []
            return
        
        df = pd.read_csv(csv_path)
        self.jobs = []
        for _, row in df.iterrows():
            skills_str = row.get('skills', '')
            if pd.isna(skills_str):
                skills_list = []
            else:
                skills_list = [s.strip().lower() for s in skills_str.split(',') if s.strip()]
            
            category = row.get('category', 'Unknown')
            if pd.isna(category):
                category = 'Unknown'
            
            self.jobs.append({
                'category': str(category),
                'skills': skills_list
            })
        
        logger.info(f"Loaded {len(self.jobs)} job categories")
    
    def match(self, resume_skills, resume_text):
        if not isinstance(resume_skills, list):
            resume_skills = []
        
        resume_skills = [s.lower().strip() for s in resume_skills if s]
        resume_skills_set = set(resume_skills)
        
        # Experience
        exp_years = extract_total_experience(resume_text) or 0
        has_cert = 'certified' in resume_text.lower() or 'certification' in resume_text.lower()
        
        results = []
        
        for job in self.jobs:
            job_skills = job.get('skills', [])
            if not isinstance(job_skills, list):
                job_skills = []
            
            # Calculate weighted score
            total_weight = 0
            matched_weight = 0
            matched_skills = []
            
            for skill in job_skills:
                weight = 2 if skill in CORE_SKILLS else 1
                total_weight += weight
                if skill in resume_skills_set:
                    matched_weight += weight
                    matched_skills.append(skill)
            
            if total_weight == 0:
                continue
            
            base_score = matched_weight / total_weight
            
            # Bonuses (max 0.15)
            bonus = 0.0
            if exp_years >= 3:  # seniority
                bonus += 0.05
            if has_cert:
                bonus += 0.05
            if 'senior' in resume_text.lower() or 'lead' in resume_text.lower():
                bonus += 0.05
            
            final_score = min(base_score + bonus, 1.0)
            
            # Threshold - only show good matches
            if final_score >= 0.35:  # 50% threshold
                results.append({
                    'category': job['category'],
                    'match_score': round(final_score, 2),
                    'matched_skills': matched_skills
                })
        
        # Sort by score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:5]  # top 5