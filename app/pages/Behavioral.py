
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[2]   # go 2 levels up (from app/pages/...)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from agents.behavioral import analyze_text

st.title("Behavioral & Cultural Fit Analyzer")
st.write("---")

sample = st.text_area("Paste candidate interview response / chat transcript here:", height=200,
                      value="I enjoy working with teams and iterating quickly. I helped take ownership of a production bug and documented the fix.")

if st.button("Analyze Behavioral Fit"):
    if not sample.strip():
        st.warning("Please provide text to analyze.")
    else:
        with st.spinner("Analyzing behavioral fit..."):
            bh = analyze_text(sample)
            if "error" in bh:
                st.error("Behavioral analysis error.")
            else:
                st.subheader("Sentiment")
                st.json(bh["sentiment"])

                st.subheader("Observed Traits")
                st.write(bh["observed_traits"])

                st.subheader("Insights")
                for insight in bh.get("insights", []):
                    st.info(insight)

                st.subheader("Bias Mitigation Protocol")
                for rule in bh.get("bias_protocol", []):
                    st.write("- " + rule)
