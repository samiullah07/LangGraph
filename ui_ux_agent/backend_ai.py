from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
import uuid
import streamlit as st
load_dotenv()

# Use Groq LLaMA-3 model
chat_groq = ChatGroq(model="llama3-8b-8192")

class Base_Chat(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def generate_answers(state: Base_Chat):
    messages = state["messages"]
    query = chat_groq.invoke(messages)
    return {"messages": [query]}

# Build the workflow
checkpointers = InMemorySaver()

def build_workflow(user_query):
    state = StateGraph(Base_Chat)
    state.add_node("generate_answers", generate_answers)
    state.add_edge(START, "generate_answers")
    state.add_edge("generate_answers", END)

    workflow = state.compile(checkpointer=checkpointers)

    # Run conversation
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    # Instead of stream_mode="messages", use default streaming
    response = workflow.invoke({
        "messages": [HumanMessage(content=user_query)]
    }, config=config)

    return response