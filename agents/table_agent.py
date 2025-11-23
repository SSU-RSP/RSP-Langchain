import pandas as pd
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
from typing import List

def process_table(content: str, paper_title: str, section_title: str, table_of_contents: str, tables: List[str]) -> str:
    """
    논문의 전체 맥락 속에서 여러 CSV 표 데이터(URL)를 분석하고 서식 없는 순수 텍스트로 설명하는 에이전트
    """
    print(f"🚀 표 분석 에이전트 호출됨 (순수 텍스트 요약)...")
    
    if not tables:
        return "분석할 표 데이터가 없습니다."

    all_results = []

    try:
        for i, csv_url in enumerate(tables):
            print(f"  -> {i+1}번째 표 분석 시작 (URL: {csv_url})...")
            
            try:
                df = pd.read_csv(csv_url)
            except Exception as e:
                all_results.append(f"[{i+1}번째 표 분석 실패]: URL에서 CSV 데이터를 읽는 중 오류 발생 - {e}")
                continue

            # [수정] 지시사항을 변경하고 '출력 형식' 섹션을 제거합니다.
            analysis_question = f"""
            **역할**: 당신은 논문에 포함된 복잡한 데이터 표(Table)를 구조적으로 분석하고, 그 의미를 명확하게 설명해주는 전문 데이터 분석가입니다.

            **논문 전체 구조 (목차)**:
            {table_of_contents}

            **분석 대상**:
            - 논문 제목: "{paper_title}"
            - 현재 섹션: "{section_title}"

            **지시**:
            위 '논문 전체 구조'와 아래 '섹션 본문'을 종합적으로 참고하여, 주어진 표(DataFrame)를 심층적으로 분석해주세요.
            별도의 제목이나 글머리 기호 같은 특정 서식은 사용하지 말고, 자연스러운 문단으로 나누어 설명글 형식으로 작성해야 합니다.
            표의 종류, 구조 설명, 논문 내 역할 및 해석, 그리고 독자가 얻어야 할 핵심 인사이트를 모두 포함하여 설명해주세요.
            서론이나 부연 설명 없이, 요청한 분석 내용으로 바로 시작하세요. 대답은 모두 한국어로 해주세요.

            **섹션 본문**:
            {content}
            """

            llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0)
            agent = create_pandas_dataframe_agent(
                llm,
                df,
                verbose=True,
                agent_executor_kwargs={"handle_parsing_errors": True}
            )
            result = agent.invoke(analysis_question)
            
            # verbose=True 로그와 실제 결과물을 분리하기 위해 output만 사용합니다.
            output = result.get("output", "분석 결과를 가져올 수 없습니다.").strip()
            all_results.append(f"### {i+1}번째 표 분석 결과\n\n" + output)

        return "\n\n---\n\n".join(all_results)

    except Exception as e:
        return f"표 분석 중 전체 프로세스에서 오류 발생: {e}"

# import pandas as pd
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
# from typing import List

# def process_table(content: str, paper_title: str, section_title: str, table_of_contents: str, tables: List[str]) -> str:
#     """
#     논문의 전체 맥락 속에서 여러 CSV 표 데이터(URL)를 분석하고 설명하는 에이전트
#     """
#     print(f"🚀 표 분석 에이전트 호출됨 (CSV URL {len(tables)}개 분석)...")
    
#     if not tables:
#         return "분석할 표 데이터가 없습니다."

#     all_results = [] # 각 표의 분석 결과를 저장할 리스트

#     try:
#         # 1. 입력받은 모든 CSV URL에 대해 순차적으로 분석을 수행합니다.
#         for i, csv_url in enumerate(tables):
#             print(f"  -> {i+1}번째 표 분석 시작 (URL: {csv_url})...")
            
#             # [수정] URL로부터 직접 Pandas DataFrame을 생성합니다.
#             try:
#                 df = pd.read_csv(csv_url)
#             except Exception as e:
#                 all_results.append(f"[{i+1}번째 표 분석 실패]: URL에서 CSV 데이터를 읽는 중 오류 발생 - {e}")
#                 continue

