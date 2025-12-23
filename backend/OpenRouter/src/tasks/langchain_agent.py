'''# backend/apps/tasks/langchain_agent.py
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from src.workflows.recommender import get_recommendation 
from src.workflows.prompts import AGENT_SYSTEM_PROMPT 

@tool
def assignment_analyzer(description: str):
    """과제의 성격과 난이도를 분석하여 최적의 AI 모델과 워크플로우를 추천받습니다."""
    return get_recommendation(description)

def setup_agent():
    # OpenRouter에서 사용
    llm = ChatOpenAI(
        model="google/gemini-2.0-flash-exp:free", # OpenRouter 모델명 (GPTmodel은 model="openai/gpt-4o",)
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1", # 핵심: 주소 변경
        temperature=0
    )
    
    tools = [assignment_analyzer]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT), 
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# 기존의 run_task_analysis 함수가 있다면 유지하세요.
def run_task_analysis(user_input):
    executor = setup_agent()
    result = executor.invoke({"input": user_input})
    return result["output"]'''