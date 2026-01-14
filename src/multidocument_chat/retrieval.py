import os
from pathlib import Path
import sys
from operator import itemgetter
from typing import List
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassThrough
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import ChatPromptTemplate
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from models.models import PromptType





class ConversationalRAG:
    def __init__(self,session_id: str,retriever=None):
        try:
            self.log= CustomLogger().get_logger(__name__)
            self.session_id= session_id
            self.llm= self._load_llm()
            self.contextualize_prompt:ChatPromptTemplate= PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt:ChatPromptTemplate= PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriever is None:
                raise ValueError("Retriever cannot be None")
            self.retriever= retriever
            self._build_lcel_chain()
            self.log.info("ConversationalRAG initialized", session_id=self.session_id)



        except Exception as e:
            self.log.error("Failed to initialize ConversationalRAG", error=str(e))
            raise DocumentPortalException("Initialization error in ConversationalRAG", sys)    
        

    def load_retriever_from_faiss(self,index_path: str):
        """
        Load a FAISS vectorstore from disk and convert to retriever.
        """
        try:
            embeddings=ModelLoader().load_embeddings()
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"FAISS index path does not exist: {index_path}")
            vectorstore= FAISS.load_local(index_path, embeddings,allow_dangerous_deserialization=True)

            self.retriever= vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
            self.log.info("Retriever loaded from FAISS", index_path=index_path, session_id=self.session_id)
            self._build_lcel_chain()
            return self.retriever


        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", error=str(e))
            raise DocumentPortalException("Error loading retriever from FAISS", sys)    


    def invoke(self,user_input:str,chat_history: Optional[list[BaseMessage]]=None) -> str:
        """
        Args:
            user_input(str):_description_
            chat_history(Optional[List[BaseMessage]],optional):_description_.Defaults to None.      
        """
        try:
            chat_history =chat_history or []
            payload={"input":user_input,"chat_history":chat_history}
            answer=self.chain.invoke(payload)
            if not answer:
                self.log.warning("No answer generated",user_input=user_input,session_id=self.session_id)
                return "no answer generated"
            self.log.info("chain invoked successfully",
                          session_id=self.session_id,
                          user_input=user_input,
                          answer_preview=answer[:150]
            )
            return answer
        except Exception as e:
            self.log.error("Failed to invoke ConversationalRAG", error=str(e))
            raise DocumentPortalException("Error invoking ConversationalRAG", sys)
        

    def _load_llm(self):
        try:
            model_loader= ModelLoader()
            llm= model_loader.load_llm()
            if not llm:
                raise ValueError("LLM could not be loaded")
            self.log.info("LLM loaded successfully", session_id=self.session_id)
            return llm
        except Exception as e:
            self.log.error("Failed to load LLM", error=str(e))
            raise DocumentPortalException("Error loading LLM in ConversationalRag", sys)

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)
    

    def _build_lcel_chain(self):
        try:
            #1.Rewrite Question using chat history
            question_rewriter = (
                { "input": itemgetter("input"), "chat_history": itemgetter("chat_history") }
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser
            )   
            #2.Retrieve docs for rewritten question 
            retrieve_docs= self.retriever | self._format_docs
            #3.Feed context + original input_chat history into answer prompt
            self.chain= (
                {
                    "context": retrieve_docs,
                    "input":itemgetter("input"),
                    chat_history:itemgetter("chat_history")
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
            )
            self.log.info("LCEL chain built successfully", session_id=self.session_i  d)
        except Exception as e:    
            self.log.error("Failed to build LCEL chain", error=str(e))
            raise DocumentPortalException("Error building LCEL chain in ConversationalRAG", sys)
    