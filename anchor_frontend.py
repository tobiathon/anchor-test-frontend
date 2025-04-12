import streamlit as st
import requests
from requests.exceptions import RequestException

API_URL = "https://anchor-app.onrender.com"

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

# === SESSION DEFAULTS ===
if "token" not in st.session_state:
    st.session_state["token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "view" not in st.session_state:
    st.session_state["view"] = "login"  # either "login", "journal", or "loading"

# === SIDEBAR STATUS ===
if st.session_state["token"]:
    st.sidebar.success("✅ You are logged in.")
else:
    st.sidebar.subheader("🔐 Login")

# === HANDLE LOGIN SUCCESS — use a loading state to rerender
if st.session_state["view"] == "loading":
    st.info("🔄 Logging in, please wait...")
    st.session_state["view"] = "journal"

# === LOGIN VIEW ===
elif st.session_state["view"] == "login":
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        try:
            response = requests.post(
                f"{API_URL}/login",
                data={"username": username_input, "password": password_input},
                timeout=20
            )
            response.raise_for_status()
            token = response.json().get("access_token")

            if token:
                st.session_state["token"] = token
                st.session_state["username"] = username_input
                st.session_state["view"] = "loading"  # switch views first
                st.sidebar.success("✅ Logged in!")
            else:
                st.sidebar.error("❌ Login failed — no token received.")
        except RequestException as e:
            st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

    st.info("🔐 Please log in to submit a journal entry.")

# === JOURNAL VIEW ===
elif st.session_state["view"] == "journal":
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
