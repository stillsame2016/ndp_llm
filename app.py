import json
import os
import time
import traceback
import requests
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

Groq_KEY = "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"
Groq_KEY_2 = "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"

llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY)
llm2 = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=Groq_KEY_2)


# Add a Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display Form Title
st.title("Chat with NDP LLM")

# Display chat messages from history above current input box
for message in st.session_state.chat:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
st.write("")

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
                context += "=======================================\n"
                context += f'author: {model["metadata"]["author"]}\n'
                context += f'model id: {model["metadata"]["modelId"]}\n'
                context += f'created_at: {model["metadata"]["created_at"]}\n'
                context += f'downloads: {model["metadata"]["downloads"]}\n'
                context += f'partial description: {model["document"]}\n\n'

            result = rag_chain.invoke({"question": prompt, "context": context})
            st.markdown(result)
            st.session_state.chat.append({"role": "assistant", "content": result})

            
