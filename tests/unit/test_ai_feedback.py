import pytest
from app.ai.client import AIClient


class TestAIFeedback:
    def test_ai_mock_feedback_structure(self):
        client = AIClient(api_key="mock-key", mock_fallback=True)
        feedback = client.generate_structured_feedback(
            goal_slug="interview",
            prompt_context="Tell me about yourself.",
            user_response="I am a software engineer with 2 years of experience building Python APIs.",
            category="Introduction",
            level=1,
        )

        assert "strengths" in feedback
        assert isinstance(feedback["strengths"], list)
        assert len(feedback["strengths"]) > 0

        assert "areas_to_improve" in feedback
        assert isinstance(feedback["areas_to_improve"], list)

        assert "feedback" in feedback
        assert isinstance(feedback["feedback"], str)

        assert "recommended_practice" in feedback
        assert "confidence_message" in feedback

    def test_supportive_language_zero_shaming(self):
        client = AIClient(api_key="mock-key", mock_fallback=True)
        goals = ["interview", "presentation", "gd", "communication"]

        shaming_words = ["bad", "poor", "failure", "failed", "weak student", "stupid", "incompetent", "wrong person"]

        for goal in goals:
            fb = client.generate_structured_feedback(
                goal_slug=goal,
                prompt_context="Sample practice topic",
                user_response="Brief response for testing supportive language.",
                category="General",
                level=1,
            )
            combined_text = (
                " ".join(fb["strengths"])
                + " "
                + " ".join(fb["areas_to_improve"])
                + " "
                + fb["feedback"]
                + " "
                + fb["confidence_message"]
            ).lower()

            for word in shaming_words:
                assert word not in combined_text, f"Found forbidden shaming word '{word}' in AI feedback for goal '{goal}'"
