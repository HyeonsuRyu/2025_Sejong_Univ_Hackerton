from langchain_core.messages import AnyMessage

# 메모리 기반 세션 저장소 (데모용)
SESSIONS: dict[str, list[AnyMessage]] = {}

def get_history(session_id: str) -> list[AnyMessage]:
    return SESSIONS.get(session_id, [])

def update_history(session_id: str, messages: list[AnyMessage]):
    SESSIONS[session_id] = messages
