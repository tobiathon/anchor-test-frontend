# File: utils/cookies.py

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

COOKIE_MAX_AGE = 2592000  # 30 days

def get_cookie_manager():
    cookies = EncryptedCookieManager(prefix="anchor_", password="my_secret_password")
    if not cookies.ready():
        st.stop()
    return cookies

def set_cookie(key, value, max_age_days=30):
    st.session_state[f"_cookie_{key}"] = value
    st.experimental_set_query_params(**{key: value})  # fallback way

def get_cookie(key):
    return st.session_state.get(f"_cookie_{key}", None)

def delete_cookie(key):
    st.session_state.pop(f"_cookie_{key}", None)

def clear_cookies(keys=["token", "username"]):
    cookies = get_cookie_manager()
    for key in keys:
        if key in cookies:
            del cookies[key]
    cookies.save()

def save_cookies(data: dict):
    cookies = get_cookie_manager()
    for key, value in data.items():
        cookies[key] = value
    cookies.save()
