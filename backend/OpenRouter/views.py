from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from OpenRouter.src.integrations.openrouter_client import OpenRouterClient
from OpenRouter.src.utils.session import get_session

# 1. 과제 입력
class AssignmentInitView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        session_id = request.data.get("session_id")
        assignment = request.data.get("assignment")

        if not (api_key and session_id and assignment):
            return Response({"error": "api_key, session_id, assignment are required"}, status=400)

        sess = get_session(session_id)
        sess.assignment = assignment
        sess.add_user(f"과제 정보를 아래와 같이 입력한다:\n{assignment}\n이 과제를 해결하기 위한 전체 단계(flow)를 한국어로 5~7개로 제안해줘. 각 단계는 간결한 명사형으로.")

        client = OpenRouterClient(api_key=api_key, model=sess.selected_model)
        resp = client.chat(sess.messages, temperature=0.3)
        text = client.extract_text(resp)
        sess.add_assistant(text)

        # 간단 파싱: 줄바꿈 기준으로 단계 리스트 생성
        flow = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
        # 최소 보정
        if len(flow) < 3:
            flow = ["문제 이해", "자료 조사", "해결 방법 설계", "실행 및 검증", "결과 정리"]
        sess.flow = flow
        sess.current_step_idx = 0

        return Response({"session_id": session_id, "flow": flow, "assistant": text}, status=200)


# 2. 단계별 가이드 생성
class StepGuideView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        session_id = request.data.get("session_id")

        if not (api_key and session_id):
            return Response({"error": "api_key, session_id required"}, status=400)

        sess = get_session(session_id)
        step = sess.current_step()
        if not step:
            return Response({"error": "flow not initialized"}, status=400)

        prompt = f"현재 단계: {step}\n이 단계에서 수행해야 할 구체적 작업 체크리스트(3~7개)와 예상 산출물을 한국어로 간결하게 제시해줘."
        sess.add_user(prompt)

        client = OpenRouterClient(api_key=api_key, model=sess.selected_model)
        resp = client.chat(sess.messages, temperature=0.2)
        text = client.extract_text(resp)
        sess.add_assistant(text)

        return Response({"step": step, "guide": text}, status=200)


# 3. 모델 추천 (요금/성능 포함) - 3개
class RecommendModelsView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        session_id = request.data.get("session_id")
        task_type = request.data.get("task_type")  # 예: "image_generation", "document_summarization"

        if not (api_key and session_id and task_type):
            return Response({"error": "api_key, session_id, task_type required"}, status=400)

        sess = get_session(session_id)
        prompt = (
            f"작업 유형: {task_type}\n"
            "OpenRouter에서 사용할 수 있는 모델 중 해당 작업에 적합한 3개를 추천해줘. "
            "각 모델에 대해 다음을 표 형식 없이 항목으로 제공:\n"
            "- 모델명 (OpenRouter 식별자)\n"
            "- 요금(대략적인 프롬프트/완성 단가 또는 상대적 수준)\n"
            "- 성능(정확도/창의성/속도 등 간단 평가)\n"
            "- 장점/단점(한 줄씩)\n"
            "간결한 한국어로."
        )
        sess.add_user(prompt)

        client = OpenRouterClient(api_key=api_key, model=sess.selected_model)
        resp = client.chat(sess.messages, temperature=0.3)
        text = client.extract_text(resp)
        sess.add_assistant(text)

        # 그대로 반환 (프론트에서 파싱/표시)
        return Response({"recommendations": text}, status=200)


# 4. 모델 선택 및 세션에 반영
class SelectModelView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        model_name = request.data.get("model_name")  # 예: "openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet"
        if not (session_id and model_name):
            return Response({"error": "session_id, model_name required"}, status=400)

        sess = get_session(session_id)
        sess.selected_model = model_name
        # 선택 기록만 남김
        return Response({"session_id": session_id, "selected_model": model_name}, status=200)


# 5. 프롬프트 추천 (선택된 모델/현재 단계 기준)
class PromptSuggestView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        session_id = request.data.get("session_id")
        extra_context = request.data.get("extra_context", "")

        if not (api_key and session_id):
            return Response({"error": "api_key, session_id required"}, status=400)

        sess = get_session(session_id)
        step = sess.current_step()
        base = (
            f"현재 단계: {step}\n"
            f"선택된 모델로 보낼 프롬프트를 한국어로 제안해줘. "
            f"맥락을 반영하고, 필요한 입력값을 변수로 표시해줘(예: <키워드>, <이미지 스타일>). "
            f"추가 맥락: {extra_context}"
        )
        sess.add_user(base)

        client = OpenRouterClient(api_key=api_key, model=sess.selected_model)
        resp = client.chat(sess.messages, temperature=0.2)
        suggested = client.extract_text(resp)
        sess.add_assistant(suggested)

        return Response({"suggested_prompt": suggested}, status=200)


# 6. 사용자가 입력한 프롬프트로 실행, 응답을 전체 맥락에 추가
class ExecuteWithSelectedModelView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        session_id = request.data.get("session_id")
        user_prompt = request.data.get("prompt")

        if not (api_key and session_id and user_prompt):
            return Response({"error": "api_key, session_id, prompt required"}, status=400)

        sess = get_session(session_id)
        # 선택된 모델로 별도 호출
        client = OpenRouterClient(api_key=api_key, model=sess.selected_model)

        # 기존 맥락 + 사용자 프롬프트
        messages = list(sess.messages) + [{"role": "user", "content": user_prompt}]
        resp = client.chat(messages, temperature=0.2)
        text = client.extract_text(resp)

        # 전체 세션 맥락에 결과 추가
        sess.add_user(user_prompt)
        sess.add_assistant(text)

        return Response({"model": sess.selected_model, "result": text, "messages_len": len(sess.messages)}, status=200)


# 7. 다음 문제 해결 단계로 이동
class NextStepView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response({"error": "session_id required"}, status=400)

        sess = get_session(session_id)
        next_step = sess.next_step()
        return Response({"next_step": next_step, "current_index": sess.current_step_idx}, status=200)
