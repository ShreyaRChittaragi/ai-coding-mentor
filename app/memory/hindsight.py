from app.memory.schemas import UserMemoryProfile, PatternRecord
from datetime import datetime

_memory_store: dict[str, UserMemoryProfile] = {}

def store_session(user_id: str, session_data: dict):
    if user_id not in _memory_store:
        _memory_store[user_id] = UserMemoryProfile(user_id=user_id)

    profile = _memory_store[user_id]
    profile.total_sessions += 1
    profile.last_active = datetime.now()

    for p in session_data.get("patterns", []):
        profile.patterns.append(PatternRecord(
            pattern=p,
            confidence=0.75,        # placeholder until P4 sends confidence
            mistake_type=None
        ))

def retrieve_memory(user_id: str) -> dict:
    profile = _memory_store.get(user_id)
    if not profile:
        return {"user_id": user_id, "message": "No memory found"}
    return profile.model_dump()

def update_memory(user_id: str, new_pattern: PatternRecord):
    if user_id not in _memory_store:
        _memory_store[user_id] = UserMemoryProfile(user_id=user_id)
    _memory_store[user_id].patterns.append(new_pattern)