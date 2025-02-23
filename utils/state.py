from typing import Annotated, List 
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[List, add_messages]
    contents: bytes
    file_type: str
    dict_return: dict
    file_path: str
    memory: dict # to store the chat history