# backend/apps/tasks/langchain_agent.py
import os
import json
import operator
from typing import Annotated, Literal, TypedDict, Union

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

# ------------------------------------------------------------------
# [Import 경로 안전 처리]
# ------------------------------------------------------------------
try:
    # src 폴더가 sys.path에 있을 때 (run_test.py 실행 시)
    from workflows.recommender import get_recommendation 
    from workflows.workflow import WorkflowEngine 
    from workflows.prompts import AGENT_SYSTEM_PROMPT 
except ImportError:
    # 프로젝트 루트(backend)에서 실행하거나 전체 경로가 필요할 때
    from src.workflows.recommender import get_recommendation 
    from src.workflows.workflow import WorkflowEngine 
    from src.workflows.prompts import AGENT_SYSTEM_PROMPT

# ==================================================================
# 1. 도구(Tools) 정의
# ==================================================================
@tool
def assignment_analyzer(description: str):
    """
    과제 내용을 분석하여 최적의 AI 모델(3가지 옵션)과 워크플로우를 추천합니다.
    """
    return get_recommendation(description)

@tool
def execution_guide(task_description: str, selected_model: str, step_info_json: str):
    """
    선택된 모델을 사용하여 특정 단계의 상세 가이드를 작성합니다.
    """
    engine = WorkflowEngine()
    try:
        step_info = json.loads(step_info_json)
    except:
        step_info = {"step": "Current Step", "desc": step_info_json}
    
    return engine.expand_step_content(task_description, step_info, selected_model)

# 도구 리스트 및 이름 매핑
tools = [assignment_analyzer, execution_guide]
tools_by_name = {tool.name: tool for tool in tools}

# ==================================================================
# 2. 상태(State) 정의
# ==================================================================
class AgentState(TypedDict):
    # 메시지 리스트를 계속 누적(add)하는 방식
    messages: Annotated[list[AnyMessage], operator.add]

# ==================================================================
# 3. 모델 및 노드(Nodes) 정의
# ==================================================================

# OpenRouter 모델 설정 + 도구 바인딩 (bind_tools)
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-exp:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)
model_with_tools = llm.bind_tools(tools)

def llm_call_node(state: AgentState):
    """
    LLM이 대화 기록을 보고 답변하거나 도구를 호출할지 결정하는 노드
    """
    # 시스템 프롬프트가 맨 앞에 없으면 추가 (선택 사항)
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + messages
        
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_execution_node(state: AgentState):
    """
    LLM이 요청한 도구를 실제로 실행하고 결과를 반환하는 노드
    """
    last_message = state["messages"][-1]
    results = []
    
    # LLM이 요청한 도구들을 순회하며 실행
    for tool_call in last_message.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]
        
        # 도구 실행
        try:
            tool_output = selected_tool.invoke(tool_call["args"])
        except Exception as e:
            tool_output = f"Error: {str(e)}"
            
        # 결과를 ToolMessage로 포장
        results.append(ToolMessage(
            content=str(tool_output), 
            tool_call_id=tool_call["id"]
        ))
        
    return {"messages": results}

def should_continue(state: AgentState) -> Literal["tool_node", END]:
    """
    LLM의 응답을 보고 도구를 실행할지(tool_node), 멈출지(END) 결정하는 엣지
    """
    last_message = state["messages"][-1]
    
    # 도구 호출 요청이 있으면 -> 도구 실행 노드로 이동
    if last_message.tool_calls:
        return "tool_node"
    
    # 없으면 -> 종료
    return END

# ==================================================================
# 4. 그래프(Graph) 빌드
# ==================================================================
def setup_graph():
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("llm_node", llm_call_node)
    workflow.add_node("tool_node", tool_execution_node)

    # 엣지 연결
    workflow.add_edge(START, "llm_node")
    
    # 조건부 엣지 (LLM 결과에 따라 분기)
    workflow.add_conditional_edges(
        "llm_node",
        should_continue,
        ["tool_node", END]
    )
    
    # 도구 실행 후엔 다시 LLM에게 결과를 보고하러 감
    workflow.add_edge("tool_node", "llm_node")

    return workflow.compile()

# ==================================================================
# 5. 실행 함수
# ==================================================================
def run_task_analysis(user_input: str, history: list = []):
    try:
        agent = setup_graph()
        
        # 이전 대화 기록 + 현재 질문
        current_messages = history + [HumanMessage(content=user_input)]
        
        # 그래프 실행
        result = agent.invoke({"messages": current_messages})
        
        # 최종 답변 반환
        return result["messages"][-1].content

    except Exception as e:
        return f"에이전트 실행 중 오류 발생: {str(e)}"