import json
import requests
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def get_context(datasets):
    context = ""
    for dataset in datasets:    
        title, description = dataset['description'].split("|", 1)
        context += f"""
                      Dataset Id: {dataset['dataset_id']}   
                      Title: {title}            
                      Description: {description} 
                    """
        if len(context) > 20000:
            break
    return context
    

def search_ndp_catalog(llm, user_input):
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 
          The user is looking for datasets with the following question 
          
          Question: 
          {question}
                 
          The following are the ids and descriptions of some datasets potentially relevant 
          to the user's question:
          
          Context:
          {context}
            
          Decide which datasets in the context satisfy the user's request. Provide your answer 
          as a valid JSON list. All the datasets in the context must be included in this JSON 
          list with the following fields:
          
           a string "dataset_id" field for the dataset id,  
           a string field "title" for the data title,
           a string field "summary" for summarizing the description with maximum 100 words and without any markdown symbols, 
           a boolean field "is_relevant" for indicating if it is strongly relevant to the search terms
           a string field "reason" to explain why these datasets are definitely relevant or irrelevant to the request.
            
           Please note that the user's request may contain the state abbreviation which can be used to exclude 
           datasets. For example, TX usually indicates Texas.
            
           Images and Lidar and DEM data are raster data and not vector data.
            
           If the user requests data for a special region, make sure the region condition is satisfied.
           If the user requests data for a special type, make sure the type condition is satisfied.
           If the description contains latitude and longitude, please use them to exclude datasets.
        
           Please note that fire simulation is not earthquake simulation.
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "context"],
    )
    question_planer = prompt | llm | JsonOutputParser()
    
    response = requests.get(f"https://sparcal.sdsc.edu/staging-api/v1/Utility/ndp?search_terms={user_input}")
    datasets = json.loads(response.text)

    result1 = question_planer.invoke({"question": user_input, "context": get_context(datasets[:5])})
    result2 = question_planer.invoke({"question": user_input, "context": get_context(datasets[5:])})
    
    # context = ""
    # for dataset in datasets:    
    #     title, description = dataset['description'].split("|", 1)
    #     context += f"""
    #                   Dataset Id: {dataset['dataset_id']}   
    #                   Title: {title}            
    #                   Description: {description} 
    #                 """
    #     if len(context) > 20000:
    #         break
    
    # result = question_planer.invoke({"question": user_input, "context": context})
    return result1 + result2
