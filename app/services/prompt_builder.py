"""
prompt_builder.py — Person 3 (LLM & Feedback Service)
Builds structured prompts from evaluation results and user memory profile.
Place: app/services/prompt_builder.py
"""


BASE_SYSTEM_PROMPT = """You are a smart, encouraging coding tutor.
Your job is to help students improve their programming skills through personalized hints and feedback.

Rules:
- Never give away the full solution directly.
- Tailor your tone and depth to the student's pattern (overthinking, guessing, edge_case, etc.)
- Be concise — max 4 sentences per hint unless asked for more.
- Always end with one encouraging sentence.
- Use simple language. Avoid jargon unless the student clearly knows it.
"""

PATTERN_TONE_MAP = {
    "overthinking": (
        "The student tends to overthink. Keep hints short and direct. "
        "Tell them to trust their instinct and start with the simplest approach."
    ),
    "guessing": (
        "The student tends to guess randomly. Push them to reason step by step. "
        "Ask a guiding question to help them think it through logically."
    ),
    "edge_case": (
        "The student misses edge cases often. Gently remind them to think about "
        "boundary conditions: empty inputs, zero, negative numbers, large values."
    ),
    "slow_starter": (
        "The student takes a long time to start. Give a small nudge to break the "
        "problem into the first tiny step."
    ),
    "rushing": (
        "The student rushes and submits too quickly. Encourage them to re-read "
        "the problem and trace through their logic before submitting."
    ),
    "unknown": (
        "No known pattern yet. Give a balanced, encouraging hint."
    ),
}


class PromptBuilder:

    def build_hint_prompt(
        self,
        problem_title: str,
        problem_description: str,
        user_code: str,
        eval_result: dict,
        user_profile: dict,
    ) -> tuple[str, str]:
        pattern = user_profile.get("pattern", "unknown")
        tone_instruction = PATTERN_TONE_MAP.get(pattern, PATTERN_TONE_MAP["unknown"])
        system_prompt = BASE_SYSTEM_PROMPT + f"\n\nTone instruction: {tone_instruction}"

        passed = eval_result.get("passed", False)
        error = eval_result.get("error") or "None"
        error_type = eval_result.get("error_type") or "None"
        attempts = eval_result.get("attempts", 1)
        failed_cases = eval_result.get("failed_cases", [])
        confidence = user_profile.get("confidence", 0.0)

        status_line = "✅ All tests passed!" if passed else "❌ Some tests are failing."
        failed_cases_text = (
            "\n".join(f"  - {c}" for c in failed_cases[:3])
            if failed_cases else "  None listed."
        )

        user_message = f"""
Problem: {problem_title}
Description: {problem_description}

Student's current code:
```python
{user_code}
```

Evaluation result: {status_line}
Error: {error}
Error type: {error_type}
Attempts so far: {attempts}
Failed test cases:
{failed_cases_text}

Student profile:
  - Detected pattern: {pattern} (confidence: {confidence:.0%})
  - Common mistake type: {user_profile.get('mistake_type', 'unknown')}

Please give a helpful, personalized hint to guide this student toward the correct solution.
""".strip()

        return system_prompt, user_message

    def build_encouragement_prompt(
        self,
        problem_title: str,
        attempts: int,
        pattern: str,
    ) -> tuple[str, str]:
        tone_instruction = PATTERN_TONE_MAP.get(pattern, PATTERN_TONE_MAP["unknown"])
        system_prompt = BASE_SYSTEM_PROMPT + f"\n\nTone instruction: {tone_instruction}"
        user_message = (
            f"The student has attempted '{problem_title}' {attempts} times and is still stuck. "
            f"Write a short (2–3 sentence) motivational message to keep them going. "
            f"Don't give hints — just encouragement."
        )
        return system_prompt, user_message

    def build_success_feedback_prompt(
        self,
        problem_title: str,
        user_code: str,
        attempts: int,
    ) -> tuple[str, str]:
        system_prompt = BASE_SYSTEM_PROMPT
        user_message = f"""
The student just solved '{problem_title}' after {attempts} attempt(s).
Here is their accepted code:
```python
{user_code}
```
Congratulate them briefly, then give ONE optional improvement tip
(readability, efficiency, or Pythonic style). Keep it to 3 sentences max.
""".strip()
        return system_prompt, user_message