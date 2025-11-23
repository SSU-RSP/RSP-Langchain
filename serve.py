import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. CORS 미들웨어 import
from typing import List

# [수정] schemas에서 모든 모델을 가져옵니다.
from schemas import AnalysisRequest, AnalysisResponse, StorytellingRequest, PaperStorySummary, SectionAnalysisResult
# [수정] processor와 함께 story_agent도 가져옵니다.
from processor import analyze_section, analyze_sections_in_batch
from agents import process_story

app = FastAPI(
    title="논문 분석 API 서버",
    version="1.0",
    description="순수 FastAPI 방식으로 배포된 LangChain 멀티에이전트",
)

# 2. 허용할 프런트엔드 주소 목록 정의
origins = [
    "https://rock-scissors-paper-euuokmzip-candoshs-projects.vercel.app",
    "https://rock-scissors-paper-git-develop-candoshs-projects.vercel.app", # <-- 새 주소 추가
    "http://localhost",
    "http://localhost:3000",
]

# 3. CORS 미들웨어를 앱에 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 기존 /summarize-section API ---
@app.post("/summarize-section", response_model=AnalysisResponse)
async def summarize_section(request: AnalysisRequest):
    # ... (기존 코드와 동일) ...
    print(f"요청 수신: section_id={request.section_id}, title='{request.paper_title}'")
    response = await analyze_section(request)
    return response

# --- 신규 /storytelling API (추가) ---
@app.post("/storytelling", response_model=PaperStorySummary)
async def create_story(request: StorytellingRequest):
    """
    논문 전체 텍스트를 받아 6단계 스토리텔링으로 요약합니다.
    """
    print(f"스토리텔링 요청 수신: paper_id={request.paper_id}")

    # story_agent의 process_story 함수는 동기 함수이므로,
    # FastAPI의 비동기 환경에서 안전하게 실행하기 위해 to_thread를 사용합니다.
    story_json = await asyncio.to_thread(
        process_story,
        paper_id=request.paper_id,
        full_paper_text=request.full_paper_text
    )
    return story_json

@app.post("/summarize-section-front", response_model=List[SectionAnalysisResult])
async def summarize_sections(requests: List[AnalysisRequest]):
    """
    여러 섹션 데이터를 배열로 받아, 각 섹션을 분석하고 결과 배열을 반환합니다.
    """
    print(f"배치 요청 수신: {len(requests)}개 섹션")
    response = await analyze_sections_in_batch(requests)
    return response

# --- 서버 실행 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)