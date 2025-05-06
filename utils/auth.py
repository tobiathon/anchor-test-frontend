# utils/auth.py

import requests
from requests.exceptions import RequestException
import streamlit as st

API_URL = "https://anchor-app.onrender.com"

def login_user(username, password, remember_me=False):
    print("✅ [auth.py] login_user called with remember_me =", remember_me)

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
            return True, token
        else:
            return False, "Login failed — no token received."

    except RequestException as e:
        return False, f"Could not connect: {e}"

def register_user(username: str, password: str) -> bool:
    try:
        response = requests.post(
            f"{API_URL}/auth/signup",
            data={"username": username, "password": password},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Failed to register user: {e}")
        return False

def logout(cookies):
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False

    clear_cookies(cookies=cookies)

    st.sidebar.info("You have been logged out.")
