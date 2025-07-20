import streamlit as st
import requests
from backend import Allowed_models

api = "http://127.0.0.1:8000/chat"


st.set_page_config(page_title="LangGraph AGENT UI", page_icon=":robot_face:")
st.title("AI Chat Agent")
st.write("This is a simple chat interface for interacting with an AI agent using LangGraph.")
system_prompt = st.text_area("Define your AI Agent", height=100, placeholder="Enter your AI agent's system prompt here...")

llm_provider = st.radio("Select LLM Provider", ["GROQ", "OPENAI"])
if llm_provider == "GROQ":
    llm_id = st.selectbox("Select LLM Model", ["llama-3.1-8b-instant", "llama-3.1-70b-instant"])
elif llm_provider == "OPENAI":
    llm_id = st.selectbox("Select LLM Model", ["gpt3.5-turbo", "gpt-4o", "gpt-4o-mini"])
search_result = st.checkbox("Enable Search Results", value=True)
query = st.text_area("Enter your query", height=100, placeholder="Type your question or command here...")

if st.button("Generate Response"):
    if query.strip():
    
        payload = {
            "llm_id": llm_id,
            "llm_provider": llm_provider,
            "search_result": search_result,
            "system_prompt": system_prompt,
            "messages": [query]
        }
        response = requests.post(api, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            st.success("Response from AI Agent:")
            st.write(data.get("response", "No response received."))
        else:
            st.error(f"Error: {response.status_code} - {response.text}")




    