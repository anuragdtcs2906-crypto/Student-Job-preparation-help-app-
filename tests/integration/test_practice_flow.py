import pytest
from app.services.practice_service import PracticeService
from app.services.progress_service import ProgressService
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.content_repository import ContentRepository


class TestPracticeFlow:
    def test_complete_practice_lifecycle_with_ai_feedback(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            goal = GoalRepository.get_by_slug("interview")
            UserRepository.get_or_create_user_goal(user.id, goal.id)

            practice_service = PracticeService()

            # 1. Start Session
            session = practice_service.start_session(
                user_id=user.id,
                goal_slug="interview",
                activity_type="interview",
                target_count=5,
            )
            session_id = session["id"]
            assert session["status"] == "active"

            # 2. Query interview question
            questions = ContentRepository.get_interview_questions(level=1, limit=1)
            q = questions[0]

            # 3. Submit Practice Attempt with AI feedback
            attempt = practice_service.record_attempt(
                user_id=user.id,
                session_id=session_id,
                content_type="interview_questions",
                content_id=q.id,
                user_input="I led a team of 4 engineers to build a new payment gateway, reducing checkout drop-off by 25%.",
                is_completed=True,
                marked_for_revision=True,
                time_spent_seconds=65,
                request_ai_feedback=True,
            )

            assert attempt["is_completed"] is True
            assert attempt["marked_for_revision"] is True
            assert attempt["time_spent_seconds"] == 65
            assert "feedback" in attempt
            assert attempt["feedback"] is not None
            assert len(attempt["feedback"]["strengths"]) > 0

            # 4. Complete Session
            completed = practice_service.complete_session(
                user_id=user.id,
                session_id=session_id,
                duration_seconds=75,
            )
            assert completed["status"] == "completed"
            assert completed["duration_seconds"] == 75

            # 5. Check Dashboard Analytics
            dashboard = ProgressService.get_dashboard_summary(user.id)
            assert dashboard["overall_metrics"]["total_items_completed"] >= 1
            assert dashboard["overall_metrics"]["total_practice_time_seconds"] >= 65
