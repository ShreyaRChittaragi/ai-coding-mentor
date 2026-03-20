import time
import traceback
from typing import Any
import signal   # won't work on Windows — use threading instead
import threading
from typing import Any

def run_user_code(user_code: str, function_name: str, test_cases: list[dict]) -> dict:
    """
    Safely run user-submitted code against test cases.

    Args:
        user_code:     The raw Python code string from the user
        function_name: The function the user must define (e.g. "two_sum")
        test_cases:    List of {"input": {...}, "expected": ...}

    Returns:
        Structured EvalResult dict
    """
    namespace = {}
    edge_case_results = []
    errors = []
    passed_count = 0
    total = len(test_cases)
    start_time = time.monotonic()

    # Step 1: Try compiling and executing the user code
    try:
        exec(compile(user_code, "<user_code>", "exec"), namespace)
    except SyntaxError as e:
        return _error_result(f"Syntax error: {e}", total, start_time)
    except Exception as e:
        return _error_result(f"Runtime error on load: {e}", total, start_time)

    # Step 2: Check the required function exists
    if function_name not in namespace:
        return _error_result(
            f"Function '{function_name}' not found. Make sure you define it exactly as asked.",
            total, start_time
        )

    user_fn = namespace[function_name]

    # Step 3: Run each test case with timeout protection
    for i, tc in enumerate(test_cases):
        input_args = tc["input"]
        expected = tc["expected"]
        try:
            r = _run_with_timeout(user_fn, input_args)
            if r["error"]:
                actual = None
                passed = False
                errors.append(f"Test case {i}: {r['error']}")
            else:
                actual = r["value"]
                passed = actual == expected
            if passed:
                passed_count += 1
            edge_case_results.append({
                "case_index": i,
                "input": input_args,
                "expected": expected,
                "actual": actual,
                "passed": passed
            })
        except Exception as e:
            err_msg = f"Test case {i} failed with error: {traceback.format_exc(limit=2)}"
            errors.append(err_msg)
            edge_case_results.append({
                "case_index": i,
                "input": input_args,
                "expected": expected,
                "actual": None,
                "passed": False,
                "error": str(e)
            })

    exec_time_ms = int((time.monotonic() - start_time) * 1000)

    return {
        "passed": passed_count == total,
        "score": passed_count,
        "total": total,
        "errors": errors,
        "edge_case_results": edge_case_results,
        "execution_time_ms": exec_time_ms
    }



def _error_result(message: str, total: int, start_time: float) -> dict:
    return {
        "passed": False,
        "score": 0,
        "total": total,
        "errors": [message],
        "edge_case_results": [],
        "execution_time_ms": int((time.monotonic() - start_time) * 1000)
    }

def _run_with_timeout(fn, kwargs, timeout_sec=5):
    result = {"value": None, "error": None}
    def target():
        try:
            result["value"] = fn(**kwargs)
        except Exception as e:
            result["error"] = str(e)
    t = threading.Thread(target=target)
    t.start()
    t.join(timeout=timeout_sec)
    if t.is_alive():
        result["error"] = "Time limit exceeded (5s)"
    return result