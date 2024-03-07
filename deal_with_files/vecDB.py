from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from PyPDF2 import PdfReader

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma, FAISS
from langchain_text_splitters import CharacterTextSplitter

DB_FAISS_PATH = "vectorstore/db_faiss"
   
def vectorize(path):
    pdf_reader = PdfReader(path)
    text = ''
    for i, page in enumerate(pdf_reader.pages):
        if page:
            text = page.extract_text()
            if text:
                text += text

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_text(text)

    embedding_function = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")

    vectorstore = FAISS.from_texts(docs, embedding_function)

    vectorstore.save_local(DB_FAISS_PATH)   
    
    return vectorstore

if __name__ == '__main__':
    path = "C:\\Users\\Hp\\Desktop\\words.pdf"
    vectorize(path)
