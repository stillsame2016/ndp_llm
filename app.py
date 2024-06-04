import json
import os
import time
import traceback
import requests
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from get_llm_from_rag import get_llm_from_rag

Groq_KEY = st.secrets["Groq_KEY"]
Groq_KEY_2 = st.secrets["Groq_KEY_2"]

llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY)
llm2 = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY_2)

# Add a Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = []

st.set_page_config(page_title="LLM Finder: Chat with NDP")

# Display Form Title
st.markdown("### LLM Finder: Chat with NDP")

# Display chat messages from history above current input box
for message in st.session_state.chat:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
st.write("")

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What can I help with?"):

    # Display user's last message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("""
                        We are in the process of retrieving the relevant provisions 
                        to give you the best possible answer.
                        """):
            try:
                result = get_llm_from_rag(llm, prompt)
            except Exception as e:
                result = get_llm_from_rag(llm2, prompt)
            st.markdown(result)
            st.session_state.chat.append({"role": "assistant", "content": result})

            
