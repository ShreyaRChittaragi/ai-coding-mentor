"""
tests/test_feedback_service.py — Person 3 tests
Run: python -m pytest tests/test_feedback_service.py -v
"""

import pytest
from unittest.mock import MagicMock, patch
from app.services.prompt_builder import PromptBuilder
from app.services.feedback_service import (
    FeedbackService,
    DUMMY_EVAL_RESULT,
    DUMMY_USER_PROFILE,
    DUMMY_PROBLEM,
    DUMMY_CODE,
    extract_pattern_info,
    extract_eval_info,
)


class TestExtractors:
    def test_extract_pattern_info_returns_latest(self):
        profile = {
            "user_id": "u1",
            "patterns": [
                {"pattern": "guessing", "confidence": 0.5, "mistake_type": None},
                {"pattern": "overthinking", "confidence": 0.78, "mistake_type": "edge_case"},
            ]
        }
        result = extract_pattern_info(profile)
        assert result["pattern"] == "overthinking"
        assert result["confidence"] == 0.78
        assert result["mistake_type"] == "edge_case"

    def test_extract_pattern_info_empty_patterns(self):
        profile = {"user_id": "u1", "patterns": []}
        result = extract_pattern_info(profile)
        assert result["pattern"] == "unknown"
        assert result["confidence"] == 0.0

    def test_extract_eval_info_failed(self):
        eval_result = {
            "passed": False,
            "score": 1,
            "total": 3,
            "errors": ["IndexError: list index out of range"],
            "edge_case_results": [
                {"input": {}, "expected": 0, "actual": None, "passed": False}
            ],
            "execution_time_ms": 42,
        }
        result = extract_eval_info(eval_result)
        assert result["passed"] == False
        assert "IndexError" in result["error"]
        assert len(result["failed_cases"]) == 1

    def test_extract_eval_info_passed(self):
        eval_result = {
            "passed": True,
            "score": 3,
            "total": 3,
            "errors": [],
            "edge_case_results": [],
            "execution_time_ms": 20,
        }
        result = extract_eval_info(eval_result)
        assert result["passed"] == True
        assert result["error"] is None


class TestPromptBuilder:
    def setup_method(self):
        self.builder = PromptBuilder()

    def test_hint_prompt_returns_two_strings(self):
        sys_p, usr_p = self.builder.build_hint_prompt(
            problem_title="Two Sum",
            problem_description="Find two numbers that add up to target.",
            user_code="def two_sum(nums, target): pass",
            eval_result=extract_eval_info(DUMMY_EVAL_RESULT),
            user_profile=extract_pattern_info(DUMMY_USER_PROFILE),
        )
        assert isinstance(sys_p, str) and isinstance(usr_p, str)

    def test_hint_prompt_contains_problem_title(self):
        _, usr_p = self.builder.build_hint_prompt(
            problem_title="Two Sum",
            problem_description="Find two numbers.",
            user_code="pass",
            eval_result=extract_eval_info(DUMMY_EVAL_RESULT),
            user_profile=extract_pattern_info(DUMMY_USER_PROFILE),
        )
        assert "Two Sum" in usr_p

    def test_hint_prompt_contains_pattern(self):
        _, usr_p = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass",
            eval_result=extract_eval_info(DUMMY_EVAL_RESULT),
            user_profile=extract_pattern_info(DUMMY_USER_PROFILE),
        )
        assert "overthinking" in usr_p

    def test_encouragement_prompt(self):
        _, usr_p = self.builder.build_encouragement_prompt(
            problem_title="Two Sum", attempts=5, pattern="overthinking"
        )
        assert "5" in usr_p

    def test_success_feedback_prompt(self):
        _, usr_p = self.builder.build_success_feedback_prompt(
            problem_title="Two Sum",
            user_code="def two_sum(nums, target): ...",
            attempts=2,
        )
        assert "Two Sum" in usr_p and "2" in usr_p


class TestFeedbackService:
    def setup_method(self):
        with patch("app.services.feedback_service.GroqClient") as mock_groq:
            mock_instance = MagicMock()
            mock_instance.chat.return_value = "Mocked response."
            mock_groq.return_value = mock_instance
            self.service = FeedbackService(api_key="fake-key")

    def test_failed_returns_hint(self):
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=DUMMY_EVAL_RESULT, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["status"] == "failed"
        assert result["hint"] is not None
        assert result["success_feedback"] is None

    def test_passed_returns_success_feedback(self):
        passed_eval = {**DUMMY_EVAL_RESULT, "passed": True}
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=passed_eval, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["status"] == "passed"
        assert result["success_feedback"] is not None
        assert result["hint"] is None

    def test_encouragement_triggered_at_threshold(self):
        many_attempts = {**DUMMY_EVAL_RESULT, "passed": False, "total": 4}
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=many_attempts, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["encouragement"] is not None

    def test_encouragement_not_triggered_below_threshold(self):
        few_attempts = {**DUMMY_EVAL_RESULT, "passed": False, "total": 1}
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=few_attempts, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["encouragement"] is None

    def test_get_hint_only_returns_string(self):
        result = self.service.get_hint_only(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=DUMMY_EVAL_RESULT, user_profile=DUMMY_USER_PROFILE,
        )
        assert isinstance(result, str)

    def test_get_encouragement_returns_string(self):
        result = self.service.get_encouragement(
            problem_title="Two Sum", attempts=5, pattern="guessing"
        )
        assert isinstance(result, str)