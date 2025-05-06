# File: utils/cookies.py

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

COOKIE_MAX_AGE = 2592000  # 30 days

def get_cookie_manager():
    cookies = EncryptedCookieManager(
        prefix="anchor_",
        password="my_secret_password",
        key="CookieManager",
        secure=True,           # Force HTTPS cookies
        samesite="None"         # Allow cross-site (iframe) cookies if needed
    )
    if not cookies.ready():
        st.stop()
    return cookies

def set_cookie(cookies, key, value, max_age_days=30):
    cookies[key] = value
    cookies.save()

def get_cookie(cookies, key):
    return cookies.get(key)

def delete_cookie(cookies, key):
    if key in cookies:
        del cookies[key]
    cookies.save()

def clear_cookies(cookies, keys=["token", "username"]):
    for key in keys:
        if key in cookies:
            del cookies[key]
    cookies.save()

def save_cookies(cookies, data: dict):
    for key, value in data.items():
        cookies[key] = value
    cookies.save()

def save_token_cookie(cookies, token, username):
    """
    Save token and username into cookies using the provided cookie manager.
    """
    set_cookie(cookies, "token", token)
    set_cookie(cookies, "username", username)

def load_token_cookie(cookies):
    """
    Load token and username from cookies.
    """
    token = cookies.get("token")
    username = cookies.get("username")
    return token, username
