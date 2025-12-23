# run_test.py (프로젝트 최상위 폴더)
import os
import sys
import django

# ------------------------------------------------------------------
# 경로 설정 (backend 폴더 인식용)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ------------------------------------------------------------------

# 1. Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# 2. 클라이언트 가져오기
from src.integrations.openrouter_client import OpenRouterClient

def main():
    print("[OpenRouterClient 기능 테스트 시작]\n")

    # ==========================================
    # [TEST 1] 기본 모드 (.env 서버 키 사용)
    # ==========================================
    print("[TEST 1] 기본 키(.env) 사용 테스트")
    try:
        # 인자 없이 생성 -> .env 키 사용
        bot_default = OpenRouterClient() 
        
        result = bot_default.generate_text(
            prompt="안녕? 너는 어떤 모델이니?", 
            model="google/gemini-2.0-flash-exp:free", # 테스트니까 저렴한 모델로
            system_message="짧게 대답해."
        )
        print(f"결과: {result}\n")
        
    except Exception as e:
        print(f"TEST 1 실패: {e}\n")


    # ==========================================
    # [TEST 2] BYOK 모드 (유저 키 사용)
    # ==========================================
    print("[TEST 2] 유저 입력 키(BYOK) 사용 테스트")
    
    # 테스트를 위해 '가짜 키'를 넣어봅니다.
    # 만약 로직이 정상이라면, .env에 진짜 키가 있어도 이 가짜 키를 쓰려다가 '401 에러'가 나야 합니다.
    # (401 에러가 나면 성공입니다! 서버 키를 안 썼다는 증거니까요.)
    fake_user_key = "sk-or-v1-fake-key-for-testing" 
    print(f"테스트용 가짜 키 입력: {fake_user_key}")

    try:
        # 유저 키를 넣어서 생성
        bot_user = OpenRouterClient(user_api_key=fake_user_key)
        
        bot_user.generate_text(
            prompt="이 요청은 실패해야 해.",
            model="openai/gpt-4o-mini"
        )
        print("실패: 에러가 안 났습니다. (가짜 키인데 성공하면 안 됨)")
        
    except Exception as e:
        # 401 Error가 뜨면 성공
        if "401" in str(e) or "AuthenticationError" in str(e):
            print(f"성공: 예상대로 인증 에러가 발생했습니다. (유저 키가 우선 적용됨)")
            print(f"   (에러 메시지: {e})")
        else:
            print(f"⚠️ 다른 에러 발생: {e}")

    print("\n==========================================")
    print("테스트 종료")

if __name__ == "__main__":
    main()