import json
import os
from typing import Optional
from app.services.problem_generator import get_generated_problem

PROBLEMS_FILE = os.path.join(os.path.dirname(__file__), "problems.json")

def load_problems() -> list[dict]:
    with open(PROBLEMS_FILE, "r") as f:
        return json.load(f)

def get_all_problems() -> list[dict]:
    return load_problems()

def get_problem_by_id(problem_id: str):
    # Check generated cache first
    if problem_id.startswith("gen_"):
        return get_generated_problem(problem_id)
    
    # Otherwise check problems.json
    problems = load_problems()
    for p in problems:
        if p["id"] == problem_id:
            return p
    return None


def get_problems_by_difficulty(difficulty: str) -> list[dict]:
    problems = load_problems()
    return [p for p in problems if p["difficulty"] == difficulty]

def get_problems_by_topic(topic: str) -> list[dict]:
    problems = load_problems()
    return [p for p in problems if p["topic"] == topic]