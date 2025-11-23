# test_connection.py

import config  # 우리가 만든 config.py 파일을 불러옵니다.
from langchain_google_genai import ChatGoogleGenerativeAI

print("Gemini API 연결 테스트를 시작합니다...")

try:
    # 1. config 파일에 설정된 모델과 API 키로 LLM을 초기화합니다.
    llm = ChatGoogleGenerativeAI(
        model=config.GEMINI_PRO_MODEL,
        google_api_key=config.GOOGLE_API_KEY
    )

    # 2. LLM에게 간단한 질문을 던져봅니다.
    print("Gemini 모델에 질문을 전송합니다...")
    response = llm.invoke("Hello, Gemini! 한국어로 인사해줘. 오늘 기분은 어때?")

    # 3. 성공적으로 답변을 받았는지 출력합니다.
    print("✅ 연결 성공!")
    print(f"🤖 Gemini 응답: {response.content}")

except Exception as e:
    # 연결 과정에서 문제가 생기면 에러 메시지를 출력합니다.
    print(f"❌ 연결 실패: {e}")
    print("API 키가 .env 파일에 정확히 설정되었는지 확인해주세요.")