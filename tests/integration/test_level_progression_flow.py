import pytest
from app.services.assessment_service import AssessmentService
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository


class TestLevelProgressionFlow:
    def test_level_progression_advancement_on_mastery(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            goal = GoalRepository.get_by_slug("presentation")
            ug = UserRepository.get_or_create_user_goal(user.id, goal.id)
            ug.current_level = 1
            ug.starting_level = 1

            assessment_service = AssessmentService()
            prog_assessment = assessment_service.get_progression_assessment("presentation", level_number=1)
            assert prog_assessment["assessment_type"] == "level_progression"

            # Answer all progression questions correctly
            answers = []
            for q in prog_assessment["questions"]:
                answers.append({
                    "question_id": q["id"],
                    "user_response": "A",
                })

            result = assessment_service.submit_assessment(
                user_id=user.id,
                goal_slug="presentation",
                assessment_id=prog_assessment["id"],
                answers_payload=answers,
            )

            assert result["passed_progression"] is True
            assert result["calculated_level"] == 2

            # Verify in DB
            user_goal = UserRepository.get_user_goal_by_slug(user.id, "presentation")
            assert user_goal.current_level == 2
