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
            route = get_request_route(llm, prompt)
            st.code(route)     
            if route['request_type'] == 'NPD LLM information system':
                result = get_llm_from_rag(llm, prompt)
            elif route['request_type'] == 'NDP Data Catalog':
                response = requests.get(f"https://sparcal.sdsc.edu/staging-api/v1/Utility/ndp?search_terms={prompt}")
                datasets = json.loads(response.text)
                result = json.dumps(datasets, indent=4)
                # result = search_ndp_catalog(llm, prompt, context)
            else:
                result = process_off_topic_request(llm, prompt)
                
            st.markdown(result)
            st.session_state.chat.append({"role": "assistant", "content": result})

            
