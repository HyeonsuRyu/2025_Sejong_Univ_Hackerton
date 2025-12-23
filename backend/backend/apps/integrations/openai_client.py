# backend/apps/integrations/openai_client.py
# OpenAI 모델 통신 담당
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY가 .env 파일에 없습니다!")
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt, system_message="You are a helpful assistant."):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 # 추천 로직에는 약간의 창의성이 필요할 수 있음
        )
        return response.choices[0].message.content