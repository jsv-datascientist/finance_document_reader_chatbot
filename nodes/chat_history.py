from utils.state import State 

def update_chat_memory(state: State) -> State:
    
    # Ensure memory is initialized
    if "memory" not in state:
        state["memory"] = {"chat_history": []}
        
    # Retrieve current chat history or start fresh
    chat_history = state.get("memory", {}).get("chat_history", [])
    
    # Append the content of all messages in the current state (both HumanMessage and AIMessage)
    for msg in state["messages"]:
        if hasattr(msg, "content"):
            chat_history.append(msg.content)
        else:
            chat_history.append(str(msg))
    
    # Update the memory with the new chat history
    state["memory"]["chat_history"] = chat_history
    return state
    