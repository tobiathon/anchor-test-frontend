# Login UI

# File: frontend/components/login_form.py

import streamlit as st
from utils.cookies import save_token_cookie
from utils.api import login_user

def login_form():
    st.subheader("Login")
    username_input = st.text_input("Username", key="login_username")
    password_input = st.text_input("Password", type="password", key="login_password")
    remember_me = st.checkbox("Remember me", key="remember_me_checkbox")

    if st.button("Login", key="login_button"):
        token = login_user(username_input, password_input)
        if token:
            st.session_state["token"] = token
            st.session_state["username"] = username_input
            st.session_state["remember_me"] = remember_me
            if remember_me:
                save_token_cookie(token, username_input)
            st.experimental_rerun()
        else:
            st.sidebar.error("❌ Login failed.")
