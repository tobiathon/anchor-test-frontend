# File: pages/journal.py

import streamlit as st
from utils.api import submit_journal_entry

st.subheader("📓 New Journal Entry")

entry_text = st.text_area("What’s on your mind today?")

if st.button("Submit"):
    if not entry_text.strip():
        st.warning("Please enter some thoughts before submitting.")
    else:
        result = submit_journal_entry(entry_text)
        if result:
            echo_output = result.get("echo_output", {})
            echo_thoughts = echo_output.get("echo_thoughts", "")

            st.success("📝 Journal submitted!")
            st.write("### 🧠 Echo's Reflection")
            st.write("**Summary:**", echo_output.get("summary", "No summary"))
            st.write("**Emotions:**", ", ".join(echo_output.get("emotions", [])))

            st.write("**Insights:**")
            for i in echo_output.get("insights", []):
                st.write(f"- {i}")

            st.write("**Questions:**")
            for q in echo_output.get("questions", []):
                st.write(f"- {q}")

            if echo_thoughts:
                st.markdown("---")
                st.write("### 💬 Echo’s Thoughts")
                st.info(echo_thoughts)
        else:
            st.error("❌ Failed to submit journal.")
