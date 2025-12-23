# OpenRouter/src/integrations/openrouter_client.py
import requests

class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "google/gemma-3-27b-it:free"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def chat(self, messages: list[dict], **params) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
        }
        # 옵션 파라미터 (temperature 등) 전달
        payload.update(params)
        resp = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def extract_text(response: dict) -> str:
        try:
            return response["choices"][0]["message"]["content"]
        except Exception:
            return ""
