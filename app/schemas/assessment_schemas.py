from typing import Any, List, Optional
from pydantic import BaseModel, Field


class AssessmentAnswerItem(BaseModel):
    """Answer provided for a single assessment question."""

    question_id: str = Field(..., description="ID of the assessment question")
    user_response: Any = Field(..., description="User's selected option key, word, text, or multiple answers")


class AssessmentSubmissionRequest(BaseModel):
    """Payload for submitting a completed diagnostic or progression assessment."""

    assessment_id: Optional[str] = Field(None, description="Assessment ID (optional if goal_slug is provided)")
    answers: List[AssessmentAnswerItem] = Field(..., min_length=1, description="List of answers submitted")
