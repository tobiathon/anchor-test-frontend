# utils/session_manager.py

import time
import streamlit as st

def init_session_state():
    if "token" not in st.session_state:
        st.session_state["token"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "rerun_triggered" not in st.session_state:
        st.session_state["rerun_triggered"] = False
    if "remember_me" not in st.session_state:
        st.session_state["remember_me"] = False

def set_session_state(username, token):
    st.session_state["username"] = username
    st.session_state["token"] = token

def logout_handler():
    st.session_state.clear()
    st.sidebar.info("You have been logged out.")
    time.sleep(1)
    st.rerun()
