from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.schema import AIMessage
from langchain.chains import RetrievalQA

import chromadb
from pypdf import PdfReader

from api.utils.state import State

import os
import json



def document_loader(file):
    """
    This method is to load the pdf document
    """
    loader = PyPDFLoader(file)
    loaded_document = loader.load()
    return loaded_document


def text_splitter(data):
    """
    This method splits the data into chunk 
    """
    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,       
                    chunk_overlap=200,     
                    separators=["\n\n", "\n", " ", ""]
                    )
    
    chunks = text_splitter.split_documents(data)
    return chunks

def vector_database(chunks):
    
    embedding_function = OpenAIEmbeddings(model = "text-embedding-3-small")
    
    ids = [str(i) for i in range(0, len(chunks))]
    
    
    vector_store = Chroma.from_documents(
        chunks,
        embedding= embedding_function,
        persist_directory="./chroma_db",
        ids = ids
    )
    return vector_store
    
    

 
def create_vector_store(state: State) -> Chroma:
    
    file_path_dir = state["file_path"]

    splits = document_loader(file_path_dir)
    chunks = text_splitter(splits)
    
    print(f"Total chunks documents : {len(chunks)}")
    print(chunks[0])
    
    vector_store = vector_database(chunks)
     
    """  
    # Process the question using your vector store
    results = vector_store.similarity_search("what is the company name mentioned in this document and their investors name?", k=3)  # Adjust as needed
    
    
    # Format the response
    response = {
        "question": "What is the company name mentioned in this document and their investors name?",
        "answers": [result.page_content for result in results]
    }
    print("response", response)
    """
    
    
    """retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4-turbo"),
        retriever=retriever
    )

    query = "What is the company name mentioned in document?"
    response = qa_chain.run(query)
    print(response)"""
    
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



def get_vector_store( persist_directory="./chroma_db"):
    
    
    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
        # Check if the vector store already exists
    if os.path.exists(persist_directory):
        print("Loading existing vector store from disk...")
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        return vector_store
    else:
        print("Vector Database is not present")
        return "error"
  