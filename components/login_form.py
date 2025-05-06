import streamlit as st
from utils.cookies import save_token_cookie, load_token_cookie, get_cookie_manager
from utils.auth import login_user

# Create cookies manager ONCE
cookies = get_cookie_manager()

def login_form():
    st.subheader("Login")

    # Load cookies
    saved_token, saved_username = load_token_cookie()

    if saved_username and "login_username" not in st.session_state:
        st.session_state["login_username"] = saved_username
    if saved_token and "token" not in st.session_state:
        st.session_state["token"] = saved_token

    # Build the form
    username_input = st.text_input("Username", key="login_username")
    password_input = st.text_input("Password", type="password", key="login_password")
    remember_me = st.checkbox("Remember me", key="remember_me_checkbox")

    if st.button("Login", key="login_button"):
        success, token = login_user(username_input, password_input, remember_me)
        if success and token:
            st.session_state["token"] = token
            st.session_state["username"] = username_input
            st.session_state["remember_me"] = remember_me
            if remember_me:
                save_token_cookie(token, username_input)

            # Use already-created cookies object if needed
            st.write("✅ Current Cookies after login:", cookies.dump())

            st.rerun()
        else:
            st.sidebar.error("❌ Login failed.")
