import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

MODEL_NAME = "gpt-5.6-luna"
MEMORY_LIMIT = 10

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -----------------------------
# Initialize memory
# -----------------------------
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# -----------------------------
# Helper: limit memory
# -----------------------------
def limit_memory():
    if len(st.session_state.conversation_history) > MEMORY_LIMIT:
        st.session_state.conversation_history = (
            st.session_state.conversation_history[-MEMORY_LIMIT:]
        )


# -----------------------------
# Header
# -----------------------------
st.title("🤖 AI Chatbot with Memory")

st.caption(
    f"Powered by Ollama • {MODEL_NAME} • "
    f"Memory limit: {MEMORY_LIMIT} messages"
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("🧠 Memory")

    message_count = len(
        st.session_state.conversation_history
    )

    st.write(
        f"Messages in memory: "
        f"**{message_count}/{MEMORY_LIMIT}**"
    )

    if st.button("🗑️ Clear Memory"):

        st.session_state.conversation_history = []

        st.rerun()

    st.divider()

    st.subheader("Commands")

    st.write("**/clear** — Clear conversation memory")

    st.write("**/memory** — Show stored memory")

    st.divider()

    st.subheader("About")

    st.write(
        "This chatbot uses an in-memory conversation "
        "history to remember previous messages."
    )

    st.write(
        "Older messages are automatically removed "
        "when the memory limit is reached."
    )


# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.conversation_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------
user_message = st.chat_input("Type your message...")


if user_message:

    user_message = user_message.strip()

    # -------------------------
    # Input validation
    # -------------------------
    if not user_message:

        st.warning("Please enter a message.")

        st.stop()


    # -------------------------
    # /clear command
    # -------------------------
    if user_message.lower() == "/clear":

        st.session_state.conversation_history = []

        st.rerun()


    # -------------------------
    # /memory command
    # -------------------------
    if user_message.lower() == "/memory":

        st.subheader("🧠 Current Memory")

        if not st.session_state.conversation_history:

            st.info("Memory is empty.")

        else:

            for message in st.session_state.conversation_history:

                role = message["role"].capitalize()

                content = message["content"]

                st.write(f"**{role}:** {content}")

        st.stop()


    # -------------------------
    # Add user message
    # -------------------------
    st.session_state.conversation_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    limit_memory()


    # -------------------------
    # Display user message
    # -------------------------
    with st.chat_message("user"):

        st.markdown(user_message)


    # ------------------------
# Send conversation to OpenAI
# ------------------------
try:
    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in st.session_state.conversation_history
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=conversation_text
    )

    assistant_message = response.output_text

except Exception as e:
    assistant_message = f"❌ Error: {e}"


    # -------------------------
    # Display AI response
    # -------------------------
    with st.chat_message("assistant"):

        st.markdown(assistant_message)


    # -------------------------
    # Store AI response
    # -------------------------
    st.session_state.conversation_history.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    limit_memory()