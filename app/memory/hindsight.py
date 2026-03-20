from hindsight_client import Hindsight
from app.core.config import settings

client = Hindsight(
    api_key=settings.HINDSIGHT_API_KEY,
    base_url=settings.HINDSIGHT_URL
)

BANK_ID = "coding-mentor"

def store_session(user_id: str, session_data: dict):
    content = (
        f"User {user_id} completed a session. "
        f"Patterns: {session_data.get('patterns', [])}. "
        f"Time: {session_data.get('time_taken_seconds')}s. "
        f"Attempts: {session_data.get('attempts')}. "
        f"Solved: {session_data.get('solved')}."
    )
    client.retain(
        bank_id=BANK_ID,
        text=content,
        metadata={"user_id": user_id}
    )

def retrieve_memory(user_id: str) -> dict:
    results = client.recall(
        bank_id=BANK_ID,
        query=f"behavioral patterns of user {user_id}",
        filters={"user_id": user_id}
    )
    return {"user_id": user_id, "memory": results}

def reflect_on_user(user_id: str, question: str) -> str:
    response = client.reflect(
        bank_id=BANK_ID,
        query=question,
        filters={"user_id": user_id}
    )
    return response