import os
import streamlit as st
from google import genai
from dotenv import load_dotenv


# =============================
# Load Environment Variables
# =============================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error(
        "❌ GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )
    st.stop()


# =============================
# Gemini Configuration
# =============================

MODEL = "gemini-3.6-flash"
MEMORY_LIMIT = 10

client = genai.Client(api_key=GEMINI_API_KEY)


# =============================
# Page Configuration
# =============================

st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)


# =============================
# Initialize Conversation Memory
# =============================

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# =============================
# Memory Management
# =============================

def limit_memory():
    """Keep only the most recent messages."""

    if len(st.session_state.conversation_history) > MEMORY_LIMIT:
        st.session_state.conversation_history = (
            st.session_state.conversation_history[-MEMORY_LIMIT:]
        )


def clear_memory():
    """Clear the current conversation memory."""

    st.session_state.conversation_history = []


# =============================
# Header
# =============================

st.title("🤖 AI Chatbot with Memory")

st.caption(
    f"Powered by Gemini • {MODEL} • "
    f"Memory limit: {MEMORY_LIMIT} messages"
)


# =============================
# Sidebar
# =============================

with st.sidebar:

    st.header("🧠 Memory")

    message_count = len(
        st.session_state.conversation_history
    )

    st.write(
        f"Messages in memory: "
        f"**{message_count}/{MEMORY_LIMIT}**"
    )

    if st.button(
        "🗑️ Clear Memory",
        use_container_width=True
    ):
        clear_memory()
        st.rerun()

    st.divider()

    st.subheader("Commands")

    st.write("**/clear** — Clear conversation memory")
    st.write("**/memory** — Show stored memory")

    st.divider()

    st.subheader("About")

    st.write(
        "This chatbot uses Google's Gemini API "
        "through the official Python SDK."
    )

    st.write(
        "Conversation history is stored temporarily "
        "during the active Streamlit session."
    )


# =============================
# Display Previous Messages
# =============================

for message in st.session_state.conversation_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =============================
# Chat Input
# =============================

user_message = st.chat_input("Type your message...")


if user_message:

    user_message = user_message.strip()

    if not user_message:
        st.warning("Please enter a message.")
        st.stop()


    # =========================
    # Commands
    # =========================

    if user_message.lower() == "/clear":

        clear_memory()
        st.rerun()


    if user_message.lower() == "/memory":

        st.subheader("🧠 Current Memory")

        if not st.session_state.conversation_history:

            st.info("Memory is empty.")

        else:

            for message in st.session_state.conversation_history:

                role = message["role"].capitalize()
                content = message["content"]

                st.write(
                    f"**{role}:** {content}"
                )

        st.stop()


    # =========================
    # Store User Message
    # =========================

    st.session_state.conversation_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    limit_memory()


    # =========================
    # Display User Message
    # =========================

    with st.chat_message("user"):
        st.markdown(user_message)


    # =========================
    # Prepare Conversation
    # =========================

    # Gemini uses "user" and "model" roles.
    # Our Streamlit memory uses "user" and "assistant".

    gemini_history = []

    for message in st.session_state.conversation_history:

        role = message["role"]

        if role == "assistant":
            role = "model"

        gemini_history.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )


    # =========================
    # Send Conversation to Gemini
    # =========================

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=gemini_history
        )

        assistant_message = response.text

        if not assistant_message:
            assistant_message = (
                "❌ Gemini returned an empty response."
            )


    except Exception as e:

        assistant_message = (
            f"❌ Gemini API error:\n\n{e}"
        )


    # =========================
    # Display AI Response
    # =========================

    with st.chat_message("assistant"):
        st.markdown(assistant_message)


    # =========================
    # Store AI Response
    # =========================

    st.session_state.conversation_history.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    limit_memory()