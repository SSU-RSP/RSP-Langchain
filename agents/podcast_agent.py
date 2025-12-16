from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

def process_podcast(content: str, title: str = "논문 내용") -> str:
    """
    텍스트를 받아서 팟캐스트 대본 형식으로 변환하는 에이전트
    
    Args:
        content: 변환할 텍스트 내용
        title: 팟캐스트 제목 (기본값: "논문 내용")
    
    Returns:
        팟캐스트 대본 형식의 문자열
    """
    print(f"🎙️ 팟캐스트 대본 생성 에이전트 호출됨 (제목: '{title}')...")
    
    llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY)
    
    template = """
    **역할**: 당신은 전문 팟캐스트 작가입니다. 제공된 텍스트를 자연스럽고 흥미로운 팟캐스트 대본으로 변환해주세요.

    **팟캐스트 제목**: "{title}"

    **지시**:
    아래 텍스트를 바탕으로 팟캐스트 대본을 작성해주세요. 대본은 다음과 같은 형식을 따라야 합니다:

    **대본 형식**:
    - 한 명의 발화자(호스트)가 자연스럽게 설명하는 형식
    - 발화자 표시나 역할 구분 없이 바로 대본 내용으로 시작
    - 자연스러운 말투 사용 (구어체)
    - 너무 길지 않게 적절히 문단으로 나누어 작성
    - 전문 용어는 쉽게 풀어서 설명
    - 청중에게 직접 말하는 것처럼 친근하고 자연스러운 톤
    - 적절한 어조 변화와 강조를 문장 구조로 표현

    **작성 가이드**:
    - 서두에 간단한 인사와 주제 소개 포함 (예: "안녕하세요, 오늘은...")
    - 본문은 핵심 내용을 자연스럽게 설명하는 형식
    - 마무리는 요약이나 마무리 멘트로 구성
    - 언어는 **한국어**로 작성
    - 불필요한 형식적 표현은 피하고 자연스러운 말하기 흐름 유지
    - TTS로 읽었을 때 자연스럽게 들리도록 작성

    **원본 텍스트**:
    {text_content}
    """
    
    prompt = PromptTemplate.from_template(template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.invoke({
        "title": title,
        "text_content": content
    })
    
    return result.get("text", "대본 생성에 실패했습니다.").strip()

