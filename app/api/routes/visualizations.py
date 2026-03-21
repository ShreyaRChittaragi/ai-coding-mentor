from fastapi import APIRouter
from app.memory.hindsight import retrieve_memory

router = APIRouter()

@router.get("/visualizations/{user_id}")
def get_visualizations(user_id: str):
    memory = retrieve_memory(user_id)

    patterns = memory.get("patterns", [])
    total_sessions = memory.get("total_sessions", 0)

    if not patterns or total_sessions == 0:
        return {
            "user_id": user_id,
            "message": "No sessions yet",
            "pattern_trends": [],
            "mistake_categories": {},
            "dominant_pattern": None,
            "total_sessions": 0
        }

    # Build pattern trends from real data
    pattern_trends = [
        {
            "session": i + 1,
            "pattern": p["pattern"],
            "confidence": p["confidence"],
            "detected_at": p["detected_at"]
        }
        for i, p in enumerate(patterns)
    ]

    # Count mistake categories
    mistake_categories = {}
    for p in patterns:
        mistake = p.get("mistake_type") or p.get("pattern")
        if mistake:
            mistake_categories[mistake] = mistake_categories.get(mistake, 0) + 1

    # Find dominant pattern
    dominant = max(mistake_categories, key=mistake_categories.get) if mistake_categories else None

    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "pattern_trends": pattern_trends,
        "mistake_categories": mistake_categories,
        "dominant_pattern": dominant,
        "last_active": memory.get("last_active")
    }