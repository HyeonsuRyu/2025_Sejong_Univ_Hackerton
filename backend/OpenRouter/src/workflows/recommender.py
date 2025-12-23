# backend/apps/workflows/recommender.py
import json
from src.integrations.openrouter_client import OpenRouterClient

def get_recommendation(task_description):
    client = OpenRouterClient()
    
    # OpenRouter의 실제 무료 모델 ID 예시를 프롬프트에 포함
    system_message = """
    당신은 'AI 도구 큐레이션 전문가'입니다. 사용자의 과제를 분석하여 JSON 형식으로만 응답하세요.
    
    반드시 다음 3가지 카테고리로 나누어 도구를 추천해야 합니다.
    각 카테고리에 맞는 'OpenRouter Model ID'를 정확하게 추천하세요:

    1. 'free_ver': 비용 없는 무료 버전
        - 추천 예시: 'google/gemini-2.0-flash-exp:free', 'meta-llama/llama-3.3-70b-instruct:free', 'mistralai/mistral-7b-instruct:free'
    
    2. 'performance_ver': 성능 최상 버전 (비용 무관)
        - 추천 예시: 'openai/gpt-4o-2024-08-06', 'anthropic/claude-3.5-sonnet', 'google/gemini-pro-1.5'
    
    3. 'cost_efficiency_ver': 가성비 버전 (성능/비용 균형)
        - 추천 예시: 'anthropic/claude-3-haiku', 'openai/gpt-4o-mini', 'google/gemini-flash-1.5'

    응답 JSON 구조:
    {
        "task_analysis": "과제 내용 요약",
        "recommendations": {
            "free_ver": {"model": "실제_OpenRouter_Model_ID", "reason": "이 모델이 무료임에도 이 과제에 적합한 이유"},
            "performance_ver": {"model": "실제_OpenRouter_Model_ID", "reason": "성능상 이점이 있는 이유"},
            "cost_efficiency_ver": {"model": "실제_OpenRouter_Model_ID", "reason": "비용 대비 효율적인 이유"}
        },
        "initial_workflow": [{"step": "1단계", "desc": "설명"}, ...]
    }
    """

    user_prompt = f"다음 과제를 분석해서 3가지 맞춤형 도구를 추천해줘: {task_description}"

    try:
        raw_response = client.generate_text(
            prompt=user_prompt, 
            system_message=system_message,
            model="google/gemini-2.0-flash-exp:free"
        )
        
        json_str = raw_response.strip().replace("```json", "").replace("```", "")
        return json.loads(json_str)

    except Exception as e:
        print(f"추천 에러: {e}")
        return {"error": str(e)}