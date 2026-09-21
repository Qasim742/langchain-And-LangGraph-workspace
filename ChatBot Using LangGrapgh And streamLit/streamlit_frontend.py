import streamlit as st
from chatBot_backend import chatbot
from langchain_core.messages import HumanMessage


# Configure thread ID for the session 
CONFIG = {"configurable": {"thread_id": "1"}} 

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # Get the assistant's response
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]} , config=CONFIG)
    ai_response = response["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": ai_response })
    with st.chat_message("assistant"):
        st.text(ai_response)  # Placeholder for the assistant's response
