# API request functions

# File: frontend/utils/api.py

import requests
import streamlit as st
from requests.exceptions import RequestException

API_URL = "https://anchor-app.onrender.com"  # Or "http://localhost:8000" for local testing

def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state['token']}"}

def send_chat_message(message: str):
    try:
        res = requests.post(
            f"{API_URL}/chat/echo_chat",
            json={"user_id": st.session_state["username"], "message": message},
            headers=get_auth_headers(),
            timeout=20
        )
        res.raise_for_status()
        return res.json().get("echo_response", "")
    except RequestException as e:
        st.error(f"❌ Failed to contact Echo: {e}")
        return None

def submit_journal_entry(entry_text: str):
    try:
        res = requests.post(
            f"{API_URL}/upload_journal",
            json={"user_id": st.session_state["username"], "entry_text": entry_text},
            headers=get_auth_headers(),
            timeout=20
        )
        res.raise_for_status()
        return res.json()
    except RequestException as e:
        st.error(f"❌ Failed to submit journal: {e}")
        return None

def login_user(username: str, password: str):
    try:
        res = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password},
            timeout=20
        )
        res.raise_for_status()
        return res.json().get("access_token")
    except RequestException as e:
        st.sidebar.error(f"⚠️ Could not connect: {e}")
        return None

def signup_user(username: str, password: str):
    try:
        res = requests.post(
            f"{API_URL}/auth/signup",
            data={"username": username, "password": password},
            timeout=20
        )
        res.raise_for_status()
        return True
    except RequestException as e:
        st.sidebar.error(f"❌ Failed to create account: {e}")
        return False
