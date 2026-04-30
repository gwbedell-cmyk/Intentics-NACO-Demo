import streamlit as st
from anthropic import Anthropic
import json
import os
from datetime import datetime
import numpy as np
from mge_plus_bridge import MGEPlusBridge

st.set_page_config(page_title="Intentics Human-AI Team Optimizer", layout="wide")
st.title("🟢 Intentics Human-AI Team Optimizer")
st.subheader("Testimony → Gap Analysis → AI Agent Design")
st.caption("Real MGE+ Ξ Geometry • Raise team coherence > 0.90 • The Quadratic")

# ====================== CONFIG ======================
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Anthropic API Key (for AI agent design)", type="password")
client = Anthropic(api_key=api_key) if api_key else None

bridge = MGEPlusBridge()

# ====================== BUILD HUMAN TEAM ======================
st.subheader("1. Build Your Human Team")
if "human_team" not in st.session_state:
    st.session_state.human_team = []

col1, col2 = st.columns([3,1])
with col1:
    name = st.text_input("Human Team Member Name", key="human_name")
with col2:
    if st.button("Add Human", type="primary"):
        if name:
            st.session_state.human_team.append({"name": name, "text": ""})
            st.rerun()

for i, member in enumerate(st.session_state.human_team):
    with st.expander(f"{member['name']}", expanded=True):
        member["text"] = st.text_area("Testimony", key=f"human_text_{i}", value=member["text"], height=130)
        if st.button("Remove", key=f"remove_human_{i}"):
            st.session_state.human_team.pop(i)
            st.rerun()

# ====================== ANALYZE & DESIGN BUTTON ======================
if st.button("Analyze Team + Design AI Agents to Reach >0.90 Coherence", type="primary", use_container_width=True):
    if len(st.session_state.human_team) == 0:
        st.error("Add at least one human team member.")
    else:
        # Compute current team geometry
        team_texts = [m["text"] for m in st.session_state.human_team if m["text"].strip()]
        if not team_texts:
            st.warning("Please add testimony for the team members.")
        else:
            team_geo = bridge.compute_real_coherence(" ".join(team_texts))
            team_centroid = np.mean([bridge.text_to_moral_vector(t) for t in team_texts], axis=0)

            st.markdown("### Current Human Team Geometry")
            st.metric("Current Coherence", f"{team_geo['coherence_score']:.3f}")
            with st.expander("Team Moral Vector"):
                st.json({"centroid": [round(x, 4) for x in team_centroid.tolist()]})

            # === DESIGN AI AGENTS TO CLOSE GAPS ===
            if client:
                st.markdown("### Proposed AI Agents to Close Gaps")
                gap_prompt = f"""Current team coherence: {team_geo['coherence_score']:.3f}
Team moral centroid: {team_centroid.tolist()}

Design 1–3 specialized AI agents that will raise overall team coherence above 0.90.
For each agent provide:
- Agent Name & Role
- Key moral contribution (which gap it closes)
- Suggested testimony/personality (short paragraph)
- Expected coherence lift

Return in clean bullet format."""

                try:
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=800,
                        messages=[{"role": "user", "content": gap_prompt}]
                    )
                    st.markdown(response.content[0].text)
                except Exception as e:
                    st.error(f"AI design failed: {e}")
            else:
                st.info("Enter Anthropic API key to auto-design AI agents that close the gaps.")

            st.success("✅ Gap analysis complete. AI agents designed to push team coherence > 0.90")

st.caption("Intentics Human-AI Team Optimizer • Real MGE+ Geometry • Testimony-Driven Agent Design")
