# Login, signup, logout logic

# File: utils/auth.py
import requests
from requests.exceptions import RequestException
import streamlit as st
from utils.cookies import get_cookie_manager

API_URL = "https://anchor-app.onrender.com"

# --- Login Function ---
def login_user(username, password, remember_me):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password},
            timeout=20
        )
        response.raise_for_status()
        token = response.json().get("access_token")

        if token:
            st.session_state["token"] = token
            st.session_state["username"] = username
            st.session_state["remember_me"] = remember_me
            if remember_me:
                cookies = get_cookie_manager()
                cookies["token"] = token
                cookies["username"] = username
                cookies.save()

            st.rerun()  # 🔁 Trigger app to refresh with login state

            return True, None  # Optional: this line won't be reached after rerun
        else:
            return False, "Login failed — no token received."

    except RequestException as e:
        return False, f"Could not connect: {e}"

# --- Signup Function ---
def signup_user(new_username, new_password):
    try:
        response = requests.post(
            f"{API_URL}/auth/signup",
            data={"username": new_username, "password": new_password},
            timeout=20
        )
        response.raise_for_status()
        return True, None
    except RequestException as e:
        return False, f"Failed to create account: {e}"

# --- Logout Function ---
def logout():
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False

    cookies = get_cookie_manager()
    if "token" in cookies:
        del cookies["token"]
    if "username" in cookies:
        del cookies["username"]
    cookies.save()

    st.sidebar.info("You have been logged out.")
