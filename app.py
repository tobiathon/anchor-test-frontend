# app.py
import streamlit as st
st.set_page_config(page_title="Anchor Journal", layout="centered")
from pages.auth_ui import login_signup_flow
from pages.journal import render_journal_entry_form
from pages.chat import render_chat_interface
from utils.session_manager import init_session_state, logout_handler

#st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

init_session_state()

try:
    if not st.session_state["token"]:
        login_signup_flow()
    else:
        st.sidebar.success("✅ You are logged in.")
        if st.sidebar.button("🚪 Logout"):
            logout_handler()

        render_journal_entry_form()
        render_chat_interface()

except Exception as e:
    st.error(f"Something went wrong: {e}")
