from app.services.execution_service import run_user_code
from app.services.problem_store import get_problem_by_id
from app.services.signal_tracker import capture_signals, classify_errors
from app.models import CodeSubmission, EvalResult

print("\n===== TEST 1: Correct solution =====")
p = get_problem_by_id("p001")
good_code = """
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
"""
result = run_user_code(good_code, p["function_name"], p["test_cases"])
print(result)
assert result["all_passed"] == True, "FAIL: should have passed"
print("PASS ✅")

print("\n===== TEST 2: Wrong solution =====")
bad_code = "def two_sum(nums, target): return []"
result2 = run_user_code(bad_code, p["function_name"], p["test_cases"])
print(result2)
assert result2["all_passed"] == False, "FAIL: should not have passed"
assert result2["passed_count"] == 0
print("PASS ✅")

print("\n===== TEST 3: Syntax error =====")
syntax_code = "def two_sum(nums target):\n    pass"
result3 = run_user_code(syntax_code, p["function_name"], p["test_cases"])
print(result3)
assert result3["all_passed"] == False
assert any("Syntax" in e for e in result3["error_types"])
print("PASS ✅")

print("\n===== TEST 4: Signal tracker =====")
submission = CodeSubmission(
    user_id="user_001",
    problem_id="p001",
    code=good_code,
    language="python",
    time_taken=45.5,
    attempt_number=1,
    code_edit_count=3
)
eval_result = EvalResult(**result)
signals = capture_signals(submission, eval_result)
print(signals)
assert signals["user_id"] == "user_001"
assert signals["all_passed"] == True
assert signals["attempt_number"] == 1
print("PASS ✅")

print("\n===== TEST 5: Error classifier =====")
labels = classify_errors(["SyntaxError: invalid syntax", "NameError: x not defined"])
print(labels)
assert "syntax_error" in labels
assert "undefined_variable" in labels
print("PASS ✅")

print("\n\n All tests passed! You're good to commit. 🚀")