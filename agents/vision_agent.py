from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL
from typing import List

def process_vision(content: str, paper_title: str, section_title: str, table_of_contents: str, images: List[str]) -> str:
    """
    논문의 전체 맥락 속에서 여러 이미지 URL을 분석하고 서식 없는 순수 텍스트로 설명하는 에이전트
    """
    print(f"🚀 비전 에이전트 호출됨 (순수 텍스트 요약)...")
    
    try:
        llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)

        # [수정] 지시사항을 변경하고 '출력 형식' 섹션을 제거합니다.
        text_prompt = f"""
        **역할**: 당신은 복잡한 논문에 포함된 그림(Figure), 그래프, 다이어그램 등을 명확하게 해석하고 그 의미를 설명해주는 전문 연구 분석가입니다.

        **논문 전체 구조 (목차)**:
        {table_of_contents}

        **분석 대상**:
        - 논문 제목: "{paper_title}"
        - 현재 섹션: "{section_title}"
        - 분석할 이미지: 지금부터 첨부되는 모든 이미지들

        **지시**:
        위 '논문 전체 구조'와 아래 '섹션 본문'을 종합적으로 참고하여, 첨부된 각 이미지에 대해 설명해주세요.
        별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 작성해야 합니다.
        각 이미지의 종류, 시각적 상세 설명, 논문 내 역할 및 해석, 그리고 독자가 얻어야 할 핵심 인사이트를 모두 포함하여 설명해주세요.
        여러 이미지가 있다면 순서대로 분석하고, 서론이나 부연 설명 없이 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

        **섹션 본문**:
        {content}
        """
        
        message_content = [{"type": "text", "text": text_prompt}]

        for image_url in images:
            message_content.append({
                "type": "image_url",
                "image_url": image_url
            })
        
        if len(message_content) > 1:
            message = HumanMessage(content=message_content)
            response = llm.invoke([message])
            return response.content.strip() if hasattr(response, 'content') else "이미지 분석 결과를 가져올 수 없습니다."
        else:
            return "분석할 이미지가 없습니다."

    except Exception as e:
        return f"이미지 분석 중 오류 발생: {e}"

# from langchain_core.messages import HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL
# from typing import List

# def process_vision(content: str, paper_title: str, section_title: str, table_of_contents: str, images: List[str]) -> str:
#     """
#     논문의 전체 맥락 속에서 여러 이미지 URL을 분석하고 설명하는 에이전트
#     """
#     print(f"🚀 비전 에이전트 호출됨 (이미지 URL {len(images)}개 분석)...")
    
#     try:
#         llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)

#         # 이미지(Figure) 분석에 특화된 프롬프트 템플릿
#         text_prompt = f"""
#         **역할**: 당신은 복잡한 논문에 포함된 그림(Figure), 그래프, 다이어그램 등을 명확하게 해석하고 그 의미를 설명해주는 전문 연구 분석가입니다.

#         **논문 전체 구조 (목차)**:
#         {table_of_contents}

#         **분석 대상**:
#         - 논문 제목: "{paper_title}"
#         - 현재 섹션: "{section_title}"
#         - 분석할 이미지: 지금부터 첨부되는 모든 이미지들

#         **지시**:
#         위 '논문 전체 구조'와 아래의 '섹션 본문'을 종합적으로 참고하여, 지금부터 제공되는 각 이미지에 대해 아래 '출력 형식'에 맞춰 상세하고 명확하게 설명해주세요. 여러 개의 이미지가 있다면 순서대로 모두 분석한 결과를 하나의 답변으로 통합해주세요. 출력 형식 외의 다른 문장은 생성하지 마세요.

#         **섹션 본문**:
#         {content}
        
#         **출력 형식**:
#         - **[이미지 종류]**: 해당 이미지가 어떤 종류인지 설명해주세요. (예: 막대그래프, 순서도, 모델 아키텍처 다이어그램 등)
#         - **[이미지 상세 설명]**: 이미지가 시각적으로 무엇을 보여주는지 객관적으로 설명해주세요. (예: x축은 시간을, y축은 정확도를 나타내며, 파란색 선은 A 모델의 성능을 보여줌)
#         - **[논문 내 역할 및 해석]**: 이 이미지가 '섹션 본문'의 내용을 어떻게 뒷받침하며, 논문의 주장을 증명하는 데 어떤 역할을 하는지 해석해주세요.
#         - **[핵심 인사이트]**: 독자가 이 이미지를 통해 얻어야 할 가장 중요한 정보나 결론은 무엇인지 설명해주세요.
#         """
        
#         message_content = [{"type": "text", "text": text_prompt}]

#         # [수정] 입력받은 모든 이미지 URL을 메시지 리스트에 바로 추가합니다.
#         for image_url in images:
#             message_content.append({
#                 "type": "image_url",
#                 "image_url": image_url
#             })
        
#         # 이미지가 하나 이상 첨부된 경우에만 모델을 호출합니다.
#         if len(message_content) > 1:
#             message = HumanMessage(content=message_content)
#             response = llm.invoke([message])
#             return response.content if hasattr(response, 'content') else "이미지 분석 결과를 가져올 수 없습니다."
#         else:
#             return "분석할 이미지가 없습니다."

#     except Exception as e:
#         return f"이미지 분석 중 오류 발생: {e}"