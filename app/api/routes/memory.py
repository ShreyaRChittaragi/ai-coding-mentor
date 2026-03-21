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
from app.memory.adaptive import get_adaptive_context, build_llm_prompt

class AdaptiveRequest(BaseModel):
    user_id: str
    problem: str
    user_code: str
    topic: str

@router.post("/adaptive-prompt")
def adaptive_prompt(data: AdaptiveRequest):
    prompt = build_llm_prompt(
        user_id=data.user_id,
        problem=data.problem,
        user_code=data.user_code,
        topic=data.topic
    )
    return {"user_id": data.user_id, "prompt": prompt}

@router.get("/adaptive-context/{user_id}/{topic}")
def adaptive_context(user_id: str, topic: str):
    context = get_adaptive_context(user_id=user_id, topic=topic)
    return context