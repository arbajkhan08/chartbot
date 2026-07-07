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