from typing import List, Optional
from pydantic import BaseModel, Field


class AIEvaluationRequest(BaseModel):
    """Payload to request AI qualitative feedback for any communication practice input."""

    goal_slug: str = Field(..., description="Goal slug (e.g. 'interview', 'presentation', 'gd')")
    prompt_context: str = Field(..., description="The question, task prompt, or discussion topic")
    user_response: str = Field(..., min_length=2, description="The user's response text to evaluate")
    category: Optional[str] = Field(None, description="Category (e.g. 'Behavioral', 'Self-Intro')")
    level: Optional[int] = Field(1, ge=1, le=5, description="Current user level")


class AIFeedbackStructured(BaseModel):
    """Standardized structured schema returned by the AI Feedback Engine."""

    strengths: List[str] = Field(default_factory=list, description="Positive elements identified in response")
    areas_to_improve: List[str] = Field(default_factory=list, description="Constructive, supportive focus areas")
    feedback: str = Field(..., description="Encouraging and structured narrative explanation")
    recommended_practice: List[str] = Field(default_factory=list, description="Recommended next practice actions")
    confidence_message: str = Field(..., description="Positive, affirming closing sentence")
