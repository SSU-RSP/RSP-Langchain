import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# Gemini API 키를 가져옵니다.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")

# 사용할 모델 이름 설정
GEMINI_PRO_MODEL = "gemini-2.0-flash" 
GEMINI_PRO_VISION_MODEL = "gemini-2.0-flash"