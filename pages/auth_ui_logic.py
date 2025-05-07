# pages/auth_ui_logic.py

import streamlit as st
from utils.auth import login_user, register_user
from utils.session_manager import set_session_state

def login_signup_flow():
    tab_login, tab_signup = st.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")

        username_input = st.text_input(
            "Username",
            key="login_username",
            autocomplete="username"  # ✅ helps browser autofill
        )

        password_input = st.text_input(
            "Password",
            type="password",
            key="login_password",
            autocomplete="current-password"  # ✅ helps browser autofill
        )

        login_clicked = st.button("Login", key="login_button")

        if login_clicked:
            success, token = login_user(username_input, password_input)
            if success:
                set_session_state(username_input, token)
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
