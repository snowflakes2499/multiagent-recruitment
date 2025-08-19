import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[2]   # go 2 levels up (from app/pages/...)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import json
from utils.db import init_db, add_candidate, bulk_insert_candidates
import utils.generator as generator

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("Admin Panel - Candidate Ingestion & Management")
st.write("---")

init_db()

# Bulk synthetic generation
st.subheader("Bulk Synthetic Candidate Generation")
n = st.number_input("Generate synthetic candidates (n)", min_value=1, max_value=50000, value=100, step=50)
if st.button("Bulk Generate"):
    with st.spinner("Generating synthetic candidates..."):
        inserted = generator.bulk_generate(int(n))
        st.success(f"Inserted {inserted} synthetic candidates into DB.")

# Upload JSON
st.subheader("Upload Candidate JSON")
uploaded = st.file_uploader("Upload candidates JSON", type=["json"])
if uploaded is not None:
    try:
        data = json.load(uploaded)
        to_insert = []
        for item in data:
            name = item.get("name") or item.get("full_name")
            headline = item.get("headline", "")
            profile = item.get("profile", item)
            to_insert.append({"name": name, "headline": headline, "profile": profile})
        count = bulk_insert_candidates(to_insert)
        st.success(f"Inserted {count} candidates from uploaded file.")
    except Exception as e:
        st.error(f"Failed to parse uploaded JSON: {e}")

# Add single candidate
st.subheader("Add Single Candidate")
with st.form("add_form"):
    name_in = st.text_input("Name")
    headline_in = st.text_input("Headline (e.g., Backend Engineer at ABC)")
    summary_in = st.text_area("One-line summary / bullets (comma separated)")
    submitted = st.form_submit_button("Add Candidate")
    if submitted:
        profile = {
            "linkedin": {
                "headline": headline_in,
                "work_history": [
                    {"title": headline_in.split(" at ")[0] if " at " in headline_in else headline_in,
                     "company": headline_in.split(" at ")[1] if " at " in headline_in else "",
                     "start": "2020-01", "end": "2022-12",
                     "bullets": [s.strip() for s in summary_in.split(",") if s.strip()]}
                ]
            },
            "github": {"repos": []}
        }
        add_candidate(name_in, headline_in, profile)
        st.success(f"Added candidate: {name_in}")
