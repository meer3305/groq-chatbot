import streamlit as st
import requests, os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = "http://localhost:8000/chat"  # FastAPI endpoint

# --- Custom CSS for better UI ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .main {
        background: transparent;
    }
    .chat-message {
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .chat-message.user {
        background: #f1f5f9;
        align-self: flex-end;
        border: 1px solid #c7d2fe;
    }
    .chat-message.assistant {
        background: #eef2ff;
        border: 1px solid #818cf8;
    }
    .stChatInput > div {
        border-radius: 12px !important;
        border: 1.5px solid #818cf8 !important;
        background: #f1f5f9 !important;
    }
    .stSpinner > div {
        color: #6366f1 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 1rem;">
        <img src="https://img.icons8.com/color/96/robot-2.png" width="48"/>
        <h1 style="margin-bottom: 0;">Groq Chatbot</h1>
    </div>
    <p style="color: #6366f1; font-size: 1.1rem; margin-top: 0;">
        <b>Built with LLaMA 3, FastAPI & Streamlit</b>
    </p>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages with custom styling
for msg in st.session_state.messages:
    align = "flex-end" if msg["role"] == "user" else "flex-start"
    avatar = (
        "https://img.icons8.com/color/48/user-male-circle--v1.png"
        if msg["role"] == "user"
        else "https://img.icons8.com/color/48/robot-2.png"
    )
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: {align};">
            <img src="{avatar}" width="32" style="margin-right: 0.5rem;"/>
            <div class="chat-message {msg['role']}">{msg['content']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    align = "flex-end"
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: {align};">
            <img src="https://img.icons8.com/color/48/user-male-circle--v1.png" width="32" style="margin-right: 0.5rem;"/>
            <div class="chat-message user">{user_input}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("🤖 Groq is thinking..."):
        try:
            response = requests.post(BACKEND_URL, json={"message": user_input})
            data = response.json()
            reply = data.get("reply") or data.get("error", "Unknown error.")
        except Exception as e:
            reply = f"API error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    align = "flex-start"
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: {align};">
            <img src="https://img.icons8.com/color/48/robot-2.png" width="32" style="margin-right: 0.5rem;"/>
            <div class="chat-message assistant">{reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
