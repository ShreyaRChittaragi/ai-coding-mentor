from fastapi import APIRouter, HTTPException
from app.services.problem_store import (
    get_problem_by_id,
    get_all_problems,
    get_problems_by_difficulty,
    get_problems_by_topic
)

router = APIRouter()

# STATIC routes first — always before dynamic {problem_id}
@router.get("/problems")
def list_problems():
    return get_all_problems()

@router.get("/problems/difficulty/{difficulty}")
def problems_by_difficulty(difficulty: str):
    problems = get_problems_by_difficulty(difficulty)
    if not problems:
        raise HTTPException(
            status_code=404,
            detail=f"No problems found with difficulty '{difficulty}'"
        )
    return problems

@router.get("/problems/topic/{topic}")
def problems_by_topic(topic: str):
    problems = get_problems_by_topic(topic)
    if not problems:
        raise HTTPException(
            status_code=404,
            detail=f"No problems found for topic '{topic}'"
        )
    return problems

# DYNAMIC route last — otherwise it swallows everything above
@router.get("/get_problem/{problem_id}")
def get_problem(problem_id: str):
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(
            status_code=404,
            detail=f"Problem '{problem_id}' not found"
        )
    return problem