# backend/apps/workflows/recommender.py
import json
from backend.apps.integrations.openrouter_client import OpenRouterClient

def get_recommendation(task_description):
    # 1. 클라이언트 생성
    client = OpenRouterClient()
    
    # 2. 구조화된 응답을 받기 위한 페르소나와 제약조건 설정
    system_message = """
    당신은 과제 솔루션 아키텍트입니다. 사용자의 과제를 분석하여 JSON 형식으로만 응답하세요.
    응답에는 반드시 다음 키가 포함되어야 합니다:
    1. 'category': 과제 유형 (예: '데이터 분석', '문학 레포트', '웹 프로그래밍' 등)
    2. 'recommended_model': 가장 적합한 모델 (OpenAI gpt-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro 중 택 1)
    3. 'reason': 해당 모델을 추천하는 이유
    4. 'workflow': 작업을 완료하기 위한 상세 단계 리스트 (각 단계는 'step'과 'desc' 포함)
    """

    user_prompt = f"다음 과제를 분석해서 최적의 실행 계획을 세워줘: {task_description}"

    try:
        # 3. OpenRouter 클라이언트를 통해 분석 요청
        raw_response = client.generate_text(user_prompt, system_message=system_message)
        
        if not raw_response:
            raise ValueError("AI 응답이 비어있습니다.")

        # 4. 문자열 응답을 Python 딕셔너리로 변환
        json_str = raw_response.strip().replace("```json", "").replace("```", "")
        recommendation_data = json.loads(json_str)
        
        return recommendation_data

    except Exception as e:
        # 에러 발생 시 기본 구조 반환 (시스템 안정성 확보)
        print(f"Recommender Error: {e}")
        return {
            "category": "분석 실패",
            "recommended_model": "openai/gpt-4o",
            "reason": f"분석 중 오류가 발생했습니다: {str(e)}",
            "workflow": [{"step": "수동 확인", "desc": "과제 내용을 다시 확인해 주세요."}]
        }