from typing import Any, Dict, List, Optional
from app.ai.client import AIClient


class AIAssessmentHelper:
    """
    Synthesizes category performance and diagnostic patterns into supportive recommendations.
    Deterministic rules control level boundaries, while AI adds qualitative encouragement.
    """

    def __init__(self, ai_client: Optional[AIClient] = None):
        self.ai_client = ai_client or AIClient()

    def generate_assessment_summary(
        self,
        goal_slug: str,
        assigned_level: int,
        percentage: float,
        category_breakdown: Dict[str, Any],
        strengths: List[str],
        areas_to_improve: List[str],
    ) -> Dict[str, Any]:
        """
        Generate qualitative encouraging summary for assessment results.
        """
        strong_categories = [
            cat for cat, stats in category_breakdown.items() if stats.get("percentage", 0) >= 70
        ]
        focus_categories = [
            cat for cat, stats in category_breakdown.items() if stats.get("percentage", 0) < 70
        ]

        if not strong_categories:
            strong_categories = list(category_breakdown.keys())[:1] or ["General Awareness"]
        if not focus_categories:
            focus_categories = ["Advanced Nuances"]

        supportive_msg = (
            f"Great job completing your {goal_slug.replace('_', ' ').title()} assessment! "
            f"You demonstrated solid familiarity in {', '.join(strong_categories)}. "
            f"Starting at Level {assigned_level} gives you the perfect tailored roadmap to strengthen {', '.join(focus_categories)}."
        )

        return {
            "summary_text": supportive_msg,
            "highlighted_strengths": strengths or [f"Strong understanding in {cat}" for cat in strong_categories],
            "focus_areas": areas_to_improve or [f"Practice {cat} exercises" for cat in focus_categories],
            "confidence_booster": "Every step you practice builds lasting speaking confidence!",
        }
