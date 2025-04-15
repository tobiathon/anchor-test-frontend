# File: frontend/utils/session_manager.py

import time
import streamlit as st
from utils.cookies import get_cookie_manager, clear_cookies

cookies = get_cookie_manager()

def init_session_state():
    if "token" not in st.session_state:
        st.session_state["token"] = cookies.get("token") if "token" in cookies else None
    if "username" not in st.session_state:
        st.session_state["username"] = cookies.get("username") if "username" in cookies else None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "rerun_triggered" not in st.session_state:
        st.session_state["rerun_triggered"] = False
    if "remember_me" not in st.session_state:
        st.session_state["remember_me"] = False

def logout_handler():
    st.session_state["token"] = None
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["remember_me"] = False

    clear_cookies()
    st.sidebar.info("You have been logged out.")
    time.sleep(1)
    st.experimental_rerun()
