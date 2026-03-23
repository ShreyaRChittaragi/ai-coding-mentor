from app.services.cognitive_analyzer import analyze_patterns

guessing_signals = {
    "user_id": "user_001", "problem_id": "p001",
    "attempt_number": 1, "time_taken_sec": 8.0,
    "code_edit_count": 1, "all_passed": False,
    "passed_count": 0, "total_cases": 3,
    "execution_time_ms": 12, "error_types": [], "failed_cases": []
}
overthinking_signals = {
    "user_id": "user_001", "problem_id": "p001",
    "attempt_number": 3, "time_taken_sec": 150.0,
    "code_edit_count": 12, "all_passed": True,
    "passed_count": 3, "total_cases": 3,
    "execution_time_ms": 45, "error_types": [], "failed_cases": []
}
concept_gap_signals = {
    "user_id": "user_001", "problem_id": "p001",
    "attempt_number": 2, "time_taken_sec": 60.0,
    "code_edit_count": 4, "all_passed": False,
    "passed_count": 0, "total_cases": 3,
    "execution_time_ms": 8,
    "error_types": ["undefined_variable", "type_error"], "failed_cases": []
}
boundary_signals = {
    "user_id": "user_001", "problem_id": "p001",
    "attempt_number": 2, "time_taken_sec": 90.0,
    "code_edit_count": 5, "all_passed": False,
    "passed_count": 2, "total_cases": 3,
    "execution_time_ms": 20, "error_types": [],
    "failed_cases": [{"input": {"nums": [3,3], "target": 6}, "expected": [0,1], "actual": None}]
}
rushing_signals = {
    "user_id": "user_001", "problem_id": "p001",
    "attempt_number": 1, "time_taken_sec": 5.0,
    "code_edit_count": 1, "all_passed": False,
    "passed_count": 0, "total_cases": 3,
    "execution_time_ms": 3,
    "error_types": ["syntax_error"], "failed_cases": []
}

def test_guessing():
    r = analyze_patterns(guessing_signals)
    assert r["dominant_pattern"] == "guessing"

def test_overthinking():
    r = analyze_patterns(overthinking_signals)
    assert r["dominant_pattern"] == "overthinking"

def test_concept_gap():
    r = analyze_patterns(concept_gap_signals)
    assert r["dominant_pattern"] == "concept_gap"

def test_boundary_weakness():
    r = analyze_patterns(boundary_signals)
    assert r["dominant_pattern"] == "boundary_weakness"

def test_rushing():
    r = analyze_patterns(rushing_signals)
    assert r["dominant_pattern"] == "rushing"