import asyncio
from typing import List
# schemas에서 새로 정의한 모델들을 가져옵니다.
from schemas import (
    TextAnalysisRequest, TextAnalysisResponse,
    VisionAnalysisRequest, VisionAnalysisResponse,
    TableAnalysisRequest, TableAnalysisResponse,
    MathAnalysisRequest, MathAnalysisResponse,
    AnalysisResultItem
)
# agents에서 각 처리 함수를 가져옵니다.
from agents import process_text, process_vision, process_math, process_table

# 1. 텍스트 분석 프로세서
async def analyze_text_only(request: TextAnalysisRequest) -> TextAnalysisResponse:
    print(f"📄 텍스트 분석 요청: {request.paper_title}")
    result_text = await asyncio.to_thread(
        process_text,
        content=request.text,
        paper_title=request.paper_title
    )
    return TextAnalysisResponse(result=result_text)

# 2. 비전(그림) 분석 프로세서
async def analyze_vision_only(request: VisionAnalysisRequest) -> VisionAnalysisResponse:
    print(f"🖼️ 비전 분석 요청: {len(request.images)}장")
    if not request.images:
        return VisionAnalysisResponse(results=[])
    
    # agents.process_vision은 List[Dict]를 반환하므로 이를 스키마에 맞게 변환
    raw_results = await asyncio.to_thread(
        process_vision,
        content=request.text,
        paper_title=request.paper_title,
        images=request.images
    )
    
    # Dict -> Pydantic Model 변환
    formatted_results = [AnalysisResultItem(**item) for item in raw_results]
    return VisionAnalysisResponse(results=formatted_results)

# 3. 표 분석 프로세서
async def analyze_table_only(request: TableAnalysisRequest) -> TableAnalysisResponse:
    print(f"📊 표 분석 요청: {len(request.tables)}개")
    if not request.tables:
        return TableAnalysisResponse(results=[])

    raw_results = await asyncio.to_thread(
        process_table,
        content=request.text,
        paper_title=request.paper_title,
        tables=request.tables
    )
    
    formatted_results = [AnalysisResultItem(**item) for item in raw_results]
    return TableAnalysisResponse(results=formatted_results)

# 4. 수식 분석 프로세서
async def analyze_math_only(request: MathAnalysisRequest) -> MathAnalysisResponse:
    print(f"➗ 수식 분석 요청: {len(request.equations)}개")
    if not request.equations:
        return MathAnalysisResponse(results=[])

    raw_results = await asyncio.to_thread(
        process_math,
        content=request.text,
        paper_title=request.paper_title,
        equations=request.equations
    )
    
    formatted_results = [AnalysisResultItem(**item) for item in raw_results]
    return MathAnalysisResponse(results=formatted_results)

# import asyncio
# from schemas import AnalysisRequest, AnalysisResponse, SectionAnalysisResult
# # [주의] process_text 등은 이제 processor.py와 같은 폴더의 agents.py에 있다고 가정합니다.
# from agents import process_text, process_vision, process_math, process_table
# from typing import List

# async def analyze_section(request: AnalysisRequest) -> AnalysisResponse:
#     """
#     API 요청을 받아 각 데이터 유형에 맞는 에이전트를 '동시에' 호출하고 결과를 종합합니다.
#     """
#     tasks = []

#     # 1. 텍스트 분석 (전체 요약)
#     # process_text(content: str, paper_title: str) -> str
#     if request.text:
#         tasks.append(
#             asyncio.to_thread(
#                 process_text,
#                 content=request.text,
#                 paper_title=request.paper_title
#                 # section_title, table_of_contents 인자 제거됨
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=None))

#     # 2. 이미지(Vision) 분석
#     # process_vision(content, paper_title, images) -> List[Dict]
#     if request.images:
#         tasks.append(
#             asyncio.to_thread(
#                 process_vision,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 images=request.images
#                 # section_title, table_of_contents 인자 제거됨
#             )
#         )
#     else:
#         # 빈 리스트 반환하도록 설정 (스키마에 맞춤)
#         tasks.append(asyncio.sleep(0, result=[]))

