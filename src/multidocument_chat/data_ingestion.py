import uuid
from pathlib import Path
import sys
from datetime import datetime,timezone
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from utils.model_loader import ModelLoader





class DocumentIngestor:
    SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt", ".md"]
    def __init__(self,temp_dir: str="data/multi_document_chat",faiss_dir: str="faiss_index",session_id: str | None=None):
        try:
            self.log=CustomLogger().get_logger(__name__)
            self.temp_dir= Path(temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir= Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.session_id= session_id if session_id else f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir= self.temp_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir= self.faiss_dir / self.session_id
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)
            self.model_loader= ModelLoader()
            self.log.info(
                "DocumentIngestor initialized",
                temp_base=str(self.temp_dir),
                faiss_base=str(self.faiss_dir),
                session_id=self.session_id,
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir)
            )
        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", error=str(e))
            raise DocumentPortalException("Initialization error in ChatIngestor", sys) 

    def ingest_files(self,uploaded_files):
        try:
            documents=[]
            for uploaded_file in uploaded_files:
                ext=Path(uploaded_file.name).suffix.lower()
                if ext not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning("Unsupported file type", file_name=uploaded_file.name,session_id=self.session_id)
                    continue
                original_name = Path(uploaded_file.name).name
                temp_path= self.session_temp_dir / original_name
                uploaded_file.seek(0)
                with open(temp_path,"wb") as f:
                    f.write(uploaded_file.read())
                    self.log.info("File saved for ingestion", file_name=uploaded_file.name, saved_as=str(temp_path),session_id=self.session_id)

                if ext==".pdf":
                    loader= PyPDFLoader(str(temp_path))
                elif ext==".docx":
                    loader= Docx2txtLoader(str(temp_path))
                elif ext in [".txt",".md"]:
                    loader= TextLoader(str(temp_path))
                else:
                    self.log.warning("unsupported file type", file_name=uploaded_file.name)
                    continue

                docs= loader.load()
                documents.extend(docs)

            if not documents:
                raise DocumentPortalException("No valid documents loaded", sys)
                
                self.log.info("Files loaded successfully", total_docs=len(documents), session_id=self.session_id)
            return self._create_retriever(documents)


        except Exception as e:
            self.log.error("Failed to ingest files", error=str(e))
            raise DocumentPortalException("Error during file ingestion",sys)
    def _create_retriever(self,documents):
        try:
            splitter= RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks= splitter.split_documents(documents)
            self.log.info("Documents split into chunks", total_chunks=len(chunks), session_id=self.session_id)

            embeddings= self.model_loader.load_embeddings()
            vectorstore= FAISS.from_documents(chunks, embeddings)

            vectorstore.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS index saved to disk", faiss_path=str(self.session_faiss_dir), session_id=self.session_id)

            retriever= vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
            self.log.info("FAISS retriever created successfully", session_id=self.session_id)
            return retriever

        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentPortalException("retriever Error in DocumentIngestor",sys)

