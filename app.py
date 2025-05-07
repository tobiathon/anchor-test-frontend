# app.py
import sys
import os
import streamlit as st

# Add the current directory (root of your project) to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Anchor Journal", layout="centered")

from utils.auth_ui_logic import login_signup_flow
from utils.session_manager import init_session_state, logout_handler

# Initialize session state
init_session_state()

st.title("🧠 Anchor Journal Portal")

try:
    if not st.session_state.get("token"):
        login_signup_flow()
    else:
        st.sidebar.success(f"✅ Logged in as {st.session_state.get('username')}.")

        # 🎯 Manual sidebar navigation
        st.sidebar.markdown("---")
        st.sidebar.header("🧭 Navigation")

        page = st.sidebar.radio(
            "Go to",
            ["🏠 Welcome", "📝 Journal", "💬 Chat with Echo", "🎛️ Customize Echo"]
        )

        if page == "🏠 Welcome":
            st.title("🏠 Welcome to Anchor")
            st.write("This is your mental fortress portal. Ready to dive in?")

        elif page == "📝 Journal":
            from pages.journal import render_journal_entry_form
            render_journal_entry_form()

        elif page == "💬 Chat with Echo":
            from pages.chat_with_echo import render_chat_with_echo
            render_chat_with_echo()

        elif page == "🎛️ Customize Echo":
            from pages.echo_setup import render_page as render_setup_page
            render_setup_page()

        st.sidebar.markdown("---")
        st.sidebar.header("🧠 Echo Settings")

        if st.sidebar.button("🚪 Logout"):
            logout_handler()

except Exception as e:
    st.error(f"Something went wrong: {e}")
