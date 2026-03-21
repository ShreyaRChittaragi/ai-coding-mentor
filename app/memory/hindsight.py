from app.memory.schemas import UserMemoryProfile, PatternRecord
from datetime import datetime
import json
import os

MEMORY_FILE = "memory_data.json"

# ✅ Define store FIRST
_memory_store: dict[str, UserMemoryProfile] = {}

def _save_to_disk():
    data = {uid: profile.model_dump() for uid, profile in _memory_store.items()}
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, default=str)

def _load_from_disk():
    if not os.path.exists(MEMORY_FILE):
        return
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)
    for uid, profile_data in data.items():
        try:
            _memory_store[uid] = UserMemoryProfile(**profile_data)
        except Exception:
            pass  # skip corrupted entries, don't crash startup

# ✅ Load AFTER store is defined and functions exist
_load_from_disk()

def store_session(user_id: str, session_data: dict):
    if user_id not in _memory_store:
        _memory_store[user_id] = UserMemoryProfile(user_id=user_id)

    profile = _memory_store[user_id]
    profile.total_sessions += 1
    profile.last_active = datetime.now()

    for p in session_data.get("patterns", []):
        if isinstance(p, dict):
            profile.patterns.append(PatternRecord(
                pattern=p.get("pattern", "unknown"),
                confidence=p.get("confidence", 0.75),
                mistake_type=p.get("mistake_type", None)
            ))
        else:
            profile.patterns.append(PatternRecord(
                pattern=p,
                confidence=0.75,
                mistake_type=None
            ))

    _save_to_disk()  # ✅ persist after every store

def retrieve_memory(user_id: str) -> dict:
    profile = _memory_store.get(user_id)
    if not profile:
        return {
            "user_id": user_id,
            "total_sessions": 0,
            "patterns": [],
            "last_active": None,
            "notes": None
        }
    return profile.model_dump()

def update_memory(user_id: str, new_pattern: PatternRecord):
    if user_id not in _memory_store:
        _memory_store[user_id] = UserMemoryProfile(user_id=user_id)
    _memory_store[user_id].patterns.append(new_pattern)
    _save_to_disk()  # ✅ persist this too

def reflect_on_user(user_id: str, question: str) -> str:
    profile = _memory_store.get(user_id)
    if not profile or not profile.patterns:
        return "No behavioral history found for this user yet."

    pattern_summary = ", ".join(
        f"{p.pattern} (confidence: {p.confidence})"
        for p in profile.patterns[-5:]
    )

    return (
        f"User {user_id} has completed {profile.total_sessions} session(s). "
        f"Recent patterns: {pattern_summary}. "
        f"Use this to adapt your hints accordingly."
    )