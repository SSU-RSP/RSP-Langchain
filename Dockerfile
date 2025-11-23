# 1. 베이스 이미지 선택 (파이썬 3.10)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 라이브러리 설치 (소스코드보다 먼저 복사하여 빌드 속도 향상)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 소스코드 전체 복사
COPY . .

# 5. 컨테이너가 8080 포트를 외부에 노출하도록 설정
EXPOSE 8080

# 6. 컨테이너가 시작될 때 실행할 명령어
# Gunicorn으로 Uvicorn 워커를 사용해 FastAPI 앱을 실행
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "serve:app", "--bind", "0.0.0.0:8080"]