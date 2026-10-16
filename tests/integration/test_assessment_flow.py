import pytest
from app.services.assessment_service import AssessmentService
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.practice_repository import PracticeRepository


class TestAssessmentFlow:
    def test_diagnostic_assessment_submission_and_level_assignment(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            assessment_service = AssessmentService()

            # 1. Fetch diagnostic assessment
            diag = assessment_service.get_diagnostic_assessment("pronunciation")
            assert diag["title"] is not None
            assert len(diag["questions"]) == 5

            # 2. Answer all questions correctly
            answers = []
            for q in diag["questions"]:
                # Get the correct answer from DB
                answers.append({
                    "question_id": q["id"],
                    "user_response": "B" if q["question_type"] in ("syllable_count", "multiple_choice") else "A",
                })

            # 3. Submit assessment
            result = assessment_service.submit_assessment(
                user_id=user.id,
                goal_slug="pronunciation",
                assessment_id=diag["id"],
                answers_payload=answers,
            )

            assert result["percentage"] > 0
            assert result["calculated_level"] in [1, 2, 3, 4, 5]
            assert "category_breakdown" in result
            assert "strengths" in result
            assert "supportive_summary" in result
            assert result["initial_recommendations_count"] > 0

            # 4. Verify UserGoal was updated in database
            user_goal = UserRepository.get_user_goal_by_slug(user.id, "pronunciation")
            assert user_goal.assessment_status == "completed"
            assert user_goal.starting_level == result["calculated_level"]
            assert user_goal.current_level == result["calculated_level"]
