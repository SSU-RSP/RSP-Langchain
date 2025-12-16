from pydantic import BaseModel, Field
from typing import List, Optional

# --- 공통 결과 모델 (이미지, 표, 수식용) ---
class AnalysisResultItem(BaseModel):
    image_url: str
    description: str

# --- 1. 텍스트 에이전트용 스키마 ---
class TextAnalysisRequest(BaseModel):
    paper_title: str
    text: str  # 논문 전체 텍스트 (또는 요약 대상 텍스트)

class TextAnalysisResponse(BaseModel):
    result: str

# --- 2. 비전(그림) 에이전트용 스키마 ---
class VisionAnalysisRequest(BaseModel):
    paper_title: str
    text: str       # 배경 지식용 텍스트 (Context)
    images: List[str] # 분석할 이미지 URL 리스트

class VisionAnalysisResponse(BaseModel):
    results: List[AnalysisResultItem]

# --- 3. 표(Table) 에이전트용 스키마 ---
class TableAnalysisRequest(BaseModel):
    paper_title: str
    text: str       # 배경 지식용 텍스트 (Context)
    tables: List[str] # 분석할 표 이미지 URL 리스트

class TableAnalysisResponse(BaseModel):
    results: List[AnalysisResultItem]

# --- 4. 수식(Math) 에이전트용 스키마 ---
class MathAnalysisRequest(BaseModel):
    paper_title: str
    text: str       # 배경 지식용 텍스트 (Context)
    equations: List[str] # 분석할 수식 이미지 URL 리스트

class MathAnalysisResponse(BaseModel):
    results: List[AnalysisResultItem]

# --- 스토리텔링용 (기존 유지) ---
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

    # --- 6. 팟캐스트(Podcast) 에이전트용 스키마 ---
class PodcastRequest(BaseModel):
    paper_title: str
    text: str       # 요약된 텍스트나 논문 전체 텍스트

class PodcastResponse(BaseModel):
    script: str     # 생성된 팟캐스트 대본

# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict

# # [신규] 이미지/표/수식 분석 결과를 담는 상세 모델
# class AnalysisResultItem(BaseModel):
#     image_url: str
#     description: str

# class AnalysisRequest(BaseModel):
#     section_id: int
#     # table_of_contents, section_title은 에이전트에서 쓰지 않더라도 
#     # 프론트엔드 호환성을 위해 남겨둘 수 있으나, 필요 없다면 Optional로 둡니다.
#     table_of_contents: Optional[str] = ""
#     paper_title: str
#     section_title: Optional[str] = "" # 에이전트 입력에서 제외됨
#     text: Optional[str] = None # 논문 전체 텍스트
#     images: Optional[List[str]] = Field(default_factory=list)
#     tables: Optional[List[str]] = Field(default_factory=list)
#     equations: Optional[List[str]] = Field(default_factory=list)

# class AnalysisResponse(BaseModel):
#     text_result: Optional[str] = None # 텍스트 요약은 여전히 str
#     # [수정] 아래 3개는 이제 문자열이 아니라 리스트(객체 배열)입니다.
#     image_results: List[AnalysisResultItem] = Field(default_factory=list)
#     table_results: List[AnalysisResultItem] = Field(default_factory=list)
#     equation_results: List[AnalysisResultItem] = Field(default_factory=list)

# class StorytellingRequest(BaseModel):
#     paper_id: int
#     full_paper_text: str

# class StorySection(BaseModel):
#     step: int
#     heading: str
#     content: str

# class PaperStorySummary(BaseModel):
#     paper_id: int
#     title: str
#     sections: List[StorySection]

# class SectionAnalysisResult(BaseModel):
#     section_id: int
#     text_result: Optional[str] = None
#     # [수정] 배치 처리 결과 모델도 동일하게 리스트로 변경
#     image_results: List[AnalysisResultItem] = Field(default_factory=list)
#     table_results: List[AnalysisResultItem] = Field(default_factory=list)
#     equation_results: List[AnalysisResultItem] = Field(default_factory=list)

# # schemas.py
# from pydantic import BaseModel, Field
# from typing import List, Optional

# class AnalysisRequest(BaseModel):
#     section_id: int
#     table_of_contents: str
#     paper_title: str
#     section_title: str
#     text: Optional[str] = None
#     images: Optional[List[str]] = Field(default_factory=list)
#     tables: Optional[List[str]] = Field(default_factory=list)
#     equations: Optional[List[str]] = Field(default_factory=list)

# class AnalysisResponse(BaseModel):
#     text_result: Optional[str] = None
#     image_results: Optional[str] = None
#     table_results: Optional[str] = None
#     equation_results: Optional[str] = None

# class StorytellingRequest(BaseModel):
#     paper_id: int
#     full_paper_text: str

# class StorySection(BaseModel):
#     step: int
#     heading: str
#     content: str

# class PaperStorySummary(BaseModel):
#     paper_id: int
#     title: str
#     sections: List[StorySection]

# class SectionAnalysisResult(BaseModel):
#     section_id: int
#     text_result: Optional[str] = None
#     image_results: Optional[str] = None
#     table_results: Optional[str] = None
#     equation_results: Optional[str] = None