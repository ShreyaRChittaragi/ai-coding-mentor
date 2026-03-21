from fastapi import APIRouter
from app.models import FeedbackOut
from app.services.feedback_service import FeedbackService
from app.services.problem_store import get_problem_by_id
from app.memory.hindsight import retrieve_memory
from dotenv import load_dotenv
import os

load_dotenv()  # ← this loads .env file

router = APIRouter()
service = FeedbackService(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/get_feedback")
def get_feedback(user_id: str, problem_id: str):
    # Get problem details
    problem = get_problem_by_id(problem_id)
    if not problem:
        problem = {
            "title": problem_id,
            "description": "Solve the given problem."
        }

    # Get user memory profile
    user_profile = retrieve_memory(user_id)

    # Dummy eval result
    eval_result = {
        "passed": False,
        "score": 0,
        "total": 3,
        "errors": ["IndexError: list index out of range"],
        "edge_case_results": [],
        "execution_time_ms": 42,
    }

    # Get real AI feedback from Groq
    feedback = service.get_feedback(
        problem=problem,
        user_code="# no code submitted yet",
        eval_result=eval_result,
        user_profile=user_profile,
    )

    pattern = None
    patterns = user_profile.get("patterns", [])
    if patterns:
        pattern = patterns[-1].get("pattern")

    return FeedbackOut(
        user_id=user_id,
        problem_id=problem_id,
        feedback=feedback.get("hint") or feedback.get("success_feedback") or "",
        pattern_detected=pattern
    )