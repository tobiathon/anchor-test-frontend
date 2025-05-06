# File: frontend/utils/session_manager.py

import time
import streamlit as st
from utils.cookies import clear_cookies

def init_session_state(cookies):
    if "token" not in st.session_state:
        st.session_state["token"] = cookies.get("token") if cookies.get("token") else None
    if "username" not in st.session_state:
        st.session_state["username"] = cookies.get("username") if cookies.get("username") else None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "rerun_triggered" not in st.session_state:
        st.session_state["rerun_triggered"] = False
    if "remember_me" not in st.session_state:
        st.session_state["remember_me"] = False

def set_session_state(username, token):
    st.session_state["username"] = username
    st.session_state["token"] = token

def logout_handler(cookies):
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False

    clear_cookies(["token", "username"], cookies)
    st.sidebar.info("You have been logged out.")
    time.sleep(1)
    st.rerun()