#     # 3. 표(Table) 분석
#     # process_table(content, paper_title, tables) -> List[Dict]
#     if request.tables:
#         tasks.append(
#             asyncio.to_thread(
#                 process_table,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 tables=request.tables
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=[]))
        
#     # 4. 수식(Math) 분석
#     # process_math(content, paper_title, equations) -> List[Dict]
#     if request.equations:
#         tasks.append(
#             asyncio.to_thread(
#                 process_math,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 equations=request.equations
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=[]))

#     # --- 실행 및 결과 수집 ---
#     print(f"총 {len(tasks)}개의 분석 작업을 동시에 시작합니다...")
#     results = await asyncio.gather(*tasks)
#     print("모든 분석 작업 완료.")

#     # results[0]: str (텍스트 요약)
#     # results[1]: List[Dict] (이미지)
#     # results[2]: List[Dict] (표)
#     # results[3]: List[Dict] (수식)

#     response = AnalysisResponse(
#         text_result=results[0],
#         image_results=results[1] if results[1] else [],
#         table_results=results[2] if results[2] else [],
#         equation_results=results[3] if results[3] else []
#     )
    
#     return response

# async def analyze_sections_in_batch(requests: List[AnalysisRequest]) -> List[SectionAnalysisResult]:
#     """
#     여러 섹션 요청을 리스트로 받아, 병렬로 처리하고 결과 리스트를 반환합니다.
#     """
#     if not requests:
#         return []

#     # 각 요청에 대해 analyze_section 호출
#     batch_tasks = [analyze_section(req) for req in requests]
    
#     print(f"총 {len(requests)}개 요청의 동시 분석을 시작합니다...")
#     batch_results = await asyncio.gather(*batch_tasks)
#     print("모든 배치 분석 완료.")

#     final_response = []
#     for request, result in zip(requests, batch_results):
#         final_response.append(
#             SectionAnalysisResult(
#                 section_id=request.section_id,
#                 text_result=result.text_result,
#                 image_results=result.image_results,
#                 table_results=result.table_results,
#                 equation_results=result.equation_results
#             )
#         )
        
#     return final_response

# processor.py

# import asyncio
# from schemas import AnalysisRequest, AnalysisResponse, SectionAnalysisResult
# from agents import process_text, process_vision, process_math, process_table
# from typing import List

# async def analyze_section(request: AnalysisRequest) -> AnalysisResponse:
#     """
#     API 요청을 받아 각 데이터 유형에 맞는 에이전트를 '동시에' 호출하고 결과를 종합합니다.
#     """
#     tasks = []

#     # 1. 각 데이터 유형에 맞는 에이전트 호출을 '작업'으로 추가합니다.
#     if request.text:
#         tasks.append(
#             asyncio.to_thread(
#                 process_text,
#                 content=request.text,
#                 paper_title=request.paper_title,
#                 section_title=request.section_title,
#                 table_of_contents=request.table_of_contents
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=None))

#     if request.images:
#         tasks.append(
#             asyncio.to_thread(
#                 process_vision,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 section_title=request.section_title,
#                 table_of_contents=request.table_of_contents,
#                 images=request.images
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=None))

#     if request.tables:
#         tasks.append(
#             asyncio.to_thread(
#                 process_table,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 section_title=request.section_title,
#                 table_of_contents=request.table_of_contents,
#                 tables=request.tables
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=None))
        
#     if request.equations:
#         tasks.append(
#             asyncio.to_thread(
#                 process_math,
#                 content=request.text or "",
#                 paper_title=request.paper_title,
#                 section_title=request.section_title,
#                 table_of_contents=request.table_of_contents,
#                 equations=request.equations
#             )
#         )
#     else:
#         tasks.append(asyncio.sleep(0, result=None))

