# **Finance Document Reader Chatbot CMI ADOR** 

## **Objective**
The objective is to build a financial document reader tool
augmented by IA. The final product should be able to
classify or summarize documents, discover predefined topics, recognize named
entities or answer questions related to the provided document.

The Proof of Concept (PoC) should demonstrate how the tool can parse and extract financial entities from documents.
Depending on the nature of the provided document you can use a rule-based parser, a
NER model or a Large Language Model (LLM)

#### Architecture WI
The first expected work item is a Global Architecture Document (GAD) that describes the interactions
between the CMI Information System (IS) components and the document reader. The reader can be invoked
programatically via APIs, and will also provide a User Interface (UI) enabling end users to upload a document and launch a
classification, summarization, topic modelling, NER or Q&A feature. Documents will vary in size, format and level of
confidentiality. They can be sent through different communication channels and processed in a synchronous or
asynchronous way.

#### Handling Docx file
 Some kind of documents (e.g. docx files) can be processed by a rule-based parser coded in Python. For this
work item, the expected artifact is a program that takes a document as input and returns a set of named entity values. The
entities to extract are listed in the next slide. You can choose which Python packages to use and the format of the output
files.


#### Handling .txt file
Other kind of documents (e.g.chats) can be processed by a NER model. This work item is a combination of
Python code and a Global Methodology Document (GMD). The Python code will give an overview of how to download and
run a general-purpose NER model to extract named entities. You can choose which model to use. The methodology
document will explain how this model can be fine-tuned to extract the financial entities listed in the next slide.


#### Handling PDF file 
The last type of documents (e.g. pdf files) are more verbose, unstructured and require a more
advanced language model. For this work item a GMD will explain how to build an entity extraction pipeline that relies on
LLMs. The document will also include a description of the prompting and/or Retrieval-Augmented Generation (RAG)
techniques to be used.

# **Solution Proposed**

## **Tools & Technologies**

- **Streamlit** - For frontend 
- **Fastapi** - For backend
- **Langgraph & LangChain** : Here the using the langchain **agent** to decide what action to be taken based on the input file format.
- **LLM** - OpenAI to process the PDF 
- **VectorStore** - Chroma present in Langchain

We choose to go with the Agent Exector architecture for our use case

<img src="images/image.png" alt="LangGraph Flow" width="400" height="400" />



If the format is docx, we use regex expressions to extract the data required.

If the format is txt, we use NER via Spacy library to extract the required field. 
Here we have tries using the EntityRuler to extract the information. 

Same could be achieved via Matcher or ParseMatcher or via a customize training of the NLP model. 

For the pdf, we store the pdf in chroma vector store. And Q&A could be performed on it.
Since its POC and limitations are there to use OpenSource, accuracy would be less. 
Replaced with Pinecone or other in PROD would give better results. 

We can also ask the questions based on the documents uploaded. 
We use basic RAG methodology here. 

Below is the LangGraph generated 

<img src="images/langGraph-flow.png" alt="LangGraph Flow" width="400" height="400" />
 

Few example of data 

- **For .txt file**

<img src="images/txt-image.png" alt="Text file chatbot processing" width="400" height="400" />


- **For .docx file**

<img src="images/docx-image.png" alt="Docx file chatbot processing" width="400" height="400" />

- **For pdf file**

<img src="images/pdf-image.png" alt="Pdf file chatbot processing" width="400" height="400" />


# Run the App 

## **1. Install the dependencies**

- Create a conda or python environment and install all the depencies in requirements.txt

```
conda create -n myenv python=3.9
conda activate myenv
```
- Install conda compatible packages 

```
conda install spacy pydantic requests python-dotenv python-docx pypdf regex
```
- Install remaining via pip 

```
pip install streamlit langchain langchain-chroma langchain-community langchain-core langchain-openai langgraph openai
```

## **2 To Run the Fast api , run the below command**

```
python api.py
```

Api should run in  http://127.0.0.1:8000 ( in my case)

<img src="images/fastapi-log.png" alt="Fast API log" />


## **3 To Run the Streamlit app , run the below command**

```
streamlit run app.py

```

App should be available in http://localhost:8501 (in my case )

<img src="images/streamlit-log.png" alt="Streamlit log" />
