import streamlit as st
from dotenv import load_dotenv

# Page config MUST be the first Streamlit command
st.set_page_config(page_title="PitchSide AI", page_icon="⚽", layout="centered", initial_sidebar_state="expanded")

import database

# Load environment variables
load_dotenv()

# Initialize our metrics database
database.init_db()

# Apply custom styling
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("style.css")

# --- SIDEBAR (Resume Enhancement) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8843/8843236.png", width=80)
    st.title("PitchSide Analytics")
    st.markdown("---")
    st.markdown("**Engine:** Gemini 2.5 Flash")
    st.markdown("**Status:** Online 🟢")
    st.markdown("---")

# Define pages for multi-page structure
chat_page = st.Page("views/chat.py", title="AI Chat & Predictions", icon="🤖", default=True)
scores_page = st.Page("views/scores.py", title="Live Scores", icon="🏟️")
analytics_page = st.Page("views/analytics.py", title="Team Analytics", icon="📊")

# Run navigation
pg = st.navigation([chat_page, scores_page, analytics_page])
pg.run()
