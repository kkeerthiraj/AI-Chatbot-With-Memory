# 🤖 AI Chatbot with Memory

A local AI chatbot built with **Python, Streamlit, Ollama, and Llama 3.2** that maintains short-term conversational memory during an active session.

The chatbot runs the language model locally through Ollama, allowing conversations without relying on a cloud-based AI API.
## 📸 Demo

### 💬 Chatbot with Memory

![AI Chatbot with Memory - Chat](demo-1.png)

### 🧠 Memory in Action

![AI Chatbot with Memory - Memory](demo-2.png)

The chatbot remembers previous messages during the active Streamlit session and can display the stored conversation using the `/memory` command.
---

## ✨ Features

- 💬 Interactive Streamlit chat interface
- 🧠 Short-term conversation memory
- 🦙 Local Llama 3.2 3B model through Ollama
- 🔒 Local AI inference
- 🗑️ Clear conversation memory
- 📋 View stored conversation memory
- 🔢 Configurable memory limit
- ⚡ Lightweight implementation
- 🐍 Python-based

---

## 🧠 How Memory Works

The chatbot stores the conversation history using Streamlit's session state.

Each conversation contains:

```text
User Message
      ↓
Conversation Memory
      ↓
Ollama / Llama 3.2
      ↓
AI Response
      ↓
Conversation Memory

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Ollama**
- **Llama 3.2 3B**
- **Requests**

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/kkeerthiraj/AI-Chatbot-With-Memory.git
cd AI-Chatbot-With-Memory