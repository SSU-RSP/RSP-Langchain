# summarize_paper.py

from processor import route_and_process

def summarize_kcbert_introduction():
    """KCBERT 논문의 '서론' 섹션을 요약하는 기능만 독립적으로 테스트합니다."""
    
    print("🚀 KcBERT 논문 '서론' 섹션 요약 테스트를 시작합니다...")
    
    # 1. 논문 목차 정보 정의
    kcbert_toc = """
    1. 서론
    2. 기존 연구
        2.1 한국어 BERT 공개 모델
        2.2 한국어 Transformer 계열 공개 모델
    3. KCBERT 모델 학습
        3.1 데이터셋
        3.2 학습 텍스트 정제
        3.3 WordPiece 토크나이저 학습
        3.4 학습 설정 및 환경
        3.5 학습 결과 및 체크포인트
    4. 한국어 Transformers 계열 모델 간 성능 비교
    5. 결론
    """
    
    # 2. '1. [cite_start]서론' 섹션의 전체 텍스트 내용 [cite: 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    kcbert_introduction_content = """
    최근 NLP 연구에서는 큰 분량의 레이블 되지 않은 말뭉치를 통해 언어 모델을 학습하고, 이러한 사전 학습(Pretraining)을 거친 모델을 대상 데이터셋에 대해 전이 학습(Transfer learning, Fine tune)을 통해 높은 성능을 성취한다. 대표적인 모델로 구글에서 공개한 BERT(Bidirectional Encoder Representations from Transformers) [1]가 있으며, 이러한 Transformers [2]를 사용한 전이 학습 언어 모델들이 등장하고 있다. 한편, 이 러한 연구는 언어 모델을 학습하기 위해 사용한 데이터셋에 종속적이다. [3] 구글 등에서 공개한 다국어 모델은 학습 데이 터셋의 특성상 한국어의 비중이 낮다. 이로인해 토크나이저 에서 글자 대부분이 음소 단위로 잘리는 등 한국어에 적합하 지 않은 특성을 보이기도 한다. 따라서 한국어 말뭉치만으로 학습한 한국어 대형 언어 모델의 중요성이 대두되어, ETRI, SKT, TwoBlockAI, 서울대 등에서 KorBERT[4], KOBERT [5], HanBERT[6], KR-BERT [7] 등 다양한 한국어 BERT 모델을 공개했다. 하지만 현재 공개된 한국어 BERT 모델들은 대부 분 한국어 위키피디아를 포함해 책과 온라인 뉴스 등 문어체 데이터를 기반으로 학습한 모델이다. 따라서 일반 사용자들이 작성하는 구어체, 오타와 신조어 등에 대해 모델이 상대적으 로 대응하기 어려운 경우가 있다. 또한, 현재 공개된 대부분의 모델이 BERT Base 모델이며, Large 모델은 대부분 공개되지 않았다. 본 연구에서는 이를 해결하기 위해 한국어 댓글 데이터를 기반으로 학습한 KCBERT와 토크나이저를 개발하였다. 학습 데이터로 2019년 1월 1일부터 2020년 06월 11일 자까지 네이버 뉴스 내 댓글 약 1억 1천만개를 수집하였다. 해당 데이터에 최소 한의 전처리를 진행한 뒤 Huggingface의 BERT WordPiece 토 크나이저 [8]를 학습하였고, BERT Base, Large 모델의 학습을 진행해 Huggingface의 Transformers[9] 허브에 오픈소스로 공 개 12하였다. 또한, 학습에 진행한 데이터셋을 캐글과 깃험'에 공개하였다.
    """

    # 3. 에이전트에 전달할 데이터 구성
    text_data = {
        "type": "text",
        "paper_title": "KCBERT: 한국어 댓글로 학습한 BERT",
        "section_title": "1. 서론",
        "table_of_contents": kcbert_toc,
        "content": kcbert_introduction_content
    }
    
    # 4. 라우터를 통해 텍스트 에이전트 호출 및 결과 출력
    result = route_and_process(text_data)
    print("\n--- 요약 결과 ---")
    print(result)
    print("\n--- 테스트 종료 ---")

# 이 파일을 직접 실행할 때만 summarize_kcbert_introduction 함수가 호출되도록 설정
if __name__ == "__main__":
    summarize_kcbert_introduction()