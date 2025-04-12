import streamlit as st
import requests

API_URL = "https://anchor-app.onrender.com"  # Replace with your public backend URL when hosted
token = st.session_state.get("token", "")

st.title("🧠 Anchor Journal Portal")

# === LOGIN SECTION ===
st.sidebar.subheader("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

import requests
from requests.exceptions import RequestException

if st.sidebar.button("Login"):
    try:
        response = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password},
            timeout=20
        )
        response.raise_for_status()  # will raise if status >= 400

        token = response.json().get("access_token")
        if token:
            st.session_state["token"] = token
            st.sidebar.success("✅ Logged in!")
            st.stop()
        else:
            st.sidebar.error("❌ Login failed — no token received.")

    except RequestException as e:
        st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

# === JOURNAL FORM ===
if token:
    st.subheader("📓 New Journal Entry")
    entry_text = st.text_area("What’s on your mind today?")
    if st.button("Submit"):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "user_id": username,
            "entry_text": entry_text
        }
        res = requests.post(f"{API_URL}/upload_journal", json=payload, headers=headers)
        if res.status_code == 200:
            echo_output = res.json()["echo_output"]
            st.success("Journal submitted successfully!")
            st.write("### 🧠 Echo's Reflection")
            st.write("**Summary:**", echo_output["summary"])
            st.write("**Emotions:**", ", ".join(echo_output["emotions"]))
            st.write("**Insights:**")
            for insight in echo_output["insights"]:
                st.write(f"- {insight}")
            st.write("**Questions:**")
            for q in echo_output["questions"]:
                st.write(f"- {q}")
        else:
            st.error("Something went wrong submitting your journal.")

else:
    st.info("Please log in to submit entries.")
