# Hindsight SDK mock — replace with real SDK once confirmed
# from hindsight import Hindsight

from app.core.config import settings

# In-memory store to simulate Hindsight (temporary)
_memory_store: dict = {}

def store_session(user_id: str, session_data: dict):
    """Store a coding session's behavioral signals."""
    if user_id not in _memory_store:
        _memory_store[user_id] = []
    _memory_store[user_id].append(session_data)
    print(f"[Memory] Stored session for {user_id}: {session_data}")

def retrieve_memory(user_id: str) -> list:
    """Retrieve all stored sessions for a user."""
    return _memory_store.get(user_id, [])