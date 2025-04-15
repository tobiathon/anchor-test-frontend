# Signup UI

# File: frontend/components/signup_form.py

import streamlit as st
from utils.api import signup_user

def signup_form():
    st.subheader("Create Account")
    new_username = st.text_input("New Username", key="signup_username")
    new_password = st.text_input("New Password", type="password", key="signup_password")

    if st.button("Sign Up", key="signup_button"):
        success = signup_user(new_username, new_password)
        if success:
            st.sidebar.success("✅ Account created! Please log in.")
