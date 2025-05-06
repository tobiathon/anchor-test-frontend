# app.py
import sys
import os
import streamlit as st

# Add the current directory (root of your project) to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Anchor Journal", layout="centered")

from pages.auth_ui_logic import login_signup_flow
from pages.journal import render_journal_entry_form
from pages.chat import render_chat_interface
from utils.cookies import get_cookie_manager
from utils.session_manager import init_session_state, logout_handler

# Get the cookie manager
cookies = get_cookie_manager()

# Initialize session state with cookies
init_session_state(cookies)

st.title("🧠 Anchor Journal Portal")

try:
    if not st.session_state.get("token"):
        login_signup_flow(cookies)  # ✅ Pass cookies here
    else:
        st.sidebar.success("✅ You are logged in.")

        # 🎛️ Add Echo Setup Link
        st.sidebar.markdown("---")
        st.sidebar.markdown("🧠 **Echo Settings**")
        st.sidebar.page_link("pages/echo_setup.py", label="🎛️ Customize Echo")

        # 🚪 Logout Button
        if st.sidebar.button("🚪 Logout"):
            logout_handler(cookies)

        render_journal_entry_form()
        render_chat_interface()

except Exception as e:
    st.error(f"Something went wrong: {e}")

    ## testing for later
