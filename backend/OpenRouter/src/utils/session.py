# OpenRouter/src/utils/session.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AISession:
    assignment: str = ""
    flow: List[str] = field(default_factory=list)
    current_step_idx: int = 0
    messages: List[Dict[str, str]] = field(default_factory=lambda: [
        {"role": "system", "content": "You are an expert assistant that helps users solve assignments step-by-step. Always be concise and actionable."}
    ])
    selected_model: str = "openai/gpt-4o-mini"

    def add_user(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def current_step(self) -> str:
        if not self.flow:
            return ""
        return self.flow[self.current_step_idx]

    def next_step(self) -> str:
        if self.current_step_idx + 1 < len(self.flow):
            self.current_step_idx += 1
            return self.flow[self.current_step_idx]
        return "완료"

# 간단한 메모리 저장소 (데모용). 실제 서비스는 DB 모델로 전환.
SESSIONS: dict[str, AISession] = {}

def get_session(session_id: str) -> AISession:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = AISession()
    return SESSIONS[session_id]
