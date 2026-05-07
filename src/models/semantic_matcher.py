import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = "data/processed/processed_dataset.parquet"


def main():

    print("Loading dataset...")

    df = pd.read_parquet(DATA_PATH)

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    resumes = df["resume_clean"].tolist()
    jds = df["jd_clean"].tolist()

    print("Encoding resumes...")
    resume_emb = model.encode(resumes)

    print("Encoding job descriptions...")
    jd_emb = model.encode(jds)

    print("Computing similarity scores...")

    scores = []

    for r, j in zip(resume_emb, jd_emb):

        sim = cosine_similarity([r], [j])[0][0]

        scores.append(sim)

    df["match_score"] = scores

    print("\nTop 10 matches:\n")

    print(df[["Role","match_score"]].sort_values(
        by="match_score",
        ascending=False
    ).head(10))


if __name__ == "__main__":
    main()