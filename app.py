# <<<<<<< HEAD
import os
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
st.set_page_config(page_title="Groq Chat", page_icon="💛", layout="wide")


@st.cache_resource
def get_client():
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


client = get_client()

# ---------------- Session State Init ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

# ==================== SIDEBAR ====================
st.sidebar.title("⚙️ Settings")

# Feature 1: New Chat (multiple conversations)
if st.sidebar.button("➕ New Chat"):
    new_name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_name] = []
    st.session_state.current_chat = new_name

# Feature 2: Switch between chats
st.session_state.current_chat = st.sidebar.selectbox(
    "💬 Your Chats",
    list(st.session_state.chats.keys()),
    index=list(st.session_state.chats.keys()).index(st.session_state.current_chat),
)

# Feature 3: Rename current chat
new_title = st.sidebar.text_input("✏️ Rename chat", value=st.session_state.current_chat)
if new_title != st.session_state.current_chat and new_title.strip():
    st.session_state.chats[new_title] = st.session_state.chats.pop(st.session_state.current_chat)
    st.session_state.current_chat = new_title

# Feature 4: Delete current chat
if st.sidebar.button("🗑️ Delete this chat"):
    del st.session_state.chats[st.session_state.current_chat]
    if not st.session_state.chats:
        st.session_state.chats = {"Chat 1": []}
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]
    st.rerun()

st.sidebar.divider()

MODEL = st.sidebar.selectbox("🤖 Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])

# Feature 5: Temperature control
temperature = st.sidebar.slider("🌡️ Creativity (Temperature)", 0.0, 1.0, 0.4, 0.1)

# Feature 6: Max response length control
max_tokens = st.sidebar.slider("📏 Max Response Length", 100, 2000, 1024, 100)

# Feature 7: Editable system prompt / persona
st.session_state.system_prompt = st.sidebar.text_area(
    "🧠 Bot Personality (System Prompt)",
    value=st.session_state.system_prompt,
    height=100,
)

# Feature 8: Clear current chat
if st.sidebar.button("🧹 Clear Current Chat"):
    st.session_state.chats[st.session_state.current_chat] = []
    st.rerun()

st.sidebar.divider()

# Feature 9: Download chat as .txt
messages = st.session_state.chats[st.session_state.current_chat]
if messages:
    chat_text = "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
    st.sidebar.download_button(
        "⬇️ Download This Chat",
        chat_text,
        file_name=f"{st.session_state.current_chat}.txt",
    )

# ==================== MAIN AREA ====================
st.title("💛 Groq Chatbot")
st.caption(f"Chat: **{st.session_state.current_chat}**  |  Model: `{MODEL}`")

messages = st.session_state.chats[st.session_state.current_chat]

USER_AVATAR = "🧑"
BOT_AVATAR = "🤖"

# Show existing messages with avatars
for msg in messages:
    avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])


def generate_reply():
    """Calls Groq API with streaming (typewriter effect) and shows stats."""
    messages_to_send = [{"role": "system", "content": st.session_state.system_prompt}]
    messages_to_send.extend(messages)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        placeholder = st.empty()
        full_reply = ""
        start_time = time.time()

        # Feature 10: Real streaming response (like ChatGPT typewriter effect)
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages_to_send,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_reply += delta
            placeholder.write(full_reply + "▌")
        placeholder.write(full_reply)

        # Feature 11: Response time + word count stats
        elapsed = round(time.time() - start_time, 2)
        word_count = len(full_reply.split())
        st.caption(f"⏱️ {elapsed}s  |  📝 {word_count} words")

    messages.append({"role": "assistant", "content": full_reply})


# Chat input box
user_text = st.chat_input("Type your message here...")
if user_text:
    messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.write(user_text)
    generate_reply()

# Feature 12: Regenerate last response
if messages and messages[-1]["role"] == "assistant":
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔄 Regenerate"):
            messages.pop()
            st.rerun()
# ===
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
st.set_page_config(page_title="Groq Chat", page_icon="💛")
@st.cache_resource
def get_client():
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
client = get_client()
#Sidebar
st.sidebar.title("Settings")
MODEL = st.sidebar.selectbox("Model", ["llama-3.1-8b-instant",
                                        "llama-3.3-70b-versatile"])  
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"user","content":"Hello"}]
for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])        

user_text = st.chat_input("Type your message here...")
if user_text:
    st.session_state.messages.append({"role":"user","content":user_text})
    with st.chat_message("user"):
        st.write(user_text)

#Ask Groq for a reply
with st.chat_message("assistant"):
    messages_to_send = [{"role":"system", "content":"you are helpful assistent."}]
    messages_to_send.extend(st.session_state.messages)
    stream = client.chat.completions.create(
        model =MODEL,
        messages=messages_to_send,
        temperature=0.4,
    )
    reply = stream.choices[0].message.content.strip()
    st.session_state.messages.append({"role":"assistant","content":reply})
    st.write(reply)
# >>>>>>> f290fd1271020eb7b3256d49aafac1030c386f19
