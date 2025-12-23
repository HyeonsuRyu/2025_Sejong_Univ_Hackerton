# backend/apps/integrations/openrouter_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        # .env에서 OPENROUTER_API_KEY를 가져옵니다.
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY가 .env 파일에 없습니다!")
            
        # 핵심: OpenRouter 주소(base_url) 설정
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def generate_text(self, prompt, model="openai/gpt-4o", system_message="You are a helpful assistant."):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                # OpenRouter 랭킹 집계를 위한 헤더 (선택사항이지만 권장)
                extra_headers={
                    "HTTP-Referer": "http://localhost:8000", 
                    "X-Title": "Student AI Agent",
                },
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter 호출 중 에러: {e}")
            raise e  # 에러를 상위로 던져서 디버깅을 돕습니다.