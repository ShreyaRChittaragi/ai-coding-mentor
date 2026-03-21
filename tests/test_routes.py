from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ===== TEST 1: Root =====
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("PASS ✅ root")

# ===== TEST 2: Health =====
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("PASS ✅ health")

# ===== TEST 3: Get Problem =====
def test_get_problem():
    response = client.get("/get_problem/p001")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data or "problem_id" in data or "title" in data
    print("PASS ✅ get_problem")

# ===== TEST 4: Get All Problems =====
def test_get_all_problems():
    response = client.get("/problems")
    assert response.status_code == 200
    print("PASS ✅ get all problems")

# ===== TEST 5: Submit Code =====
def test_submit_code():
    response = client.post("/submit_code", json={
        "user_id": "test_user",
        "problem_id": "p001",
        "code": "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i",
        "language": "python",
        "time_taken": 60.0,
        "attempt_number": 1,
        "code_edit_count": 3
    })
    assert response.status_code == 200
    data = response.json()
    assert "passed_count" in data
    assert "all_passed" in data
    print("PASS ✅ submit_code")

# ===== TEST 6: Get Feedback =====
def test_get_feedback():
    response = client.post(
        "/get_feedback?user_id=test_user&problem_id=p001&code=def two_sum(nums, target): return []"
    )
    assert response.status_code == 200
    data = response.json()
    assert "feedback" in data
    print("PASS ✅ get_feedback") 

# ===== TEST 7: User Profile =====
def test_user_profile():
    response = client.get("/user_profile/test_user")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    print("PASS ✅ user_profile")

# ===== TEST 8: Visualizations =====
def test_visualizations():
    response = client.get("/visualizations/test_user")
    assert response.status_code == 200
    data = response.json()
    assert "pattern_trends" in data
    assert "pattern_trends" in data
    assert "total_sessions" in data 
    print("PASS ✅ visualizations")