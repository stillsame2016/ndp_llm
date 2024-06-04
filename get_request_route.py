from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


#####################################################################
# Implement the Router
def get_request_route(llm, question):
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert at 
        routing user questions to the appropriate system: the NPD Data Catalog or the NPD Large Language 
        Model (LLM) Information System.

        Use the NPD LLM Information System for all questions related to large language models. Examples 
        include:
            What large language models can be used for generating Python code?
            Can you provide detailed information about PyCodeGPT?
            List large language models that support multi-language embedding.
            Can you recommend a couple of great language models for use on cell phones?
            What large language models can be used for biology?
            How is the Phi-3 model?
            Are Llava models mainly used for computer vision?
            
        The NDP Data Catalog is a collection of datasets related to geology, ecology, environmental 
        science, and other disciplines. A user can describe conditions for searching datasets in the 
        NDP Data Catalog using natural language.
        
        The NDP Data Catalog is used to find datasets such as LiDAR datasets, GPS datasets, and more, 
        that meet specific criteria. It is not intended for answering specific factual questions or 
        general inquiries about concepts or potential connections (e.g., "What is the size of the 
        state of Utah?", "Is La Jolla a county?", or "Do you think there might be a connection 
        between earthquakes and vegetation?"). These questions, along with requests for tools 
        (which are not datasets), should be categorized as "Other."
        
        Classify the user's question into one of the following categories: 'NPD LLM Information System', 
        'NDP Data Catalog', or 'Other'. Return a JSON object with a single key 'request_type' and a key 
        'explanation' for the reasons behind your classification.
        
        Question to route: {question}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question"],
    )
    question_router = prompt | llm | JsonOutputParser()
    result = question_router.invoke({"question": question})
    return result
