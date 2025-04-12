import streamlit as st
import requests
from requests.exceptions import RequestException

API_URL = "https://anchor-app.onrender.com"  # Your backend URL

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

# === LOGIN CHECK ===
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
                st.sidebar.success("✅ Logged in!")
                st.experimental_rerun()  # Refresh UI after login
            else:
                st.sidebar.error("❌ Login failed — no token received.")
        except RequestException as e:
            st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

else:
    # === JOURNAL FORM ===
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
            st.write("**Summary:**", echo_output["summary"])
            st.write("**Emotions:**", ", ".join(echo_output["emotions"]))
            st.write("**Insights:**")
            for insight in echo_output["insights"]:
                st.write(f"- {insight}")
            st.write("**Questions:**")
            for q in echo_output["questions"]:
                st.write(f"- {q}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to submit journal: {e}")

    st.sidebar.success("✅ You are logged in.")
