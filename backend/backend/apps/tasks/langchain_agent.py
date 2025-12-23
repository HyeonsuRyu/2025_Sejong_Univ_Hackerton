# backend/apps/tasks/langchain_agent.py
import os
from langchain.agents import AgentExecutor, create_tool_calling_agent # Import 확인
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from apps.workflows.recommender import get_recommendation 
from apps.workflows.prompts import AGENT_SYSTEM_PROMPT 

@tool
def assignment_analyzer(description: str):
    """과제의 성격과 난이도를 분석하여 최적의 AI 모델과 워크플로우를 추천받습니다."""
    return get_recommendation(description)

def setup_agent():
    # OpenRouter에서 사용
    llm = ChatOpenAI(
        model="google/gemini-2.0-flash-exp:free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0
    )
    
    tools = [assignment_analyzer]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT), 
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 변경 전: create_openai_functions_agent(llm, tools, prompt) -> Import 안됨
    # 변경 후: create_tool_calling_agent 사용
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_task_analysis(user_input):
    executor = setup_agent()
    result = executor.invoke({"input": user_input})
    return result["output"]