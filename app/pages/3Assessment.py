import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[2]   # go 2 levels up (from app/pages/...)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import json
from utils.db import list_candidates
from agents.assessment import build_assessment_package

st.title("Assessment Designer")
st.write("---")

# Candidate selection
candidates = list_candidates(limit=2000)
if not candidates:
    st.warning("No candidates found. Use Admin Panel to populate DB.")
else:
    selected = st.selectbox("Select candidate", candidates)
    target_role_input = st.text_input("Target Role (leave blank to use candidate headline)", value="")
    if st.button("Generate Assessment Package"):
        with st.spinner("Generating Assessment Package..."):
            role_arg = target_role_input.strip() or ""
            pkg = build_assessment_package(selected, role_arg)
            st.json(pkg)
            st.download_button(
                "Download Assessment (JSON)",
                data=json.dumps(pkg, indent=2, ensure_ascii=False),
                file_name=f"{selected.replace(' ','_')}_assessment.json"
            )
