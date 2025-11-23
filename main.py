import requests
import json

def test_api():
    """
    배포된 API 서버에 테스트 요청을 보내는 클라이언트 스크립트
    """
    print("--- API 서버 테스트 시작 ---")

    # [수정] 1. API 서버의 주소를 배포된 Cloud Run 서비스 URL로 변경합니다.
    # 예시: url = "https://paper-analyzer-service-xxxxxxxxxx-an.a.run.app/summarize-section"
    url = "YOUR_DEPLOYED_CLOUD_RUN_SERVICE_URL/summarize-section"

    # 2. 서버에 보낼 테스트 데이터 (JSON) - 변경 없음
    test_payload = {
        "section_id": 1,
        "table_of_contents": "1. 서론\n2. KcBERT 모델 학습\n3. 결론",
        "paper_title": "KCBERT: 한국어 댓글로 학습한 BERT",
        "section_title": "1. 서론",
        "text": "최근 NLP 연구에서는 ... (서론 본문 생략)",
        "images": [
            "https://i.imgur.com/FS75b9z.png" # 예시 이미지 URL
        ],
        "tables": [
            "Model,Accuracy,Parameters\nModel A,85.2,110M\nModel B,92.1,340M" # 예시 CSV 데이터
        ],
        "equations": [
            "https://i.imgur.com/2A2d2e2.png" # 예시 수식 이미지 URL
        ]
    }

    # 3. 요청 및 결과 확인 로직 - 변경 없음
    try:
        response = requests.post(url, json=test_payload)
        response.raise_for_status()

        print("\n✅ 요청 성공!")
        print(f"상태 코드: {response.status_code}")
        
        pretty_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
        print("\n👉 서버 응답:")
        print(pretty_response)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 요청 실패: {e}")
        print(f"API 서버 주소가 정확한지 확인해주세요: {url}")
        
    print("\n--- API 서버 테스트 종료 ---")


if __name__ == "__main__":
    test_api()

# from processor import route_and_process
# from agents import process_story

# def main():
#     print("--- 멀티에이전트 시스템 데모 시작 ---")

#     # 1. 텍스트 에이전트 테스트
#     # [수정] 1. 텍스트 에이전트 테스트 (목차 정보 추가)
#     print("\n[1. 텍스트 에이전트 테스트]")
    
#     # 논문 목차 예시 (문자열 형식)
#     sample_toc = """
#     1. Introduction
#     2. Background
#     3. Model Architecture
#        3.1 Encoder and Decoder Stacks
#        3.2 Attention
#        3.3 Position-wise Feed-Forward Networks
#     4. Why Self-Attention
#     5. Training
#     6. Results
#     7. Conclusion
#     """
    
#     text_data = {
#         "type": "text",
#         "paper_title": "Attention Is All You Need",
#         "section_title": "3. Model Architecture",
#         "table_of_contents": sample_toc,
#         "content": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
#     }
#     result_1 = route_and_process(text_data)
#     print(f"\n👉 결과:\n{result_1}")

#     # 2. 수식 에이전트 테스트
#     print("\n[2. 수식 에이전트 테스트]")
#     math_data = {
#         "type": "text_with_math",
#         "question": "논문에 따르면 원의 반지름이 5일 때 원의 넓이는 얼마인가? (원의 넓이 = pi * r^2)"
#     }
#     result_2 = route_and_process(math_data)
#     print(f"\n👉 결과:\n{result_2}")

#     # 3. 비전 에이전트 테스트
#     print("\n[3. 비전 에이전트 테스트]")
#     # data 폴더에 'sample_figure_image.jpg' 파일을 넣어주세요.
#     vision_data = {
#         "type": "text_with_image",
#         "text_prompt": "이 이미지는 무엇을 나타내는 그래프인가요? x축과 y축은 무엇을 의미하는지 설명해주세요.",
#         "image_path": "data/sample_figure_image.jpg"
#     }
#     result_3 = route_and_process(vision_data)
#     print(f"\n👉 결과:\n{result_3}")
    
#     # 4. 표 분석 에이전트 테스트
#     print("\n[4. 표 분석 에이전트 테스트]")
#     # data 폴더에 아래 내용의 'sample_figure_table.csv' 파일을 생성해주세요.
#     # Model,Accuracy,Parameters
#     # Model A,85.2,110M
#     # Model B,92.1,340M
#     # Model C,89.5,250M
#     table_data = {
#         "type": "text_with_table",
#         "question": "정확도(Accuracy)가 가장 높은 모델은 무엇이고, 그 모델의 파라미터(Parameters) 수는 얼마인가요?",
#         "table_path": "data/sample_figure_table.csv"
#     }
#     result_4 = route_and_process(table_data)
#     print(f"\n👉 결과:\n{result_4}")

#     # 5. 스토리텔링 에이전트 테스트
#     print("\n[5. 스토리텔링 에이전트 테스트]")
#     test_paper_text = """
#     2018년, AI와 CS 분야의 연구자들은 기존 방법의 한계에 부딪혔고, 더 나은 성능과 효율성을 위한 새로운 돌파구가 필요했습니다. 
#     특히 정확도와 성능이 부족하다는 문제가 해결되지 않고 있었으며, 기존 접근법들은 속도나 정확도 면에서 만족스럽지 못했습니다. 
#     이에 Jacob Devlin 등의 연구팀은 어텐션 메커니즘을 활용한 새로운 모델을 제안했습니다. 
#     이 아이디어는 기존과는 완전히 다른 혁신적인 접근법이었습니다. 
#     연구팀은 4가지 실험을 통해 이 아이디어를 검증했습니다. 
#     2개의 핵심 수식으로 이론적 기반을 마련했고, 다양한 데이터셋에서 성능을 테스트했습니다. 
#     실험 결과는 놀라웠습니다. 특정 영역에서 의미 있는 성능 개선을 이뤄내 해당 분야에 중요한 진전을 가져왔습니다. 
#     이 연구는 AI 연구자, 소프트웨어 개발자 등에게 직접적인 영향을 미칠 것으로 예상됩니다. 
#     특정 영역의 성능 향상에 기여할 핵심 기술로 자리 잡을 것입니다.
#     """
    
#     try:
#         story_result = process_story(paper_id=1, full_paper_text=test_paper_text)
#         print(f"\n👉 결과:\n{story_result}")
#     except Exception as e:
#         print(f"\n👉 오류: {e}")

#     print("\n--- 모든 데모 종료 ---")

# if __name__ == "__main__":
#     main()