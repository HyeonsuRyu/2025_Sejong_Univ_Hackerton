from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
#from OpenRouter.src.tasks.langchain_agent import setup_agent
from OpenRouter.src.integrations.openrouter_client import OpenRouterClient

# 1. setup_agent 실행
#agent = setup_agent()

client = OpenRouterClient()

class GenerateTextView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        # 2. 요청에서 ext 입력받기
        text = request.data.get("text")
        api_key = request.data.get("api_key")
        if not text:
            return Response({"error": "ext is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not api_key:
            return Response({"error": "api_key is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = OpenRouterClient(user_api_key=api_key)
            result = client.generate_text(text)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
