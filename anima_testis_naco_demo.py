import streamlit as st
from anthropic import Anthropic
import json
import os
from datetime import datetime
from mge_plus_bridge import MGEPlusBridge

st.set_page_config(page_title="ANIMA TESTIS NACO 2026", layout="centered")
st.title("ANIMA TESTIS")
st.subheader("Live Demonstrations - NACO Ottawa 2026")
st.caption("The Quadratic - Intentics in Action - Real MGE+ Xi Geometry")

# ====================== CONFIG ======================
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Anthropic API Key (for readable analysis)", type="password", placeholder="sk-ant-...")
MODEL = "claude-3-5-sonnet-20241022"
client = Anthropic(api_key=api_key) if api_key else None

bridge = MGEPlusBridge()

demo_choice = st.radio("Select Demo", ["Nurse Governance Demo", "Gap Solver Teams Demo"], horizontal=True)

if demo_choice == "Nurse Governance Demo":
    st.info("Nurse Governance Demo with Screen 0 Gap + cEPC (full code available from previous messages)")

elif demo_choice == "Gap Solver Teams Demo":
    st.markdown("### Gap Solver Teams Demo")
    st.caption("Live testimony -> Real MGE+ Xi geometry + basin analysis")

    tab1, tab2, tab3, tab4 = st.tabs(["Solo Founder", "Founder Team", "VC Professional", "Angel Investor"])

    def analyze_testimony(category, q1, q2, q3, personal_testimony=""):
        full_text = f"Category: {category}\nQ1: {q1}\nQ2: {q2}\nQ3: {q3}\nPersonal Testimony: {personal_testimony}"
        geo_result = bridge.compute_real_coherence(full_text)
        
        llm_text = "Enter API key for human-readable analysis."
        if client:
            try:
                prompt = f"You are an ANIMA TESTIS coherence analyst.\n{full_text}\n\nReturn EXACTLY this structure:\nSTRENGTHS: [two specific dimensions]\nGAPS: [two specific dimensions]\nGAP_SUMMARY: [one sentence]\nBEST_MATCH: [name or category]\nMATCH_REASON: [one sentence - values resonance]"
                response = client.messages.create(model=MODEL, max_tokens=300, messages=[{"role": "user", "content": prompt}])
                llm_text = response.content[0].text
            except:
                llm_text = "LLM analysis unavailable."

        return {"geometry": geo_result, "llm_analysis": llm_text}

    def save_testimony(category, answers, personal_testimony, result):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "answers": answers,
            "personal_testimony": personal_testimony,
            "geometry": result["geometry"],
            "llm_analysis": result["llm_analysis"]
        }
        filename = "testimonies.json"
        data = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        data.append(entry)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        st.success(f"Saved with real Xi geometry to {filename}")

    def show_geometry(geo):
        with st.expander("Real MGE+ Xi Geometry", expanded=True):
            st.json({
                "moral_vector (T,J,C,E)": [round(x, 4) for x in geo["moral_vector"]],
                "xi_m": round(geo["xi_m"], 6),
                "basin_distance_to_alpha_U": round(geo["basin_distance_to_alpha_U"], 4),
                "coherence_score": round(geo["coherence_score"], 4),
                "in_ubuntu_basin": geo["is_in_ubuntu_basin"]
            })
            st.progress(geo["coherence_score"])

    # Solo Founder
    with tab1:
        st.write("**Solo Founder**")
        q1 = st.text_area("Whats an idea or obsession thats kept you up at night?", height=100, key="solo_q1")
        q2 = st.text_area("When you were younger, what kind of person did you want to become?", height=100, key="solo_q2")
        q3 = st.text_area("Who has influenced you most in a positive way?", height=100, key="solo_q3")
        st.markdown("**Additional Personal Testimony (optional)**")
        personal_testimony = st.text_area("", height=200, key="solo_personal")
        if st.button("Analyze Basin ->", key="solo_btn", type="primary"):
            result = analyze_testimony("Solo Founder", q1, q2, q3, personal_testimony)
            st.markdown(result["llm_analysis"])
            show_geometry(result["geometry"])
            answers = {"Q1": q1, "Q2": q2, "Q3": q3}
            save_testimony("Solo Founder", answers, personal_testimony, result)

    # Founder Team
    with tab2:
        st.write("**Founder Team**")
        q1 = st.text_area("Tell us about a real moment of tension or conflict within your team.", height=100, key="team_q1")
        q2 = st.text_area("If your team had to replace you tomorrow, what would they look for?", height=100, key="team_q2")
        q3 = st.text_area("How do you balance personal relationships and professional decisions?", height=100, key="team_q3")
        st.markdown("**Additional Personal Testimony (optional)**")
        personal_testimony = st.text_area("", height=200, key="team_personal")
        if st.button("Analyze Basin ->", key="team_btn", type="primary"):
            result = analyze_testimony("Founder Team", q1, q2, q3, personal_testimony)
            st.markdown(result["llm_analysis"])
            show_geometry(result["geometry"])
            answers = {"Q1": q1, "Q2": q2, "Q3": q3}
            save_testimony("Founder Team", answers, personal_testimony, result)

    # VC Professional
    with tab3:
        st.write("**VC Professional**")
        q1 = st.text_area("Tell us about a company you passed on that later succeeded.", height=100, key="vc_q1")
        q2 = st.text_area("If an AI system played a key role in building a company, what would you need to see?", height=100, key="vc_q2")
        q3 = st.text_area("Think of an investment that didnt go as expected.", height=100, key="vc_q3")
        st.markdown("**Additional Personal Testimony (optional)**")
        personal_testimony = st.text_area("", height=200, key="vc_personal")
        if st.button("Analyze Basin ->", key="vc_btn", type="primary"):
            result = analyze_testimony("VC Professional", q1, q2, q3, personal_testimony)
            st.markdown(result["llm_analysis"])
            show_geometry(result["geometry"])
            answers = {"Q1": q1, "Q2": q2, "Q3": q3}
            save_testimony("VC Professional", answers, personal_testimony, result)

    # Angel Investor
    with tab4:
        st.write("**Angel Investor**")
        q1 = st.text_area("Think of someone you deeply trust in business.", height=100, key="angel_q1")
        q2 = st.text_area("What would make you immediately walk away from an opportunity?", height=100, key="angel_q2")
        q3 = st.text_area("Describe a founder relationship you found especially rewarding.", height=100, key="angel_q3")
        st.markdown("**Additional Personal Testimony (optional)**")
        personal_testimony = st.text_area("", height=200, key="angel_personal")
        if st.button("Analyze Basin ->", key="angel_btn", type="primary"):
            result = analyze_testimony("Angel Investor", q1, q2, q3, personal_testimony)
            st.markdown(result["llm_analysis"])
            show_geometry(result["geometry"])
            answers = {"Q1": q1, "Q2": q2, "Q3": q3}
            save_testimony("Angel Investor", answers, personal_testimony, result)

    st.markdown("---")
    st.subheader("Collect & Match")
    if st.button("Run Global Matching", type="primary"):
        if os.path.exists("testimonies.json"):
            with open("testimonies.json", "r") as f:
                data = json.load(f)
            st.write(f"Found {len(data)} testimonies with real Xi geometry")
            for entry in data:
                st.write(f"**{entry['timestamp'][:16]} — {entry['category']}**")
                if "geometry" in entry:
                    show_geometry(entry["geometry"])
                if "llm_analysis" in entry:
                    st.markdown(entry["llm_analysis"])
                st.divider()
        else:
            st.info("No testimonies saved yet.")

st.caption("ANIMA TESTIS - Real MGE+ Xi Geometry - The Quadratic - NACO 2026")
