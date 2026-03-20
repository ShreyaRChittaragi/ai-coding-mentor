from fastapi import APIRouter, HTTPException
from app.models import CodeSubmission, EvalResult
from app.services.execution_service import run_user_code
from app.services.problem_store import get_problem_by_id
from app.services.signal_tracker import capture_signals

router = APIRouter()

@router.post("/submit_code", response_model=EvalResult)
def submit_code(submission: CodeSubmission):
    problem = get_problem_by_id(submission.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{submission.problem_id}' not found")

    result_dict = run_user_code(
        user_code=submission.code,
        function_name=problem["function_name"],
        test_cases=problem["test_cases"]
    )

    result = EvalResult(**result_dict)

    # Capture behavioral signals (Person 4's job — now yours)
    signals = capture_signals(submission, result)
    print(f"[signals] {signals}")   # temporary — Person 1 will store these in memory later

    return result