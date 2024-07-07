from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings)
from langchain_text_splitters import CharacterTextSplitter
import os
from langchain_community.document_loaders import PyPDFLoader

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
db = Chroma.from_documents(chunked_documents, embedding_function)
# query it
query = "I am a 1-18y-Year-Old Male with Sickle cell disease. I have eaten 10g of Hummus. I am about to eat 20g of Firm Tofu, should I eat it?"
docs = db.similarity_search(query)
# print results
print(docs[0].page_content)