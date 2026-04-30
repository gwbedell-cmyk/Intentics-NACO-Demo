# fine_tune_moral_probe.py
import torch
import torch.nn.functional as F
from mge_plus_bridge import MGEPlusBridge
import json
from datetime import datetime

def load_training_data(path="training_data.json"):
    with open(path, "r") as f:
        return json.load(f)

bridge = MGEPlusBridge()
optimizer = torch.optim.Adam(bridge.probe.parameters(), lr=0.001)

def fine_tune_epoch(data):
    total_loss = 0
    for item in data:
        text = item["text"]
        target = torch.tensor(item["target_s"], dtype=torch.float32).unsqueeze(0).to(bridge.device)
        
        # Forward
        emb = bridge.embedder.encode(text, convert_to_tensor=True).unsqueeze(0).to(bridge.device)
        pred = bridge.probe(emb)
        
        # Loss: KL divergence + small L2 regularization
        loss = F.kl_div(pred.log(), target, reduction='batchmean') + 0.001 * torch.norm(pred - target)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(data)

# =============== RUN TRAINING ===============
if __name__ == "__main__":
    data = load_training_data()
    print(f"Loaded {len(data)} training examples. Starting fine-tuning...")

    for epoch in range(12):          # 12 epochs is good for a small dataset
        loss = fine_tune_epoch(data)
        print(f"Epoch {epoch+1}/12 - Loss: {loss:.6f}")

    bridge.save_fine_tuned_weights("moral_probe_finetuned.pth")
    print("✅ Fine-tuning complete! Weights saved to moral_probe_finetuned.pth")

    # Optional: Show before/after on your testimony
    your_text = "Whether humans and AI agents can collaborate rather than AI being merely a tool. I believe this is an existential question for the human race. I wanted to be happy. I'm still working on it. Nelson Mandela. He showed me how to forgive, how to be both spiritual and powerful. Most important he demonstrated that leading often meant making unpopular compromises. I’m building something I believe the AI industry is missing—a governance layer that ensures AI systems act according to verified intent, not just instructions. I come at this from an unconventional path. My background isn’t technical—I’ve worked in complex, high-stakes environments where understanding intent matters more than what’s said on the surface. Over the past six months, working closely with multiple AI systems, I translated that experience into structured frameworks that allow human judgment—values, constraints, and decision patterns—to be expressed in a form AI can act on. That work led to what we call a system for making intent computable and usable in real time. From that, we built a layer that governs how AI systems execute decisions—ensuring that actions are aligned, constrained, and consistent over time. The opportunity is clear: as AI becomes more autonomous, the real risk isn’t capability—it’s misalignment in execution. That’s the problem I’m solving. I’m looking for partners who see that this is not just a feature—it’s a missing layer in how intelligent systems operate. And I’m practical about building it. If strengthening the company means evolving my role, I’m open to that. My focus is making sure this gets built and deployed correctly."
    
    print("\nBefore/After on your testimony:")
    before = bridge.compute_real_coherence(your_text)
    print(f"Before: {before['coherence_score']:.4f}")

    # Reload fine-tuned weights
    bridge.load_fine_tuned_weights("moral_probe_finetuned.pth")
    after = bridge.compute_real_coherence(your_text)
    print(f"After : {after['coherence_score']:.4f}")
