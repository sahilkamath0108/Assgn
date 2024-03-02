from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
import google.generativeai as genai
from PyPDF2 import PdfReader


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
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = FAISS.from_documents(text_chunks, embeddings)

    vectorstore.save_local(DB_FAISS_PATH)
    
    return vectorstore

def processPDF(path):
    pdf_reader = PdfReader(path)
    text = ''
    for i, page in enumerate(pdf_reader.pages):
        if page:
            text = page.extract_text()
            if text:
                text += text
    print(text)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

    vectorstore = FAISS.from_texts(text_chunks, embeddings)

    vectorstore.save_local(DB_FAISS_PATH)
    
    return vectorstore

