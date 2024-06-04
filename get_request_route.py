from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


#####################################################################
# Implement the Router
def get_request_route(llm, question):
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert 
        at routing a user question to NDP Data Catalog or NPD large lanugae model information system. 

        Use NPD large lanugae model information system for all large language model related questions. 
        For example, 
            What large language models can be used for generating Python code? 
            Can you provide detailed information about PyCodeGPT?
            List large language models that support multi-language embedding.
            Can you recommend a couple of great language models for use on cell phones?
            What large language models can be used for biology?
            How is the Phi-3 model?
            Are Llava models mainly used for computer vision?

        The NDP Data Catalog is a collection of many datasets related to geology, ecology, environmental 
        science and other disciplines.The NDP Data Catalog supports searches for users describing their 
        needs in natural language.

        In particular, the NDP Data Catalog is used to find datasets such as Lidar datasets, GPS datasets, 
        and so on, that meet the appropriate criteria. The NDP catalog is not intended to be used to answer 
        specific questions, e.g., What is the size of the state of Utah and is La Jolla a county? These 
        questions are not lookup datasets and therefore must be categorized as “Other”.
        
        Using your knowledge to classify the user's question into the categogy 'NPD LLM information system' 
        or 'NDP Data Catalog' or 'Other' and return a JSON with a single key 'request_type' and a key 
        'explanation' for reasons. 
        
        Question to route: {question} 
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question"],
    )
    question_router = prompt | llm | JsonOutputParser()
    result = question_router.invoke({"question": question})
    return result
