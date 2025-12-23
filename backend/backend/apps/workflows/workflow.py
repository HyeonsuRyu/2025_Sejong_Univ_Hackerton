import json
from backend.apps.integrations.openai_client import OpenAIClient
# 나중에 prompts.py가 완성되면 거기서 가져오도록 리팩토링 가능
from backend.apps.workflows.prompts import WORKFLOW_EXPANSION_PROMPT

class WorkflowEngine:
    def __init__(self):
        # 상황에 따라 GeminiClient, AnthropicClient 등으로 교체 가능하도록 설계
        self.client = OpenAIClient()

    def expand_step_content(self, task_description: str, step_info: dict) -> dict:
        """
        특정 단계(Step)에 대한 상세 가이드(실천 팁, 예시 코드, 체크리스트)를 생성합니다.
        """
        step_title = step_info.get("step", "")
        step_desc = step_info.get("desc", "")

        # 1. 상세 가이드 생성을 위한 프롬프트 구성
        system_message = """
        당신은 실무 멘토입니다. 사용자의 과제와 현재 진행 단계를 보고, 
        실제로 수행할 수 있는 구체적인 'Action Item'과 'Tip'을 JSON으로 제공하세요.
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
            # 2. LLM 호출
            raw_response = self.client.generate_text(user_prompt, system_message=system_message)
            
            # 3. JSON 파싱
            json_str = raw_response.strip().replace("```json", "").replace("```", "")
            expanded_content = json.loads(json_str)
            
            # 기존 step 정보에 상세 정보를 병합하여 반환
            return {**step_info, **expanded_content}

        except Exception as e:
            # 에러 시 기본 정보만 반환
            return {
                **step_info,
                "detailed_guide": "상세 가이드를 불러오는 중 오류가 발생했습니다.",
                "checklist": [],
                "error": str(e)
            }

    def process_full_workflow(self, task_description: str, workflow_steps: list) -> list:
        """
        추천된 전체 워크플로우(리스트)를 받아서, 모든 단계의 상세 내용을 한 번에 생성합니다.
        (시간이 좀 걸릴 수 있으므로 비동기 처리를 권장합니다)
        """
        detailed_workflow = []
        for step in workflow_steps:
            detailed_step = self.expand_step_content(task_description, step)
            detailed_workflow.append(detailed_step)
        
        return detailed_workflow