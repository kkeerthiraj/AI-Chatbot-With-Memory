import requests


# ==============================
# Configuration
# ==============================

MODEL = "llama3.2:3b"
MAX_MESSAGES = 10

# In-memory conversation history
conversation_history = []


# ==============================
# Memory Management
# ==============================

def trim_memory():
    """
    Keep only the most recent conversation messages.
    Older messages are removed using FIFO.
    """

    while len(conversation_history) > MAX_MESSAGES:
        conversation_history.pop(0)

        # Remove the matching message so user/assistant
        # messages stay together.
        if conversation_history:
            conversation_history.pop(0)


def show_memory():
    """Display current memory information."""

    print()
    print("-" * 40)
    print(f"Memory: {len(conversation_history)}/{MAX_MESSAGES} messages")

    if conversation_history:
        print("Stored conversation:")
        for message in conversation_history:
            role = message["role"].capitalize()
            content = message["content"]

            # Keep the display short
            if len(content) > 60:
                content = content[:60] + "..."

            print(f"  {role}: {content}")
    else:
        print("Memory is empty.")

    print("-" * 40)
    print()


def clear_memory():
    """Delete all stored conversation history."""

    conversation_history.clear()

    print()
    print("Memory cleared successfully.")
    print()


def show_help():
    """Display available commands."""

    print()
    print("=" * 40)
    print("AVAILABLE COMMANDS")
    print("=" * 40)
    print("/help    - Show available commands")
    print("/memory  - Show current memory")
    print("/clear   - Clear conversation memory")
    print("/exit    - Exit the chatbot")
    print("=" * 40)
    print()


# ==============================
# Chatbot Interface
# ==============================

print("=" * 50)
print("        AI CHATBOT WITH MEMORY")
print("=" * 50)
print(f"Model: {MODEL}")
print(f"Memory limit: {MAX_MESSAGES} messages")
print("Type /help for available commands.")
print()


# ==============================
# Main Chat Loop
# ==============================

while True:

    # Get user input
    user_message = input("You: ").strip()

    # Block empty messages
    if not user_message:
        print("Please enter a message.")
        continue

    # ==========================
    # Commands
    # ==========================

    if user_message.lower() == "/help":
        show_help()
        continue

    if user_message.lower() == "/memory":
        show_memory()
        continue

    if user_message.lower() == "/clear":
        clear_memory()
        continue

    if user_message.lower() in {"/exit", "exit", "quit"}:
        print("AI: Goodbye!")
        break

    # ==========================
    # Store User Message
    # ==========================

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Keep memory within the limit
    trim_memory()

    # ==========================
    # Send to Ollama
    # ==========================

    try:

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL,
                "messages": conversation_history,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        # Extract AI response
        assistant_message = response.json()["message"]["content"]

        # ==========================
        # Store AI Response
        # ==========================

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Keep memory within the limit
        trim_memory()

        # ==========================
        # Display Response
        # ==========================

        print(f"AI: {assistant_message}")
        print(
            f"[Memory: "
            f"{len(conversation_history)}/{MAX_MESSAGES} messages]"
        )
        print()

    except requests.exceptions.ConnectionError:

        print()
        print("Error: Ollama is not running.")
        print("Please start Ollama and try again.")
        print()

    except requests.exceptions.Timeout:

        print()
        print("Error: Ollama took too long to respond.")
        print()

    except Exception as e:

        print()
        print(f"Error: {e}")
        print()