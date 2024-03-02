from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
import google.generativeai as genai

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

embedding_function = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")


def processCSV(path, llm):
    loader = CSVLoader(file_path=path, encoding="utf-8", csv_args={
                'delimiter': ','})
    data = loader.load()
    
    vectorstore = FAISS.from_documents(data, embedding_function)
    
    chain = ConversationalRetrievalChain.from_llm(
    llm = llm,
    retriever=vectorstore.as_retriever())
    
    return chain

