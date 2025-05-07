# File: pages/chat_with_echo.py
# streamlit_page_hidden

import streamlit as st
from utils.api import send_chat_message

def render_chat_with_echo():
    st.title("💬 Chat with Echo")

    # === Initialize chat session state ===
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # === Custom Message Renderer (modern bubbles) ===
    def render_message(sender, message):
        is_user = sender == "You"

        bubble_color = "#DCF8C6" if is_user else "#ECECEC"
        align = "flex-end" if is_user else "flex-start"
        text_align = "right" if is_user else "left"
        border_radius = "18px 18px 0px 18px" if is_user else "18px 18px 18px 0px"

        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: {align};
                margin: 5px 0;
            ">
                <div style="
                    background-color: {bubble_color};
                    color: black;
                    padding: 10px 15px;
                    border-radius: {border_radius};
                    max-width: 70%;
                    text-align: {text_align};
                    box-shadow: 0px 1px 5px rgba(0,0,0,0.1);
                    word-wrap: break-word;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # === Chat Display Area ===
    chat_placeholder = st.container()

    with chat_placeholder:
        for sender, message in st.session_state.chat_history:
            render_message(sender, message)

    # === Input Form at Bottom ===
    st.markdown("---")
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input = st.text_area(
            "Message Echo...",
            placeholder="Type your message and press Enter",
            height=80,
            max_chars=2000,
            key="chat_input_area"
        )
            # === Input Form at Bottom ===
    st.markdown("---")
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input = st.text_area(
            "Message Echo...",
            placeholder="Type your message and press Enter",
            height=80,
            max_chars=2000,
            key="chat_input_area"
        )
        st.markdown(
        """
        <div style="display:none">
        <script>
        const interval = setInterval(() => {
            const textarea = window.parent.document.querySelector('textarea[data-streamlit-key="chat_input_area"]');
            if (textarea) {
                textarea.addEventListener('keydown', function(event) {
                    if (event.key === 'Enter' && !event.shiftKey) {
                        event.preventDefault();
                        const submitButton = window.parent.document.querySelector('button[kind="formSubmit"]');
                        if (submitButton) {
                            submitButton.click();
                        }
                    }
                });
                clearInterval(interval);  // Stop checking once we find it
            }
        }, 300);  // Check every 300ms until it loads
        </script>
        </div>
        """,
        unsafe_allow_html=True
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
