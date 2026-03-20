"""
tests/test_feedback_service.py — Person 3 tests
Run: pytest tests/test_feedback_service.py -v
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
)


class TestPromptBuilder:
    def setup_method(self):
        self.builder = PromptBuilder()

    def test_hint_prompt_returns_two_strings(self):
        sys_p, usr_p = self.builder.build_hint_prompt(
            problem_title="Two Sum",
            problem_description="Find two numbers that add up to target.",
            user_code="def two_sum(nums, target): pass",
            eval_result=DUMMY_EVAL_RESULT,
            user_profile=DUMMY_USER_PROFILE,
        )
        assert isinstance(sys_p, str) and isinstance(usr_p, str)

    def test_hint_prompt_contains_problem_title(self):
        _, usr_p = self.builder.build_hint_prompt(
            problem_title="Two Sum",
            problem_description="Find two numbers.",
            user_code="pass",
            eval_result=DUMMY_EVAL_RESULT,
            user_profile=DUMMY_USER_PROFILE,
        )
        assert "Two Sum" in usr_p

    def test_hint_prompt_contains_error(self):
        _, usr_p = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass", eval_result=DUMMY_EVAL_RESULT,
            user_profile=DUMMY_USER_PROFILE,
        )
        assert "IndexError" in usr_p

    def test_hint_prompt_contains_pattern(self):
        _, usr_p = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass", eval_result=DUMMY_EVAL_RESULT,
            user_profile=DUMMY_USER_PROFILE,
        )
        assert "overthinking" in usr_p

    def test_system_prompt_tone_overthinking(self):
        sys_p, _ = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass", eval_result=DUMMY_EVAL_RESULT,
            user_profile={"pattern": "overthinking", "confidence": 0.8},
        )
        assert "overthink" in sys_p.lower()

    def test_system_prompt_tone_guessing(self):
        sys_p, _ = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass", eval_result=DUMMY_EVAL_RESULT,
            user_profile={"pattern": "guessing", "confidence": 0.6},
        )
        assert "guess" in sys_p.lower() or "reason" in sys_p.lower()

    def test_unknown_pattern_fallback(self):
        sys_p, _ = self.builder.build_hint_prompt(
            problem_title="Test", problem_description="Test.",
            user_code="pass", eval_result=DUMMY_EVAL_RESULT,
            user_profile={"pattern": "nonexistent", "confidence": 0.5},
        )
        assert isinstance(sys_p, str)

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
            self.mock_client = mock_instance

    def test_failed_returns_hint(self):
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=DUMMY_EVAL_RESULT, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["status"] == "failed"
        assert result["hint"] is not None
        assert result["success_feedback"] is None

    def test_passed_returns_success_feedback(self):
        passed_eval = {**DUMMY_EVAL_RESULT, "passed": True, "attempts": 1}
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=passed_eval, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["status"] == "passed"
        assert result["success_feedback"] is not None
        assert result["hint"] is None

    def test_encouragement_triggered_at_threshold(self):
        many_attempts = {**DUMMY_EVAL_RESULT, "passed": False, "attempts": 4}
        result = self.service.get_feedback(
            problem=DUMMY_PROBLEM, user_code=DUMMY_CODE,
            eval_result=many_attempts, user_profile=DUMMY_USER_PROFILE,
        )
        assert result["encouragement"] is not None

    def test_encouragement_not_triggered_below_threshold(self):
        few_attempts = {**DUMMY_EVAL_RESULT, "passed": False, "attempts": 1}
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