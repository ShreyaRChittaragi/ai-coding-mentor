from pydantic import BaseModel
from typing import List, Optional

class CodeSubmission(BaseModel):
    user_id: str
    problem_id: str
    code: str
    language: str = "python"
    time_taken: float
    attempt_number: int
    code_edit_count: int

class ProblemOut(BaseModel):
    problem_id: str
    title: str
    description: str
    difficulty: str
    tags: List[str]
    function_signature: str

class EvalResult(BaseModel):
    passed_count: int
    total: int
    all_passed: bool
    error_types: List[str]

class FeedbackOut(BaseModel):
    user_id: str
    problem_id: str
    feedback: str
    pattern_detected: Optional[str] = None

class UserProfile(BaseModel):
    user_id: str
    total_submissions: int
    detected_patterns: List[str]
    weak_areas: List[str]
    summary: dict