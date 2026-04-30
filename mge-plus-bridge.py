# mge_plus_bridge.py
import numpy as np
import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
from typing import Dict
from datetime import datetime
import json

class MoralProbe(nn.Module):
    def __init__(self, embed_dim: int = 384, moral_dim: int = 4):
        super().__init__()
        self.proj = nn.Linear(embed_dim, moral_dim)
        nn.init.xavier_uniform_(self.proj.weight)
        nn.init.zeros_(self.proj.bias)

    def forward(self, emb: torch.Tensor) -> torch.Tensor:
        logits = self.proj(emb)
        return torch.softmax(logits, dim=-1)

class MGEPlusBridge:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.probe = MoralProbe()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.probe.to(self.device)
        self.eps = 1e-6
        self.alpha_U = np.array([0.40, 0.30, 0.20, 0.10], dtype=np.float32)

    def text_to_moral_vector(self, text: str) -> np.ndarray:
        if not text.strip():
            return self.alpha_U.copy()
        embedding = self.embedder.encode(text, convert_to_tensor=True)
        embedding = embedding.unsqueeze(0).to(self.device)
        with torch.no_grad():
            s = self.probe(embedding).cpu().numpy()[0]
        return s.astype(np.float32)

    def xi_m(self, s: np.ndarray) -> float:
        s = np.asarray(s, dtype=np.float64).reshape(-1)
        n = len(s)
        mat = np.diag(s) - np.outer(s, s) + self.eps * np.eye(n)
        det_val = np.linalg.det(mat)
        return -np.log(np.abs(det_val) + 1e-12)

    def basin_distance(self, s: np.ndarray) -> float:
        return np.linalg.norm(s - self.alpha_U)

    def compute_real_coherence(self, text: str) -> Dict:
        s = self.text_to_moral_vector(text)
        xi = self.xi_m(s)
        dist = self.basin_distance(s)
        normalized_score = np.clip(1.0 / (1.0 + xi), 0.0, 1.0)
        return {
            "moral_vector": s.tolist(),
            "xi_m": float(xi),
            "basin_distance_to_alpha_U": float(dist),
            "coherence_score": float(normalized_score),
            "is_in_ubuntu_basin": dist < 0.25,
            "timestamp": datetime.now().isoformat()
        }
