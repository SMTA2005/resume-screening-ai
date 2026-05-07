# import os
# import yaml
# import pandas as pd
# from datasets import load_dataset


# CONFIG_PATH = "configs/data_config.yaml"


# def load_config():
#     with open(CONFIG_PATH, "r") as f:
#         return yaml.safe_load(f)


# def download_dataset():

#     config = load_config()

#     dataset_name = config["dataset"]["huggingface_repo"]
#     save_path = config["dataset"]["save_path"]

#     os.makedirs(save_path, exist_ok=True)

#     print(f"\nDownloading dataset: {dataset_name}\n")

#     dataset = load_dataset(dataset_name)

#     print(dataset)

#     for split in dataset.keys():

#         df = pd.DataFrame(dataset[split])

#         file_path = os.path.join(save_path, f"{split}.parquet")

#         df.to_parquet(file_path, index=False)

#         print(f"{split} saved to {file_path}")

#     print("\nDataset download complete!")


# def dataset_summary():

#     config = load_config()

#     save_path = config["dataset"]["save_path"]

#     print("\nDataset Summary\n")

#     for file in os.listdir(save_path):

#         if file.endswith(".parquet"):

#             path = os.path.join(save_path, file)

#             df = pd.read_parquet(path)

#             print(f"\nFile: {file}")
#             print(f"Shape: {df.shape}")
#             print(f"Columns: {list(df.columns)}")
#             print(df.head(2))


# if __name__ == "__main__":

#     download_dataset()

#     dataset_summary()





# src/data/download_dataset.py (final version)
import yaml
from datasets import load_dataset
import pandas as pd
from pathlib import Path
import logging
from collections import Counter
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_skills(text: str, common_skills: list) -> list:
    text_lower = text.lower()
    found = []
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill)
    return found

def build_job_categories():
    # Common skills ki list (configs/skills_list.txt se le sakte ho)
    # Is list mein wohi skills hon jo resume mein aati hain
    common_skills = [
        "python", "java", "javascript", "react", "angular", "vue", "node.js", "django", "flask",
        "spring", "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
        "sql", "mysql", "postgresql", "mongodb", "redis", "oracle",
        "html", "css", "bootstrap", "tailwind", "figma", "photoshop",
        "android", "ios", "flutter", "react native", "kotlin", "swift",
        "machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy",
        "git", "github", "gitlab", "jira", "confluence",
        "agile", "scrum", "kanban", "tdd", "ci/cd",
        "selenium", "junit", "pytest", "manual testing", "automation",
        "solidity", "web3", "blockchain", "cryptography",
        # ... aur bhi skills
    ]
    
    # Load dataset
    dataset = load_dataset("AzharAli05/Resume-Screening-Dataset")
    df = pd.DataFrame(dataset['train'])

    job_skills = {}
    for _, row in df.iterrows():
        role = row['Role']
        job_desc = row.get('Job_Description', '')
        resume = row.get('Resume', '')
        text = job_desc + " " + resume
        skills = extract_skills(text, common_skills)
        if role not in job_skills:
            job_skills[role] = []
        job_skills[role].extend(skills)

    # Har role ke liye top 10 skills
    job_list = []
    for role, skills in job_skills.items():
        top_skills = [skill for skill, _ in Counter(skills).most_common(10)]
        job_list.append({
            "category": role,
            "skills": ", ".join(top_skills),
            "min_experience": 0,
            "education": ""
        })

    # Save
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(job_list).to_csv(processed_dir / "job_categories.csv", index=False)
    logger.info(f"Saved {len(job_list)} job categories.")

if __name__ == "__main__":
    build_job_categories()