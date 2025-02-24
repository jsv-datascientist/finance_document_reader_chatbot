from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import AIMessage


from utils.state import State

import os
import json

global vector_store
 
def create_vector_store(state: State) -> Chroma:
    global vector_store
    
    file_path_dir = state["file_path"]

    loader = PyPDFLoader(file_path=file_path_dir)
    
    data = loader.load()
    #print("printing the data ************")
    #print(data[0])
    
    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,       
                    chunk_overlap=200,     
                    separators=["\n\n", "\n", " ", ""]
                    )
    
    docs = text_splitter.split_documents(data)
    
    embedding_function = OpenAIEmbeddings(model = "text-embedding-3-small")
    vector_store = Chroma.from_documents(
        docs,
        embedding= embedding_function,
        persist_directory=os.getcwd()
        
    )
    #vector_store.persist()
    
    return vector_store


def pdf_processing(state: State) -> State:
    """
    This method is for processing the pdf file. 
    We store it in vector store for later querying
    """
    
    create_vector_store(state)
    result= {'file_type': "pdf", "entities":"Document uploaded successfully in vectorstore. You can now ask questions."}
    json_result = json.dumps(result, indent=2)
    
    response_message = AIMessage(content=json_result)
    state["messages"].append(response_message)
         
    return state

# Function to get the global vector store
def get_vector_store():
    global vector_store
    return vector_store