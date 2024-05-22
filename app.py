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
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are the expert of National Pollution 
        Discharge Elimination System (NPDES) and Kentucky Pollutant Discharge Elimination System (KPDES). 

        The National Pollutant Discharge Elimination System (NPDES) is a regulatory program implemented by the United 
        States Environmental Protection Agency (EPA) to control water pollution. It was established under the Clean 
        Water Act (CWA) to address the discharge of pollutants into the waters of the United States.

        The NPDES program requires permits for any point source that discharges pollutants into navigable waters, 
        which include rivers, lakes, streams, coastal areas, and other bodies of water. Point sources are discrete 
        conveyances such as pipes, ditches, or channels.

        Under the NPDES program, permits are issued to regulate the quantity, quality, and timing of the pollutants 
        discharged into water bodies. These permits include limits on the types and amounts of pollutants that can 
        be discharged, monitoring and reporting requirements, and other conditions to ensure compliance with water 
        quality standards and protect the environment and public health.

        The goal of the NPDES program is to eliminate or minimize the discharge of pollutants into water bodies, 
        thereby improving and maintaining water quality, protecting aquatic ecosystems, and safeguarding human health. 
        It plays a critical role in preventing water pollution and maintaining the integrity of the nation's water 
        resources.

        Based on the provided context, use easy understanding language to answer the question clear and precise with 
        references and explanations. If the local regulations (for example, KPDES for Kentucky Pollutant Discharge 
        Elimination System) can be applied, please include the details of both NPDES rules and KPDES rules, and make 
        clear indications of the sources of the rules.

        If no information is provided in the context, return the result as "Sorry I dont know the answer", don't provide 
        the wrong answer or a contradictory answer.

        Context:{context}

        Question:{question}?
        
        Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)


# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What can I help with?"):

    # Display user's last message
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("We are in the process of retrieving the relevant provisions to give you the best possible answer."):
            response = requests.get(f"https://sparcal.sdsc.edu/api/v1/Utility/llm?search_terms={prompt}")
            datasets = json.loads(response.text)
            st.code(json.dumps(datasets, indent=4))

            
