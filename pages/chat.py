# File: pages/chat.py

import streamlit as st
from utils.api import send_chat_message
from components.chat_bubble import render_chat_bubble

def render_chat_interface():
    st.markdown("---")
    st.subheader("💬 Chat with Echo")

    with st.container():
        for sender, message in st.session_state.get("chat_history", []):
            render_chat_bubble(sender, message)

    with st.form(key="chat_form"):
        chat_input = st.text_input("Type your message...")
        submit_chat = st.form_submit_button("Send")

    if submit_chat and chat_input.strip():
        echo_reply = send_chat_message(chat_input.strip())
        if echo_reply:
            st.session_state.chat_history.append(("You", chat_input.strip()))
            st.session_state.chat_history.append(("Echo", echo_reply))
            st.experimental_rerun()
        else:
            st.error("❌ Failed to get response from Echo.")
    elif submit_chat:
        st.warning("Please enter a message.")
