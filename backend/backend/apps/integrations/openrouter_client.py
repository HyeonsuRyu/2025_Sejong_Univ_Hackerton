# backend/apps/integrations/openrouter_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self, user_api_key=None):
        # 유저가 키를 주면 그걸 사용, 안주면 .env 키 사용
        self.api_key = user_api_key if user_api_key else os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("API Key가 없습니다. .env를 확인하거나 키를 입력해주세요.")
            
        # OpenRouter 주소(base_url) 설정    
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def generate_text(self, prompt, model="google/gemini-2.0-flash-exp:free", system_message="You are a helpful assistant."):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                # OpenRouter 랭킹 집계를 위한 헤더
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