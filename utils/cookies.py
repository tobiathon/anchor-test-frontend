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
    cookies = get_cookie_manager()
    cookies[key] = value
    cookies.save()

def get_cookie(key):
    cookies = get_cookie_manager()
    return cookies.get(key)

def delete_cookie(key):
    cookies = get_cookie_manager()
    if key in cookies:
        del cookies[key]
    cookies.save()

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

def save_token_cookie(token, username):
    """
    Save token and username into cookies using the same cookie manager.
    """
    set_cookie("token", token)
    set_cookie("username", username)
