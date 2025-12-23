from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from OpenRouter.src.tasks.langchain_agent import run_task_analysis

class TaskAnalysisView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        user_input = request.data.get("text")
        api_key = request.data.get("api_key")

        if not session_id or not user_input or not api_key:
            return Response({"error": "session_id and text are required"}, status=400)

        result = run_task_analysis(user_input, session_id, api_key)
        return Response({"reply": result}, status=200)