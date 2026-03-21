import time
import traceback
import threading

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


def run_user_code(user_code: str, function_name: str, test_cases: list[dict]) -> dict:
    namespace = {}
    edge_case_results = []
    errors = []
    passed_count = 0
    total = len(test_cases)
    start_time = time.monotonic()

    # Step 1: Compile and execute user code
    try:
        exec(compile(user_code, "<user_code>", "exec"), namespace)
    except SyntaxError as e:
        return _error_result(f"Syntax error: {e}", total, start_time)
    except Exception as e:
        return _error_result(f"Runtime error on load: {e}", total, start_time)

    # Step 2: Check function exists
    if function_name not in namespace:
        return _error_result(
            f"Function '{function_name}' not found. Make sure you define it exactly as asked.",
            total, start_time
        )

    user_fn = namespace[function_name]

    # Step 3: Run each test case with timeout
    for i, tc in enumerate(test_cases):
        input_args = tc["input"]
        expected = tc["expected"]

        r = _run_with_timeout(user_fn, input_args, timeout_sec=5)

        if r["error"]:
            errors.append(f"Test case {i}: {r['error']}")
            edge_case_results.append({
                "case_index": i,
                "input": input_args,
                "expected": expected,
                "actual": None,
                "passed": False,
                "error": r["error"]
            })
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

    exec_time_ms = int((time.monotonic() - start_time) * 1000)

    return {
        "passed_count": passed_count,
        "total": total,
        "all_passed": passed_count == total,
        "error_types": errors,
        "edge_case_results": edge_case_results,
        "execution_time_ms": exec_time_ms
    }


def _error_result(message: str, total: int, start_time: float) -> dict:
    return {
        "passed_count": 0,
        "total": total,
        "all_passed": False,
        "error_types": [message],
        "edge_case_results": [],
        "execution_time_ms": int((time.monotonic() - start_time) * 1000)
    }