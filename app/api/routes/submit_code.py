from fastapi import APIRouter
from app.models import CodeSubmission, EvalResult

router = APIRouter()

@router.post("/submit_code")
def submit_code(submission: CodeSubmission):
    # execution_service will handle this — placeholder for now
    return {
        "user_id": submission.user_id,
        "problem_id": submission.problem_id,
        "status": "received",
        "message": "Code submitted successfully"
    }