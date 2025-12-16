from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL
from typing import List, Dict


def process_vision(content: str, paper_title: str, images: List[str]) -> List[Dict[str, str]]:
    """
    논문의 전체 요약(content)을 배경지식으로 하여,
    표(Table), 그림(Figure), 수식(Equation)을 한 번에 시각적으로 분석하고 설명하는 에이전트
    """
    print(f"🚀 비전(그림/표/수식) 에이전트 호출됨 (총 {len(images)}개 이미지 분석 시작)...")

    results = []

    # Vision 모델 초기화
    try:
        llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"모델 초기화 실패: {e}")
        return []

    # 각 이미지 URL에 대해 순차적으로 분석 수행
    for image_url in images:
        try:
            # 프롬프트: 논문 전체 맥락에서 "표 vs 그림 vs 수식"을 먼저 구분한 뒤, 타입에 맞게 해석하도록 지시
            text_prompt = f"""
            **역할**: 당신은 논문에 포함된 표(Table), 그림(Figure), 그래프, 다이어그램, 수식(Equation) 등을 해석하여
            연구의 핵심 내용을 시각적으로 풀어 설명해주는 전문 연구 분석가입니다.

            **분석 배경**:
            - 논문 제목: "{paper_title}"
            - 논문 핵심 요약:
            {content}

            **1단계 – 타입 판별 (표인지, 그림/그래프/다이어그램인지, 수식인지):**
            먼저 제공된 이미지를 보고 이것이 **표(테이블)**, **일반 그림/그래프/다이어그램**, 또는 **수식(Equation)** 중 무엇인지 스스로 판단하세요.

            **2단계 – 타입에 따른 해석 방식:**
            - 만약 표(Table)라면:
              - 행(row)과 열(column)이 각각 무엇을 의미하는지 설명하세요.
              - 가장 중요한 수치나 패턴(최고/최저 값, 뚜렷한 증가·감소 등)을 짚어주세요.
              - 이 표가 논문에서 어떤 주장을 뒷받침하는지, 결과적으로 어떤 메시지를 주는지 설명하세요.
            
            - 만약 그림/그래프/다이어그램이라면:
              - 이것이 어떤 종류의 시각 자료인지 먼저 짧게 말하고 (예: 성능 비교 그래프, 모델 구조도 등),
              - 축, 축 레이블, 색/선/박스 등의 시각적 요소가 무엇을 의미하는지 설명하세요.
              - 이 그림이 논문의 어떤 아이디어나 결과를 강조하는지, 연구 흐름 속 역할을 설명하세요.
            
            - 만약 수식(Equation)이라면:
              - 이 수식이 논문 핵심 요약의 맥락에서 어떤 의미를 갖는지 설명해주세요.
              - 수식에 사용된 각 변수(기호)가 무엇을 의미하는지 논문 맥락을 근거로 설명해주세요.
              - 이 수식이 전체적으로 무엇을 계산하거나 무엇을 의미하는지 평이한 언어로 설명해주세요.
              - 이 수식의 결과나 의미가 논문의 결론에 어떤 영향을 미치는지 설명해주세요.
              - 단순히 수식 기호를 읽는 것이 아니라, 이 수식이 연구의 방법론이나 결과 입증 과정에서 **어떤 역할을 하는지** 해석해야 합니다.

            **작성 가이드**:
            - 표/그림/수식 구분 결과를 자연스럽게 문장 안에 녹여서 설명하되, 별도의 마크다운 목록은 쓰지 마세요.
            - 수치를 나열하기보다는, 독자가 이해해야 할 **핵심 의미와 인사이트** 위주로 설명하세요.
            - 서식 없는 자연스러운 문단 형태로 작성하고, 불필요한 서론 없이 바로 분석 내용으로 시작하세요.
            - 언어는 **한국어**입니다.
            """

            message_content = [
                {"type": "text", "text": text_prompt},
                {"type": "image_url", "image_url": image_url},
            ]

            message = HumanMessage(content=message_content)

            # API 호출
            response = llm.invoke([message])
            description = response.content.strip() if hasattr(response, "content") else "이미지 분석 결과를 가져올 수 없습니다."

            # 결과 리스트에 추가 (URL과 설명 매핑)
            results.append(
                {
                    "image_url": image_url,
                    "description": description,
                }
            )

        except Exception as e:
            print(f"이미지({image_url}) 분석 중 오류 발생: {e}")
            results.append(
                {
                    "image_url": image_url,
                    "description": "이미지 분석 중 오류가 발생했습니다.",
                }
            )

    return results

# from langchain_core.messages import HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from config import GOOGLE_API_KEY, GEMINI_PRO_VISION_MODEL
# from typing import List

# def process_vision(content: str, paper_title: str, section_title: str, table_of_contents: str, images: List[str]) -> str:
#     """
#     논문의 전체 맥락 속에서 여러 이미지 URL을 분석하고 서식 없는 순수 텍스트로 설명하는 에이전트
#     """
#     print(f"🚀 비전 에이전트 호출됨 (순수 텍스트 요약)...")
    
#     try:
#         llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_VISION_MODEL, google_api_key=GOOGLE_API_KEY)

#         # [수정] 지시사항을 변경하고 '출력 형식' 섹션을 제거합니다.
#         text_prompt = f"""
#         **역할**: 당신은 복잡한 논문에 포함된 그림(Figure), 그래프, 다이어그램 등을 명확하게 해석하고 그 의미를 설명해주는 전문 연구 분석가입니다.

#         **논문 전체 구조 (목차)**:
#         {table_of_contents}

#         **분석 대상**:
#         - 논문 제목: "{paper_title}"
#         - 현재 섹션: "{section_title}"
#         - 분석할 이미지: 지금부터 첨부되는 모든 이미지들

#         **지시**:
#         위 '논문 전체 구조'와 아래 '섹션 본문'을 종합적으로 참고하여, 첨부된 각 이미지에 대해 설명해주세요.
#         별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 작성해야 합니다.
#         각 이미지의 종류, 시각적 상세 설명, 논문 내 역할 및 해석, 그리고 독자가 얻어야 할 핵심 인사이트를 모두 포함하여 설명해주세요.
#         여러 이미지가 있다면 순서대로 분석하고, 서론이나 부연 설명 없이 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

#         **섹션 본문**:
#         {content}
#         """
        
#         message_content = [{"type": "text", "text": text_prompt}]

#         for image_url in images:
#             message_content.append({
#                 "type": "image_url",
#                 "image_url": image_url
#             })
        
#         if len(message_content) > 1:
#             message = HumanMessage(content=message_content)
#             response = llm.invoke([message])
#             return response.content.strip() if hasattr(response, 'content') else "이미지 분석 결과를 가져올 수 없습니다."
#         else:
#             return "분석할 이미지가 없습니다."

#     except Exception as e:
#         return f"이미지 분석 중 오류 발생: {e}"

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