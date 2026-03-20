from app.services.execution_service import run_user_code
from app.services.problem_store import get_problem_by_id, get_all_problems, get_problems_by_difficulty

def test_correct_solution():
    p = get_problem_by_id("p001")
    code = "def two_sum(nums, target):\n    seen={}\n    for i,n in enumerate(nums):\n        if target-n in seen: return [seen[target-n],i]\n        seen[n]=i"
    r = run_user_code(code, p["function_name"], p["test_cases"])
    assert r["all_passed"] == True        # was r["passed"]
    assert r["passed_count"] == r["total"]

def test_wrong_solution():
    p = get_problem_by_id("p001")
    code = "def two_sum(nums, target): return []"
    r = run_user_code(code, p["function_name"], p["test_cases"])
    assert r["all_passed"] == False       # was r["passed"]
    assert r["passed_count"] == 0

def test_syntax_error():
    p = get_problem_by_id("p001")
    code = "def two_sum(nums target):\n    pass"
    r = run_user_code(code, p["function_name"], p["test_cases"])
    assert r["all_passed"] == False       # was r["passed"]
    assert any("Syntax" in e for e in r["error_types"])  # was r["errors"]

def test_missing_function():
    p = get_problem_by_id("p001")
    code = "def wrong_name(): pass"
    r = run_user_code(code, p["function_name"], p["test_cases"])
    assert "not found" in r["error_types"][0]  # was r["errors"]

def test_all_problems_load():
    problems = get_all_problems()
    assert len(problems) > 0

def test_filter_by_difficulty():
    easy = get_problems_by_difficulty("easy")
    assert all(p["difficulty"] == "easy" for p in easy)