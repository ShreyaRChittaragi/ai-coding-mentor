"""
feedback_service.py — Person 3 (LLM & Feedback Service)
Updated to use real P1 + P2 data formats.
"""

from app.services.groq_client import GroqClient
from app.services.prompt_builder import PromptBuilder


# ── Real dummy data matching P1 + P2 actual formats ───────────────────────────

DUMMY_EVAL_RESULT = {
    "passed": False,
    "score": 1,
    "total": 3,
    "errors": ["IndexError: list index out of range"],
    "edge_case_results": [
        {"case_index": 0, "input": {}, "expected": 0, "actual": None, "passed": False},
        {"case_index": 1, "input": {"nums": [1]}, "expected": 1, "actual": None, "passed": False},
    ],
    "execution_time_ms": 42,
}

DUMMY_USER_PROFILE = {
    "user_id": "user_001",
    "total_sessions": 5,
    "patterns": [
        {
            "pattern": "overthinking",
            "confidence": 0.78,
            "mistake_type": "edge_case",
        }
    ],
    "last_active": None,
    "notes": None,
}

DUMMY_PROBLEM = {
    "title": "Two Sum",
    "description": (
        "Given an array of integers and a target, return indices of the two numbers "
        "that add up to the target."
    ),
}

DUMMY_CODE = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
""".strip()

ENCOURAGEMENT_THRESHOLD = 3


# ── Helpers to extract from real formats ─────────────────────────────────────

def extract_pattern_info(user_profile: dict) -> dict:
    """
    Extract pattern, confidence, mistake_type from P1's UserMemoryProfile.
    Gets the most recent pattern from the patterns list.
    """
    patterns = user_profile.get("patterns", [])
    if patterns:
        latest = patterns[-1]  # most recent pattern
        return {
            "pattern": latest.get("pattern", "unknown"),
            "confidence": latest.get("confidence", 0.0),
            "mistake_type": latest.get("mistake_type", None),
        }
    return {
        "pattern": "unknown",
        "confidence": 0.0,
        "mistake_type": None,
    }


def extract_eval_info(eval_result: dict) -> dict:
    """
    Extract clean info from P2's EvalResult for use in prompts.
    """
    errors = eval_result.get("errors", [])
    edge_cases = eval_result.get("edge_case_results", [])

    # Get failed cases as readable strings
    failed_cases = [
        f"Input: {r['input']}, Expected: {r['expected']}, Got: {r['actual']}"
        for r in edge_cases if not r.get("passed", True)
    ]

    return {
        "passed": eval_result.get("passed", False),
        "error": errors[0] if errors else None,
        "error_type": errors[0].split(":")[0] if errors else None,
        "attempts": eval_result.get("score", 0),
        "failed_cases": failed_cases,
        "execution_time_ms": eval_result.get("execution_time_ms", 0),
    }


# ── Main Service ──────────────────────────────────────────────────────────────

class FeedbackService:
    def __init__(self, api_key: str = None):
        self.client = GroqClient(api_key=api_key)
        self.builder = PromptBuilder()

    def get_feedback(
        self,
        problem: dict,
        user_code: str,
        eval_result: dict,
        user_profile: dict,
    ) -> dict:
        """
        Full feedback response for a submission.

        eval_result → from P2's execution_service.py
        user_profile → from P1's UserMemoryProfile
        """
        # ── Extract clean data from real formats
        clean_eval = extract_eval_info(eval_result)
        clean_profile = extract_pattern_info(user_profile)

        passed = clean_eval["passed"]
        attempts = eval_result.get("total", 1)
        pattern = clean_profile["pattern"]

        result = {
            "hint": None,
            "encouragement": None,
            "success_feedback": None,
            "status": "passed" if passed else "failed",
        }

        if passed:
            sys_p, usr_p = self.builder.build_success_feedback_prompt(
                problem_title=problem.get("title", "this problem"),
                user_code=user_code,
                attempts=attempts,
            )
            result["success_feedback"] = self.client.chat(sys_p, usr_p)

        else:
            sys_p, usr_p = self.builder.build_hint_prompt(
                problem_title=problem.get("title", "this problem"),
                problem_description=problem.get("description", ""),
                user_code=user_code,
                eval_result=clean_eval,
                user_profile=clean_profile,
            )
            result["hint"] = self.client.chat(sys_p, usr_p)

            if attempts >= ENCOURAGEMENT_THRESHOLD:
                sys_e, usr_e = self.builder.build_encouragement_prompt(
                    problem_title=problem.get("title", "this problem"),
                    attempts=attempts,
                    pattern=pattern,
                )
                result["encouragement"] = self.client.chat(sys_e, usr_e)

        return result

    def get_hint_only(self, problem, user_code, eval_result, user_profile) -> str:
        clean_eval = extract_eval_info(eval_result)
        clean_profile = extract_pattern_info(user_profile)
        sys_p, usr_p = self.builder.build_hint_prompt(
            problem_title=problem.get("title", ""),
            problem_description=problem.get("description", ""),
            user_code=user_code,
            eval_result=clean_eval,
            user_profile=clean_profile,
        )
        return self.client.chat(sys_p, usr_p)

    def get_encouragement(self, problem_title: str, attempts: int, pattern: str) -> str:
        sys_p, usr_p = self.builder.build_encouragement_prompt(
            problem_title=problem_title,
            attempts=attempts,
            pattern=pattern,
        )
        return self.client.chat(sys_p, usr_p)


# ── Quick local test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    from dotenv import load_dotenv
    load_dotenv()

    print("🔧 Running FeedbackService with real format dummy data...\n")
    service = FeedbackService()
    feedback = service.get_feedback(
        problem=DUMMY_PROBLEM,
        user_code=DUMMY_CODE,
        eval_result=DUMMY_EVAL_RESULT,
        user_profile=DUMMY_USER_PROFILE,
    )
    print(json.dumps(feedback, indent=2))