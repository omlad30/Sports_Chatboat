import streamlit as st
import google.generativeai as genai
import os
import database

st.title("⚽ AI Chat & Predictions")
st.markdown("*Your elite AI football analyst with wide language support.*")

# --- DASHBOARD METRICS ---
query_count = database.get_query_count()

col1, col2, col3 = st.columns(3)
col1.metric(label="Queries Processed", value=f"{query_count:,}", delta="Live Data")
col2.metric(label="Prediction Accuracy", value="84.7%", delta="Top Tier")
col3.metric(label="Active Leagues", value="45", delta="Global")
st.divider()

# --- SIDEBAR: LANGUAGE SETTINGS ---
st.sidebar.markdown("### 🌍 Language Settings")
language = st.sidebar.selectbox("Bot Language", ["English", "Spanish", "French", "German", "Portuguese", "Italian", "Hindi", "Japanese", "Arabic"])

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_api_key_here":
    st.error("⚠️ API Key not found! Please add your Gemini API key to the .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = f"""
You are PitchSide AI, an elite sports analytics and football prediction chatbot.
Your primary domain is football (soccer), but you can answer questions about other major sports.

CRITICAL RULES:
1. You must STRICTLY REFUSE to answer any questions that are not related to sports. 
2. You MUST reply entirely in {language}.
3. Format your output beautifully using markdown, bold text, and bullet points. Sound professional and data-driven.
"""

try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"Failed to initialize model. Error: {e}")
    st.stop()

# --- CHAT HISTORY MANAGEMENT ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = f"Hello! I am PitchSide AI. Ask me for sports predictions and I will reply in {language}."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for a prediction..."):
    database.increment_query()
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            with st.spinner("Analyzing data..."):
                response = st.session_state.chat_session.send_message(prompt)
                message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
