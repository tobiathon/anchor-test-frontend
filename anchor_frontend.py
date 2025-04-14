import streamlit as st
import requests
from requests.exceptions import RequestException
import time
from streamlit_cookies_manager import EncryptedCookieManager

# Set the cookie max-age (30 days)
COOKIE_MAX_AGE = 2592000  # in seconds

# Initialize the cookie manager (use a strong secret in production)
cookies = EncryptedCookieManager(prefix="anchor_", password="my_secret_password")
if not cookies.ready():
    st.stop()

API_URL = "https://anchor-app.onrender.com"
# API_URL = "http://localhost:8000"  # For local testing

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

# === SESSION INITIALIZATION ===
# Load token and username from cookies if not already in session_state
if "token" not in st.session_state:
    st.session_state["token"] = cookies.get("token") if "token" in cookies else None

if "username" not in st.session_state:
    st.session_state["username"] = cookies.get("username") if "username" in cookies else None

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "rerun_triggered" not in st.session_state:
    st.session_state["rerun_triggered"] = False
if "remember_me" not in st.session_state:
    st.session_state["remember_me"] = False

# === LOGOUT & CLEAR CACHE ===
def logout():
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False
    if "token" in cookies:
        del cookies["token"]
    if "username" in cookies:
        del cookies["username"]
    cookies.save()
    st.sidebar.info("You have been logged out.")
    time.sleep(1)
    try:
        st.experimental_rerun()
    except st.runtime.scriptrunner.RerunException:
        pass

# === LOGIN + SIGNUP FORM ===
if not st.session_state["token"]:
    tab_login, tab_signup = st.sidebar.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")
        username_input = st.text_input("Username", key="login_username")
        password_input = st.text_input("Password", type="password", key="login_password")
        remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
        login_clicked = st.button("Login", key="login_button")

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
                    st.session_state["remember_me"] = remember_me
                    st.sidebar.success("✅ Logged in!")
                    # If "Remember me" is checked, persist token and username in cookies.
                    if remember_me:
                        cookies["token"] = token
                        cookies["username"] = username_input
                        # If the library supports it, set cookie expiry (max_age)
                        # (Customize the library or use an alternative if needed for max_age)
                        cookies.save()
                    st.session_state["rerun_triggered"] = True
                    try:
                        st.experimental_rerun()
                    except st.runtime.scriptrunner.RerunException:
                        pass
                else:
                    st.sidebar.error("❌ Login failed — no token received.")
            except RequestException as e:
                st.sidebar.error(f"⚠️ Could not connect to backend: {e}")

    with tab_signup:
        st.subheader("Create Account")
        # Use distinct keys to avoid conflicts with the login form.
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        create_clicked = st.button("Sign Up", key="signup_button")

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
    if st.sidebar.button("🚪 Logout"):
        logout()

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

                st.session_state.chat_history.append(("You", chat_input.strip()))
                st.session_state.chat_history.append(("Echo", echo_reply))

            except RequestException as e:
                st.error(f"❌ Failed to contact Echo: {e}")
        else:
            st.warning("Please enter a message before sending.")
