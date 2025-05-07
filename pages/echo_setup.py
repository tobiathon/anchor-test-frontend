# File: pages/echo_setup.py
# streamlit_page_hidden

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
    # Prepare tone safely
    tone_options = ["warm & gentle", "casual & direct", "reflective", "playful"]
    saved_tone = profile.get("preferred_tone", "warm & gentle")
    if saved_tone not in tone_options:
        saved_tone = "warm & gentle"

    tone = st.selectbox(
        "What tone feels best when someone talks with you?",
        tone_options,
        index=tone_options.index(saved_tone)
    )

    name = st.text_input("What should Echo call you?", value=profile.get("preferred_name", ""))

    goals_raw = ", ".join(profile.get("goals", []))
    goals = st.text_area(
        "What are 1–2 goals you're working on right now?",
        value=goals_raw,
        help="Separate multiple goals with commas"
    )

    avoid_raw = ", ".join(profile.get("avoid_phrases", []))
    avoid = st.text_area(
        "Are there any phrases Echo should avoid?",
        value=avoid_raw,
        help="Separate multiple phrases with commas"
    )

    submitted = st.form_submit_button("Save Settings")

if submitted:
    payload = {
        "preferred_tone": tone,
        "preferred_name": name,
        "goals": [g.strip() for g in goals.split(",") if g.strip()],
        "avoid_phrases": [p.strip() for p in avoid.split(",") if p.strip()]
    }

    try:
        res = requests.post(
            f"{API_URL}/profile/{user_id}/update",
            json=payload,
            headers=headers,
            timeout=15
        )
        res.raise_for_status()
        st.success("✨ Echo is now tuned to your preferences.")
    except Exception as e:
        st.error(f"❌ Failed to save profile. {e}")

#-- second form --#

st.markdown("---")
st.header("🛠️ Deeper Setup (Optional)")

# --- Load initial preferences ---
@st.cache_data(ttl=60)
def load_initial_preferences():
    try:
        res = requests.get(f"{API_URL}/profile/{user_id}/initial_preferences", headers=headers, timeout=15)
        res.raise_for_status()
        return res.json().get("initial_preferences", {})
    except Exception as e:
        st.error("⚠️ Could not load initial preferences.")
        return {}

initial_prefs = load_initial_preferences()

# --- Form for deeper setup ---
with st.form("initial_preferences_form"):
    language = st.selectbox(
        "Preferred Language",
        ["english", "spanish"],
        index=["english", "spanish"].index(initial_prefs.get("language", "english"))
    )

    communication_style = st.selectbox(
        "Communication Style",
        ["friendly", "professional", "direct", "thoughtful"],
        index=["friendly", "professional", "direct", "thoughtful"].index(initial_prefs.get("communication_style", "friendly"))
    )

    emotional_depth = st.selectbox(
        "Emotional Depth",
        ["deeper", "light", "balanced"],
        index=["deeper", "light", "balanced"].index(initial_prefs.get("emotional_depth", "deeper"))
    )

    stuck_strategy = st.selectbox(
        "If you feel stuck, should Echo:",
        ["give advice", "ask questions", "offer encouragement"],
        index=["give advice", "ask questions", "offer encouragement"].index(initial_prefs.get("stuck_strategy", "give advice"))
    )

    reply_length = st.selectbox(
        "Preferred Reply Length",
        ["short", "detailed", "balanced"],
        index=["short", "detailed", "balanced"].index(initial_prefs.get("reply_length", "detailed"))
    )

    deeper_submitted = st.form_submit_button("Save Deeper Preferences")

if deeper_submitted:
    payload = {
        "language": language,
        "communication_style": communication_style,
        "emotional_depth": emotional_depth,
        "stuck_strategy": stuck_strategy,
        "reply_length": reply_length
    }

    try:
        res = requests.post(f"{API_URL}/profile/{user_id}/set_initial_preferences", json=payload, headers=headers, timeout=15)
        res.raise_for_status()
        st.success("✨ Deeper preferences saved successfully!")
    except Exception as e:
        st.error(f"❌ Failed to save deeper preferences. {e}")
