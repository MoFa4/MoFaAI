# memory.py
from typing import Dict, List, Tuple
import time

sessions: Dict[str, List[Tuple[str, str, float]]] = {}

def get_session(session_id: str) -> List[str]:
    if session_id not in sessions: sessions[session_id] = []
    return [f"{role}: {msg}" for role, msg, _ in sessions[session_id][-6:]]

def save_message(session_id: str, role: str, content: str):
    if session_id not in sessions: sessions[session_id] = []
    sessions[session_id].append((role, content, time.time()))