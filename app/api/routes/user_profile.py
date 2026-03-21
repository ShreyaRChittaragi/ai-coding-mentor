from fastapi import APIRouter, HTTPException
from app.models import UserProfile
from app.memory.hindsight import retrieve_memory

router = APIRouter()

@router.get("/user_profile/{user_id}")
def get_user_profile(user_id: str):
    memory = retrieve_memory(user_id)

    if memory["total_sessions"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No profile found for user '{user_id}'. Submit a problem first."
        )

    # Extract unique weak areas from detected patterns
    weak_areas = list(set(
        p["pattern"] for p in memory["patterns"]
    ))

    # Build summary from memory
    summary = {
        "total_sessions": memory["total_sessions"],
        "last_active": str(memory["last_active"]),
        "dominant_pattern": weak_areas[0] if weak_areas else "none",
        "pattern_count": len(memory["patterns"])
    }

    return UserProfile(
        user_id=user_id,
        total_submissions=memory["total_sessions"],
        detected_patterns=weak_areas,
        weak_areas=weak_areas,
        summary=summary
    )