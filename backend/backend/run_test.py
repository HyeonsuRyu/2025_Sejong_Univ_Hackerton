# run_test.py (프로젝트 최상위 폴더)
import os
import django
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 1. Django 환경 설정 (앱 모듈을 불러오기 위해 필수)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings") # backend 폴더명 확인!
django.setup()

# 2. 우리가 만든 클라이언트 가져오기
from apps.integrations.openrouter_client import OpenRouterClient

def main():
    # ==========================================
    # 여기에 원하는 입력값을 하드코딩 하세요!
    # ==========================================
    TEST_PROMPT = "파이썬으로 리스트 컴프리헨션 예제 3개만 알려줘."
    
    # 원하는 모델을 골라보세요 (OpenRouter 모델명 기준)
    # 1. GPT-4o: "openai/gpt-4o"
    # 2. Claude 3.5: "anthropic/claude-3.5-sonnet"
    # 3. Gemini Pro: "google/gemini-pro-1.5"
    TARGET_MODEL = "openai/gpt-4o" 

    print(f"[모델: {TARGET_MODEL}] 에게 질문하는 중...\n")

    # 3. 함수 실행
    bot = OpenRouterClient()
    result = bot.generate_text(
        prompt=TEST_PROMPT, 
        model=TARGET_MODEL,
        system_message="당신은 친절한 코딩 선생님입니다."
    )

    # 4. 결과 출력
    print("="*50)
    print(result)
    print("="*50)

if __name__ == "__main__":
    main()