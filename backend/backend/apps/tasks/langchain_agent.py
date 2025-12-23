# backend/apps/tasks/langchain_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from apps.workflows.recommender import get_recommendation # 경로 주의 (Django 기준)

@tool
def assignment_analyzer(description: str):
    """과제의 성격과 난이도를 분석하여 최적의 AI 모델과 워크플로우를 추천받습니다."""
    return get_recommendation(description)

def setup_agent():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [assignment_analyzer]
    
    # 커스텀 프롬프트 설정 (정의하신 SYSTEM_PROMPT 반영)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 최고의 과제 도우미 에이전트입니다. 사용자의 과제 내용을 분석하여 유형 파악, 모델 추천, 실행 계획 수립을 수행하세요."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    # verbose=True는 개발 단계에서 로그 확인에 아주 좋습니다.
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_task_analysis(user_input):
    executor = setup_agent()
    # 최신 LangChain은 invoke 사용 권장
    result = executor.invoke({"input": user_input})
    return result["output"]