import os
from dotenv import load_dotenv
from groq import Groq
import ollama

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

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
        return f"Local LLM error: {str(e)}"


# ==============================
# GROQ CHAT FUNCTION
# ==============================
def groq_chat(history):
    if not groq_client:
        return "Groq API key not found."

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ⭐ UPDATED MODEL
            messages=history
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Groq error: {str(e)}"