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
def get_feedback(user_id: str, problem_id: str, code: str):
    problem = get_problem_by_id(problem_id)
    if not problem:
        problem = {"title": problem_id, "description": "Solve the given problem."}

    # Run actual code instead of dummy data
    from app.services.execution_service import run_user_code
    result_dict = run_user_code(
        user_code=code,
        function_name=problem.get("function_name", "solution"),
        test_cases=problem.get("test_cases", [])
    )

    user_profile = retrieve_memory(user_id)

    feedback = service.get_feedback(
        problem=problem,
        user_code=code,
        eval_result=result_dict,   # real result now
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
