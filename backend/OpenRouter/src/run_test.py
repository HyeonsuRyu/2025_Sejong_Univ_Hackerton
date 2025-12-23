# backend/OpenRouter/src/run_test.py
import os
import sys
import django

# 1. 경로 설정: 현재 파일 기준 최상위 프로젝트 루트 찾기
# 현재 위치: backend/OpenRouter/src/run_test.py
current_dir = os.path.dirname(os.path.abspath(__file__)) # src
openrouter_dir = os.path.dirname(current_dir)             # OpenRouter
project_root = os.path.dirname(openrouter_dir)          # 최상위 backend

# 최상위 폴더를 경로 맨 앞에 추가하여 'backend.settings'를 찾을 수 있게 함
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# src 폴더도 추가하여 내부 모듈(tasks, workflows)을 찾게 함
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. Django 환경 설정
# 프로젝트 루트가 추가되었으므로 'backend.settings'를 패키지로 인식합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

try:
    django.setup()
except Exception as e:
    print(f"❌ Django 설정 실패: {e}")
    print(f"현재 sys.path: {sys.path}")
    sys.exit(1)

# 3. 에이전트 가져오기 (src가 path에 있으므로 직접 참조 가능)
try:
    from tasks.langchain_agent import run_task_analysis
    from langchain_core.messages import HumanMessage, AIMessage
except ImportError as e:
    print(f"❌ Import 실패: {e}")
    sys.exit(1)

def main():
    print(f"🚀 [LangGraph 통합 에이전트 테스트 시작]")
    print(f"📂 인식된 프로젝트 루트: {project_root}\n")

    chat_history = []

    # [STEP 1] 과제 분석
    print("🔵 [STEP 1] 과제 분석 및 추천 테스트")
    user_input_1 = "파이썬 성적 계산기 과제 분석해줘."
    try:
        response_1 = run_task_analysis(user_input_1, chat_history)
        print(f"🤖 AI 분석 결과:\n{response_1}\n")
        
        chat_history.append(HumanMessage(content=user_input_1))
        chat_history.append(AIMessage(content=response_1))
    except Exception as e:
        print(f"❌ STEP 1 실패: {e}")
        return

    # [STEP 2] 실행 가이드
    print("🟠 [STEP 2] 상세 실행 가이드 테스트")
    user_input_2 = "가성비 모델로 1단계 가이드 작성해줘."
    try:
        response_2 = run_task_analysis(user_input_2, chat_history)
        print(f"🤖 AI 실행 가이드:\n{response_2}\n")
    except Exception as e:
        print(f"❌ STEP 2 실패: {e}")

if __name__ == "__main__":
    main()