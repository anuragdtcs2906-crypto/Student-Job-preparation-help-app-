from typing import Any, Dict, Optional
from app.ai.client import AIClient
from app.repositories.practice_repository import PracticeRepository


class AIFeedbackEngine:
    """
    High-level service orchestrating AI evaluation, validation, and storage for practice attempts.
    """

    def __init__(self, ai_client: Optional[AIClient] = None):
        self.ai_client = ai_client or AIClient()

    def evaluate_response(
        self,
        user_id: str,
        goal_id: str,
        goal_slug: str,
        prompt_context: str,
        user_response: str,
        category: Optional[str] = None,
        level: int = 1,
        source_type: str = "practice_attempt",
        source_id: Optional[str] = None,
        practice_attempt_id: Optional[str] = None,
        save_to_db: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluate user's communication response and optionally store feedback.
        """
        feedback_data = self.ai_client.generate_structured_feedback(
            goal_slug=goal_slug,
            prompt_context=prompt_context,
            user_response=user_response,
            category=category,
            level=level,
        )

        if save_to_db and source_id:
            PracticeRepository.save_ai_feedback(
                user_id=user_id,
                goal_id=goal_id,
                source_type=source_type,
                source_id=source_id,
                practice_attempt_id=practice_attempt_id,
                strengths=feedback_data.get("strengths", []),
                areas_to_improve=feedback_data.get("areas_to_improve", []),
                feedback_text=feedback_data.get("feedback", ""),
                recommended_practice=feedback_data.get("recommended_practice", []),
                confidence_message=feedback_data.get("confidence_message", ""),
                model_used=self.ai_client.model,
            )

        return feedback_data
