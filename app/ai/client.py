import json
import logging
import os
from typing import Any, Dict, Optional
from openai import OpenAI
from app.ai.prompts import (
    SUPPORTIVE_COACH_SYSTEM_PROMPT,
    INTERVIEW_EVALUATION_PROMPT_TEMPLATE,
    PRESENTATION_EVALUATION_PROMPT_TEMPLATE,
    GD_EVALUATION_PROMPT_TEMPLATE,
    COMMUNICATION_EVALUATION_PROMPT_TEMPLATE,
)

logger = logging.getLogger(__name__)


class AIClient:
    """
    Modular AI Client adapter using official OpenAI Python SDK with mock fallback support.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        mock_fallback: bool = True,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "mock-dev-key")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.mock_fallback = mock_fallback
        self._is_mock = (
            not self.api_key
            or self.api_key.startswith("mock")
            or self.api_key == "your-openai-api-key-here"
        )
        self._client: Optional[OpenAI] = None
        if not self._is_mock:
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}. Defaulting to mock.")
                self._is_mock = True

    def generate_structured_feedback(
        self,
        goal_slug: str,
        prompt_context: str,
        user_response: str,
        category: Optional[str] = None,
        level: int = 1,
    ) -> Dict[str, Any]:
        """
        Generate structured supportive feedback JSON for any open-ended user communication response.
        """
        category = category or "General Communication"

        # If running in mock/offline mode, return high quality rule-templated supportive feedback
        if self._is_mock or not self._client:
            return self._generate_mock_feedback(goal_slug, prompt_context, user_response, category, level)

        # Select appropriate prompt template
        if goal_slug == "interview":
            user_prompt = INTERVIEW_EVALUATION_PROMPT_TEMPLATE.format(
                category=category, level=level, prompt_context=prompt_context, user_response=user_response
            )
        elif goal_slug == "presentation":
            user_prompt = PRESENTATION_EVALUATION_PROMPT_TEMPLATE.format(
                category=category, level=level, prompt_context=prompt_context, user_response=user_response
            )
        elif goal_slug == "gd":
            user_prompt = GD_EVALUATION_PROMPT_TEMPLATE.format(
                category=category, level=level, prompt_context=prompt_context, user_response=user_response
            )
        else:
            user_prompt = COMMUNICATION_EVALUATION_PROMPT_TEMPLATE.format(
                category=category, level=level, prompt_context=prompt_context, user_response=user_response
            )

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SUPPORTIVE_COACH_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=600,
            )
            raw_content = response.choices[0].message.content
            parsed = json.loads(raw_content)
            return self._validate_and_sanitize_feedback(parsed)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}. Falling back to deterministic supportive feedback.")
            if self.mock_fallback:
                return self._generate_mock_feedback(goal_slug, prompt_context, user_response, category, level)
            raise

    def _validate_and_sanitize_feedback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate structure and ensure all required fields are present."""
        strengths = data.get("strengths", [])
        if not isinstance(strengths, list) or not strengths:
            strengths = ["Clear and direct communication style", "Demonstrated thoughtful engagement with the topic"]

        areas = data.get("areas_to_improve", [])
        if not isinstance(areas, list) or not areas:
            areas = ["Consider expanding on specific practical examples to illustrate key points"]

        feedback = data.get("feedback")
        if not feedback or not isinstance(feedback, str):
            feedback = "You communicated your main idea well. With continued practice, adding structured examples will make your points even stronger."

        recommended = data.get("recommended_practice", [])
        if not isinstance(recommended, list) or not recommended:
            recommended = ["Practice delivering a 1-minute summary focusing on concrete examples"]

        confidence = data.get("confidence_message")
        if not confidence or not isinstance(confidence, str):
            confidence = "You have a solid foundation and clear expression—keep up the great momentum!"

        return {
            "strengths": strengths,
            "areas_to_improve": areas,
            "feedback": feedback,
            "recommended_practice": recommended,
            "confidence_message": confidence,
        }

    def _generate_mock_feedback(
        self,
        goal_slug: str,
        prompt_context: str,
        user_response: str,
        category: str,
        level: int,
    ) -> Dict[str, Any]:
        """
        Generate rich, supportive mock feedback when running offline or in test environments.
        """
        word_count = len(user_response.split())
        
        if goal_slug == "interview":
            return {
                "strengths": [
                    "Directly addressed the core of the interview question.",
                    "Maintained a professional, authentic tone throughout the response.",
                    "Showcased relevant problem-solving readiness.",
                ],
                "areas_to_improve": [
                    "Try structuring your narrative using the STAR method (Situation, Task, Action, Result).",
                    "Add measurable outcomes where possible to highlight personal impact.",
                ],
                "feedback": (
                    f"Your answer to '{prompt_context[:60]}...' has great energy and clear direction. "
                    "By clearly highlighting the action you took and the positive result achieved, your answers will become even more compelling to interviewers."
                ),
                "recommended_practice": [
                    "Practice 3 behavioral questions focusing specifically on the Action and Result phases.",
                    "Keep your response concise within a 90-second delivery window.",
                ],
                "confidence_message": "You are expressing your experiences with great clarity—keep building this momentum!",
            }
        elif goal_slug == "presentation":
            return {
                "strengths": [
                    "Clear thematic focus that is easy for the audience to follow.",
                    "Organized thoughts with a logical progression from start to finish.",
                ],
                "areas_to_improve": [
                    "Incorporate a stronger opening hook or rhetorical question to capture attention immediately.",
                    "Use explicit transition phrases between subtopics.",
                ],
                "feedback": (
                    "You have laid out the core concepts effectively. Adding a vivid introduction and memorable concluding sentence will elevate your presentation flow."
                ),
                "recommended_practice": [
                    "Practice delivering the first 30 seconds of your presentation with extra vocal energy.",
                    "Rehearse summarizing key points in a 3-bullet recap slide format.",
                ],
                "confidence_message": "Your presentation ideas are clear and engaging—great job on this topic!",
            }
        elif goal_slug == "gd":
            return {
                "strengths": [
                    "Articulated a balanced, reasoned perspective on the topic.",
                    "Used respectful, constructive language suitable for collaborative discussions.",
                ],
                "areas_to_improve": [
                    "Consider acknowledging other perspectives explicitly before introducing your viewpoint.",
                    "Practice summarizing group consensus to naturally take on a leadership role.",
                ],
                "feedback": (
                    "Your contribution adds meaningful value to the discussion. Connecting your points to previous statements helps maintain high group engagement."
                ),
                "recommended_practice": [
                    "Practice phrases like 'Building upon what was mentioned...' to transition smoothly into discussions.",
                    "Work on 1-minute concise perspective summaries.",
                ],
                "confidence_message": "You have a thoughtful, constructive discussion style that inspires collaborative dialogue!",
            }
        else:
            return {
                "strengths": [
                    "Clear sentence construction and effective vocabulary choices.",
                    "Message is easy to understand and well-paced.",
                ],
                "areas_to_improve": [
                    "Experiment with varied sentence lengths to make the rhythm even more engaging.",
                ],
                "feedback": (
                    "You communicated your thoughts accurately and clearly. Continuing daily practice with different scenarios will make natural expression second nature."
                ),
                "recommended_practice": [
                    "Review 5 new vocabulary phrases in context today.",
                ],
                "confidence_message": "Your clarity is improving with every exercise—keep up the fantastic practice!",
            }