#             # 3. 논문의 전체 맥락을 담아 Pandas Agent에게 던질 질문(프롬프트)을 생성합니다.
#             analysis_question = f"""
#             **역할**: 당신은 논문에 포함된 복잡한 데이터 표(Table)를 구조적으로 분석하고, 그 의미를 명확하게 설명해주는 전문 데이터 분석가입니다.

#             **논문 전체 구조 (목차)**:
#             {table_of_contents}

#             **분석 대상**:
#             - 논문 제목: "{paper_title}"
#             - 현재 섹션: "{section_title}"

#             **지시**:
#             위 '논문 전체 구조'와 아래 '섹션 본문'을 종합적으로 참고하여, 주어진 표(DataFrame)를 심층적으로 분석해주세요.
#             아래 '출력 형식'에 맞춰 답변해주세요. 출력 형식 외의 다른 문장은 생성하지 마세요.

#             **섹션 본문**:
#             {content}

#             **출력 형식**:
#             - **[표의 종류]**: 이 표가 어떤 종류의 데이터를 담고 있는지 설명해주세요. (예: 모델 성능 비교표, Ablation Study 결과표 등)
#             - **[표의 구조 설명]**: 표의 행(row)과 열(column)이 각각 무엇을 나타내는지 설명해주세요.
#             - **[논문 내 역할 및 해석]**: 이 표가 '섹션 본문'의 주장을 어떻게 뒷받침하며, 논문 전체의 결론에 어떤 기여를 하는지 해석해주세요.
#             - **[핵심 인사이트]**: 독자가 이 표를 통해 얻어야 할 가장 중요한 정보나 결론은 무엇인지 설명해주세요.
#             """

#             llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0)
#             agent = create_pandas_dataframe_agent(
#                 llm,
#                 df,
#                 verbose=True,
#                 agent_executor_kwargs={"handle_parsing_errors": True}
#             )
#             result = agent.invoke(analysis_question)
            
#             all_results.append(f"### {i+1}번째 표 분석 결과\n\n" + result.get("output", "분석 결과를 가져올 수 없습니다."))

#         return "\n\n---\n\n".join(all_results)

#     except Exception as e:
#         return f"표 분석 중 전체 프로세스에서 오류 발생: {e}"

# import pandas as pd
# import io
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
# from typing import List

# def process_table(content: str, paper_title: str, section_title: str, table_of_contents: str, tables: List[str]) -> str:
#     """
#     논문의 전체 맥락 속에서 여러 CSV 표 데이터를 분석하고 설명하는 에이전트
#     """
#     print(f"🚀 표 분석 에이전트 호출됨 (CSV 데이터 {len(tables)}개 분석)...")
    
#     if not tables:
#         return "분석할 표 데이터가 없습니다."

#     all_results = [] # 각 표의 분석 결과를 저장할 리스트

#     try:
#         # 1. 입력받은 모든 CSV 데이터에 대해 순차적으로 분석을 수행합니다.
#         for i, csv_content in enumerate(tables):
#             print(f"  -> {i+1}번째 표 분석 시작...")
            
#             try:
#                 df = pd.read_csv(io.StringIO(csv_content))
#             except Exception as e:
#                 all_results.append(f"[{i+1}번째 표 분석 실패]: CSV 데이터를 읽는 중 오류 발생 - {e}")
#                 continue

#             # [수정] table_of_contents와 전체 content를 포함하도록 프롬프트를 강화합니다.
#             analysis_question = f"""
#             **역할**: 당신은 논문에 포함된 복잡한 데이터 표(Table)를 구조적으로 분석하고, 그 의미를 명확하게 설명해주는 전문 데이터 분석가입니다.

#             **논문 전체 구조 (목차)**:
#             {table_of_contents}

#             **분석 대상**:
#             - 논문 제목: "{paper_title}"
#             - 현재 섹션: "{section_title}"

#             **지시**:
#             위 '논문 전체 구조'와 아래 '섹션 본문'을 종합적으로 참고하여, 주어진 표(DataFrame)를 심층적으로 분석해주세요.
#             아래 '출력 형식'에 맞춰 답변해주세요. 출력 형식 외의 다른 문장은 생성하지 마세요.

#             **섹션 본문**:
#             {content}

