# backend/apps/workflows/workflow.py
import json
import concurrent.futures
from OpenRouter.src.integrations.openrouter_client import OpenRouterClient

class WorkflowEngine:
    def __init__(self, user_api_key=None):
        self.client = OpenRouterClient(user_api_key=user_api_key)

    # selected_model을 받아서 실행하고, 프롬프트까지 반환
    def expand_step_content(self, task_description: str, step_info: dict, selected_model: str) -> dict:
        step_title = step_info.get("step", "")
        step_desc = step_info.get("desc", "")

        system_message = "당신은 실무 멘토입니다. JSON 형식으로 구체적인 가이드를 제공하세요."

        # 실제 사용된 프롬프트 (나중에 사용자에게 보여줄 것)
        user_prompt = f"""
        [전체 과제]: {task_description}
        [현재 단계]: {step_title} - {step_desc}
        
        이 단계에서 학생이 바로 따라 할 수 있는 상세 가이드(detailed_guide)와 
        실제 활용 가능한 예시(example_content)를 작성해줘.
        """

        try:
            # 사용자가 선택한 모델(selected_model)로 호출
            raw_response = self.client.generate_text(
                prompt=user_prompt, 
                system_message=system_message,
                model=selected_model 
            )
            
            json_str = raw_response.strip().replace("```json", "").replace("```", "")
            result_content = json.loads(json_str)
            
            # 결과에 '사용된 프롬프트'와 '모델 정보'를 포함시킴
            return {
                **step_info,
                **result_content,
                "meta_info": {
                    "used_model": selected_model,
                    "used_prompt": user_prompt, # 사용자가 공부할 수 있게 공개
                    "system_message": system_message
                }
            }

        except Exception as e:
            return {**step_info, "error": str(e)}

    # 병렬 처리 함수도 모델명을 받도록 수정
    def process_full_workflow(self, task_description: str, workflow_steps: list, selected_model: str) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # map에 selected_model 인자 전달
            results = executor.map(
                lambda step: self.expand_step_content(task_description, step, selected_model), 
                workflow_steps
            )
            return list(results)