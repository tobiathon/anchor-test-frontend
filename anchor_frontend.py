# anchor_frontend.py
import streamlit as st
import requests
from requests.exceptions import RequestException
import time
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="Anchor Journal", layout="centered")

COOKIE_MAX_AGE = 2592000
cookies = EncryptedCookieManager(prefix="anchor_", password="my_secret_password")
if not cookies.ready():
    st.stop()

API_URL = "https://anchor-app.onrender.com"
st.title("🧠 Anchor Journal Portal")

# === Session Initialization ===
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

# === Logout ===
def logout():
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False
    if "token" in cookies: del cookies["token"]
    if "username" in cookies: del cookies["username"]
    cookies.save()
    st.sidebar.info("You have been logged out.")
    time.sleep(1)
    st.experimental_rerun()

# === Login + Signup ===
if not st.session_state["token"]:
    tab_login, tab_signup = st.sidebar.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")
        username_input = st.text_input("Username", key="login_username")
        password_input = st.text_input("Password", type="password", key="login_password")
        remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
        if st.button("Login", key="login_button"):
            try:
                res = requests.post(f"{API_URL}/auth/login", data={"username": username_input, "password": password_input}, timeout=20)
                res.raise_for_status()
                token = res.json().get("access_token")
                if token:
                    st.session_state["token"] = token
                    st.session_state["username"] = username_input
                    st.session_state["remember_me"] = remember_me
                    if remember_me:
                        cookies["token"] = token
                        cookies["username"] = username_input
                        cookies.save()
                    st.experimental_rerun()
                else:
                    st.sidebar.error("❌ Login failed — no token received.")
            except RequestException as e:
                st.sidebar.error(f"⚠️ Could not connect: {e}")

    with tab_signup:
        st.subheader("Create Account")
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_button"):
            try:
                res = requests.post(f"{API_URL}/auth/signup", data={"username": new_username, "password": new_password}, timeout=20)
                res.raise_for_status()
                st.sidebar.success("✅ Account created! Please log in.")
            except RequestException as e:
                st.sidebar.error(f"❌ Failed to create account: {e}")

    st.info("🔐 Please log in to continue.")

# === Journal + Chat ===
else:
    st.sidebar.success("✅ You are logged in.")
    if st.sidebar.button("🚪 Logout"):
        logout()

    st.subheader("📓 New Journal Entry")
    entry_text = st.text_area("What’s on your mind today?")
    if st.button("Submit"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        payload = {"user_id": st.session_state["username"], "entry_text": entry_text}
        try:
            res = requests.post(f"{API_URL}/upload_journal", json=payload, headers=headers, timeout=20)
            res.raise_for_status()
            response_data = res.json()
            echo_output = response_data.get("echo_output", {})
            echo_thoughts = echo_output.get("echo_thoughts", "")
            st.success("📝 Journal submitted!")
            st.write("### 🧠 Echo's Reflection")
            st.write("**Summary:**", echo_output.get("summary", "No summary"))
            st.write("**Emotions:**", ", ".join(echo_output.get("emotions", [])))
            st.write("**Insights:**")
            for i in echo_output.get("insights", []): st.write(f"- {i}")
            st.write("**Questions:**")
            for q in echo_output.get("questions", []): st.write(f"- {q}")
            if echo_thoughts:
                st.markdown("---")
                st.write("### 💬 Echo’s Thoughts")
                st.info(echo_thoughts)
        except RequestException as e:
            st.error(f"❌ Failed to submit journal: {e}")

    # === Scrollable Chat Interface ===
    st.markdown("---")
    st.subheader("💬 Chat with Echo")

    with st.container():
        for sender, message in st.session_state.chat_history:
            if sender == "You":
                st.markdown(
                    f"""
                    <div style='text-align:right;background:#f5f5f5;color:#000;padding:10px 14px;border-radius:12px;margin:6px 0;max-width:80%;margin-left:auto'>
                        {message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='text-align:left;background:#ffffff;color:#000;padding:10px 14px;border-radius:12px;margin:6px 0;max-width:80%;margin-right:auto'>
                        {message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with st.form(key="chat_form"):
        chat_input = st.text_input("Type your message...")
        submit_chat = st.form_submit_button("Send")

    if submit_chat and chat_input.strip():
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        payload = {"user_id": st.session_state["username"], "message": chat_input.strip()}
        try:
            res = requests.post(f"{API_URL}/chat/echo_chat", json=payload, headers=headers, timeout=20)
            res.raise_for_status()
            echo_reply = res.json().get("echo_response", "Echo is reflecting...")
            st.session_state.chat_history.append(("You", chat_input.strip()))
            st.session_state.chat_history.append(("Echo", echo_reply))
            st.experimental_rerun()
        except RequestException as e:
            st.error(f"❌ Failed to contact Echo: {e}")
    elif submit_chat:
        st.warning("Please enter a message.")
