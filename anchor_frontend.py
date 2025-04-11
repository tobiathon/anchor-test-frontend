import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Replace with your public backend URL when hosted
token = st.session_state.get("token", "")

st.title("🧠 Anchor Journal Portal")

# === LOGIN SECTION ===
st.sidebar.subheader("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state["token"] = token
        st.sidebar.success("Logged in!")
    else:
        st.sidebar.error("Invalid login.")

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
