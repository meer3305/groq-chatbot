import streamlit as st
import os
import requests
from datetime import datetime

# --- API Key ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# --- Custom CSS for better UI and input visibility ---
st.markdown("""
    <style>
    body { background: #18181b; color: #f4f4f5; }
    .stApp { background: #18181b; }
    .main { background: transparent; }
    .chat-message {
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        color: #18181b;
    }
    .chat-message.user {
        background: #fff;
        align-self: flex-end;
        border: 1px solid #d4d4d8;
    }
    .chat-message.assistant {
        background: #f4f4f5;
        border: 1px solid #18181b;
    }
    .stChatInput > div {
        border-radius: 12px !important;
        border: 1.5px solid #18181b !important;
        background: #fff !important;
        color: #18181b !important;
    }
    .stChatInput textarea, .stChatInput input {
        color: #18181b !important;
        background: #fff !important;
    }
    .stSpinner > div { color: #18181b !important; }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 1rem;">
        <img src="https://img.icons8.com/color/96/robot-2.png" width="48"/>
        <h1 style="margin-bottom: 0; color: #fff;">Groq Chatbot</h1>
    </div>
    <p style="color: #a1a1aa; font-size: 1.1rem; margin-top: 0;">
        <b>Built with LLaMA 3 & Streamlit</b>
    </p>
    """,
    unsafe_allow_html=True
)

# --- Session State for Multiple Chats ---
if "chats" not in st.session_state:
    st.session_state.chats = {}  # {chat_id: [messages]}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --- Sidebar for Chat Sessions ---
st.sidebar.title("💬 Chats")
chat_names = list(st.session_state.chats.keys())
if st.sidebar.button("➕ New Chat"):
    chat_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chats[chat_id] = []
    st.session_state.current_chat = chat_id

# Select chat
if chat_names:
    selected = st.sidebar.radio("Previous Chats", chat_names, index=chat_names.index(st.session_state.current_chat) if st.session_state.current_chat in chat_names else 0)
    st.session_state.current_chat = selected
else:
    # If no chat, create one
    chat_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chats[chat_id] = []
    st.session_state.current_chat = chat_id

messages = st.session_state.chats[st.session_state.current_chat]

# --- Display Chat History ---
for msg in messages:
    align = "flex-end" if msg["role"] == "user" else "flex-start"
    avatar = (
        "https://img.icons8.com/color/48/user-male-circle--v1.png"
        if msg["role"] == "user"
        else "https://img.icons8.com/color/48/robot-2.png"
    )
    label = "You" if msg["role"] == "user" else "Groq"
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: {align};">
            <img src="{avatar}" width="32" style="margin-right: 0.5rem;"/>
            <div>
                <div style="font-size:0.9rem;color:#6366f1;font-weight:bold;">{label}</div>
                <div class="chat-message {msg['role']}">{msg['content']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- User Input ---
user_input = st.chat_input("Type your message and press Enter...")

# --- Groq API Function ---
def get_groq_response(user_message, chat_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages += chat_history
    messages.append({"role": "user", "content": user_message})
    payload = {
        "model": "llama3-70b-8192",
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# --- Handle User Message ---
if user_input:
    messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Groq is thinking..."):
        try:
            reply = get_groq_response(user_input, messages[:-1])
        except Exception as e:
            reply = f"Error: {e}"
    messages.append({"role": "assistant", "content": reply})

    # Show assistant reply
    align = "flex-start"
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; justify-content: {align};">
            <img src="https://img.icons8.com/color/48/robot-2.png" width="32" style="margin-right: 0.5rem;"/>
            <div>
                <div style="font-size:0.9rem;color:#6366f1;font-weight:bold;">Groq</div>
                <div class="chat-message assistant">{reply}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Footer Section ---
st.markdown(
    """
    <footer style="text-align: center; margin-top: 2rem;">
        <p style="color: #6366f1;">&copy; 2023 Groq Inc. All rights reserved.</p>
        <p style="color: #6366f1;">Built with ❤️ using Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True
)
