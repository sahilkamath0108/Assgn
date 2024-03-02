from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
import google.generativeai as genai


from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
DB_FAISS_PATH = "vectorstore/db_faiss"

def processCSV(path):
    loader = CSVLoader(file_path=path, encoding="ISO-8859-1", csv_args={
                'delimiter': ','})
    data = loader.load()
    print(data)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)

    print(len(text_chunks))

# Download Sentence Transformers Embedding From Hugging Face
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

# COnverting the text Chunks into embeddings and saving the embeddings into FAISS Knowledge Base
    vectorstore = FAISS.from_documents(text_chunks, embeddings)

    vectorstore.save_local(DB_FAISS_PATH)
    
    return vectorstore

