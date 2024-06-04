from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def process_off_topic_request(llm, user_input):
    template = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert of the 
            NDP Data Catalog and The NPD large lanugae model information system. 

            The NPD large lanugae model information system contains the detail information about large 
            language models hosted in HuggingFace. Users can ask any questions for those large langugae
            models. For example, 
                What large language models can be used for generating Python code? 
                Can you provide detailed information about PyCodeGPT?
                List large language models that support multi-language embedding.
                Can you recommend a couple of great language models for use on cell phones?
                What large language models can be used for biology?
                How is the Phi-3 model?
                Are Llava models mainly used for computer vision?

            The NDP Data Catalog is a collection of datasets related to geology, ecology, environmental 
            science and other disciplines. A user can use natural language to describe the conditions for searching
            datasets in the NDP Data Catalog. 

            Based on the provided context, use easy understanding language to answer the question.
            
            Question:{question}?

            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question"],
    )
    rag_chain = template | llm | StrOutputParser()
    return rag_chain.invoke({"question": input})
