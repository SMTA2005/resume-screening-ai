# import pandas as pd
# import numpy as np

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import precision_score, recall_score, f1_score

# from sklearn.feature_extraction.text import TfidfVectorizer

# import torch
# import torch.nn as nn
# import torch.optim as optim


# DATA_PATH = "data/processed/processed_dataset.parquet"


# class DeepClassifier(nn.Module):

#     def __init__(self, input_dim):

#         super().__init__()

#         self.network = nn.Sequential(

#             nn.Linear(input_dim, 512),
#             nn.ReLU(),

#             nn.Linear(512, 256),
#             nn.ReLU(),

#             nn.Linear(256, 64),
#             nn.ReLU(),

#             nn.Linear(64, 1),
#             nn.Sigmoid()
#         )

#     def forward(self, x):
#         return self.network(x)


# def main():

#     print("Loading dataset...")

#     df = pd.read_parquet(DATA_PATH)

#     texts = df["resume_clean"] + " " + df["jd_clean"]

#     y = df["label"].values

#     print("Building TF-IDF vectors...")

#     vectorizer = TfidfVectorizer(
#         max_features=8000,
#         ngram_range=(1,2)
#     )

#     X = vectorizer.fit_transform(texts).toarray()

#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42
#     )

#     X_train = torch.tensor(X_train).float()
#     X_test = torch.tensor(X_test).float()

#     y_train = torch.tensor(y_train).float().unsqueeze(1)

#     model = DeepClassifier(X_train.shape[1])

#     criterion = nn.BCELoss()

#     optimizer = optim.Adam(model.parameters(), lr=0.001)

#     print("\nTraining deep neural network...\n")

#     for epoch in range(100):

#         optimizer.zero_grad()

#         outputs = model(X_train)

#         loss = criterion(outputs, y_train)

#         loss.backward()

#         optimizer.step()

#         print(f"Epoch {epoch+1} Loss: {loss.item():.4f}")

#     print("\nEvaluating model...\n")

#     preds = model(X_test).detach().numpy()

#     preds = (preds > 0.5).astype(int)

#     precision = precision_score(y_test, preds)
#     recall = recall_score(y_test, preds)
#     f1 = f1_score(y_test, preds)

#     print("Precision:", precision)
#     print("Recall:", recall)
#     print("F1 Score:", f1)


# if __name__ == "__main__":
#     main()





import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import pandas as pd

class ResumeClassifier(nn.Module):
    def __init__(self, num_classes=25):
        super().__init__()
        self.bert = AutoModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(768, num_classes)
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        x = self.dropout(pooled)
        return self.classifier(x)