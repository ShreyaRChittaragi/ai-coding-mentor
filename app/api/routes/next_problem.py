from fastapi import APIRouter
from app.memory.adaptive_selector import get_next_problem, get_dominant_pattern

router = APIRouter()

@router.get("/next_problem/{user_id}")
def next_problem(user_id: str, current_problem_id: str = None):
    """
    Returns the best next problem for a user
    based on their behavioral memory.
    """
    result = get_next_problem(
        user_id=user_id,
        current_problem_id=current_problem_id
    )
    return {
        "user_id": user_id,
        "dominant_pattern": result["pattern_used"],
        "reason": result["reason"],
        "next_problem": result["problem"]
    }

@router.get("/user_pattern/{user_id}")
def user_pattern(user_id: str):
    """Quick check — what pattern does this user currently show?"""
    pattern = get_dominant_pattern(user_id)
    return {
        "user_id": user_id,
        "dominant_pattern": pattern
    }