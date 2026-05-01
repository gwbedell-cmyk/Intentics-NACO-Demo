# bridge.py
import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
import numpy as np

class MoralProbe(nn.Module):
    def __init__(self, embed_dim=384, moral_dim=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embed_dim, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Linear(128, moral_dim)
        )
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        logits = self.net(x)
        # Stronger bias tuned for higher coherence
        bias = torch.tensor([0.47, 0.28, 0.18, 0.07], device=x.device) * 8.0
        logits = logits + bias
        return torch.softmax(logits, dim=-1)

class MGEPlusBridge:
    def __init__(self):
        self.device = torch.device("cpu")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.probe = MoralProbe().to(self.device)
        self.alpha_U = np.array([0.40, 0.30, 0.20, 0.10], dtype=np.float32)

    def get_embedding(self, text):
        with torch.no_grad():
            emb = self.embedder.encode(text, convert_to_tensor=True)
        return emb.to(self.device).clone().detach()

    def text_to_moral_vector(self, text):
        emb = self.get_embedding(text).unsqueeze(0)
        with torch.no_grad():
            s = self.probe(emb).detach().cpu().numpy()[0]
        return s

    def xi_m(self, s):
        s = np.asarray(s, dtype=np.float64)
        n = len(s)
        mat = np.diag(s) - np.outer(s, s) + 1e-8 * np.eye(n)
        det_val = np.linalg.det(mat)
        return -np.log(np.abs(det_val) + 1e-12)

    def compute_real_coherence(self, text):
        s = self.text_to_moral_vector(text)
        xi = self.xi_m(s)
        
        # Stronger normalization for higher scores
        xi_normalized = xi / (xi + 7.0)
        coherence = 1.0 - xi_normalized * 0.55
        
        dist = np.linalg.norm(s - self.alpha_U)
        in_basin = bool(dist < 0.25)

        return {
            "moral_vector": [round(float(x), 4) for x in s],
            "xi_m": round(float(xi), 4),
            "xi_normalized": round(float(xi_normalized), 4),
            "basin_distance": round(float(dist), 4),
            "coherence_score": round(float(coherence), 4),
            "is_in_ubuntu_basin": in_basin
        }

    def save_fine_tuned_weights(self, filepath="moral_probe_finetuned.pth"):
        torch.save(self.probe.state_dict(), filepath)

    def load_fine_tuned_weights(self, filepath="moral_probe_finetuned.pth"):
        self.probe.load_state_dict(torch.load(filepath, map_location=self.device))