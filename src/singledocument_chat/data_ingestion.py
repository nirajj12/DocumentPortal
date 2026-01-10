import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorestores import  FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
 


class SingleDocIngestor:
    def __init__(self):
        try:
            self.log= CustomLogger.get_logger(__name__)
            self.loader = ModelLoader()
            self.pdf_loader = PyPDFLoader()
            self.text_splitter = RecursiveCharacterTextSplitter()
            self.vector_store = FAISS()

        except Exception as e:
            self.log.error("Failed to initialize SingleDocIngestor", error=str(e))
            raise DocumentPortalException("Error initializing SingleDocIngestor", sys)
        

    def ingest_files(self):
        try:
            pass
        except Exception as e:    
            self.log.error("Failed to ingest files", error=str(e))
            raise DocumentPortalException("Error during file ingestion",sys)


    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentPortalException("Error creating FAISS retriever", sys)     