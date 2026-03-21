from fastapi import APIRouter, HTTPException
from app.models import CodeSubmission, EvalResult
from app.services.execution_service import run_user_code
from app.services.problem_store import get_problem_by_id
from app.services.signal_tracker import capture_signals
from app.services.cognitive_analyzer import analyze_patterns
from app.memory.hindsight import store_session

router = APIRouter()

@router.post("/submit_code", response_model=EvalResult)
def submit_code(submission: CodeSubmission):
    # Step 1: Load problem
    problem = get_problem_by_id(submission.problem_id)
    if not problem:
        raise HTTPException(
            status_code=404,
            detail=f"Problem '{submission.problem_id}' not found"
        )

    # Step 2: Run the code
    result_dict = run_user_code(
        user_code=submission.code,
        function_name=problem["function_name"],
        test_cases=problem["test_cases"]
    )

    result = EvalResult(**result_dict)

    # Step 3: Capture behavioral signals
    signals = capture_signals(submission, result)

    # Step 4: Analyze into cognitive patterns
    patterns = analyze_patterns(signals)

    # Step 5: Store into memory
    store_session(
        user_id=submission.user_id,
        session_data={
            "patterns": patterns["patterns"],
            "time_taken_seconds": signals["time_taken_sec"],
            "attempts": signals["attempt_number"],
            "solved": result.all_passed,
            "problem_id": submission.problem_id,
            "dominant_pattern": patterns["dominant_pattern"],
            "dominant_confidence": patterns["dominant_confidence"]
        }
    )

    return result