from app.memory.schemas import UserMemoryProfile, PatternRecord
from datetime import datetime

# In-memory store — replace with real Hindsight API later
_memory_store: dict[str, UserMemoryProfile] = {}

def store_session(user_id: str, session_data: dict):
    """Store a session and its detected patterns into user memory."""
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

def retrieve_memory(user_id: str) -> dict:
    """Get the full memory profile for a user."""
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
    """Add a single new pattern to an existing user profile."""
    if user_id not in _memory_store:
        _memory_store[user_id] = UserMemoryProfile(user_id=user_id)
    _memory_store[user_id].patterns.append(new_pattern)

def reflect_on_user(user_id: str, question: str) -> str:
    """
    Summarize what we know about a user's patterns.
    Mock version — replace with real Hindsight reflect() call later.
    """
    profile = _memory_store.get(user_id)
    if not profile or not profile.patterns:
        return "No behavioral history found for this user yet."

    pattern_summary = ", ".join(
        f"{p.pattern} (confidence: {p.confidence})"
        for p in profile.patterns[-5:]  # last 5 patterns only
    )

    return (
        f"User {user_id} has completed {profile.total_sessions} session(s). "
        f"Recent patterns: {pattern_summary}. "
        f"Use this to adapt your hints accordingly."
    )