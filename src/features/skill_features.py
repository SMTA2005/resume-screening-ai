# import os


# SKILL_FILE = "configs/skills_list.txt"


# def load_skills():
#     """
#     Load skills from config file
#     """

#     if not os.path.exists(SKILL_FILE):
#         raise FileNotFoundError(
#             f"{SKILL_FILE} not found. Please create the skills list file."
#         )

#     with open(SKILL_FILE, "r", encoding="utf-8") as f:
#         skills = [line.strip().lower() for line in f.readlines() if line.strip()]

#     print(f"{len(skills)} skills loaded")

#     return skills


# # ----------------------------------------------------


# def extract_skills(text, skills):
#     """
#     Extract skills from a given text
#     """

#     text = str(text).lower()

#     found_skills = []

#     for skill in skills:

#         if skill in text:
#             found_skills.append(skill)

#     return set(found_skills)


# # ----------------------------------------------------


# def compute_skill_features(df):
#     """
#     Compute skill overlap features between resume and job description
#     """

#     print("Computing skill features...")

#     skills = load_skills()

#     skill_overlap_list = []
#     skill_match_ratio_list = []
#     jd_skill_coverage_list = []

#     for i in range(len(df)):

#         resume_text = df["resume_clean"].iloc[i]
#         jd_text = df["jd_clean"].iloc[i]

#         resume_skills = extract_skills(resume_text, skills)
#         jd_skills = extract_skills(jd_text, skills)

#         overlap = len(resume_skills.intersection(jd_skills))

#         jd_skill_count = len(jd_skills)

#         if jd_skill_count == 0:
#             ratio = 0
#         else:
#             ratio = overlap / jd_skill_count

#         skill_overlap_list.append(overlap)
#         skill_match_ratio_list.append(ratio)
#         jd_skill_coverage_list.append(jd_skill_count)

#     df["skill_overlap"] = skill_overlap_list
#     df["skill_match_ratio"] = skill_match_ratio_list
#     df["jd_skill_count"] = jd_skill_coverage_list

#     print("Skill features created")

#     return df




from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_skill_embeddings(skills: List[str]) -> np.ndarray:
    """Convert skills to vector embeddings."""
    return model.encode(skills)

def semantic_similarity(resume_skills: List[str], job_skills: List[str]) -> float:
    """Find semantic similarity between skill sets."""
    if not resume_skills or not job_skills:
        return 0.0
    
    resume_emb = model.encode(resume_skills)
    job_emb = model.encode(job_skills)
    
    # Average embedding
    resume_vec = np.mean(resume_emb, axis=0)
    job_vec = np.mean(job_emb, axis=0)
    
    # Cosine similarity
    similarity = np.dot(resume_vec, job_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(job_vec))
    return float(similarity)