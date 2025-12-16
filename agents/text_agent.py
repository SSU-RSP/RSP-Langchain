from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

def process_text(content: str, paper_title: str) -> str:
    """
    어떤 분야의 논문이든 전체 텍스트를 받아 핵심 논리와 결론을 
    하나의 완성된 글로 요약하는 범용 에이전트
    """
    print(f"🚀 텍스트 에이전트 호출됨 (논문 '{paper_title}' 전체 요약)...")
    
    llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY)
    
    # 수정된 프롬프트: 범용적인 학술 논문 구조(서론-본론-결론)에 맞춘 요약 요청
    template = """
    **역할**: 당신은 다양한 학문 분야의 논문을 깊이 있게 분석하고, 저자의 핵심 주장을 명확하게 정리하는 전문 학술 에디터입니다.

    **분석 대상**:
    - 논문 제목: "{paper_title}"

    **지시**:
    제공된 '논문 전체 텍스트'를 바탕으로 논문의 내용을 요약해주세요.
    이 논문은 AI/컴퓨터 분야일 수도 있고, 인문/사회/과학 등 다른 분야일 수도 있습니다. 
    따라서 특정 기술 용어에 집착하기보다는 **저자의 논리적 전개와 핵심 주장**을 파악하는 데 집중하세요.

    요약문은 다음 흐름이 자연스럽게 녹아든 **하나의 통합된 글(Narrative)**이어야 합니다:
    1. **연구의 배경 및 목적**: 저자가 이 글을 통해 해결하거나 규명하고자 하는 질문(또는 문제 의식)은 무엇인가?
    2. **연구 방법 및 전개**: 저자는 자신의 주장을 뒷받침하기 위해 어떤 방식(실험, 조사, 문헌 분석, 논리적 추론 등)을 사용했는가?
    3. **결론 및 시사점**: 연구의 결과 도출된 핵심 발견은 무엇이며, 이것이 학계나 사회에 주는 의미는 무엇인가?

    **형식 제약**:
    - 개조식(글머리 기호)이나 소제목을 사용하지 마세요.
    - 문단(Paragraph)으로 구분된 자연스러운 줄글 형식으로 작성하세요.
    - 서두(예: "이 요약은...")를 생략하고 바로 분석 내용으로 시작하세요.
    - 언어는 **한국어**로 작성해주세요.

    **논문 전체 텍스트**:
    {text_content}
    """
    
    prompt = PromptTemplate.from_template(template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # 입력값 구조: 제목과 전체 내용만 전달
    result = chain.invoke({
        "paper_title": paper_title,
        "text_content": content 
    })
    
    return result.get("text", "결과를 가져올 수 없습니다.").strip()

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

# def process_text(content: str, paper_title: str, section_title: str, table_of_contents: str) -> str:
#     """텍스트를 전체 목차 구조의 맥락과 함께 분석하여, 서식 없는 순수 텍스트로 요약하는 에이전트"""
#     print("🚀 텍스트 에이전트 호출됨 (순수 텍스트 요약)...")
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY)
    
#     template = """
#     **역할**: 당신은 복잡한 AI 논문의 전체 구조를 파악하고, 특정 부분의 역할을 명확하게 설명해주는 전문 분석가입니다.

#     **논문 전체 구조 (목차)**:
#     {table_of_contents}

#     **분석 대상**:
#     - 논문 제목: "{paper_title}"
#     - 현재 섹션: "{section_title}"

#     **지시**:
#     위 '논문 전체 구조'와 아래 '텍스트 본문'을 참고하여, 이 섹션의 핵심적인 역할과 내용을 설명해주세요.
#     별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 요약해주세요.
#     핵심 내용은 한두 문장으로 간결하게 압축하고, 이 섹션이 논리의 흐름상 이전/이후 섹션과 어떻게 연결되는지를 포함해야 합니다.
#     서론이나 부연 설명 없이, 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

#     **텍스트 본문**:
#     {text_content}
#     """
    
#     prompt = PromptTemplate.from_template(template)
    
#     chain = LLMChain(llm=llm, prompt=prompt)
    
#     result = chain.invoke({
#         "table_of_contents": table_of_contents,
#         "paper_title": paper_title,
#         "section_title": section_title,
#         "text_content": content
#     })
#     return result.get("text", "결과를 가져올 수 없습니다.").strip()