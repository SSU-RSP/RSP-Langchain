from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
# schemas에서 새로 정의한 Response 모델을 가져옵니다 (파서 검증용)
from schemas import StorytellingResponse

# ... (process_text, process_vision 등 다른 함수들은 유지) ...

def process_story(content: str, paper_title: str) -> dict:
    """
    논문 텍스트를 입력받아 6단계(배경, 문제, 해결, 실험, 결과, 영향)로 구조화된 JSON을 반환합니다.
    """
    print(f"📖 스토리텔링 에이전트 호출됨 (제목: '{paper_title}')...")

    # Pydantic 모델을 기반으로 파서 설정
    parser = JsonOutputParser(pydantic_object=StorytellingResponse)
    
    llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)
    
    # 프롬프트: 6가지 키를 가진 JSON을 요구
    prompt_template = """
    **역할**: 당신은 논문 분석 전문가입니다.
    **분석 대상**: "{paper_title}"
    
    **지시**:
    제공된 논문 텍스트를 분석하여 다음 6가지 핵심 요소로 요약하고, 
    전체 내용을 아우르는 창의적인 한 줄 제목을 지어주세요.
    
    **요약 항목**:
    1. background (배경): 연구가 시작된 배경이나 기존 연구의 한계
    2. problem (문제): 이 논문이 해결하고자 하는 구체적인 문제
    3. method (해결): 저자가 제안하는 핵심 방법론이나 해결책
    4. experiment (실험): 검증을 위해 수행한 실험 내용
    5. result (결과): 실험을 통해 얻은 정량적/정성적 결과
    6. impact (영향): 이 연구가 학계나 산업에 미치는 의의

    **출력 형식**:
    반드시 아래의 JSON 키를 사용하여 응답해주세요. 언어는 **한국어**입니다.
    
    {{
        "title": "여기에 창의적인 제목 작성",
        "background": "배경 내용 요약...",
        "problem": "문제점 요약...",
        "method": "해결책 요약...",
        "experiment": "실험 내용 요약...",
        "result": "결과 요약...",
        "impact": "영향 및 의의 요약..."
    }}

    **논문 텍스트**:
    {text}
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | parser
    
    # invoke 실행
    result = chain.invoke({
        "paper_title": paper_title,
        "text": content
    })
    
    return result

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
# from schemas import PaperStorySummary

# def process_story(paper_id: int, full_paper_text: str) -> dict:
#     """
#     논문 전체 텍스트를 입력받아 6단계의 스토리텔링 JSON을 생성합니다.
#     """
#     parser = JsonOutputParser(pydantic_object=PaperStorySummary)
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)
    
#     # [수정] 지시사항과 예시 출력 형식을 변경하여 동적 제목 생성을 유도합니다.
#     prompt_template = """
#     당신은 논문 전체를 읽고 핵심 내용을 추출하여 6단계의 스토리텔링 구조로 요약하는 전문 분석가입니다.
#     다음 텍스트를 '배경', '문제', '해결책', '실험', '결과', '영향'의 6가지 관점으로 분석하고 요약해주세요.
    
#     각 단계별 요약은 간결하고 명확해야 합니다.
#     **모든 내용을 요약한 후, 전체 스토리를 가장 잘 나타내는 창의적이고 간결한 제목을 'title' 필드에 생성해주세요.**
    
#     <paper_text>
#     {text}
#     </paper_text>
    
#     아래 예시와 같이 JSON 형식으로만 응답을 생성해주세요.
#     응답 JSON에는 반드시 "paper_id"를 포함해야 합니다.
    
#     <예시 출력 형식>
#     {{"paper_id": {paper_id}, "title": "요약된 내용에 맞는 창의적인 제목 (예: 어텐션 메커니즘, 순환 신경망을 대체하다)", "sections": [
#       {{"step": 1, "heading": "배경 (Background)", "content": "..."}},
#       {{"step": 2, "heading": "문제 (Problem)", "content": "..."}},
#       ...
#       {{"step": 6, "heading": "영향 (Impact)", "content": "..."}}
#     ]}}
#     """
    
#     prompt = ChatPromptTemplate.from_template(prompt_template)
#     chain = prompt | llm | parser
#     result = chain.invoke({"paper_id": paper_id, "text": full_paper_text})
    
#     return result

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
# from schemas import PaperStorySummary

# def process_story(paper_id: int, full_paper_text: str) -> dict:
#     """
#     논문 전체 텍스트를 입력받아 6단계의 스토리텔링 JSON을 생성합니다.
#     """
#     parser = JsonOutputParser(pydantic_object=PaperStorySummary)
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)
    
