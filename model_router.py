import os
from dotenv import load_dotenv
from groq import Groq
import ollama
import streamlit as st

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

# Get API key from local (.env) OR Streamlit secrets (cloud)
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

# Create Groq client safely
groq_client = Groq(api_key=api_key) if api_key else None


# ==============================
# LOCAL CHAT FUNCTION
# ==============================
def local_chat(history):
    try:
        response = ollama.chat(
            model="llama3",
            messages=history
        )
        return response["message"]["content"]

    except Exception as e:
        return (
            "⚠️ Local LLM unavailable.\n\n"
            "This happens when Ollama is not installed (e.g., cloud deployment).\n\n"
            f"Error: {str(e)}"
        )


# ==============================
# GROQ CHAT FUNCTION
# ==============================
def groq_chat(history):
    if not groq_client:
        return (
            "⚠️ Groq API key not found.\n\n"
            "Add GROQ_API_KEY in Streamlit secrets or .env file."
        )

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"⚠️ Groq error: {str(e)}"

