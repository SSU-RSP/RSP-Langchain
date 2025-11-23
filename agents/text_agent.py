from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

def process_text(content: str, paper_title: str, section_title: str, table_of_contents: str) -> str:
    """텍스트를 전체 목차 구조의 맥락과 함께 분석하여, 서식 없는 순수 텍스트로 요약하는 에이전트"""
    print("🚀 텍스트 에이전트 호출됨 (순수 텍스트 요약)...")
    llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY)
    
    template = """
    **역할**: 당신은 복잡한 AI 논문의 전체 구조를 파악하고, 특정 부분의 역할을 명확하게 설명해주는 전문 분석가입니다.

    **논문 전체 구조 (목차)**:
    {table_of_contents}

    **분석 대상**:
    - 논문 제목: "{paper_title}"
    - 현재 섹션: "{section_title}"

    **지시**:
    위 '논문 전체 구조'와 아래 '텍스트 본문'을 참고하여, 이 섹션의 핵심적인 역할과 내용을 설명해주세요.
    별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 요약해주세요.
    핵심 내용은 한두 문장으로 간결하게 압축하고, 이 섹션이 논리의 흐름상 이전/이후 섹션과 어떻게 연결되는지를 포함해야 합니다.
    서론이나 부연 설명 없이, 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

    **텍스트 본문**:
    {text_content}
    """
    
    prompt = PromptTemplate.from_template(template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.invoke({
        "table_of_contents": table_of_contents,
        "paper_title": paper_title,
        "section_title": section_title,
        "text_content": content
    })
    return result.get("text", "결과를 가져올 수 없습니다.").strip()

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

# # 함수가 table_of_contents (목차)를 추가로 받도록 수정합니다.
# def process_text(content: str, paper_title: str, section_title: str, table_of_contents: str) -> str:
#     """텍스트를 전체 목차 구조의 맥락과 함께 분석하는 에이전트"""
#     print("🚀 텍스트 에이전트 호출됨 (전체 목차 구조 참조)...")
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY)
    
#     template = """
#     **역할**: 당신은 복잡한 AI 논문의 전체 구조를 파악하고, 특정 부분의 역할을 명확하게 설명해주는 전문 분석가입니다.

#     **논문 전체 구조 (목차)**:
#     {table_of_contents}

#     **분석 대상**:
#     - 논문 제목: "{paper_title}"
#     - 현재 섹션: "{section_title}"  <- 목차에서 이 부분에 해당합니다.

#     **지시**:
#     위 '논문 전체 구조'를 참고하여, '분석 대상'에 해당하는 섹션의 '텍스트 본문'을 요약해주세요.
#     이 섹션이 논문 전체의 논리적 흐름에 어떻게 기여하는지에 초점을 맞춰 설명해야 합니다. 출력 형식 외의 다른 문장은 생성하지 마세요.
    
#     **텍스트 본문**:
#     {text_content}
    
#     **출력 형식**:
#     - **[섹션의 역할 및 기여도]**: 이 섹션이 논문 전체 구조에서 차지하는 위치와 핵심적인 역할(예: 문제 제기, 제안 모델의 핵심 구조 설명 등)을 한 문장으로 설명해주세요.
#     - **[핵심 내용 요약]**: 위 역할을 수행하기 위해, 이 섹션에서 구체적으로 설명하는 주요 주장이나 정보를 글머리 기호(bullet point)로 요약해주세요.
#     - **[구조적 연결성]**: 이 섹션은 이전 섹션의 내용을 어떻게 이어받으며, 다음 섹션의 내용을 위해 무엇을 준비하는지 간략하게 설명해주세요.
#     """
    
#     prompt = PromptTemplate.from_template(template)
    
#     chain = LLMChain(llm=llm, prompt=prompt)
    
#     result = chain.invoke({
#         "table_of_contents": table_of_contents,
#         "paper_title": paper_title,
#         "section_title": section_title,
#         "text_content": content
#     })
#     return result.get("text", "결과를 가져올 수 없습니다.")