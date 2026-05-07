import os
import yaml
import pandas as pd

from src.data.resume_parser import parse_resume
from src.data.jd_parser import parse_job_description


CONFIG_PATH = "configs/data_config.yaml"


def load_config():

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def load_raw_data():

    config = load_config()

    path = config["dataset"]["save_path"]

    train_path = os.path.join(path, "train.parquet")

    df = pd.read_parquet(train_path)

    print("\nDataset columns:", df.columns)

    return df


def preprocess_data(df):

    print("\nCleaning resume text...")

    df["resume_clean"] = df["Resume"].apply(parse_resume)

    print("Cleaning job description...")

    df["jd_clean"] = df["Job_Description"].apply(parse_job_description)

    print("Handling missing values...")

    df = df.dropna(subset=["resume_clean", "jd_clean", "Decision"])

    print("Encoding labels...")

    df["label"] = df["Decision"].apply(
        lambda x: 1 if str(x).lower() == "select" else 0
    )

    return df


def save_processed(df):

    save_path = "data/processed"

    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, "processed_dataset.parquet")

    df.to_parquet(file_path, index=False)

    print(f"\nProcessed dataset saved at {file_path}")


def main():

    print("\nLoading dataset...\n")

    df = load_raw_data()

    print("Dataset shape:", df.shape)

    df = preprocess_data(df)

    print("Processed dataset shape:", df.shape)

    save_processed(df)


if __name__ == "__main__":

    main()