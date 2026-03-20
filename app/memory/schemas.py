from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatternRecord(BaseModel):
    pattern: str                    # e.g. "overthinking"
    confidence: float               # e.g. 0.78
    mistake_type: Optional[str]     # e.g. "edge_case"
    detected_at: datetime = datetime.now()

class UserMemoryProfile(BaseModel):
    user_id: str
    total_sessions: int = 0
    patterns: list[PatternRecord] = []
    last_active: Optional[datetime] = None
    notes: Optional[str] = None     # LLM-generated summary (added later)