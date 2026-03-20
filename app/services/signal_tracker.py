from app.models import EvalResult, CodeSubmission

def capture_signals(submission: CodeSubmission, result: EvalResult) -> dict:
    """
    Takes raw submission + eval result, returns structured behavioral signals.
    This feeds into the cognitive analyzer.
    """
    error_types = classify_errors(result.error_types)

    return {
        "user_id": submission.user_id,
        "problem_id": submission.problem_id,
        "attempt_number": submission.attempt_number,
        "time_taken_sec": submission.time_taken,
        "code_edit_count": submission.code_edit_count,
        "all_passed": result.all_passed,
        "passed_count": result.passed_count,
        "total_cases": result.total,
        "execution_time_ms": result.execution_time_ms,
        "error_types": error_types,
        "failed_cases": [
            ec for ec in result.edge_case_results if not ec.get("passed")
        ]
    }

def classify_errors(errors: list[str]) -> list[str]:
    """
    Convert raw error strings into clean category labels.
    """
    categories = []
    for e in errors:
        e_lower = e.lower()
        if "syntax" in e_lower:
            categories.append("syntax_error")
        elif "time limit" in e_lower or "timeout" in e_lower:
            categories.append("timeout")
        elif "nameerror" in e_lower or "not defined" in e_lower:
            categories.append("undefined_variable")
        elif "typeerror" in e_lower:
            categories.append("type_error")
        elif "indexerror" in e_lower:
            categories.append("index_error")
        elif "not found" in e_lower:
            categories.append("missing_function")
        else:
            categories.append("runtime_error")
    return categories