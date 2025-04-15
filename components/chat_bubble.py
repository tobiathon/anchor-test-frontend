# HTML components for chat styling

# File: frontend/components/chat_bubble.py

import streamlit as st

def render_chat_bubble(sender: str, message: str):
    if sender == "You":
        st.markdown(
            f"""
            <div style='text-align:right;background:#f5f5f5;color:#000;
                        padding:10px 14px;border-radius:12px;margin:6px 0;
                        max-width:80%;margin-left:auto'>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align:left;background:#ffffff;color:#000;
                        padding:10px 14px;border-radius:12px;margin:6px 0;
                        max-width:80%;margin-right:auto'>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )
