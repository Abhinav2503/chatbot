import streamlit as st
from model_router import local_chat, groq_chat

st.set_page_config(page_title="Chatbot")

st.title("💬 Chatbot (Local + Groq)")

# Chat memory
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar mode selector
mode = st.sidebar.radio(
    "Select Mode",
    ["Local LLM", "Groq API"]
)

# Show history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
prompt = st.chat_input("Type a message...")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if mode == "Local LLM":
                reply = local_chat(st.session_state.history)
            else:
                reply = groq_chat(st.session_state.history)

            st.write(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})