def analyze_patterns(signals: dict) -> dict:
    """
    Takes behavioral signals from signal_tracker,
    returns cognitive pattern labels with confidence scores.
    """
    patterns = []

    patterns += _check_overthinking(signals)
    patterns += _check_guessing(signals)
    patterns += _check_concept_gap(signals)
    patterns += _check_boundary_weakness(signals)
    patterns += _check_rushing(signals)

    top = max(patterns, key=lambda x: x["confidence"]) if patterns else None

    return {
        "user_id": signals["user_id"],
        "problem_id": signals["problem_id"],
        "patterns": patterns,
        "dominant_pattern": top["pattern"] if top else "none",
        "dominant_confidence": top["confidence"] if top else 0.0
    }


def _check_overthinking(signals: dict) -> list:
    """High edit count + long time + eventually passed"""
    score = 0.0
    if signals["code_edit_count"] > 8:
        score += 0.4
    if signals["time_taken_sec"] > 120:
        score += 0.3
    if signals["all_passed"]:
        score += 0.2
    if signals["attempt_number"] > 2:
        score += 0.1
    if score >= 0.4:
        return [{"pattern": "overthinking", "confidence": round(score, 2)}]
    return []


def _check_guessing(signals: dict) -> list:
    """Low time + low edits + failed — likely guessed without understanding"""
    score = 0.0
    if signals["time_taken_sec"] < 20:
        score += 0.4
    if signals["code_edit_count"] <= 1:
        score += 0.3
    if not signals["all_passed"]:
        score += 0.2
    if signals["passed_count"] == 0:
        score += 0.1
    if "syntax_error" in signals["error_types"]:
        score -= 0.4       # ← new line, syntax error means they typed code, not guessed
    if score >= 0.4:
        return [{"pattern": "guessing", "confidence": round(score, 2)}]
    return []


def _check_concept_gap(signals: dict) -> list:
    """Specific error types that show missing knowledge"""
    score = 0.0
    gap_errors = {"undefined_variable", "missing_function", "type_error"}
    matched = gap_errors & set(signals["error_types"])
    if matched:
        score += 0.5 * (len(matched) / len(gap_errors))
    if not signals["all_passed"] and signals["attempt_number"] >= 2:
        score += 0.3
    if signals["passed_count"] == 0:
        score += 0.2
    if score >= 0.4:
        return [{"pattern": "concept_gap", "confidence": round(score, 2)}]
    return []


def _check_boundary_weakness(signals: dict) -> list:
    """Passes most cases but fails edge cases"""
    score = 0.0
    total = signals["total_cases"]
    passed = signals["passed_count"]
    if total > 0:
        ratio = passed / total
        if 0.5 <= ratio < 1.0:
            score += 0.5
    failed = signals.get("failed_cases", [])
    if any("edge" in str(fc.get("input", "")).lower() for fc in failed):
        score += 0.3
    if signals["attempt_number"] >= 2:
        score += 0.2
    if score >= 0.4:
        return [{"pattern": "boundary_weakness", "confidence": round(score, 2)}]
    return []


def _check_rushing(signals: dict) -> list:
    """Very fast + syntax errors = didn't read carefully"""
    score = 0.0
    if signals["time_taken_sec"] < 15:
        score += 0.3
    if "syntax_error" in signals["error_types"]:
        score += 0.5       # ← bumped from 0.4, syntax error is the strongest signal
    if signals["code_edit_count"] <= 2:
        score += 0.2
    if score >= 0.4:
        return [{"pattern": "rushing", "confidence": round(score, 2)}]
    return []