from fastapi import APIRouter
from app.memory.hindsight import retrieve_memory 

router = APIRouter()

@router.get("/visualizations/{user_id}")
def get_visualizations(user_id: str):
    memory = retrieve_memory(user_id)

    if not memory or memory["total_sessions"] == 0:
        return {
            "user_id": user_id,
            "message": "No sessions yet — showing sample data",
            "pattern_trends": [
                {"session": 1, "pattern": "guessing",     "confidence": 0.8},
                {"session": 2, "pattern": "guessing",     "confidence": 0.7},
                {"session": 3, "pattern": "overthinking", "confidence": 0.6},
                {"session": 4, "pattern": "concept_gap",  "confidence": 0.5},
                {"session": 5, "pattern": "overthinking", "confidence": 0.4}
            ],
            "accuracy_improvement": [
                {"session": 1, "passed": 1, "total": 3},
                {"session": 2, "passed": 2, "total": 3},
                {"session": 3, "passed": 2, "total": 3},
                {"session": 4, "passed": 3, "total": 3},
                {"session": 5, "passed": 3, "total": 3}
            ],
            "mistake_categories": {
                "edge_case": 3,
                "logic":     2,
                "syntax":    1,
                "timeout":   0
            },
            "dominant_pattern": "guessing",
            "total_sessions": 5
        }

    return {
        "user_id": user_id,
        "pattern_trends": memory.get("patterns", []),
        "total_sessions": memory.get("total_sessions", 0),
        "dominant_pattern": memory.get("dominant_pattern", None),
        "last_active": memory.get("last_active", None)
    }