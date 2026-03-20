from fastapi import APIRouter
from pydantic import BaseModel
from app.memory.hindsight import store_session, retrieve_memory
from app.memory.patterns import detect_patterns

router = APIRouter(prefix="/memory", tags=["Memory"])

class SessionData(BaseModel):
    user_id: str
    time_taken_seconds: int
    attempts: int
    error_types: list[str]
    solved: bool

@router.post("/store")
def store(data: SessionData):
    session_dict = data.model_dump()
    patterns = detect_patterns(session_dict)
    session_dict["patterns"] = patterns["patterns"]
    store_session(data.user_id, session_dict)
    return {"status": "stored", "patterns": patterns}

@router.get("/recall/{user_id}")
def recall(user_id: str):
    memory = retrieve_memory(user_id)
    return {"user_id": user_id, "memory": memory}