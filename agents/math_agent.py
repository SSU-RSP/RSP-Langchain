from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL
from typing import List

def process_math(content: str, paper_title: str, section_title: str, table_of_contents: str, equations: List[str]) -> str:
    """
    논문의 전체 맥락 속에서 여러 수식 이미지(URL)를 분석하고 서식 없는 순수 텍스트로 설명하는 에이전트
    """
    print(f"🚀 수식 이미지 분석 에이전트 호출됨 (순수 텍스트 요약)...")
    
    try:
        llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)

        # [수정] 지시사항을 변경하고 '출력 형식' 섹션을 제거합니다.
        text_prompt = f"""
        **역할**: 당신은 복잡한 논문에 포함된 수식을 해당 분야의 전문가가 아닌 사람도 이해할 수 있도록 쉽게 풀어 설명하는 수석 연구원입니다.

        **논문 전체 구조 (목차)**:
        {table_of_contents}

        **분석 대상**:
        - 논문 제목: "{paper_title}"
        - 현재 섹션: "{section_title}"
        - 분석할 수식: 지금부터 첨부되는 이미지에 포함된 모든 수식들

        **지시**:
        위 '논문 전체 구조'와 아래의 '섹션 본문'을 종합적으로 참고하여, 첨부된 각 이미지 속 수식에 대해 설명해주세요.
        별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 작성해야 합니다.
        각 수식의 역할, 변수 설명, 수식의 의미, 그리고 논문 내 중요성을 모두 포함하여 설명해주세요.
        여러 개의 수식이 있다면 순서대로 분석하고, 서론이나 부연 설명 없이 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

        **섹션 본문**:
        {content}
        """
        
        message_content = [{"type": "text", "text": text_prompt}]

        for image_url in equations:
            message_content.append({
                "type": "image_url",
                "image_url": image_url
            })
            
        if len(message_content) > 1:
            message = HumanMessage(content=message_content)
            response = llm.invoke([message])
            return response.content.strip() if hasattr(response, 'content') else "수식 이미지 분석 결과를 가져올 수 없습니다."
        else:
            return "분석할 수식 이미지가 없습니다."

    except Exception as e:
        return f"수식 이미지 분석 중 오류 발생: {e}"
    
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL # Vision 모델을 사용하도록 변경
# from typing import List

# # 함수가 formula: str 대신 equations: List[str] (URL 리스트)를 받도록 수정합니다.
# def process_math(content: str, paper_title: str, section_title: str, table_of_contents: str, equations: List[str]) -> str:
#     """논문의 전체 맥락 속에서 여러 수식 이미지(URL)를 분석하고 설명하는 에이전트"""
#     print(f"🚀 수식 이미지 분석 에이전트 호출됨 (이미지 {len(equations)}개)...")
    
#     # 1. 텍스트가 아닌 이미지를 분석하기 위해 Vision 모델을 초기화합니다.
#     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)
    
#     # 2. 텍스트 지시사항과 이미지 URL들을 함께 담을 메시지 내용을 구성합니다.
    
#     # 먼저 텍스트로 된 지시사항과 논문 컨텍스트를 정의합니다.
#     text_prompt = f"""
#     **역할**: 당신은 복잡한 논문에 포함된 수식을 해당 분야의 전문가가 아닌 사람도 이해할 수 있도록 쉽게 풀어 설명하는 수석 연구원입니다.

#     **논문 전체 구조 (목차)**:
#     {table_of_contents}

#     **분석 대상**:
#     - 논문 제목: "{paper_title}"
#     - 현재 섹션: "{section_title}"
#     - 분석할 수식: 지금부터 첨부되는 이미지에 포함된 모든 수식들

#     **지시**:
#     위 '논문 전체 구조'와 아래의 '섹션 본문'을 종합적으로 참고하여, 지금부터 제공되는 각 이미지 속 수식에 대해 아래 '출력 형식'에 맞춰 상세하고 명확하게 설명해주세요. 여러 개의 수식이 있다면 순서대로 모두 분석한 결과를 하나의 답변으로 통합해주세요. 출력 형식 외의 다른 문장은 생성하지 마세요.

#     **섹션 본문**:
#     {content}
    
#     **출력 형식**:
#     - **[수식의 역할]**: 이 수식이 현재 섹션과 논문 전체에서 어떤 핵심적인 역할을 하는지 설명해주세요.
#     - **[변수 설명]**: 수식에 사용된 각 변수(기호)가 무엇을 의미하는지 '섹션 본문'을 근거로 설명해주세요.
#     - **[수식의 의미]**: 이 수식이 전체적으로 무엇을 계산하거나 무엇을 의미하는지 평이한 언어로 설명해주세요.
#     - **[논문 내 중요성]**: 이 수식의 결과나 의미가 논문의 결론에 어떤 영향을 미치는지 설명해주세요.
#     """
    
#     # 전체 메시지를 담을 리스트를 생성하고, 첫 번째 요소로 텍스트 프롬프트를 추가합니다.
#     message_content = [{"type": "text", "text": text_prompt}]

#     # 입력받은 모든 이미지 URL을 메시지 리스트에 추가합니다.
#     for image_url in equations:
#         message_content.append({
#             "type": "image_url",
#             "image_url": image_url
#         })
        
#     # 3. 최종적으로 HumanMessage 객체를 만들어 모델을 호출합니다.
#     message = HumanMessage(content=message_content)
    
#     response = llm.invoke([message])
    
#     return response.content if hasattr(response, 'content') else "수식 이미지 분석 결과를 가져올 수 없습니다."