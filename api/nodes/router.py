from api.utils.state import State

def route_based_on_file_type(state: State):
    
    #get the file type
    file_type = state['file_type']
    
    print(f"Routing the file type {file_type}")
    
    if file_type == "txt":
        return "text"
    elif file_type == "docx":
        return "docx"
    else:
        return "pdf"
    