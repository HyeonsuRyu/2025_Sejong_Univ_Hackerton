# backend/apps/workflows/recommender.py
import json
from backend.apps.integrations.openrouter_client import OpenRouterClient

def get_recommendation(task_description):
    client = OpenRouterClient()
    
    # 3가지 버전(무료, 성능, 가성비)으로 추천
    system_message = """
    당신은 'AI 도구 큐레이션 전문가'입니다. 사용자의 과제를 분석하여 JSON 형식으로만 응답하세요.
    
    반드시 다음 3가지 카테고리로 나누어 도구를 추천해야 합니다:
    1. 'free_ver': 비용 없는 무료 버전 (예: ChatGPT Free, Gemini, HuggingFace 등)
    2. 'performance_ver': 성능 최상 버전 (비용 무관, 예: GPT-4o, Claude 3.5 Opus 등)
    3. 'cost_efficiency_ver': 가성비 버전 (적당한 성능과 저렴한 비용, 예: Claude 3 Haiku, GPT-4o-mini 등)

    응답 JSON 구조:
    {
        "task_analysis": "과제 내용 요약",
        "recommendations": {
            "free_ver": {"model": "모델명(OpenRouter ID)", "reason": "이유"},
            "performance_ver": {"model": "모델명(OpenRouter ID)", "reason": "이유"},
            "cost_efficiency_ver": {"model": "모델명(OpenRouter ID)", "reason": "이유"}
        },
        "initial_workflow": [{"step": "1단계", "desc": "설명"}, ...]
    }
    """

    user_prompt = f"다음 과제를 분석해서 3가지 맞춤형 도구를 추천해줘: {task_description}"

    try:
        # Agent 1은 GPT가 분석을 담당합니다.
        raw_response = client.generate_text(
            prompt=user_prompt, 
            system_message=system_message,
            model="openai/gpt-4o"
        )
        
        json_str = raw_response.strip().replace("```json", "").replace("```", "")
        return json.loads(json_str)

    except Exception as e:
        print(f"추천 에러: {e}")
        return {"error": str(e)}