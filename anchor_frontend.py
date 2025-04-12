import streamlit as st
import requests
from requests.exceptions import RequestException

API_URL = "https://anchor-app.onrender.com"  # Public backend URL

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

# === 🧠 Only rerun if token exists and just_logged_in is set ===
if (
    st.session_state.get("just_logged_in") 
    and st.session_state.get("token")
):
    st.session_state["just_logged_in"] = False
    st.experimental_rerun()

# === LOGIN FLOW ===
if "token" not in st.session_state:
    st.sidebar.subheader("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        try:
            response = requests.post(
                f"{API_URL}/login",
                data={"username": username, "password": password},
                timeout=20
            )
            response.raise_for_status()
            token = response.json().get("access_token")

            if token:
                st.session_state["token"] = token
                st.session_state["username"] = username
                st.session_state["just_logged_in"] = True
                # Let the rerun happen next cycle
            else:
                st.sidebar.error("❌ Login failed — no token received.")
        except RequestException as e:
            st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

    st.info("🔐 Please log in to submit a journal entry.")

# === JOURNAL FLOW ===
else:
    st.sidebar.success("✅ You are logged in.")
    st.subheader("📓 New Journal Entry")

    entry_text = st.text_area("What’s on your mind today?")

    if st.button("Submit"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        payload = {
            "user_id": st.session_state["username"],
            "entry_text": entry_text
        }

        try:
            res = requests.post(f"{API_URL}/upload_journal", json=payload, headers=headers, timeout=15)
            res.raise_for_status()
            echo_output = res.json()["echo_output"]

            st.success("📝 Journal submitted successfully!")
            st.write("### 🧠 Echo's Reflection")
            st.write("**Summary:**", echo_output.get("summary", "No summary."))
            st.write("**Emotions:**", ", ".join(echo_output.get("emotions", [])))

            st.write("**Insights:**")
            for insight in echo_output.get("insights", []):
                st.write(f"- {insight}")

            st.write("**Questions:**")
            for q in echo_output.get("questions", []):
                st.write(f"- {q}")

        except RequestException as e:
            st.error(f"❌ Failed to submit journal: {e}")
