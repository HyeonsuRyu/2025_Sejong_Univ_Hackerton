# backend/apps/workflows/workflow.py
import json
import concurrent.futures
from backend.apps.integrations.openrouter_client import OpenRouterClient

class WorkflowEngine:
    def __init__(self):
        self.client = OpenRouterClient()

    def expand_step_content(self, task_description: str, step_info: dict) -> dict:
        step_title = step_info.get("step", "")
        step_desc = step_info.get("desc", "")

        system_message = """
        당신은 실무 멘토입니다. 사용자의 과제와 현재 진행 단계를 보고, 
        구체적인 'Action Item'과 'Tip'을 JSON으로 제공하세요.
        반드시 다음 키를 포함하세요:
        - "detailed_guide": 구체적인 설명
        - "checklist": ["할일1", "할일2"] 형태의 리스트
        - "resources": 참고할 만한 검색 키워드나 라이브러리 추천
        - "code_snippet": (필요시) Python/C++ 등 관련 예시 코드 (없으면 null)
        """

        user_prompt = f"""
        [전체 과제]: {task_description}
        [현재 단계]: {step_title} - {step_desc}
        
        이 단계에서 학생이 바로 따라 할 수 있는 상세 가이드를 만들어줘.
        """

        try:
            # OpenRouter 모델 지정 (openai/gpt-4o 사용)
            raw_response = self.client.generate_text(
                user_prompt, 
                system_message=system_message,
                model="openai/gpt-4o" 
            )
            
            json_str = raw_response.strip().replace("```json", "").replace("```", "")
            expanded_content = json.loads(json_str)
            
            return {**step_info, **expanded_content}

        except Exception as e:
            return {
                **step_info,
                "detailed_guide": "상세 가이드를 불러오는 중 오류가 발생했습니다.",
                "checklist": [],
                "error": str(e)
            }

    def process_full_workflow(self, task_description: str, workflow_steps: list) -> list:
        # 병렬 처리 로직은 완벽합니다! 그대로 둡니다.
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(lambda step: self.expand_step_content(task_description, step), workflow_steps)
            return list(results)