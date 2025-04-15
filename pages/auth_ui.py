# File: utils/auth.py

import streamlit as st
from utils.cookies import save_cookies, clear_cookies
from utils.api import login_user as api_login_user, signup_user as api_signup_user
from utils.session_manager import logout_handler

# --- Login Function ---
def login_user(username: str, password: str, remember_me: bool = False):
    token = api_login_user(username, password)
    if token:
        st.session_state["token"] = token
        st.session_state["username"] = username
        st.session_state["remember_me"] = remember_me

        if remember_me:
            save_cookies({
                "token": token,
                "username": username
            })

        st.success("✅ Logged in!")
        st.rerun()
    else:
        st.error("❌ Login failed. Please try again.")

# --- Signup Function ---
def signup_user(username: str, password: str):
    success = api_signup_user(username, password)
    if success:
        st.success("✅ Account created! You can now log in.")
    else:
        st.error("❌ Signup failed.")

# --- Logout Function ---
def logout():
    logout_handler()

# --- Login Check Helper ---
def is_logged_in():
    return bool(st.session_state.get("token"))
