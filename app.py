import json
import os
import time
import traceback
import requests
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

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

template = PromptTemplate(
    template="""You are the expert of Large Language Models on National Data Platform. 

        Based on the provided context, use easy understanding language to answer the question 
        clear and precise with explanations. The context may contain truncated sentences; do 
        not include any truncated sentences or bullets in the answer. If no 
        information is provided in the context, return the result as "Sorry I dont know the 
        answer", don't provide the wrong answer or a contradictory answer. 

        Context:{context}

        Question:{question}?

        Answer:""",
    input_variables=["question", "context"],
)

rag_chain = template | llm | StrOutputParser()
rag_chain_2 = template | llm2 | StrOutputParser()

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What can I help with?"):

    # Display user's last message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner(
                "We are in the process of retrieving the relevant provisions to give you the best possible answer."):
            response = requests.get(f"https://sparcal.sdsc.edu/api/v1/Utility/llm?search_terms={prompt}")
            models = json.loads(response.text)
            models = models[0:8]

            context = ""
            for model in models:
                model_info = "=======================================\n"
                model_info += f'author: {model["metadata"]["author"]}\n'
                model_info += f'model id: {model["metadata"]["modelId"]}\n'
                model_info += f'created_at: {model["metadata"]["created_at"]}\n'
                model_info += f'downloads: {model["metadata"]["downloads"]}\n'
                model_info += f'partial description: {model["document"]}\n\n'

                if len(context + model_info) > 20000:
                    break
                else:
                    context += model_info

            try:
                result = rag_chain.invoke({"question": prompt, "context": context})
            except Exception as e:
                result = rag_chain_2.invoke({"question": prompt, "context": context})
                
            st.markdown(result)
            st.session_state.chat.append({"role": "assistant", "content": result})

            
