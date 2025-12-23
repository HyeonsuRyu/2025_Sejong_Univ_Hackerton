# backend/apps/tasks/langchain_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from apps.workflows.recommender import get_recommendation 

# 분리한 프롬프트 불러오기
from apps.workflows.prompts import AGENT_SYSTEM_PROMPT

@tool
def assignment_analyzer(description: str):
    """과제의 성격과 난이도를 분석하여 최적의 AI 모델과 워크플로우를 추천받습니다."""
    # workflows 폴더에 있는 로직 호출
    return get_recommendation(description)

def setup_agent():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [assignment_analyzer]
    
    # 불러온 상수를 사용
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT), 
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)