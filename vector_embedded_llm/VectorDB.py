import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from chromadb.utils import embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-ada-002"
            )

os.environ["OPENAI_API_KEY"] = "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"
cwd = os.getcwd()
documents = []
for file in os.listdir('data'):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(cwd, "data", file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(
  documents,
  embedding=openai_ef,
  persist_directory='./embeddings'
)
vectordb.persist()

# qa_chain = ConversationalRetrievalChain.from_llm(
#     ChatOpenAI(),
#     vectordb.as_retriever(search_kwargs={'k': 6}),
#     return_source_documents=True
# )


##User Interface
st.title("IOEA's Sickle Cell Disease Nutrtition Consultant")

if "messages" not in st.session_state:
    st.chat_history = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
            stream = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(),
                vectordb.as_retriever(search_kwargs={'k': 20}),
                return_source_documents=True,
                #model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})


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




