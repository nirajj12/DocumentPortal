import sys
import uuid
from pathlib import Path
import fitz
from datetime import datetime, timezone
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentIngestion:
    """
    Handles saving,reading and combining of PDF's for comparison with session-based versioning.
    """

    def __init__(self,base_dir:str="data/document_compare",session_id=None):
        self.log= CustomLogger().get_logger(__name__)
        self.base_dir=Path(base_dir)
        self.session_id=session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{(uuid.uuid4()).hex[:8]}"
        self.session_path=self.base_dir/self.session_id
        self.session_path.mkdir(parents=True,exist_ok=True)

        self.log.info("DocumentComparator initialized",session_id=self.session_id,session_path=str(self.session_path))

    # def delete_existing_file(self):
    #     """
    #     Deletes an existing file at the specified path.
    #     """
    #     try:
    #         if self.base_dir.exists() and self.base_dir.is_dir():
    #             for file in self.base_dir.iterdir():
    #                 if file.is_file():
    #                     file.unlink()
    #                     self.log.info("File Deleted",path=str(file))
    #             self.log.info("Directory cleaned",directory=str(self.base_dir))
    #     except Exception as e:
    #         self.log.error(f"Error deleting existing file: {e}")
    #         raise DocumentPortalException("An Error occurred while deleting existing file",sys)

    def save_uploaded_file(self,reference_file,actual_file):
        """
        Saves Uploaded files to a specific directory.
        """
        try:
            # self.delete_existing_file()
            # self.log.info(f"Existing file deleted successfully")
            ref_path=self.session_path/reference_file.name
            act_path=self.session_path/actual_file.name

            if not reference_file.name.lower().endswith('.pdf') or not actual_file.name.lower().endswith('.pdf'):
                raise ValueError("Invalid file format. Only PDF files are allowed.")
            
            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())

            with open(act_path,"wb") as f:    
                f.write(actual_file.getbuffer())

            self.log.info("Files saved",reference=str(ref_path),actual=str(act_path),session=self.session_id)
            return ref_path,act_path




        except Exception as e:
            self.log.error(f"Error saving uploaded file: {e}")
            raise DocumentPortalException("An Error occurred while saving uploaded file",sys)

    def read_pdf(self,pdf_path:Path)-> str:
        """
        Reads a PDF file and extracts text from each page
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()  # type: ignore
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num + 1} --- \n{text}")
            self.log.info("PDF read successfully", file=str(pdf_path), pages=len(all_text))
            return "\n".join(all_text)
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}",file=str(pdf_path),error=str(e))
            raise DocumentPortalException("An Error occurred while reading PDF",sys)
        
    def combine_documents(self)-> str:
        try:
            content_dict={}
            doc_parts=[]
            for filename in sorted(self.session_path.iterdir()):
                if filename.is_file() and filename.suffix.lower() == '.pdf':
                    content_dict[filename.name]=self.read_pdf(filename)      

            for filename,content in content_dict.items():
                doc_parts.append(f"Document:{filename}\n{content}")

            combined_text="\n\n".join(doc_parts)            
            self.log.info("Documents combined successfully",count=len(doc_parts),session=self.session_id)
            return combined_text

        except Exception as e:
            self.log.error(f"Error combining documents",error=str(e),session=self.session_id)
            raise DocumentPortalException("An Error occurred while combining documents",sys)            
                                    

    def clean_old_sessions(self, keep_latest: int = 3):
        """
        optional method to Cleans up old session folders, keeping only the latest 'keep_latest' sessions.
        """
        try:
            session_folders = sorted([f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True)
            for folder in session_folders[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()    
                self.log.info("Old session folder deleted", path=str(folder))
        except Exception as e:
            self.log.error("Error cleaning old sessions", error=str(e))
            raise DocumentPortalException("Error cleaning old sessions", sys)                               
