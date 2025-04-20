# File: pages/echo_setup.py

import streamlit as st
import requests

API_URL = "https://anchor-app.onrender.com"  # Adjust if running locally
headers = {}

# Load token and username from session
if "token" not in st.session_state or "username" not in st.session_state:
    st.warning("🔐 Please log in to access Echo's setup.")
    st.stop()

headers["Authorization"] = f"Bearer {st.session_state['token']}"
user_id = st.session_state["username"]

st.title("🎛️ Set Up Echo Just for You")
st.write("Let’s personalize Echo so it speaks to you in a way that feels natural, supportive, and real.")

# --- Load current profile ---
@st.cache_data(ttl=60)
def load_profile():
    try:
        res = requests.get(f"{API_URL}/profile/{user_id}", headers=headers, timeout=15)
        res.raise_for_status()
        return res.json().get("profile", {})
    except Exception as e:
        st.error("⚠️ Could not load profile.")
        return {}

profile = load_profile()

# --- UI Form ---
with st.form("echo_setup_form"):
    tone = st.selectbox(
        "What tone feels best when someone talks with you?",
        ["warm & gentle", "casual & direct", "reflective", "playful"],
        index=["warm & gentle", "casual & direct", "reflective", "playful"].index(profile.get("preferred_tone", "warm & gentle"))
    )

    name = st.text_input("What should Echo call you?", value=profile.get("preferred_name", ""))

    goals_raw = ", ".join(profile.get("goals", []))
    goals = st.text_area("What are 1–2 goals you're working on right now?", value=goals_raw, help="Separate multiple goals with commas")

    avoid_raw = ", ".join(profile.get("avoid_phrases", []))
    avoid = st.text_area("Are there any phrases Echo should avoid?", value=avoid_raw, help="Separate multiple phrases with commas")

    submitted = st.form_submit_button("Save Settings")

if submitted:
    payload = {
        "preferred_tone": tone,
        "preferred_name": name,
        "goals": [g.strip() for g in goals.split(",") if g.strip()],
        "avoid_phrases": [p.strip() for p in avoid.split(",") if p.strip()]
    }

    try:
        res = requests.post(f"{API_URL}/profile/{user_id}/update", json=payload, headers=headers, timeout=15)
        res.raise_for_status()
        st.success("✨ Echo is now tuned to your preferences.")
    except Exception as e:
        st.error(f"❌ Failed to save profile. {e}")