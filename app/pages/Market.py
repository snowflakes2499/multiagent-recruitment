
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[2]   # go 2 levels up (from app/pages/...)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import json
from utils.db import list_candidates, get_candidate_by_name
from agents.market import analyze_market, get_all_roles

st.title("Market Intelligence & Sourcing")
st.write("---")

try:
    roles = get_all_roles()
except Exception:
    roles = []

if roles:
    selected_role = st.selectbox("Select role for market intel", roles)
else:
    selected_role = st.text_input("Role for market intel", value="")

if st.button("Get Market Intelligence"):
    if not selected_role:
        st.warning("Please enter or select a role")
    else:
        with st.spinner("Fetching market intelligence..."):
            market = analyze_market(selected_role)
            st.json(market)
