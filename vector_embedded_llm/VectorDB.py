import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import time



os.environ["OPENAI_API_KEY"] = 'sk-proj-gCwuOaWkryuDdcYVXB04T3BlbkFJ7ovBsijtVyJUaVfUG3CK'
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
cwd = os.getcwd()
documents = []
for file in os.listdir('data'):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(cwd, "data", file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
vectorstore = Chroma.from_documents(chunked_documents, embedding_function)




general_system_template = r""" 
DO NOT USE DATA OUTSIDE OF THE DOCUMENT INFORMATION MADE AVAILABLE TO YOU.


You are a sickle cell nutrtition assistant that analyzes documents about foods, the amount of nutrients in them, their compounds and health effects.
Your first goal is to determine, via calculations, if eating a meal, will make a user exceed their recommended daily intake for sickle cell disease.

You can achieve this goal by working with the quantity of food (in grams) stated by the user.
Your second goal is to discuss compounds and their health effects found in a user's food.

Using information available to you, attempt to reason through the question as a given problem.
DO NOT USE DATA OUTSIDE OF THE DOCUMENT INFORMATION MADE AVAILABLE TO YOU.
It will require you combining various information from the given sources to arrive at a reasonable answer.
Using the data available to you, analyze information regarding food nutrients quantities, food compounds, and recommended daily intakes for sickle cell disease.
Use your findings and reasoning to attempt necessary calculations.


 ----
{context}
----
"""
general_user_template = "Question:```{question}```"
messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
]
qa_prompt = ChatPromptTemplate.from_messages(messages)


##User Interface
st.image('logo.png')
st.title("Helena Cares: SCD Nutrtition Consultant")
chat_history = []

if "messages" not in st.session_state:
     st.session_state.messages = [] 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
         st.markdown(message["content"])

if prompt := st.chat_input("Ask Me Questions"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
            
            qa = RetrievalQA.from_chain_type(
            llm= ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            chain_type="stuff",
            retriever = vectorstore.as_retriever(search_kwargs={'k': 10}),
            chain_type_kwargs={"prompt": qa_prompt},
            )   
            c_start_time = time.time()
            response = qa({"query": prompt})
            print("--- %s seconds ---" % (time.time() - c_start_time))
            result = response['result'].replace("\\n", '\n')
            print(result)
            st.write(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
 



st.markdown(
    f"""
    <style>
        img {{
            border-radius: 90%;
            overflow: hidden;
            width: 200px;
            height: 200px;
            object-fit: contain;
            text-align: center;
           
        }}

    </style>
    """,
    unsafe_allow_html=True
)



