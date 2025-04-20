import streamlit as st
from utils.auth import login_user, register_user
from utils.cookies import set_cookie, get_cookie, delete_cookie
from utils.session_manager import set_session_state

def login_signup_flow():
    # If user is already logged in, show logout button
    if st.session_state.get("token"):
        with st.sidebar:
            st.markdown("---")
            if st.button("🚪 Logout"):
                delete_cookie("username")
                st.session_state.clear()
                st.rerun()

    # Load cookies
    saved_username = get_cookie("username")

    # Tabs for Login and Signup
    tab_login, tab_signup = st.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")

        # Prefill username from cookie if it exists
        username_input = st.text_input("Username", value=saved_username or "", key="login_username")
        password_input = st.text_input("Password", type="password", key="login_password")
        remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
        login_clicked = st.button("Login", key="login_button")

        if login_clicked:
            success, token = login_user(username_input, password_input, remember_me)
            if success:
                set_session_state(username_input, token)
                
                if remember_me:
                    set_cookie("username", username_input)
                else:
                    delete_cookie("username")

                st.success("✅ Logged in successfully.")
                st.rerun()
            else:
                st.error("❌ Login failed. Please check your credentials.")

    with tab_signup:
        st.subheader("Create Account")
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        create_clicked = st.button("Sign Up", key="signup_button")

        if create_clicked:
            success = register_user(new_username, new_password)
            if success:
                st.success("✅ Account created! Please log in.")
            else:
                st.error("❌ Failed to create account. Username may already exist.")
