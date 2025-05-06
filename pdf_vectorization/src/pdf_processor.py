import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

class PDFProcessor:
    def __init__(self, persist_directory: str = "models/vector_store"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    def process_pdf(self, pdf_path: str) -> List[str]:
        """Charge et traite un fichier PDF"""
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        texts = self.text_splitter.split_documents(pages)
        return texts
    
    def create_vector_store(self, texts: List[str], collection_name: str):
        """Crée ou met à jour le vector store"""
        vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )
        vector_store.persist()
        return vector_store
    
    def load_vector_store(self, collection_name: str):
        """Charge un vector store existant"""
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=collection_name
        ) 