# backend/apps/tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.workflows.recommender import get_recommendation
from apps.workflows.workflow import WorkflowEngine

class TaskAnalyzeView(APIView):
    def post(self, request):
        task_description = request.data.get("description")
        if not task_description:
            return Response({"error": "No description"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1단계: 전체 추천 로직 실행 (Recommender) -> 3초 소요
            # 결과: { "category": "...", "workflow": [{step1}, {step2}...] }
            base_recommendation = get_recommendation(task_description)
            
            # 2단계: 상세 가이드 확장 (WorkflowEngine) -> 병렬 처리로 3~4초 소요
            workflow_engine = WorkflowEngine()
            
            # Recommender가 준 workflow 리스트를 가져와서 확장
            original_steps = base_recommendation.get("workflow", [])
            detailed_steps = workflow_engine.process_full_workflow(task_description, original_steps)
            
            # 3단계: 결과 합치기
            final_result = {
                **base_recommendation,
                "workflow": detailed_steps  # 상세 내용이 포함된 단계로 교체
            }

            return Response({"analysis_result": final_result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)