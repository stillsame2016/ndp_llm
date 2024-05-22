import json
import os
import time
import traceback
import requests
import streamlit as st

import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role


# Add a Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display Form Title
st.title("Chat with NDP LLM")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    pass  
   
template = PromptTemplate(
    template="""You are the expert of Large Language Models on National Data Platform. 

        Based on the provided context, use easy understanding language to answer the question clear and precise with 
        explanations. If no information is provided in the context, return the result as "Sorry I dont know the answer", 
        don't provide the wrong answer or a contradictory answer.

        Context:{context}

        Question:{question}?
        
        Answer:""",
    input_variables=["question", "context"],
)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What can I help with?"):

    # Display user's last message
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("We are in the process of retrieving the relevant provisions to give you the best possible answer."):
            response = requests.get(f"https://sparcal.sdsc.edu/api/v1/Utility/llm?search_terms={prompt}")
            models = json.loads(response.text)
            st.code(json.dumps(models, indent=4))

            context = ""
            for model in models:
                context += "\n\n"
                context += f'author: {model["metadata"]["author"]}'
                context += f'model id: {model["metadata"]["modelId"]}'
                context += f'created_at: {model["metadata"]["created_at"]}'
                context += f'downloads: {model["metadata"]["downloads"]}'
                context += f'partial description: {model["document"]}'
                
            st.code(context)    
                
            
            query = f"""
                You are the expert of Large Language Models on National Data Platform. Based on the provided context, use easy 
                understanding language to answer the question clear and precise with explanations. If no information is provided 
                in the context, return the result as "Sorry I dont know the answer", don't provide the wrong answer or a 
                contradictory answer.

                Context:{context}

                Question:{prompt}?
        
                Answer:""",
            
            response = st.session_state.chat.send_message(query, safety_settings=safe)
            st.markdown(response.text)
            
