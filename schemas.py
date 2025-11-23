# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisRequest(BaseModel):
    section_id: int
    table_of_contents: str
    paper_title: str
    section_title: str
    text: Optional[str] = None
    images: Optional[List[str]] = Field(default_factory=list)
    tables: Optional[List[str]] = Field(default_factory=list)
    equations: Optional[List[str]] = Field(default_factory=list)

class AnalysisResponse(BaseModel):
    text_result: Optional[str] = None
    image_results: Optional[str] = None
    table_results: Optional[str] = None
    equation_results: Optional[str] = None

class StorytellingRequest(BaseModel):
    paper_id: int
    full_paper_text: str

class StorySection(BaseModel):
    step: int
    heading: str
    content: str

class PaperStorySummary(BaseModel):
    paper_id: int
    title: str
    sections: List[StorySection]

class SectionAnalysisResult(BaseModel):
    section_id: int
    text_result: Optional[str] = None
    image_results: Optional[str] = None
    table_results: Optional[str] = None
    equation_results: Optional[str] = None