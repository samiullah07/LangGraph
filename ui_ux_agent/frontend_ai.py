import streamlit as st
from backend_ai import build_workflow
import uuid

st.sidebar.title("LangGraph AI Chatbot")

def generate_thread_id():
    return str(uuid.uuid4())  # ensure string

# Initialize session state
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

# Sidebar controls
if st.sidebar.button("Start New Conversation"):
    st.session_state["message_history"] = []
    st.session_state["thread_id"] = generate_thread_id()

st.sidebar.header("My Conversations")
st.sidebar.text(st.session_state['thread_id'])

# Display past messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save user msg
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # Generate response
    response = build_workflow(user_input)
    ai_message = response["messages"][-1]  # last assistant msg

    # Stream output
    with st.chat_message("assistant"):
        ai_text = st.write_stream([ai_message.content])  

    # Save assistant msg
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message.content})
