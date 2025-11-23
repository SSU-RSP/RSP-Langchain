# Rock-Scissors-Paper

논문을 요약하고 발표자료와 발표 대본을 자동 생성하는 프로젝트

## 프로젝트 구조

```
├── data/
│   ├── input/          # 원본 텍스트 파일 (.txt) 저장
│   └── output/         # 생성된 결과물 저장
│       ├── summary.txt     # 요약 결과물
│       ├── presentation.pptx   # PPT 결과물
│       └── script.txt      # 발표 대본 결과물
├── src/
│   ├── chains/         # LangChain의 핵심 로직 (체인)
│   │   ├── summarize_chain.py  # 1. 논문 요약 기능
│   │   ├── ppt_chain.py        # 2. 발표자료 변환 기능
│   │   └── script_chain.py     # 3. 발표 대본 생성 기능
│   ├── utils/          # 보조 기능
│   │   ├── ppt_generator.py    # 파이썬으로 실제 PPT 파일을 생성하는 코드
│   │   └── prompts.py          # Gemini에게 보낼 프롬프트 템플릿 모음
│   └── main.py         # 전체 프로세스를 실행하는 메인 파일
├── .env                # API 키 등 민감한 정보 저장
├── requirements.txt    # 프로젝트에 필요한 라이브러리 목록
└── README.md           # 프로젝트 설명서
```

## 기능

1. **논문 요약**: 입력된 논문 텍스트를 자동으로 요약
2. **발표자료 생성**: 요약된 내용을 바탕으로 PPT 파일 생성
3. **발표 대본 생성**: PPT 구조를 바탕으로 자연스러운 발표 스크립트 생성

## 사용 방법

1. `data/input/` 폴더에 논문 텍스트 파일 저장
2. `src/main.py` 실행
3. `data/output/` 폴더에서 생성된 결과물 확인
