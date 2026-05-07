import torch
import pandas as pd
import torch.nn as nn
import torch.optim as optim

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

from src.models.neural.matching_network import MatchingNetwork


DATA_PATH = "data/processed/processed_dataset.parquet"


def main():

    df = pd.read_parquet(DATA_PATH)

    X_resume = df["resume_clean"]
    X_jd = df["jd_clean"]
    y = df["label"]

    Xr_train, Xr_test, Xj_train, Xj_test, y_train, y_test = train_test_split(
        X_resume,
        X_jd,
        y,
        test_size=0.2,
        random_state=42
    )

    model = MatchingNetwork()

    criterion = nn.BCELoss()

    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    print("Training neural model...")

    for epoch in range(70):

        optimizer.zero_grad()

        outputs = model(
            Xr_train.tolist(),
            Xj_train.tolist()
        )

        targets = torch.tensor(
            y_train.values,
            dtype=torch.float32
        ).unsqueeze(1)

        loss = criterion(outputs, targets)

        loss.backward()

        optimizer.step()

        print("Epoch:", epoch, "Loss:", loss.item())

    print("Evaluating...")

    preds = model(
        Xr_test.tolist(),
        Xj_test.tolist()
    )

    preds = (preds.detach().numpy() > 0.5).astype(int)

    precision = precision_score(y_test, preds)
    recall = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)

    print("\nPrecision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


if __name__ == "__main__":
    main()