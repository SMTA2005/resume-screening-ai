import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer


class MatchingNetwork(nn.Module):

    def __init__(self):

        super().__init__()

        self.encoder = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.fc = nn.Sequential(

            nn.Linear(1, 32),
            nn.ReLU(),

            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, resume_texts, jd_texts):

        resume_emb = self.encoder.encode(
            resume_texts,
            convert_to_tensor=True
        )

        jd_emb = self.encoder.encode(
            jd_texts,
            convert_to_tensor=True
        )

        similarity = torch.cosine_similarity(
            resume_emb,
            jd_emb
        ).unsqueeze(1)

        output = self.fc(similarity)

        return output