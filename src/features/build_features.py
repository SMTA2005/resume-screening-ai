import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.features.embeddings import EmbeddingModel
from src.features.skill_features import compute_skill_features


DATA_PATH = "data/processed/processed_dataset.parquet"
SAVE_PATH = "data/processed/matching_features.parquet"


def load_dataset():

    print("Loading processed dataset...")

    df = pd.read_parquet(DATA_PATH)

    return df


# ---------------- EMBEDDING SIMILARITY ----------------

def compute_embedding_similarity(df):

    print("Computing embedding similarity...")

    model = EmbeddingModel()

    resume_embeddings = model.encode(df["resume_clean"].tolist())
    jd_embeddings = model.encode(df["jd_clean"].tolist())

    similarities = []

    for i in tqdm(range(len(df))):

        sim = cosine_similarity(
            resume_embeddings[i].reshape(1, -1),
            jd_embeddings[i].reshape(1, -1)
        )[0][0]

        similarities.append(sim)

    df["embedding_similarity"] = similarities

    return df


# ---------------- TFIDF SIMILARITY ----------------

def compute_tfidf_similarity(df):

    print("Computing TFIDF similarity...")

    vectorizer = TfidfVectorizer(max_features=5000)

    corpus = df["resume_clean"].tolist() + df["jd_clean"].tolist()

    tfidf = vectorizer.fit_transform(corpus)

    resume_vec = tfidf[:len(df)]
    jd_vec = tfidf[len(df):]

    similarities = []

    for i in tqdm(range(len(df))):

        sim = cosine_similarity(resume_vec[i], jd_vec[i])[0][0]

        similarities.append(sim)

    df["tfidf_similarity"] = similarities

    return df


# ---------------- KEYWORD OVERLAP ----------------

def keyword_overlap(df):

    print("Computing keyword overlap...")

    overlaps = []

    for i in range(len(df)):

        resume_words = set(df["resume_clean"].iloc[i].split())
        jd_words = set(df["jd_clean"].iloc[i].split())

        overlap = len(resume_words.intersection(jd_words))
        total = len(jd_words) + 1

        overlaps.append(overlap / total)

    df["keyword_overlap"] = overlaps

    return df


# ---------------- TEXT LENGTH RATIO ----------------

def text_length_ratio(df):

    print("Computing length ratio...")

    ratios = []

    for i in range(len(df)):

        r = len(df["resume_clean"].iloc[i])
        j = len(df["jd_clean"].iloc[i]) + 1

        ratios.append(r / j)

    df["length_ratio"] = ratios

    return df


# ---------------- ROLE MATCH ----------------

def role_match(df):

    print("Computing role match score...")

    scores = []

    for i in range(len(df)):

        role = str(df["Role"].iloc[i]).lower()
        resume = df["resume_clean"].iloc[i]

        if role in resume:
            scores.append(1)
        else:
            scores.append(0)

    df["role_match"] = scores

    return df


# ---------------- FEATURE TABLE ----------------

def build_feature_table(df):

    print("Building final feature table...")

    features = df[[
        "embedding_similarity",
        "tfidf_similarity",
        "keyword_overlap",
        "length_ratio",
        "role_match",
        "skill_overlap",
        "skill_match_ratio",
        "jd_skill_count",
        "label"
    ]]

    return features


# ---------------- SAVE FEATURES ----------------

def save_features(features):

    os.makedirs("data/processed", exist_ok=True)

    features.to_parquet(SAVE_PATH, index=False)

    print(f"\nFeatures saved to {SAVE_PATH}")


# ---------------- MAIN PIPELINE ----------------

def main():

    df = load_dataset()

    df = compute_embedding_similarity(df)

    df = compute_tfidf_similarity(df)

    df = keyword_overlap(df)

    df = text_length_ratio(df)

    df = role_match(df)

    df = compute_skill_features(df)

    features = build_feature_table(df)

    save_features(features)


if __name__ == "__main__":

    main()