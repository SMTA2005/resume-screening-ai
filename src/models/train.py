import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from src.models.ranking_model import build_model
from src.models.evaluate import evaluate_model


DATA_PATH = "data/processed/matching_features.parquet"
MODEL_PATH = "models_saved/matching_model.pkl"


def load_features():

    print("Loading feature dataset...")

    df = pd.read_parquet(DATA_PATH)

    return df


def split_data(df):

    X = df.drop("label", axis=1)
    y = df["label"]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def train():

    df = load_features()

    X_train, X_test, y_train, y_test = split_data(df)

    model = build_model()

    print("\nTraining model...\n")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    precision, recall, f1 = evaluate_model(y_test, predictions)

    if precision >= 0.95 and recall >= 0.95 and f1 >= 0.95:

        os.makedirs("models_saved", exist_ok=True)

        joblib.dump(model, MODEL_PATH)

        print("\nModel saved successfully!")

    else:

        print("\nModel NOT saved. Metrics below threshold.")


if __name__ == "__main__":

    train()