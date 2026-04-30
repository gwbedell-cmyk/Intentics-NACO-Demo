import streamlit as st
from anthropic import Anthropic
import json
import os
from datetime import datetime
import numpy as np
from mge_plus_bridge import MGEPlusBridge

st.set_page_config(page_title="Intentics Job Matching • Real MGE+ Ξ", layout="wide")
st.title("🟢 Intentics Job ↔ Applicant Matching")
st.subheader("Real MGE+ Geometry • Testimony, not Resumes")
st.caption("The Quadratic • NACO 2026")

# ====================== CONFIG ======================
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Anthropic API Key (for insights)", type="password")
client = Anthropic(api_key=api_key) if api_key else None

bridge = MGEPlusBridge()

# ====================== JOB TESTIMONY ======================
st.subheader("📋 Job Testimony")
job_text = st.text_area(
    "Write the job as real human testimony (values, hoped outcomes, boundaries)",
    height=300,
    placeholder="We need someone who truly cares about patient dignity, follows through even under pressure...",
    key="job_text"
)
job_button = st.button("Compute Job Moral Vector & Match Applicants", type="primary", use_container_width=True)

# ====================== APPLICANTS ======================
st.subheader("👤 Applicant Testimonies")
num_applicants = st.number_input("Number of applicants", min_value=1, max_value=10, value=3)

applicants = []
for i in range(int(num_applicants)):
    with st.expander(f"Applicant {i+1}", expanded=(i == 0)):
        name = st.text_input("Name / ID", f"Applicant {i+1}", key=f"name_{i}")
        app_text = st.text_area("Applicant testimony", height=180, key=f"app_text_{i}")
        applicants.append({"name": name, "text": app_text})

# ====================== COMPUTE MATCHING ======================
if job_button and job_text.strip():
    job_geo = bridge.compute_real_coherence(job_text)
    
    st.markdown("### Results")
    st.subheader("Job Moral Profile")
    with st.expander("🔬 Job Geometry", expanded=True):
        st.json({
            "moral_vector": [round(x, 4) for x in job_geo["moral_vector"]],
            "coherence_score": round(job_geo["coherence_score"], 4),
            "in_ubuntu_basin": job_geo["is_in_ubuntu_basin"]
        })
        st.progress(job_geo["coherence_score"])

    matches = []
    for app in applicants:
        if app["text"].strip():
            app_geo = bridge.compute_real_coherence(app["text"])
            dist = bridge.basin_distance(np.array(app_geo["moral_vector"]))
            match_score = np.clip(1.0 - (dist / 0.8), 0.0, 1.0)
            
            matches.append({
                "name": app["name"],
                "geometry": app_geo,
                "basin_distance": dist,
                "match_score": match_score
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)

    st.subheader("Applicant Ranking (Real Geometry)")
    for i, m in enumerate(matches):
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.metric(label=m["name"], value=f"{m['match_score']:.2f}")
        with col_b:
            st.progress(m["match_score"])
            st.caption(f"Basin distance: {m['basin_distance']:.3f} | Coherence: {m['geometry']['coherence_score']:.3f}")

    st.success("✅ Matching complete using real MGE+ moral geometry")
