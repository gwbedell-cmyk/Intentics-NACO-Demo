# anima_testis_naco_demo.py
import streamlit as st
from bridge import MGEPlusBridge
from datetime import datetime
import json
import os

st.set_page_config(page_title="ANIMA TESTIS • NACO 2026", layout="wide")
st.title("🟢 ANIMA TESTIS")
st.subheader("Live Demonstrations • NACO Ottawa 2026")
st.caption("The Quadratic • Intentics in Action • Real MGE+ Geometry")

bridge = MGEPlusBridge()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Solo Founder", "Founder Team", "VC Professional", "Angel Investor"])

def analyze_testimony(category, q1, q2, q3, personal=""):
    full_text = f"{q1} {q2} {q3} {personal}"
    result = bridge.compute_real_coherence(full_text)
    
    st.success(f"**{category} Analysis Complete**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Coherence Score", f"{result['coherence_score']:.4f}")
        st.metric("In Ubuntu Basin", "✅ Yes" if result['is_in_ubuntu_basin'] else "❌ No")
    with col2:
        st.metric("ξ_m (Curvature)", f"{result['xi_m']:.4f}")
        st.metric("Distance to Basin", f"{result['basin_distance']:.4f}")
    
    st.json(result)
    
    # Gap Solver Recommendations
    st.subheader("Gap Solver Recommendations")
    if result['coherence_score'] < 0.6:
        st.warning("**Opportunity to improve coherence:**")
        st.write("• Strengthen Justice and Coherence dimensions in your story")
        st.write("• Add specific examples of Ubuntu / shared humanity")
        st.write("• Balance high Trust with clear Execution examples")
    else:
        st.success("Strong coherence! Minor refinements possible.")
    
    return result

# Tab 1: Solo Founder
with tab1:
    st.header("Solo Founder")
    q1 = st.text_area("What’s an idea or obsession that’s kept you up at night?", height=80, key="solo_q1")
    q2 = st.text_area("When you were younger, what kind of person did you want to become?", height=80, key="solo_q2")
    q3 = st.text_area("Who has influenced you most in a positive way?", height=80, key="solo_q3")
    personal = st.text_area("Additional Personal Testimony (optional)", height=150, key="solo_personal")
    if st.button("Analyze Basin →", type="primary", key="solo_btn"):
        analyze_testimony("Solo Founder", q1, q2, q3, personal)

# Tab 2: Founder Team
with tab2:
    st.header("Founder Team")
    q1 = st.text_area("Tell us about a real moment of tension within your team.", height=80, key="team_q1")
    q2 = st.text_area("If your team had to replace you, what would they look for?", height=80, key="team_q2")
    q3 = st.text_area("How do you balance personal relationships and professional decisions?", height=80, key="team_q3")
    personal = st.text_area("Additional Personal Testimony (optional)", height=150, key="team_personal")
    if st.button("Analyze Basin →", type="primary", key="team_btn"):
        analyze_testimony("Founder Team", q1, q2, q3, personal)

# Tab 3 & 4 similar (shortened for space)
with tab3:
    st.header("VC Professional")
    q1 = st.text_area("Tell us about a company you passed on that later succeeded.", height=80, key="vc_q1")
    q2 = st.text_area("If an AI system played a key role in building a company, what would you need to trust it?", height=80, key="vc_q2")
    q3 = st.text_area("Think of an investment that didn’t go as expected.", height=80, key="vc_q3")
    personal = st.text_area("Additional Personal Testimony (optional)", height=150, key="vc_personal")
    if st.button("Analyze Basin →", type="primary", key="vc_btn"):
        analyze_testimony("VC Professional", q1, q2, q3, personal)

with tab4:
    st.header("Angel Investor")
    q1 = st.text_area("Think of someone you deeply trust. What made you trust them?", height=80, key="angel_q1")
    q2 = st.text_area("What would make you walk away from an opportunity?", height=80, key="angel_q2")
    q3 = st.text_area("Describe a founder relationship you found especially rewarding.", height=80, key="angel_q3")
    personal = st.text_area("Additional Personal Testimony (optional)", height=150, key="angel_personal")
    if st.button("Analyze Basin →", type="primary", key="angel_btn"):
        analyze_testimony("Angel Investor", q1, q2, q3, personal)

st.caption("ANIMA TESTIS • NACO Ottawa 2026 • The Quadratic")