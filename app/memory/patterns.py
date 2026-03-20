def detect_patterns(session: dict) -> dict:
    """
    Takes raw behavioral signals from a session
    and converts them into cognitive pattern labels.
    """
    patterns = []

    time_taken = session.get("time_taken_seconds", 0)
    attempts = session.get("attempts", 1)
    errors = session.get("error_types", [])

    # Overthinking — too much time, few attempts
    if time_taken > 600 and attempts <= 2:
        patterns.append("overthinking")

    # Guessing — many attempts, short time
    if attempts >= 5 and time_taken < 120:
        patterns.append("guessing")

    # Syntax struggles
    if errors.count("SyntaxError") >= 2:
        patterns.append("syntax_struggles")

    # Logic errors
    if errors.count("LogicError") >= 2:
        patterns.append("logic_gaps")

    # Gives up early
    if attempts == 1 and not session.get("solved", False):
        patterns.append("gives_up_early")

    return {
        "patterns": patterns,
        "summary": f"Detected {len(patterns)} pattern(s): {', '.join(patterns) if patterns else 'none'}"
    }