# app.py
import streamlit as st
from frontend.auth import login_signup_flow
from frontend.journal import render_journal_entry_form
from frontend.chat import render_chat_interface
from frontend.utils.session_manager import init_session_state, logout_handler

st.set_page_config(page_title="Anchor Journal", layout="centered")
st.title("🧠 Anchor Journal Portal")

init_session_state()

try:
    if not st.session_state["token"]:
        login_signup_flow()
    else:
        st.sidebar.success("✅ You are logged in.")
        if st.sidebar.button("🚪 Logout"):
            logout_handler()

        # Optional tabbed layout — enable if desired:
        # tab1, tab2 = st.tabs(["📓 Journal", "💬 Chat"])
        # with tab1:
        #     render_journal_entry_form()
        # with tab2:
        #     render_chat_interface()

        # Current simple layout:
        render_journal_entry_form()
        render_chat_interface()

except Exception as e:
    st.error(f"Something went wrong: {e}")
