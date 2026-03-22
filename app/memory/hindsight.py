from hindsight_client import Hindsight
from app.core.config import settings
from app.memory.schemas import UserMemoryProfile, PatternRecord
from datetime import datetime

# Real Hindsight Cloud client with API key
client = Hindsight(
    base_url=settings.HINDSIGHT_URL,
    api_key=settings.HINDSIGHT_API_KEY
)

BANK_ID = "coding-mentor"
_local_cache: dict[str, UserMemoryProfile] = {}



def store_session(user_id: str, session_data: dict):
    """Store behavioral session into Hindsight Cloud."""
    patterns = session_data.get("patterns", [])
    pattern_names = [
        p.get("pattern") if isinstance(p, dict) else p
        for p in patterns
    ]

    content = (
        f"User {user_id} completed a coding session. "
        f"Problem: {session_data.get('problem_id', 'unknown')}. "
        f"Patterns detected: {', '.join(pattern_names) if pattern_names else 'none'}. "
        f"Time taken: {session_data.get('time_taken_seconds', 0)}s. "
        f"Attempts: {session_data.get('attempts', 1)}. "
        f"Solved: {session_data.get('solved', False)}. "
        f"Dominant pattern: {session_data.get('dominant_pattern', 'none')} "
        f"(confidence: {session_data.get('dominant_confidence', 0)})."
    )

    client.retain(
        bank_id=BANK_ID,
        content=content,
        context=f"coding session for user {user_id}",
        metadata={"user_id": user_id}
    )

    # Update local cache too
    if user_id not in _local_cache:
        _local_cache[user_id] = UserMemoryProfile(user_id=user_id)

    profile = _local_cache[user_id]
    profile.total_sessions += 1
    profile.last_active = datetime.now()

    for p in patterns:
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
    """Retrieve user memory — local cache first, Hindsight Cloud as backup."""
    if user_id in _local_cache:
        return _local_cache[user_id].model_dump()

    # Try Hindsight Cloud recall
    try:
        results = client.recall(
            bank_id=BANK_ID,
            query=f"behavioral patterns of user {user_id}",
        )
        memories = [r.text for r in results.results] if results.results else []
        return {
            "user_id": user_id,
            "total_sessions": len(memories),
            "patterns": [],
            "last_active": None,
            "notes": " | ".join(memories) if memories else None
        }
    except Exception:
        return {
            "user_id": user_id,
            "total_sessions": 0,
            "patterns": [],
            "last_active": None,
            "notes": None
        }

def update_memory(user_id: str, new_pattern: PatternRecord):
    """Add a new pattern to user memory."""
    if user_id not in _local_cache:
        _local_cache[user_id] = UserMemoryProfile(user_id=user_id)
    _local_cache[user_id].patterns.append(new_pattern)

def reflect_on_user(user_id: str, question: str) -> str:
    """Use Hindsight reflect to reason about user patterns."""
    try:
        answer = client.reflect(
            bank_id=BANK_ID,
            query=question,
            budget="low",
            context=f"This question is about user {user_id}"
        )
        return answer.text if hasattr(answer, "text") else str(answer)
    except Exception:
        # Fallback to local cache
        profile = _local_cache.get(user_id)
        if not profile or not profile.patterns:
            return "No behavioral history found for this user yet."
        pattern_summary = ", ".join(
            f"{p.pattern} (confidence: {p.confidence})"
            for p in profile.patterns[-5:]
        )
        return (
            f"User {user_id} has completed {profile.total_sessions} session(s). "
            f"Recent patterns: {pattern_summary}."
        )