import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.runnables import (
    RunnableWithMessageHistory,
    RunnableLambda,
    RunnablePassthrough
)
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from prompt.prompt_library import PROMPT_REGISTRY
from models.models import PromptType
import streamlit as st

class ConversationalRAG:
    def __init__(self,session_id: str,retriever) -> None:
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever = retriever
            self.llm = self._load_llm()
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            # -------- History-aware question reformulation --------
            def contextualize_question(inputs):
                response = self.llm.invoke(
                    self.contextualize_prompt.format_messages(
                        chat_history=inputs["chat_history"],
                        input=inputs["input"]
                    )
                )
                return response.content

            history_aware_retriever = (
                RunnablePassthrough.assign(
                    standalone_question=contextualize_question
                )
                | RunnableLambda(lambda x: x["standalone_question"])
                | self.retriever
            )
            self.log.info("create history aware retriever success",session_id=session_id)
             # -------- Answer generation (stuff documents) --------
            def answer_question(inputs):
                docs = inputs["context"]
                context_text = "\n\n".join(
                    doc.page_content for doc in docs
                )

                response = self.llm.invoke(
                    self.qa_prompt.format_messages(
                        context=context_text,
                        input=inputs["input"],
                        chat_history=inputs["chat_history"] 
                    )
                )
                return {"answer": response.content}

            # -------- Full RAG chain --------
            self.rag_chain = (
                RunnablePassthrough.assign(
                    context=history_aware_retriever
                )
                | RunnableLambda(answer_question)
            )
            self.log.info("create RAG chain success",session_id=session_id)
            def get_session_history(session_id: str):
                return self._get_session_history(session_id)

            self.chain = RunnableWithMessageHistory(
                self.rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
            )

            self.log.info("create RunnableChatMessageHistory ",session_id=session_id)



        except Exception as e:
            self.log.error("Error initializing ConversationRag", error=str(e),session_id=session_id)
            raise DocumentPortalException("Error initializing ConversationRag", sys)
        
    def _load_llm(self):
        try:
            llm=ModelLoader().load_llm()
            self.log.info("LLM loaded successfully",class_name=llm.__class__.__name__)
            return llm
        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error=str(e))
            raise DocumentPortalException("Failed to load LLM", sys)
        

    def _get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        try:
            if "store" not in st.session_state:
                st.session_state.store = {}
            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
                self.log.info("New chat history created", session_id=session_id)

            return st.session_state.store[session_id]    
        except Exception as e:
            self.log.error("Error retrieving session history", session_id=session_id ,error=str(e))
            raise DocumentPortalException("Failed to retrieve session history", sys)    
        
    def load_retriever_from_faiss(self,index_path: str):
        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found at {index_path}")
            
            vectorstore= FAISS.load_local(index_path, embeddings,allow_dangerous_deserialization=True)
            self.log.info("Loaded retriever from FAISS index", index_path=index_path) 
            return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        except Exception as e:
            self.log.error("Error loading FAISS retriever", error=str(e))
            raise DocumentPortalException("Failed to load FAISS retriever", sys)    
        

    def invoke(self,user_input:str) -> str:
        try:
            response = self.chain.invoke({"input": user_input},config={"configurable": { "session_id": self.session_id}})
            answer = response.get('answer','No answer')
            if not answer:
                self.log.warning("Empty answer received", session_id=self.session_id)

            self.log.info("Chain invoked successfully", session_id=self.session_id, user_input=user_input, answer_preview=answer[:150])  
            return answer  
        except Exception as e:
            self.log.error("Failed to invoke ConversationRag", error=str(e),session_id=self.session_id)
            raise DocumentPortalException("Error during ConversationRag invocation", sys)  