from app.services.cognitive_analyzer import analyze_patterns

def detect_patterns(session: dict) -> dict:
    """
    Wrapper that delegates to cognitive_analyzer.
    Keeps memory route working while using one consistent
    pattern detection logic across the whole project.
    """
    # Map memory route field names → signal tracker field names
    signals = {
        "user_id": session.get("user_id", "unknown"),
        "problem_id": session.get("problem_id", "unknown"),
        "attempt_number": session.get("attempts", 1),
        "time_taken_sec": session.get("time_taken_seconds", 0),
        "code_edit_count": session.get("code_edit_count", 0),
        "all_passed": session.get("solved", False),
        "passed_count": session.get("passed_count", 0),
        "total_cases": session.get("total", 1),
        "execution_time_ms": session.get("execution_time_ms", 0),
        "error_types": session.get("error_types", []),
        "failed_cases": session.get("failed_cases", [])
    }

    result = analyze_patterns(signals)

    return {
        "patterns": result["patterns"],
        "summary": f"Detected {len(result['patterns'])} pattern(s): "
                   f"{result['dominant_pattern']} "
                   f"(confidence: {result['dominant_confidence']})"
    }