import streamlit as st
import requests


# =============================
# Page Configuration
# =============================

st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)


# =============================
# Configuration
# =============================

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"
MEMORY_LIMIT = 10


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
    f"Powered by Ollama • {MODEL} • "
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

    if st.button("🗑️ Clear Memory", use_container_width=True):
        clear_memory()
        st.rerun()

    st.divider()

    st.subheader("Commands")

    st.write("**/clear** — Clear conversation memory")
    st.write("**/memory** — Show stored memory")

    st.divider()

    st.subheader("About")

    st.write(
        "This chatbot uses Ollama to run "
        "a local Llama 3.2 model."
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
    # Send Conversation to Ollama
    # =========================

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": st.session_state.conversation_history,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        assistant_message = (
            response.json()["message"]["content"]
        )


    except requests.exceptions.ConnectionError:

        assistant_message = (
            "❌ Could not connect to Ollama.\n\n"
            "Please make sure Ollama is running."
        )


    except requests.exceptions.Timeout:

        assistant_message = (
            "❌ Ollama took too long to respond."
        )


    except Exception as e:

        assistant_message = f"❌ Error: {e}"


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