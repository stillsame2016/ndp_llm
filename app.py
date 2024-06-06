import json
import os
import time
import requests
import traceback
import streamlit as st

from langchain_groq import ChatGroq
from get_llm_from_rag import get_llm_from_rag
from get_request_route import get_request_route
from process_off_topic import process_off_topic_request
from search_ndp_catalog import search_ndp_catalog
from utils import justification_markdown


Groq_KEY = st.secrets["Groq_KEY"]
Groq_KEY_2 = st.secrets["Groq_KEY_2"]

llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY)
llm2 = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY_2)

# Add a Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = []

st.set_page_config(page_title="LLM Finder: Chat with NDP")

# Display Form Title
st.markdown("### Chat with NDP")
st.markdown("""Pose a question related to free large language models hosted on Hugging 
               Face. Search the NDP data catalog to find the desired datasets.""")

# Display chat messages from history above current input box
for message in st.session_state.chat:
    with st.chat_message(message['role']):
        if isinstance(message['content'], str):
            st.markdown(message['content'])
        else:
            justification_markdown(message['content'])
st.write("")

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What can I help with?"):

    # Display user's last message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner(""):
            route = get_request_route(llm, llm2, prompt)
            # st.code(route)
        if route['request_type'] == 'NPD LLM information system':
            with st.spinner("""
                            We are in the process of retrieving the relevant provisions 
                            from our LLM Information System to give you the best possible answer.
                            """):
                result = get_llm_from_rag(llm, llm2, prompt)
                st.markdown(result)
        elif route['request_type'] == 'NDP Data Catalog':
            with st.spinner("""
                            We are searching the NDP catalog to give you the best possible answer.
                            """):
                result = search_ndp_catalog(llm, llm2, prompt)
                justification_markdown(result)
        else:
            with st.spinner(""):
                result = process_off_topic_request(llm, llm2, prompt)
                st.markdown(result)
               
        st.session_state.chat.append({"role": "assistant", "content": result})
