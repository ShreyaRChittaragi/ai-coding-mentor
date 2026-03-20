from fastapi import APIRouter, HTTPException
from app.models import CodeSubmission, EvalResult
from app.services.execution_service import run_user_code
from app.services.problem_store import get_problem_by_id
from app.services.signal_tracker import capture_signals
from app.services.cognitive_analyzer import analyze_patterns

router = APIRouter()

@router.post("/submit_code", response_model=EvalResult)
def submit_code(submission: CodeSubmission):
    problem = get_problem_by_id(submission.problem_id)
    if not problem:
        raise HTTPException(
            status_code=404,
            detail=f"Problem '{submission.problem_id}' not found"
        )

    result_dict = run_user_code(
        user_code=submission.code,
        function_name=problem["function_name"],
        test_cases=problem["test_cases"]
    )

    result = EvalResult(**result_dict)

    signals = capture_signals(submission, result)
    patterns = analyze_patterns(signals)

    # Temporary until Person 1's memory module is ready
    print(f"[signals]  {signals}")
    print(f"[patterns] {patterns}")

    return result