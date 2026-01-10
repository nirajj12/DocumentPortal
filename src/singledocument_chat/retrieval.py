import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import ChatMessageHistory
from langchain_community.vectorestores import FAISS
from langchain_core.runnables.history import RunnableChatMessageHistory
from langchain.chains import create_retrieval_chain,create_history_aware_retrieval
from langchain.chains.combine_documents import create_stuff_documents_chain
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType


class ConversationRag:
    def __init__(self,session_id: str,retriever) -> None:
        try:
            self.log = CustomLogger.get_logger(__name__)
            pass
        except Exception as e:
            self.log.error("Error initializing ConversationRag", error=str(e),session_id=session_id)
            raise DocumentPortalException("Error initializing ConversationRag", sys)
        
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error=str(e))
            raise DocumentPortalException("Failed to load LLM", sys)
        

    def _get_session_history(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error retrieving session history", session_id=session_id ,error=str(e))
            raise DocumentPortalException("Failed to retrieve session history", sys)    
        
    def load_retriever_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading FAISS retriever", error=str(e))
            raise DocumentPortalException("Failed to load FAISS retriever", sys)    
        

    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke ConversationRag", error=str(e),session_id=self.session_id)
            raise DocumentPortalException("Error during ConversationRag invocation", sys)