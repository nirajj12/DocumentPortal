import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from models.models import *
from langchain_core.output_parsers import JsonOutputParser
from prompt.prompt_library import *

class DocumentAnalyzer:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.loader=ModelLoader()
            self.llm=self.loader.load_llm()


            self.parser=JsonOutputParser(pydantic_object=Metadata)
            self.prompt=prompt
            

            self.log.info("DocumentAnalyzer initialized successfully")


        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Error initializing DocumentAnalyzer",sys)


    def analyze_document(self,document_text:str)-> dict:
        try:
            chain=self.prompt | self.llm | self.parser
            self.log.info("Metadata analysis chain initialized successfully")

            response=chain.invoke(
                {
                    "format_instructions":self.parser.get_format_instructions(),
                    "document_text":document_text
                })
            
            self.log.info("Metadata extracted successfully",keys=list(response.keys()))
            return response
        except Exception as e:
            self.log.error(f"Metadata analysis failed", error=str(e))
            raise DocumentPortalException("Metadata extraction failed") from e