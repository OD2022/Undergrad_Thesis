import os
import sys
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-"


cwd = os.getcwd()
documents = []
for file in os.listdir('vector_embedded_llm/data'):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(cwd, "vector_embedded_llm", "data", file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(
  documents,
  embedding=OpenAIEmbeddings(),
  persist_directory='./embeddings'
)
vectordb.persist()

qa_chain = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(),
    vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True
)

chat_history = []
while True:
    question = input('Prompt: ')
    final_query = 'You are a nutrition assistant for sickle cell disease, you are to search for information pertaining to the Recommended Daily intake of certain nutrients based on age and gender. You are to also search for information about the nutritional content of mentioned foods to perform your calculation. Do not rely on your knowledge. ' + question
    if question == "exit" or question == "quit" or question == "q":
        print('Exiting')
        sys.exit()
    result = qa_chain({'question': final_query, 'chat_history': chat_history})
    print('Answer: ' + result['answer'])
    chat_history.append((question, result['answer']))
