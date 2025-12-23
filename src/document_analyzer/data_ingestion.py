import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentHandler:
    def __init__(self, data_dir=None,session_id=None):
        try:
            self.log= CustomLogger().get_logger(__name__)
            self.data_dir=data_dir or os.getenv(
                "DATA_STORAGE_PATH", 
                os.path.join(os.getcwd(), "data", "document_analysis")
                )
            self.session_id=session_id or f"session_{datetime.now().strftime('% Y%m%d_%H%M%S')}_{(uuid.uuid4()).hex[:8]}"
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)


        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Error initializing DocumentHandler",e) from e
        
    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)

            if not filename.lower().endswith('.pdf'):
                raise DocumentPortalException("invalid file format. Only PDF files are allowed.")
            
            save_path= os.path.join(self.session_path,filename) 
            with open(save_path,'wb') as f:
                f.write(uploaded_file.getbuffer())
            self.log.info(f"PDF saved successfully.",file=filename, save_path=save_path,session_id=self.session_id)
            return save_path
        
        except Exception as e:
            self.log.error(f"Error saving PDF: {e}")
            raise DocumentPortalException("Error saving PDF",e) from e
        
    def read_pdf(self,pdf_path:str)-> str:
        try:
            text_chunks=[]
            with fitz.open(pdf_path) as doc:
                for page_num,page in enumerate(doc,start=1):
                    text_chunks.append(f"n-- Page {page_num} ---\n {page.get_text()}")
                    text="\n".join(text_chunks)

                    self.log.info("pdf read successfully",pdf_path=pdf_path,session_id=self.session_id)
                    return text
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("Error reading PDF",e) from e    
        
if __name__ == "__main__":            
    from pathlib import Path
    from io import BytesIO
    

    pdf_path=Path(r"/Users/nirajmac/Documents/LLMOPS/document_portal/data/document_analysis/NIPS-2017-attention-is-all-you-need-Paper.pdf")


    class DummyFile:
        def __init__(self, file_path):
            self.name=Path(file_path).name
            self.file_path=file_path
        def getbuffer(self):
            return open(self.file_path,"rb").read()

    dummy_file=DummyFile(pdf_path)    

    handler = DocumentHandler()

    try:
        saved_path=handler.save_pdf(dummy_file)
        print(f"PDF saved at: {saved_path}")
        content=handler.read_pdf(saved_path)
        print(content[:500])
    except DocumentPortalException as e:    
        print(f"An error occurred: {e}")

