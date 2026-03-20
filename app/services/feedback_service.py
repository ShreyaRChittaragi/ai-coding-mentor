"""
feedback_service.py — Person 3 (LLM & Feedback Service)
Main orchestrator. Combines PromptBuilder + GroqClient to generate
adaptive hints, encouragement, and success feedback.
Place: app/services/feedback_service.py
"""

from app.services.groq_client import GroqClient
from app.services.prompt_builder import PromptBuilder


# ── Dummy data for development (swap when P2 + P1 PRs merge) ──────────────────

DUMMY_EVAL_RESULT = {
    "passed": False,
    "error": "IndexError: list index out of range",
    "error_type": "IndexError",
    "attempts": 3,
    "failed_cases": ["Input: [], Expected: 0", "Input: [1], Expected: 1"],
}

DUMMY_USER_PROFILE = {
    "pattern": "overthinking",
    "confidence": 0.78,
    "mistake_type": "edge_case",
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
        passed = eval_result.get("passed", False)
        attempts = eval_result.get("attempts", 1)
        pattern = user_profile.get("pattern", "unknown")

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
                eval_result=eval_result,
                user_profile=user_profile,
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
        sys_p, usr_p = self.builder.build_hint_prompt(
            problem_title=problem.get("title", ""),
            problem_description=problem.get("description", ""),
            user_code=user_code,
            eval_result=eval_result,
            user_profile=user_profile,
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
# Run: python -m app.services.feedback_service

if __name__ == "__main__":
    import json
    from dotenv import load_dotenv
    load_dotenv()

    print("🔧 Running FeedbackService with dummy data...\n")
    service = FeedbackService()
    feedback = service.get_feedback(
        problem=DUMMY_PROBLEM,
        user_code=DUMMY_CODE,
        eval_result=DUMMY_EVAL_RESULT,
        user_profile=DUMMY_USER_PROFILE,
    )
    print(json.dumps(feedback, indent=2))