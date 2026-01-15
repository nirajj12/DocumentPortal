from pydantic import BaseModel,Field,RootModel
from typing import Optional,List,Dict,Any,Union
from enum import Enum

class Metadata(BaseModel):
    Summary: List[str] = Field(
        ..., 
        description="3–5 concise bullet points summarizing the document"
    )

    Title: Optional[str] = Field(
        None, description="Title of the document"
    )

    Author: Optional[str] = Field(
        None, description="Author or creator of the document"
    )

    DateCreated: Optional[str] = Field(
        None, description="Original creation date if available"
    )

    LastModifiedDate: Optional[str] = Field(
        None, description="Last modified date if available"
    )

    Publisher: Optional[str] = Field(
        None, description="Publishing organization or entity"
    )

    Language: Optional[str] = Field(
        None, description="Language of the document"
    )

    PageCount: Optional[int] = Field(
        None, description="Total number of pages"
    )

    SentimentTone: Optional[str] = Field(
        None, description="Overall sentiment tone (Positive, Neutral, Negative)"
    )

class ChangeFormat(BaseModel):
    page:str
    changes:str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass 
    
class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"