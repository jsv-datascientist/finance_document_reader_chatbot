
import spacy
import json

from utils.state import State

from langchain.schema import AIMessage

def text_processing(state: State) -> State:
    """
    This method is for text processing
    We are using NER via spacy library to extract the entities
    """
    
    
    print("Started procesing the txt file..............")
    file_bytes = state["contents"]
    text = file_bytes.decode("utf-8")
    nlp = spacy.load("en_core_web_sm")
    patterns = [{"label": "NOTION", "pattern":"200 mio"},
                        {"label": "ISIN", "pattern": [{"TEXT": {"REGEX": "^[A-Z]{2}[A-Z0-9]{9}[0-9]$"}}]},
                        {"label": "BID", "pattern": "estr+45bps"},
                        {"label": "PAYMENT_FREQUENCY", "pattern": "Quarterly"},
                        {"label": "MATURITY", "pattern": "2Y EVG"},
                        {"label": "UNDERLYING", "pattern": "AVMAFC FLOAT	06/30/28"},
                        {"label": "ORG", "pattern": "BANK ABC"}
                       ]
    nlp = spacy.blank("en")

    # add entity ruler to the model
    entity_ruler  = nlp.add_pipe("entity_ruler")

    # Give the defined patterns to the enitity rules 
    entity_ruler.add_patterns(patterns)

    doc = nlp(text)

    entities = {}
    # Extract Named Entities
    for ent in doc.ents:
        #print(f"Entity: {ent.text}, Label: {ent.label_}")
        entities[ent.label_] = ent.text
            
    result= {'file_type': "txt", "entities":entities}
        # Convert dictionary to JSON string
    json_result = json.dumps(result, indent=2)
    
    response_message = AIMessage(content=json_result)
    state["messages"].append(response_message)
    
    print("Finished processing the txt file..............")
         
    return state
            
            
    