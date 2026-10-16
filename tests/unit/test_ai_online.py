import pytest
from unittest.mock import MagicMock
from app.ai.client import AIClient


class TestAIClientOnlinePath:
    def test_client_online_json_parsing(self):
        client = AIClient(api_key="sk-test-fake-key", mock_fallback=True)
        client._is_mock = False
        client._client = MagicMock()

        # Mock chat completion response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = (
            '{"strengths": ["Structured answer"], "areas_to_improve": ["Add metrics"], '
            '"feedback": "Strong delivery with clear points.", "recommended_practice": ["Practice conclusion"], '
            '"confidence_message": "Keep up the great momentum!"}'
        )
        mock_response.choices = [mock_choice]
        client._client.chat.completions.create.return_value = mock_response

        res = client.generate_structured_feedback(
            goal_slug="interview",
            prompt_context="Tell me about a project",
            user_response="I designed an API in Python",
            category="Technical",
            level=2,
        )

        assert res["strengths"] == ["Structured answer"]
        assert res["areas_to_improve"] == ["Add metrics"]
        assert "Strong delivery" in res["feedback"]
        assert "Keep up" in res["confidence_message"]
