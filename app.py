import streamlit as st
import os
from model_router import local_chat, groq_chat

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Chatbot")

st.title("💬 Chatbot (Local + Groq)")

# ==============================
# DETECT CLOUD ENVIRONMENT
# ==============================
is_cloud = "streamlit" in os.environ.get("HOSTNAME", "").lower()

# ==============================
# SESSION MEMORY
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# SIDEBAR
# ==============================
mode = st.sidebar.radio(
    "Select Mode",
    ["Local LLM", "Groq API"]
)

# Clear chat button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# Show warning if Local LLM selected in cloud
if mode == "Local LLM" and is_cloud:
    st.sidebar.warning("⚠️ Local LLM works only on local machine. Use Groq API in cloud.")

# ==============================
# DISPLAY CHAT HISTORY
# ==============================
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==============================
# USER INPUT
# ==============================
prompt = st.chat_input("Type a message...")

if prompt:
    # Save user message
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            if mode == "Local LLM":
                reply = local_chat(st.session_state.history)
            else:
                reply = groq_chat(st.session_state.history)

            st.write(reply)

    # Save assistant response
    st.session_state.history.append({"role": "assistant", "content": reply})