from fastapi import APIRouter, HTTPException
from app.models import UserProfile

router = APIRouter()

@router.get("/user_profile/{user_id}")
def get_user_profile(user_id: str):
    # Hindsight memory will populate this
    return UserProfile(
        user_id=user_id,
        total_submissions=0,
        detected_patterns=[],
        weak_areas=[],
        summary={}
    )