#     # 2. 모든 작업을 동시에 실행하고 결과를 기다립니다.
#     print(f"총 {len(tasks)}개의 분석 작업을 동시에 시작합니다...")
#     results = await asyncio.gather(*tasks)
#     print("모든 분석 작업 완료.")

#     # 3. 각 작업의 결과를 응답 객체에 담아 반환합니다.
#     # [수정] 이제 results의 각 요소는 단일 문자열이므로 그대로 할당합니다.
#     response = AnalysisResponse(
#         text_result=results[0],
#         image_results=results[1],
#         table_results=results[2],
#         equation_results=results[3]
#     )
    
#     return response

# async def analyze_sections_in_batch(requests: List[AnalysisRequest]) -> List[SectionAnalysisResult]:
#     """
#     여러 섹션 요청을 리스트로 받아, 병렬로 처리하고 결과 리스트를 반환합니다.
#     """
#     if not requests:
#         return []

#     # 각 섹션에 대한 분석 작업을 비동기 태스크 리스트로 만듭니다.
#     batch_tasks = [analyze_section(req) for req in requests]
    
#     # asyncio.gather를 사용해 모든 섹션 분석을 동시에 실행합니다.
#     print(f"총 {len(requests)}개 섹션의 동시 분석을 시작합니다...")
#     batch_results = await asyncio.gather(*batch_tasks)
#     print("모든 섹션 분석 완료.")

#     # 최종 응답 형식에 맞게 결과를 정리합니다.
#     final_response = []
#     for request, result in zip(requests, batch_results):
#         final_response.append(
#             SectionAnalysisResult(
#                 section_id=request.section_id,
#                 text_result=result.text_result,
#                 image_results=result.image_results,
#                 table_results=result.table_results,
#                 equation_results=result.equation_results
#             )
#         )
        
#     return final_response

# import pandas as pd
# import io
# from agents import process_text, process_math, process_vision, process_table

# # ================== 기존 코드==================
# def route_and_process(data: dict):
#     """입력 데이터의 유형에 따라 적절한 에이전트로 라우팅합니다. (기존 버전)"""
    
#     input_type = data.get("type")
    
#     if input_type == "text":
#         return process_text(
#             content=data["content"],
#             paper_title=data["paper_title"],
#             section_title=data["section_title"],
#             table_of_contents=data["table_of_contents"]
#         )
        
#     elif input_type == "text_with_math":
#         return process_math(question=data["question"])
        
#     elif input_type == "text_with_image":
#         return process_vision(text_prompt=data["text_prompt"], image_path=data["image_path"])
        
#     elif input_type == "text_with_table":
#         try:
#             df = pd.read_csv(data["table_path"])
#             return process_table(df=df, question=data["question"])
#         except Exception as e:
#             return f"테이블 파일을 읽는 중 오류 발생: {e}"
            
#     else:
#         return "알 수 없는 입력 유형입니다."

# # candosh 8/26
# # ================== 새로운 섹션 기반 처리 ==================
# def route_and_process_sections(sections_data: list):
#     """섹션별 JSON 데이터를 처리하는 메인 라우터 (신규 버전)"""
    
#     all_results = []
    
#     for section in sections_data:
#         section_result = process_single_section(section)
#         all_results.append(section_result)
    
#     return all_results

# def process_single_section(section_data: dict):
#     """단일 섹션 데이터 처리"""
    
#     section_id = section_data.get("section_id")
#     results = {
#         "section_id": section_id,
#         "text_analysis": None,
#         "table_analysis": [],
#         "image_analysis": [],
#         "equation_analysis": [],
#         "integrated_summary": None
#     }
    
#     # 1. 텍스트 분석
#     if section_data.get("text"):
#         results["text_analysis"] = process_section_text(
#             text=section_data["text"],
#             section_id=section_id
#         )
    
