
import json
import requests
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


#####################################################################
# Implement the Router
def get_llm_from_rag(llm, llm2, question):
    template = PromptTemplate(
        template="""You are the expert of Large Language Models on National Data Platform. 
    
            Based on the provided context, use easy understanding language to answer the question 
            clear and precise with explanations. The context may contain truncated sentences; do 
            not include any truncated sentences or bullets in the answer. If no information is 
            provided in the context, return the result as "Sorry I dont know the answer", and ask 
            the user to refine the request and try again.
    
            Context:{context}
    
            Question:{question}?
    
            Answer:""",
        input_variables=["question", "context"],
    )
    rag_chain = template | llm | StrOutputParser()
    rag_chain2 = template | llm2 | StrOutputParser()
    
    response = requests.get(f"https://sparcal.sdsc.edu/api/v1/Utility/llm?search_terms={question}")
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
        return rag_chain.invoke({"question": question, "context": context})
    except:
        return rag_chain2.invoke({"question": question, "context": context})

