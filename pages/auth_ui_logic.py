# File: pages/auth_ui_logic.py

import streamlit as st
from utils.auth import login_user, signup_user

def login_signup_flow():
    tab_login, tab_signup = st.sidebar.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab_login:
        st.subheader("Login")
        username_input = st.text_input("Username", key="login_username")
        password_input = st.text_input("Password", type="password", key="login_password")
        remember_me = st.checkbox("Remember me", key="remember_me_checkbox")

        if st.button("Login", key="login_button"):
            login_user(username_input, password_input, remember_me)

    with tab_signup:
        st.subheader("Create Account")
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")

        if st.button("Sign Up", key="signup_button"):
            signup_user(new_username, new_password)

    st.info("🔐 Please log in to continue.")
