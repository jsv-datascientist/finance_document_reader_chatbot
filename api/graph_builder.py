
from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.memory import MemorySaver

from api.utils.state import State

from api.nodes.docx_processing import docx_processing
from api.nodes.text_processing import text_processing
from api.nodes.chat_history import update_chat_memory
from api.nodes.pdf_processing import pdf_processing
from api.nodes.router import route_based_on_file_type


def build_graph():
    
    graph_builder = StateGraph(State)
    
    graph_builder.add_node("text_processing", text_processing)
    graph_builder.add_node("docx_processing", docx_processing)
    graph_builder.add_node("chat_history", update_chat_memory)
    graph_builder.add_node("pdf_processing", pdf_processing)
    
    # Since the processing to be done by the file type is predefined , 
    # we use each processing fucnction as nodes, we are not including as tools to bind with LLM
    graph_builder.add_conditional_edges(START,
                                        route_based_on_file_type,
                                        {
                                        "text": "text_processing",
                                        "docx": "docx_processing",
                                        "pdf": "pdf_processing"
                                        })
    # After text or docx processing, go to END
    graph_builder.add_edge("text_processing", "chat_history")
    graph_builder.add_edge("docx_processing", "chat_history")
    graph_builder.add_edge("pdf_processing", "chat_history")
    graph_builder.add_edge("chat_history", END)
    
    #Add for persistance if needed
    #memory_saver = MemorySaver()

    return graph_builder.compile()