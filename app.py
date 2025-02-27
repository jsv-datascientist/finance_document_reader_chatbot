

import streamlit as st 
import requests
import json

from streamlit_chat import message

def load_file():
    """
    We are creating a chat interface to upload the files 
    and process it in fastapi
    
    """
    st.title("🤖 CMI . ADOR")

    API_URL = "http://127.0.0.1:8000/finance/" 
    
    CHAT_URL = "http://127.0.0.1:8000/chat/" 


    # Initialize session state for messages and results if not already present
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'results' not in st.session_state:
        st.session_state.results = {}
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    input_file = st.file_uploader("Upload the file",type=["pdf", "docx", "txt"])

    if input_file is not None:
        st.session_state.messages.append({"content": f"Uploaded {input_file.name}", "is_user": True})

        if input_file:
            with st.spinner("Processing..."):
                files = {"file": (input_file.name, input_file.getvalue(), input_file.type)}
                
                # Make the FastAPI call here 
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.results[input_file.name] = result
                    #st.rerun()
                else:
                    st.error("Error processing file!")
                    
        
    
    # Display previous results
    if st.session_state.results:
        for file_name, result in st.session_state.results.items():
            entities = result["entities"]      
                   
            if result['file_type'] == "docx":
                    st.write(f"""
                            ### Extracted Data from {file_name}: \n
                            **CounterParty:** {entities["counterparty"]} \n
                            **Initial Valuation Date:** {entities["ivd"]} \n
                            **Notional:** {entities["notional"]} \n
                            **Valuation Date:** {entities["val_date"]} \n
                            **Maturity:** {entities["maturity"]} \n
                            **Underlying:** {entities["underlying"]} \n
                            **Coupon:** {entities["coupon"]} \n
                            **Barrier:** {entities["barrier"]} \n
                            **Calendar:** {entities["calender"]} \n
                    """)
            elif result['file_type'] == "txt":
                    st.write(f"""
                            ### Extracted Data from {file_name}: \n
                            **CounterParty:** {entities["ORG"]} \n
                            **Notional:** {entities["NOTION"]} \n
                            **ISIN:** {entities["ISIN"]} \n
                            **Underlying:** {entities["UNDERLYING"]} \n
                            **Maturity:** {entities["MATURITY"]} \n
                            **Bid:** {entities["BID"]} \n
                            **Offer:** \n
                            **Payment Frequency:** {entities["PAYMENT_FREQUENCY"]} \n
                    """)
            elif result['file_type'] == "pdf":
                    st.write(f"""
                            {entities} \n
                            """)
                    question =st.text_input("Enter your question?", key="user_input")
                        
                    if question:
                        print("Inside the question", question)
                        
                        # Prepare the request payload
                        payload = {"question": question}
                        
                        try:
                            # Send a POST request to the FastAPI endpoint
                            response = requests.post(CHAT_URL, json=payload)
                            response.raise_for_status()  # Raise an error for bad status codes
                            
                            # Parse the response
                            result = response.json()
                            
                            # Add the user's question and system's response to the chat history
                            st.session_state.chat_history.append({"role": "user", "message": question})
                            if result["answers"]:
                                st.session_state.chat_history.append({"role": "system", "message": result["answers"]})
                        
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error calling FastAPI: {e}")
                            
                        # Display the chat history
                        st.write("### Chat History")
                        for chat in st.session_state.chat_history:
                            if chat["role"] == "user":
                                st.write(f"**You:** {chat['message']}")
                            else:
                                st.write(f"**System:** {chat['message']}")
    


if __name__== "__main__":
   # load_dotenv()
    load_file()