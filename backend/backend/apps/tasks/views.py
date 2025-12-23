# backend/apps/tasks/views.py
# API 뷰
from rest_framework.views import APIView
from rest_framework.response import Response
from .langchain_agent import run_task_analysis

class TaskAnalyzeView(APIView):
    def post(self, request):
        task_description = request.data.get("description")
        # AI 팀원의 에이전트 가동
        result = run_task_analysis(task_description)
        return Response({"analysis_result": result})