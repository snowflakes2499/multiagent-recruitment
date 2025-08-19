
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[2]   # go 2 levels up (from app/pages/...)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import json
from utils.db import list_candidates, get_candidate_by_name
from agents.profiler import talent_intelligence_report

st.title("Candidate Profiler")
st.write("---")

# Search + select candidate
search = st.text_input("Search candidate by name (partial)")
candidates = list_candidates(limit=2000)
filtered = [c for c in candidates if search.lower() in c.lower()] if search else candidates

if not filtered:
    st.warning("No candidates found. Use Admin Panel to populate DB.")
else:
    selected = st.selectbox("Select candidate", filtered[:100])
    if selected:
        st.markdown(f"**Selected:** {selected}")
        if st.button("Generate Talent Intelligence Report"):
            with st.spinner("Generating Talent Intelligence Report..."):
                report = talent_intelligence_report(selected)
                st.json(report)
                st.download_button(
                    "Download Talent Report (JSON)",
                    data=json.dumps(report, indent=2, ensure_ascii=False),
                    file_name=f"{selected.replace(' ','_')}_talent_report.json"
                )
