# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

# PDF_PATH=r"/Users/nirajmac/Documents/LLMOPS/document_portal/data/document_analysis/NIPS-2017-attention-is-all-you-need-Paper.pdf"

# class DummyFile:
#     def __init__(self, file_path):
#         self.name=Path(file_path).name
#         self.file_path=file_path
#     def getbuffer(self):
#         return open(self.file_path,"rb").read()
    

# def main():
#     try:

#         print("Starting PDF Ingestion Test...")
#         dummy_pdf=DummyFile(PDF_PATH)
#         handler=DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path=handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content=handler.read_pdf(saved_path)
#         print(f"Extracted text content length: {len(text_content)} characters")

#         print("Starting Metadata Analysis...")
#         analyzer=DocumentAnalyzer()
#         analysis_result=analyzer.analyze_document(text_content)

#         print("Metadata Analysis Result:")
#         for key,value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")


# if __name__ == "__main__":    
#     main()

# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparator

# def load_fake_uploaded_file(file_path:Path):
#     return io.BytesIO(file_path.read_bytes())

# def test_compare_documents():
#     ref_path=Path("/Users/nirajmac/Documents/LLMOPS/document_portal/data/document_compare/Stability_Report_Amoxicillin.pdf")
#     act_path=Path("/Users/nirajmac/Documents/LLMOPS/document_portal/data/document_compare/Stability_Report_Paracetamol.pdf")

#     class FakeUpload:
#         def __init__(self,file_path:Path):
#             self.name=file_path.name
#             self._buffer=file_path.read_bytes()
#         def getbuffer(self):
#             return self._buffer
        
#     comparator=DocumentIngestion()
#     ref_upload=FakeUpload(ref_path)
#     act_upload=FakeUpload(act_path)


#     ref_file,act_file=comparator.save_uploaded_file(ref_upload,act_upload)
#     combined_text=comparator.combine_documents()
#     comparator.clean_old_sessions(keep_latest=3)

#     print("/nCombined Document Text Preview(first 1000 chars):/n")
#     print(combined_text[:1000])

#     llm_comparator=DocumentComparator()
#     comparison_df=llm_comparator.compare_documents(combined_text)

#     print("/nComparison Result :/n")
#     print(comparison_df)


# if __name__ == "__main__":    
#     test_compare_documents()



# # # Testing code for document chat functionality

# import sys
# from pathlib import Path
# from langchain_community.vectorstores.faiss import FAISS

# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH = Path("faiss_index")

# def test_conversational_rag_on_pdf(pdf_path:str, question:str):
#     try:
#         model_loader = ModelLoader()
        
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS index...")
#             embeddings = model_loader.load_embeddings()
#             vectorstore = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)
#             retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingesting PDF and creating index...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files = [f]
#                 ingestor = SingleDocIngestor()
#                 retriever = ingestor.ingest_files(uploaded_files)
                
#         print("Running Conversational RAG...")
#         session_id = "test_conversational_rag"
#         rag = ConversationalRAG(retriever=retriever, session_id=session_id)
#         response = rag.invoke(question)
#         print(f"\nQuestion: {question}\nAnswer: {response}")
                    
#     except Exception as e:
#         print(f"Test failed: {str(e)}")
#         sys.exit(1)
    
# if __name__ == "__main__":
#     # Example PDF path and question
#     pdf_path = "data/single_document_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf"
#     question = "What is the significance of the attention mechanism? can you explain it in simple terms?"

#     if not Path(pdf_path).exists():
#         print(f"PDF file does not exist at: {pdf_path}")
#         sys.exit(1)
    
#     # Run the test
#     test_conversational_rag_on_pdf(pdf_path, question)
    

    # testing for multidoc chat
import sys
from pathlib import Path
from src.multidocument_chat.data_ingestion import DocumentIngestor
from src.multidocument_chat.retrieval import ConversationalRAG

def test_document_ingestion_and_rag():
    try:
        test_files = [
            "data/multi_document_chat/AI_1000plus.txt",
            "data/multi_document_chat/DataScience_1000plus.pdf",
            "data/multi_document_chat/ML_1000plus.docx",
            "data/multi_document_chat/NLP_1000plus.txt",
            "data/multi_document_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf"
        ]
        
        uploaded_files = []
        
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"File does not exist: {file_path}")
                
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
            
        ingestor = DocumentIngestor()
        
        retriever = ingestor.ingest_files(uploaded_files)
        
        for f in uploaded_files:
            f.close()
                
        session_id = "test_multi_doc_chat"
        
        rag = ConversationalRAG(session_id=session_id, retriever=retriever)
        
        question = "What is Artificial Intelligence and what core abilities does it aim to replicate?"
        
        answer=rag.invoke(question)
        
        print("\n Question:", question)
        
        print("Answer:", answer)
        
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    test_document_ingestion_and_rag()