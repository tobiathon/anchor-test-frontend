# File: frontend/utils/cookies.py

from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

COOKIE_MAX_AGE = 2592000  # 30 days
cookies = EncryptedCookieManager(prefix="anchor_", password="my_secret_password")

def get_cookie_manager():
    if not cookies.ready():
        st.stop()
    return cookies

def clear_cookies(keys=["token", "username"]):
    for key in keys:
        if key in cookies:
            del cookies[key]
    cookies.save()

def save_cookies(data: dict):
    for key, value in data.items():
        cookies[key] = value
    cookies.save()
