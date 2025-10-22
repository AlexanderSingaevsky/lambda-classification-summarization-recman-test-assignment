from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ClassificationTopics(str, Enum):
    finance = "finance"
    technical = "technical"
    hr = "hr"
    marketing = "marketing"
    it_operations = "it_operations"
    general = "general"


class EmailItem(BaseModel):
    id: int = Field(..., description="Unique identifier of the item")
    subject: str = Field("", description="Subject line of the email-like text")
    body: str = Field("", description="Body content of the email-like text")


class ClassificationInput(BaseModel):
    items: List[EmailItem] = Field(..., description="Items to classify")


class ClassificationOutputItem(BaseModel):
    id: int
    topics: Optional[List[str]] = None
    error: Optional[str] = None


class SummarizationInput(BaseModel):
    items: List[EmailItem] = Field(..., description="Items to summarize")


class SummarizationOutputItem(BaseModel):
    id: int
    summary: Optional[str] = None
    error: Optional[str] = None

