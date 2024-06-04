from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def search_ndp_catalog(llm, user_input):
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 
              You are an expert of the national data platform catalog for various datasets. You also have general knowledge.
              The following is a question the user is asking:
               
               Question:
               {question}
        
               Your main job is to determine if the user is looking for data. 
               If they are looking for data, extract the search terms from the user's request.
        
               Please answer with a valid JSON string, including the following three fields:
               The boolean field "is_search_data" indicates whether the user is looking for data or not.
               The string list field "search_terms" lists the keywords for which the user is looking for data.
               The string field "alternative_answer" gives your positive answer to the user's input
               if the user is not looking for data.
                
               Please never say "I cannot" or "I could not". 
                 
               Please note that the user's request for datasets may appear in the middle of the text, 
               do your best to extract the keywords for which the user is searching for datasets.
                 
               Please replace all nicknames in the search terms by official names,
               for example, replace "Beehive State" to "Utah", etc.  
                 
               Never deny a user's request to find data. If it is not possible to extract search terms 
               from the user's request, ask the user for further clarification.

                <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question"],
    )
    question_planer = prompt | llm | JsonOutputParser()
    result = question_planer.invoke({"question": question})
    return result
