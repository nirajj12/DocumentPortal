import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from models.models import *
from langchain_core.output_parsers import JsonOutputParser

class DocumentAnalyzer:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.logger = CustomLogger()
        self.output_parser = JsonOutputParser()
        self.fixing_parser= OutputFixingParser.from_output_parser(self.output_parser)
        