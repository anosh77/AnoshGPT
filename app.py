import streamlit as st
import google.generativeai as genai
import base64
from datetime import datetime

# Configure Gemini
genai.configure(api_key="AIzaSyA2iGZTy_pvNGa5jP5h4_2xPK6dH0QD8wo")
chat_model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Anosh Chat", page_icon="anosh.png", layout="centered")

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

avatar = encode_image("anosh.png")

# Styles
st.markdown(f"""
    <style>
        .top-right-avatar {{
            position: absolute;
            top: 15px; right: 20px;
            width: 60px; height: 60px;
            border-radius: 50%;
            box-shadow: 0 0 8px rgba(0,0,0,0.3);
            object-fit: cover;
            z-index: 10;
        }}
        body {{
            background-color: #0f1117;
            color: white;
        }}
        .bubble {{
            background: rgba(255,255,255,0.07);
            padding: 1rem;
            border-radius: 16px;
            margin-bottom: 12px;
            backdrop-filter: blur(8px);
            font-family: 'Segoe UI', sans-serif;
        }}
        .me {{
            border-left: 4px solid #00bfff;
        }}
        .reply {{
            border-left: 4px solid #2ecc71;
        }}
    </style>
    <img src="data:image/png;base64,{avatar}" class="top-right-avatar">
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>💬 Chat with Anosh</h2>", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = {}

if "chat_title" not in st.session_state:
    chat_title = f"Chat {datetime.now().strftime('%H:%M:%S')}"
    st.session_state.chat_title = chat_title
    st.session_state.messages[chat_title] = []

# Sidebar - Chat history
with st.sidebar:
    st.markdown("### Chat History")
    current = st.selectbox(
        "Previous Chats",
        options=list(st.session_state.messages.keys()),
        index=list(st.session_state.messages.keys()).index(st.session_state.chat_title)
    )
    if current != st.session_state.chat_title:
        st.session_state.chat_title = current

    if st.button("➕ New Chat"):
        new_title = f"Chat {datetime.now().strftime('%H:%M:%S')}"
        st.session_state.messages[new_title] = []
        st.session_state.chat_title = new_title
        st.rerun()

# Tone selector
tone = st.selectbox("Chat Presets", ["Default", "Sarcastic", "Poetic", "Technical"])

# Show chat bubbles
for entry in st.session_state.messages[st.session_state.chat_title]:
    role = "me" if entry["role"] == "user" else "reply"
    st.markdown(f"<div class='bubble {role}'>{entry['content']}</div>", unsafe_allow_html=True)

# Input field
msg = st.chat_input("Type something...")

if msg:
    st.session_state.messages[st.session_state.chat_title].append({"role": "user", "content": msg})
    st.markdown(f"<div class='bubble me'>{msg}</div>", unsafe_allow_html=True)

    query = msg
    if tone == "Sarcastic":
        query = f"Say this sarcastically: {msg}"
    elif tone == "Poetic":
        query = f"Turn this into a short poem: {msg}"
    elif tone == "Technical":
        query = f"Explain in a technical, detailed way: {msg}"

    try:
        result = chat_model.generate_content(query)
        reply = result.text.strip()
    except:
        reply = "Hmm... something's off."

    st.session_state.messages[st.session_state.chat_title].append({"role": "reply", "content": reply})
    st.markdown(f"<div class='bubble reply'>{reply}</div>", unsafe_allow_html=True)
