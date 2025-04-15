# File: pages/auth_ui.py

import streamlit as st
from utils.auth import login_user, signup_user, logout
from utils.session import is_logged_in


def render_auth_ui():
    """Display login/signup tabs if user is not authenticated."""
    if not is_logged_in():
        tab_login, tab_signup = st.sidebar.tabs(["🔐 Login", "🆕 Sign Up"])

        with tab_login:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            remember_me = st.checkbox("Remember me", key="remember_me_checkbox")
            if st.button("Login", key="login_button"):
                login_user(username, password, remember_me)

        with tab_signup:
            st.subheader("Create Account")
            new_username = st.text_input("New Username", key="signup_username")
            new_password = st.text_input("New Password", type="password", key="signup_password")
            if st.button("Sign Up", key="signup_button"):
                signup_user(new_username, new_password)

        st.info("🔐 Please log in to continue.")

    else:
        st.sidebar.success("✅ You are logged in.")
        if st.sidebar.button("🚪 Logout"):
            logout()
