from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class StartPracticeSessionRequest(BaseModel):
    """Payload to begin a practice session."""

    goal_slug: str = Field(..., description="Slug of the goal (e.g. 'pronunciation', 'interview')")
    activity_type: Optional[str] = Field(None, description="Activity type (defaults to goal_slug)")
    target_count: Optional[int] = Field(None, ge=1, le=100, description="Optional custom item count override for this session")
    session_metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata (e.g. client device, UI mode)")


class SubmitPracticeAttemptRequest(BaseModel):
    """Payload to record an attempt on a practice item."""

    session_id: str = Field(..., description="Active practice session ID")
    content_type: str = Field(..., description="Content type (e.g. 'pronunciation_words', 'interview_questions')")
    content_id: str = Field(..., description="ID of the content item practiced")
    user_input: Optional[str] = Field(None, description="User's typed response, notes, or spoken transcript")
    is_completed: bool = Field(True, description="Whether the item was completed")
    marked_for_revision: bool = Field(False, description="Whether the user wants to revise this item again")
    time_spent_seconds: int = Field(0, ge=0, description="Actual seconds spent on this single item")
    request_ai_feedback: bool = Field(False, description="Whether to invoke AI feedback for this attempt")


class CompletePracticeSessionRequest(BaseModel):
    """Payload to wrap up a practice session."""

    duration_seconds: Optional[int] = Field(None, ge=0, description="Total session duration measured in seconds")
