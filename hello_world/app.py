from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
from llama_index import StorageContext, load_index_from_storage
from llama_index import VectorStoreIndex
from langchain.chat_models import ChatOpenAI
import json

# Here we are not creating storage folder so after updating the data folder
# we need to create the storage folder by runnign the code in "if __name__ == '__main__'.....:" below

# You can get post api call in event's body and you can use lambda function wihout python flask app to receive api call

def lambda_handler(event, context):
    question=json.loads(event['body'])['question']

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # Set up LLMPredictor with OpenAI model
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=200))
    
    # Set up ServiceContext
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    index = load_index_from_storage(storage_context = storage_context, service_context = service_context)
    
    # Perform the query and get the response
    query_engine = index.as_query_engine()
    response = query_engine.query(question)

    response = json.dumps(response.response)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST'
    }
    response = {
        'statusCode': 200,
        'headers': headers,
        'body': response,
    }
    return response



# You can also use python flask to handle POST Api requests

# from flask_lambda import FlaskLambda
# from flask import Flask, request, jsonify
# from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
# from langchain import OpenAI
# from llama_index import StorageContext, load_index_from_storage
# from llama_index import VectorStoreIndex
# from langchain.chat_models import ChatOpenAI
# import json

# @app.route('/hello', methods=['POST'])
# def index():
#     question="what is simpl"
#     if request.method == 'POST':
#         question = request.json.get('question')

#     # rebuild storage context
#     storage_context = StorageContext.from_defaults(persist_dir="./storage"

#     # Set up LLMPredictor with OpenAI model
#     llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=512))

#     # Set up ServiceContext
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

#     # Create indexing
#     index = load_index_from_storage(storage_context = storage_context, service_context = service_context)

#     # Perform the query and get the response
#     query_engine = index.as_query_engine()
#     response = query_engine.query(question

#     return(
#         json.dumps(response.response),
#         200,
#         {'Content-Type': "application/json"} 
#     )

#     # This code should run only once and will create a storage folder

# if __name__ == '__main__':
#     # Set maximum input size, num_outputs, max_chunk_overlap, and chunk_size_limit here
#     max_input_size = 4096
#     num_outputs = 2000
#     max_chunk_overlap = 0.8
#     chunk_size_limit = 200

#     prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    
#     # Load the data and construct the index
#     documents = SimpleDirectoryReader('./data').load_data()

#     # index = VectorStoreIndex.from_documents(documents)
#     index = VectorStoreIndex.from_documents(documents = documents, prompt_helper = prompt_helper)
#     index.storage_context.persist()

#     # app.static_folder = 'static'
#     app.run(debug=True)
