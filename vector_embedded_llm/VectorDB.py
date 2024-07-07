import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
from chromadb.utils import embedding_functions
from langchain.prompts import PromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate



#os.environ["OPENAI_API_KEY"] = "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"
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
cwd = os.getcwd()
documents = []
for file in os.listdir('data'):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(cwd, "data", file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
# chunked_documents = text_splitter.split_documents(documents)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
vectorstore = Chroma.from_documents(chunked_documents, embedding_function)

# vectordb = Chroma.from_documents(
#   documents,
#   embedding=embedding_function,
#   persist_directory='./embeddings'
# )
# vectordb.persist()


general_system_template = r""" 
Given a specific context, please give a short answer to the question, 

covering the required advices in general and then provide the names 
all of relevant(even if it relates a bit) products. 
 ----
{context}
----
"""
general_user_template = "Question:```{question}```"
messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
]
qa_prompt = ChatPromptTemplate.from_messages( messages )


##User Interface
st.title("Helena's Sickle Cell Disease Nutrtition Consultant")

if "messages" not in st.session_state:
     st.session_state.messages = [] 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Me Questions"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
            stream = ConversationalRetrievalChain.from_llm(
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
                retriever = vectorstore.as_retriever(search_kwargs={'k': 20}),
                chain_type="stuff",
                combine_docs_chain_kwargs={'prompt': qa_prompt}
            )
            result = stream({"question": prompt})
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




