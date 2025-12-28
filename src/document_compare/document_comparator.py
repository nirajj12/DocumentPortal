import sys
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from models.models import *
from utils.model_loader import ModelLoader
from prompt.prompt_library import PROMPT_REGISTRY
from langchain_core.output_parsers import JsonOutputParser


class DocumentComparator:
    def __init__(self):
        load_dotenv()
        self.log= CustomLogger().get_logger(__name__)
        self.loader=ModelLoader()
        self.llm=self.loader.load_llm()
        self.parser=JsonOutputParser(pydantic_object=SummaryResponse)
        self.prompt=PROMPT_REGISTRY["document_comparison"]
        self.chain=self.prompt | self.llm | self.parser
        self.log.info("DocumentComparator initialized successfully")

    def compare_documents(self,combined_docs: str) -> pd.DataFrame:
        """
        Compares two PDF documents and returns a structured comparison.
        """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instructions": self.parser.get_format_instructions()
            }

            self.log.info("Invoking document comparison LLM chain")
            response = self.chain.invoke(inputs)
            df=self.format_response(response)
            return df
        except Exception as e:
            self.log.error(f"Error in compare_documents: {e}")
            raise DocumentPortalException("An Error occurred in comparing documents",sys)
            


    def format_response(self,response_parsed:list[dict]) -> pd.DataFrame:
        """
        Formats the comparison response from the LLM into the desired structure.
        """
        try:
            df=pd.DataFrame(response_parsed)
            self.log.info("Response formatted into DataFrame",dataframe=df)
            return df
        except Exception as e:
            self.log.error(f"Error formatting response into DataFrame", error=str(e)) 
            raise DocumentPortalException("An error occurred in comparing documents.",sys)       

