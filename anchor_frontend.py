import streamlit as st
import requests
from requests.exceptions import RequestException

API_URL = "https://anchor-app.onrender.com"
# API_URL = "http://localhost:8000"  # ✅ For local testing

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

# === SESSION INITIALIZATION ===
if "token" not in st.session_state:
    st.session_state["token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# === LOGIN + SIGNUP FORM ===
if not st.session_state["token"]:
    tab_login, tab_signup = st.sidebar.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me")
        login_clicked = st.button("Login")

        if login_clicked:
            try:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    data={"username": username_input, "password": password_input},
                    timeout=20
                )
                response.raise_for_status()
                token = response.json().get("access_token")

                if token:
                    st.session_state["token"] = token
                    st.session_state["username"] = username_input
                    st.sidebar.success("✅ Logged in!")

                    # Use Streamlit's built-in rerun only inside safe update scope
                    st.session_state["rerun_triggered"] = True
                    st.experimental_rerun()
                else:
                    st.sidebar.error("❌ Login failed — no token received.")
            except RequestException as e:
                st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

    with tab_signup:
        st.subheader("Create Account")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        create_clicked = st.button("Sign Up")

        if create_clicked:
            try:
                response = requests.post(
                    f"{API_URL}/auth/signup",
                    data={"username": new_username, "password": new_password},
                    timeout=20
                )
                response.raise_for_status()
                st.sidebar.success("✅ Account created! Please log in.")
            except RequestException as e:
                st.sidebar.error(f"❌ Failed to create account: {e}")

    st.info("🔐 Please log in to submit a journal entry.")

# === JOURNAL FORM + CHAT ===
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
            res = requests.post(f"{API_URL}/upload_journal", json=payload, headers=headers, timeout=20)
            res.raise_for_status()
            response_data = res.json()
            echo_output = response_data.get("echo_output", {})
            echo_thoughts = echo_output.get("echo_thoughts", "")

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

            if echo_thoughts:
                st.markdown("---")
                st.write("### 💬 Echo’s Thoughts")
                st.info(echo_thoughts)

        except RequestException as e:
            st.error(f"❌ Failed to submit journal: {e}")

    # === Echo Chat Section ===
    st.markdown("---")
    st.subheader("💬 Chat with Echo")

    # Show chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧍‍♂️ You:** {message}")
        else:
            st.markdown(f"**🤖 Echo:** {message}")

    chat_input = st.text_input("Type your message to Echo...")

    if st.button("Send"):
        if chat_input.strip():
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            payload = {
                "user_id": st.session_state["username"],
                "message": chat_input.strip()
            }

            try:
                res = requests.post(f"{API_URL}/chat/echo_chat", json=payload, headers=headers, timeout=20)
                res.raise_for_status()
                echo_reply = res.json().get("echo_response", "Echo is reflecting...")

                # Append messages to chat history
                st.session_state.chat_history.append(("You", chat_input.strip()))
                st.session_state.chat_history.append(("Echo", echo_reply))

            except RequestException as e:
                st.error(f"❌ Failed to contact Echo: {e}")
        else:
            st.warning("Please enter a message before sending.")
