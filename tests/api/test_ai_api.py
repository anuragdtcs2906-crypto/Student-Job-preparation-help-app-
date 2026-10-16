import pytest


class TestAIAPI:
    def test_direct_ai_evaluation_endpoint(self, client, test_user):
        res = client.post(
            "/api/v1/ai/evaluate",
            headers=test_user["headers"],
            json={
                "goal_slug": "interview",
                "prompt_context": "Why are you interested in this engineering role?",
                "user_response": "I have been building distributed backends for 3 years and love solving scaling problems with modular architecture.",
                "category": "HR",
                "level": 2,
            },
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        feedback = data["data"]
        assert "strengths" in feedback
        assert "areas_to_improve" in feedback
        assert "feedback" in feedback
        assert "confidence_message" in feedback
        assert len(feedback["strengths"]) > 0
