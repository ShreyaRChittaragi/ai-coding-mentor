from fastapi import APIRouter, HTTPException
from app.models import ProblemOut

router = APIRouter()

# Static routes FIRST
@router.get("/problems")
def get_all_problems():
    return []

@router.get("/problems/difficulty/{difficulty}")
def get_problems_by_difficulty(difficulty: str):
    return []

# Dynamic route LAST
@router.get("/get_problem/{problem_id}")
def get_problem(problem_id: str):
    # problem_store will handle this — placeholder for now
    return {
        "problem_id": problem_id,
        "title": "Placeholder",
        "description": "Problem will load from problem_store",
        "difficulty": "easy",
        "tags": [],
        "function_signature": "def solution():"
    }