#     prompt_template = """
#     당신은 논문 전체를 읽고 핵심 내용을 추출하여 6단계의 스토리텔링 구조로 요약하는 전문 분석가입니다.
#     다음 텍스트를 '배경', '문제', '해결책', '실험', '결과', '영향'의 6가지 관점으로 분석하고 요약해주세요.
#     각 단계별 요약은 간결하고 명확해야 합니다.
#     <paper_text>
#     {text}
#     </paper_text>
#     아래 예시와 같이 JSON 형식으로만 응답을 생성해주세요.
#     응답 JSON에는 반드시 "paper_id"를 포함해야 합니다.
#     <예시 출력 형식>
#     {{"paper_id": {paper_id}, "title": "논문 스토리 요약 (Paper Story Summary)", "sections": [
#       {{"step": 1, "heading": "배경 (Background)", "content": "..."}},
#       {{"step": 2, "heading": "문제 (Problem)", "content": "..."}},
#       ...
#       {{"step": 6, "heading": "영향 (Impact)", "content": "..."}}
#     ]}}
#     """
    
#     prompt = ChatPromptTemplate.from_template(prompt_template)
#     chain = prompt | llm | parser
#     result = chain.invoke({"paper_id": paper_id, "text": full_paper_text})
    
#     return result

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

# # 논문 스토리텔링의 각 섹션을 정의하는 Pydantic 모델
# class StorySection(BaseModel):
#     step: int = Field(description="스토리텔링 단계의 순서 (1~6)")
#     heading: str = Field(description="섹션의 제목 (예: '배경', '문제', '해결책')")
#     content: str = Field(description="해당 섹션의 핵심 내용 요약")

# # 전체 논문 요약 JSON 형식을 정의하는 Pydantic 모델
# class PaperStorySummary(BaseModel):
#     paper_id: int = Field(description="논문의 고유 ID")
#     title: str = Field(description="스토리텔링 요약의 제목")
#     sections: list[StorySection] = Field(description="논문의 6단계 스토리 요약 리스트")

# def process_story(paper_id: int, full_paper_text: str) -> str:
#     """
#     논문 전체 텍스트를 입력받아 6단계의 스토리텔링 JSON을 생성합니다.
    
#     Args:
#         paper_id (int): 논문의 고유 ID.
#         full_paper_text (str): 논문 전체 텍스트.
        
#     Returns:
#         dict: 6단계의 스토리텔링 요약 JSON.
#     """
#     # LangChain에서 사용할 출력 파서와 모델을 설정합니다.
#     # JsonOutputParser는 Pydantic 모델의 스키마에 맞춰 JSON 생성을 유도합니다.
#     parser = JsonOutputParser(pydantic_object=PaperStorySummary)
    
#     # gemini-2.0-flash 모델을 사용합니다.
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)
    
#     # LLM에게 JSON 출력을 위한 지시사항을 포함하는 프롬프트 템플릿을 생성합니다.
#     prompt_template = """
#     당신은 논문 전체를 읽고 핵심 내용을 추출하여 6단계의 스토리텔링 구조로 요약하는 전문 분석가입니다.
#     다음 텍스트를 '배경', '문제', '해결책', '실험', '결과', '영향'의 6가지 관점으로 분석하고 요약해주세요.
    
#     각 단계별 요약은 간결하고 명확해야 합니다.
    
#     <paper_text>
#     {text}
#     </paper_text>
    
#     아래 예시와 같이 JSON 형식으로만 응답을 생성해주세요.
#     응답 JSON에는 반드시 "paper_id"를 포함해야 합니다.
    
#     <예시 출력 형식>
#     {{"paper_id": {paper_id}, "title": "논문 스토리 요약 (Paper Story Summary)", "sections": [
#       {{"step": 1, "heading": "배경 (Background)", "content": "..."}},
#       {{"step": 2, "heading": "문제 (Problem)", "content": "..."}},
#       ...
#       {{"step": 6, "heading": "영향 (Impact)", "content": "..."}}
#     ]}}
#     """
    
#     # ChatPromptTemplate은 LLMChain에 적합한 형식의 프롬프트를 만듭니다.
#     prompt = ChatPromptTemplate.from_template(prompt_template)
    
#     # 체인을 구성합니다. 프롬프트 -> LLM -> 파서 순서로 실행됩니다.
#     chain = prompt | llm | parser
    
#     # 체인을 실행하고 결과를 반환합니다.
#     result = chain.invoke({"paper_id": paper_id, "text": full_paper_text})
    
#     return result