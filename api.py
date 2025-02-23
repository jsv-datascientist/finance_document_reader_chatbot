
from dotenv import load_dotenv
import os
import uvicorn
import json 

from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse

from langchain.schema import HumanMessage

from utils.state import State
from graph_builder import build_graph
from pydantic import BaseModel

from nodes.pdf_processing import get_vector_store


app = FastAPI()
load_dotenv()

global_state = State = {
                        "messages": "",  
                        "contents": "",
                        "file_type": "",
                        "dict_return": {},
                        "file_path" : ""
}

class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
async def ask_question(request: QuestionRequest):
    
    print("********************Inside the chat", request)
    question = request.question
    
    #Get the global vector store
    vector_store = get_vector_store()
    
    if vector_store is None:
        raise HTTPException(status_code=400, detail="Vector store not initialized. Please upload a PDF first.")
    
    # Process the question using your vector store
    results = vector_store.similarity_search(question, k=5)  # Adjust as needed
    
    
    # Format the response
    response = {
        "question": question,
        "answers": [result.page_content for result in results]
    }
    print("************** result", response)
    return response

        
@app.post("/finance")
async def  upload_file(file: UploadFile = File(...)):
        
        file_ext = file.filename.split(".")[-1].lower()
        
        # Read file contents as bytes
        contents = await file.read()
        
        file_path = ""
        print("***********file type", file_ext)
        #for processing pdf files 
        if file_ext == "pdf":
            file_path = f"./temp_{file.filename}"
            with open(file_path, "wb") as f:
               f.write(contents)  # Use the already read contents
               print("updated the file")
    
        
        # Create a HumanMessage indicating that the file was uploaded
        human_message = HumanMessage(content=f"User uploaded file: {file.filename}")
        
        global_state["messages"] = [human_message]
        global_state["file_type"] = file_ext
        global_state['contents'] = contents
        global_state['file_path'] = file_path
    
        
        #State(messages = [human_message], contents= contents, file_type=file_ext, dict_return={} )
        #state = update_chat_memory(global_state)
        
        graph = build_graph()
        graph.get_graph().draw_mermaid_png(output_file_path="graph_flow.png")
        result = graph.invoke(global_state)
        
        
        #print(result.get('dict_return'))
        print('From AI Message*********************')
        print(result.get('messages'))
        
        ai_message = result["messages"][-1]
        final_result= ""
        
        if result.get('file_type') == 'txt' or result.get('file_type') == 'docx' or result.get('file_type') == 'pdf':
            # The content is a JSON string. Convert it back to a dictionary.
            final_result = json.loads(ai_message.content)

        # Now you can access the data as a dictionary:
        print(final_result)

        return JSONResponse(content=final_result, status_code=200)

@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


