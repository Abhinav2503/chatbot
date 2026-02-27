import streamlit as st
import os
import zipfile
from io import BytesIO
from model_router import local_chat, groq_chat

# ==============================
# PAGE CONFIG (MUST BE FIRST)
# ==============================
st.set_page_config(page_title="Chatbot")

st.title("BUDDY")

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
mode = st.sidebar.radio("Select Mode", ["Local LLM", "Groq API"])

# Clear chat button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# ==============================
# DOWNLOAD PROJECT BUTTON
# ==============================
def create_zip():
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for file in ["app.py", "model_router.py", "requirements.txt"]:
            if os.path.exists(file):
                z.write(file)
    buffer.seek(0)
    return buffer

st.sidebar.download_button(
    "⬇️ Download project to run locally",
    data=create_zip(),
    file_name="chatbot_project.zip",
    mime="application/zip"
)

# ==============================
# LOCAL LLM WARNING (CLOUD)
# ==============================
if mode == "Local LLM" and is_cloud:
    st.sidebar.warning(
        "⚠️ Local LLM works only on local machine.\n\n"
        "Download project and run locally with Ollama."
    )

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

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if mode == "Local LLM":
                reply = local_chat(st.session_state.history)
            else:
                reply = groq_chat(st.session_state.history)

            st.write(reply)

    # Save assistant reply
    st.session_state.history.append({"role": "assistant", "content": reply})