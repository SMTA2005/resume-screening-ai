import pandas as pd
from datasets import load_dataset
from pathlib import Path
import re
from collections import Counter

def extract_skills(text, common_skills):
    if not isinstance(text, str):
        return []
    text = text.lower()
    found = []
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.append(skill)
    return found

def main():
    # Common skills ki list (aap configs/skills_list.txt se le sakte ho)
    with open("configs/skills_list.txt") as f:
        common_skills = [line.strip().lower() for line in f if line.strip()]
    
    # Dataset load karo
    dataset = load_dataset("AzharAli05/Resume-Screening-Dataset")
    df = pd.DataFrame(dataset['train'])
    
    # Har role ke liye skills accumulate karo
    role_skills = {}
    for _, row in df.iterrows():
        role = row['Role']
        job_desc = row.get('Job_Description', '')
        resume = row.get('Resume', '')
        text = f"{job_desc} {resume}"
        skills = extract_skills(text, common_skills)
        if role not in role_skills:
            role_skills[role] = []
        role_skills[role].extend(skills)
    
    # Har role ke top 10 skills
    categories = []
    for role, skills in role_skills.items():
        top_skills = [skill for skill, _ in Counter(skills).most_common(10)]
        categories.append({
            "category": role,
            "skills": ", ".join(top_skills),
            "min_experience": 0,  # aap experience bhi extract kar sakte ho
            "education": ""
        })
    
    # Save CSV
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "job_categories.csv"
    pd.DataFrame(categories).to_csv(output_file, index=False)
    print(f"Saved {len(categories)} categories to {output_file}")

if __name__ == "__main__":
    main()