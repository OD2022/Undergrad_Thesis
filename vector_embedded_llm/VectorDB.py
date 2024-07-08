import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] 
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
You are a sickle cell nutrtition assistant that analyzes documents about foods, the amount of nutrients in them, their compounds and health effects.
Your first goal is to determine, via calculations, if eating a meal, will make a user exceed their recommended daily intake for sickle cell disease.

You can achieve this goal by working with the quantity of food (in grams) stated by the user.
Your second goal is to also discuss compounds and their health effects found in a user's food.

Using information available to you, attempt to reason through the question as a given problem.
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
            retriever = vectorstore.as_retriever(search_kwargs={'k': 15}),
            chain_type_kwargs={"prompt": qa_prompt},
            )   
            result = qa({"query": prompt})
            print(result)
            st.write_stream(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
 

# chat_history = []
# while True:
#     question = input('Prompt: ')
#     final_query = 'You are a nutrition assistant for sickle cell disease, you are to search for information pertaining to the Recommended Daily intake of certain nutrients based on age and gender. You are to also search for information about the nutritional content of mentioned foods to perform your calculation. Do not rely on your knowledge. ' + question
#     if question == "exit" or question == "quit" or question == "q":
#         print('Exiting')
#         sys.exit()
#     result = qa_chain({'question': final_query, 'chat_history': chat_history})
#     print('Answer: ' + result['answer'])
#     chat_history.append((question, result['answer']))

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



