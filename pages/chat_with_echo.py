# File: pages/chat_with_echo.py

import streamlit as st
from utils.api import send_chat_message
from components.chat_bubble import render_chat_bubble

def render_chat_with_echo():
    st.title("💬 Chat with Echo")

    # === Initialize chat session state ===
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # === Chat Display Area ===
    chat_placeholder = st.container()

    with chat_placeholder:
        for sender, message in st.session_state.chat_history:
            render_chat_bubble(sender, message)

    # === Input Form at Bottom ===
    st.markdown("---")
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message Echo...",
            placeholder="Type your message and press Enter"
        )
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.chat_history.append(("You", user_input.strip()))
        echo_response = send_chat_message(user_input.strip())
        if echo_response:
            st.session_state.chat_history.append(("Echo", echo_response))
            st.rerun()
        else:
            st.error("❌ Failed to get response from Echo.")
    elif submitted:
        st.warning("Please enter a message.")