#             **출력 형식**:
#             - **[표의 종류]**: 이 표가 어떤 종류의 데이터를 담고 있는지 설명해주세요. (예: 모델 성능 비교표, Ablation Study 결과표 등)
#             - **[표의 구조 설명]**: 표의 행(row)과 열(column)이 각각 무엇을 나타내는지 설명해주세요.
#             - **[논문 내 역할 및 해석]**: 이 표가 '섹션 본문'의 주장을 어떻게 뒷받침하며, 논문 전체의 결론에 어떤 기여를 하는지 해석해주세요.
#             - **[핵심 인사이트]**: 독자가 이 표를 통해 얻어야 할 가장 중요한 정보나 결론은 무엇인지 설명해주세요.
#             """

#             llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0)
#             agent = create_pandas_dataframe_agent(
#                 llm,
#                 df,
#                 verbose=True,
#                 agent_executor_kwargs={"handle_parsing_errors": True}
#             )
#             result = agent.invoke(analysis_question)
            
#             all_results.append(f"### {i+1}번째 표 분석 결과\n\n" + result.get("output", "분석 결과를 가져올 수 없습니다."))

#         return "\n\n---\n\n".join(all_results)

#     except Exception as e:
#         return f"표 분석 중 전체 프로세스에서 오류 발생: {e}"

# # import pandas as pd
# # import io
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# # from config import GOOGLE_API_KEY, GEMINI_PRO_MODEL

# # def process_table(df: pd.DataFrame, question: str) -> str:
# #     """표(DataFrame)와 텍스트를 함께 분석하는 에이전트 (기본 버전)"""
# #     print("🚀 표 분석 에이전트 호출됨...")
# #     llm = ChatGoogleGenerativeAI(model=GEMINI_PRO_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0)

# #     agent = create_pandas_dataframe_agent(
# #         llm,
# #         df,
# #         verbose=True,
# #         agent_executor_kwargs={"handle_parsing_errors": True} # 파싱 에러 처리
# #     )

# #     result = agent.invoke(question)
# #     return result.get("output", "분석 결과를 가져올 수 없습니다.")

# # def process_table_simple(csv_content: str, question: str) -> str:
# #     """CSV 문자열을 받아서 간단히 분석하는 함수"""
# #     try:
# #         df = pd.read_csv(io.StringIO(csv_content))
# #         return process_table(df, question)
# #     except Exception as e:
# #         return f"표 처리 중 오류: {e}"

# # def detect_table_type(df: pd.DataFrame, question: str = None) -> str:
# #     """표 타입 자동 감지 (단순 버전)"""

# #     columns = [col.lower() for col in df.columns]
# #     question_lower = question.lower() if question else ""

# #     combined_text = " ".join(columns) + " " + question_lower

# #     # 간단한 키워드 기반 분류
# #     if any(word in combined_text for word in ['accuracy', 'precision', 'f1', 'performance', '정확도']):
# #         return "performance_comparison"
# #     elif any(word in combined_text for word in ['ablation', 'component', 'contribution']):
# #         return "ablation_study"
# #     elif any(word in combined_text for word in ['baseline', 'comparison', 'vs']):
# #         return "baseline_comparison"
# #     elif any(word in combined_text for word in ['time', 'memory', 'speed', 'efficiency']):
# #         return "resource_analysis"
# #     else:
# #         return "general_analysis"

# # def get_table_type_guidance(table_type: str) -> str:
# #     """표 타입별 분석 지침 (단순 버전)"""

# #     guidance = {
# #         "performance_comparison": "각 모델의 성능을 비교하고, 가장 우수한 결과와 그 이유를 분석하세요.",
# #         "ablation_study": "각 구성요소가 전체 성능에 미치는 영향을 분석하고, 핵심 요소를 식별하세요.",
# #         "baseline_comparison": "제안 방법과 기존 방법들의 차이점을 명확히 하고, 개선점을 강조하세요.",
# #         "resource_analysis": "시간, 메모리, 계산 효율성을 종합적으로 평가하고 trade-off를 분석하세요.",
# #         "general_analysis": "표의 전체적인 패턴과 주요 인사이트를 도출하세요."
# #     }

# #     return guidance.get(table_type, guidance["general_analysis"])