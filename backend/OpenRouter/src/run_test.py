# run_test.py
import os
import sys
import django

# ------------------------------------------------------------------
# [경로 자동 보정]
# 현재 파일이 어디에 있든, 'manage.py'가 있는 프로젝트 루트를 찾아냅니다.
# ------------------------------------------------------------------
current_file_path = os.path.abspath(__file__)

# 1. 현재 폴더 (src)
current_dir = os.path.dirname(current_file_path)

# 2. 상위 폴더들로 올라가며 'backend' 패키지가 있는 루트 찾기
# (OpenRouter/src -> OpenRouter -> backend 순으로 올라감)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# 3. 프로젝트 루트를 파이썬 경로에 추가 (이제 backend.settings를 찾을 수 있음!)
if project_root not in sys.path:
    sys.path.append(project_root)

# ------------------------------------------------------------------
# Django 설정
# ------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# ------------------------------------------------------------------
# Import (경로가 잡혔으므로 이제 안전하게 import 가능)
# ------------------------------------------------------------------
try:
    from integrations.openrouter_client import OpenRouterClient
except ImportError:
    # 혹시 폴더 구조가 다른 경우를 대비
    try:
        from src.integrations.openrouter_client import OpenRouterClient
    except ImportError:
        # 마지막 시도: backend.apps...
        from src.integrations.openrouter_client import OpenRouterClient

def main():
    print(f"🚀 [OpenRouterClient 기능 테스트 시작]")
    print(f"📂 인식된 프로젝트 루트: {project_root}\n")

    # ==========================================
    # [TEST 1] 기본 모드 (.env 서버 키 사용)
    # ==========================================
    print("🔵 [TEST 1] 기본 키(.env) 사용 테스트")
    try:
        bot_default = OpenRouterClient() 
        result = bot_default.generate_text(
            prompt="안녕? 너는 어떤 모델이니?", 
            model="google/gemini-2.0-flash-exp:free",
            system_message="짧게 대답해."
        )
        print(f"✅ 결과: {result}\n")
    except Exception as e:
        print(f"❌ TEST 1 실패: {e}\n")

    # ==========================================
    # [TEST 2] BYOK 모드 (유저 키 사용)
    # ==========================================
    print("🟠 [TEST 2] 유저 입력 키(BYOK) 사용 테스트")
    fake_user_key = "sk-or-v1-fake-key-for-testing"
    print(f"👉 테스트용 가짜 키 입력: {fake_user_key}")

    try:
        bot_user = OpenRouterClient(user_api_key=fake_user_key)
        bot_user.generate_text(
            prompt="이 요청은 실패해야 해.",
            model="google/gemini-2.0-flash-exp:free",
        )
        print("❌ 실패: 에러가 안 났습니다. (가짜 키인데 성공하면 안 됨)")
    except Exception as e:
        if "401" in str(e) or "AuthenticationError" in str(e):
            print(f"✅ 성공: 예상대로 인증 에러가 발생했습니다.")
        else:
            print(f"⚠️ 다른 에러 발생: {e}")

    print("\n==========================================")
    print("테스트 종료")

if __name__ == "__main__":
    main()