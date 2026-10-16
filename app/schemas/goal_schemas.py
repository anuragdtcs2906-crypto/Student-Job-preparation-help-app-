from typing import List, Optional
from pydantic import BaseModel, Field


class GoalSelectRequest(BaseModel):
    """Payload for selecting one or more goals."""

    goal_slugs: List[str] = Field(..., min_length=1, description="List of goal slugs to activate (e.g. ['pronunciation', 'interview'])")


class DailyTargetUpdateRequest(BaseModel):
    """Payload for updating target quantity for a goal."""

    target_quantity: int = Field(..., ge=1, le=100, description="Daily quantity of content items (e.g. 10 words, 20 questions)")
    target_type: Optional[str] = Field(None, description="Optional target unit (e.g. words, questions, tasks, exercises)")