#     # 2. 표 분석 (CSV 문자열 → DataFrame 변환)
#     if section_data.get("tables"):
#         for table in section_data["tables"]:
#             csv_content = table["content"]
#             try:
#                 df = pd.read_csv(io.StringIO(csv_content))  # 문자열을 DataFrame으로
                
#                 table_result = process_table_with_section_context(
#                     df=df,
#                     page=table.get("page"),
#                     section_text=section_data.get("text", ""),
#                     section_id=section_id
#                 )
#                 results["table_analysis"].append(table_result)
#             except Exception as e:
#                 results["table_analysis"].append(f"표 처리 중 오류: {e}")
    
#     # 3. 이미지 분석
#     if section_data.get("images"):
#         for image_path in section_data["images"]:
#             try:
#                 image_result = process_image_with_section_context(
#                     image_path=image_path,
#                     section_text=section_data.get("text", ""),
#                     section_id=section_id
#                 )
#                 results["image_analysis"].append(image_result)
#             except Exception as e:
#                 results["image_analysis"].append(f"이미지 처리 중 오류: {e}")
    
#     # 4. 수식 분석
#     if section_data.get("equations"):
#         for equation in section_data["equations"]:
#             try:
#                 eq_result = process_math(question=f"이 수식의 의미를 설명해주세요: {equation}")
#                 results["equation_analysis"].append(eq_result)
#             except Exception as e:
#                 results["equation_analysis"].append(f"수식 처리 중 오류: {e}")
    
#     # 5. 섹션 통합 분석
#     results["integrated_summary"] = integrate_section_analysis(results, section_data)
    
#     return results

# def process_section_text(text: str, section_id: int):
#     """섹션 텍스트 분석 (컨텍스트 고려)"""
#     return process_text(
#         content=text,
#         paper_title=f"논문 섹션 {section_id} 분석",
#         section_title=f"Section {section_id}",
#         table_of_contents="섹션별 분석 모드"
#     )

# def process_table_with_section_context(df, page, section_text, section_id):
#     """섹션 컨텍스트를 포함한 표 분석"""
    
#     enhanced_question = f"""
#     섹션 {section_id}의 텍스트 맥락:
#     {section_text[:500]}...
    
#     이 맥락에서 다음 표를 분석해주세요.
#     표의 핵심 내용과 의미를 설명해주세요.
#     """
    
#     return process_table(df=df, question=enhanced_question)

# def process_image_with_section_context(image_path, section_text, section_id):
#     """섹션 맥락을 고려한 이미지 분석"""
    
#     enhanced_prompt = f"""
#     섹션 {section_id}의 내용:
#     {section_text[:300]}...
    
#     위 텍스트의 맥락에서 이 이미지를 분석해주세요.
#     이미지가 텍스트의 어떤 부분을 뒷받침하거나 설명하는지 포함해서 답변해주세요.
#     """
    
#     return process_vision(text_prompt=enhanced_prompt, image_path=image_path)

# def integrate_section_analysis(results, section_data):
#     """섹션 내 모든 요소를 통합 분석"""
    
#     integration_prompt = f"""
#     섹션 {section_data['section_id']} 통합 분석:
    
#     텍스트 내용: {section_data.get('text', 'N/A')[:200]}...
    
#     표 분석 결과: {str(results.get('table_analysis', []))[:200]}...
    
#     이미지 분석 결과: {str(results.get('image_analysis', []))[:200]}...
    
#     수식 분석 결과: {str(results.get('equation_analysis', []))[:200]}...
    
#     위 모든 정보를 종합해서 이 섹션의 핵심 내용을 요약해주세요.
#     텍스트, 표, 이미지, 수식이 어떻게 연결되어 하나의 논리를 구성하는지 설명해주세요.
#     """
    
#     try:
#         return process_text(
#             content=integration_prompt,
#             paper_title="논문 통합 분석",
#             section_title=f"섹션 {section_data['section_id']} 요약",
#             table_of_contents=""
#         )
#     except Exception as e:
#         return f"통합 분석 중 오류 발생: {e}"