import pytest
from datetime import date
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.practice_repository import PracticeRepository
from app.services.progress_service import ProgressService


class TestProgressService:
    def test_progress_tracking_and_time_aggregation(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            goal = GoalRepository.get_by_slug("interview")
            UserRepository.get_or_create_user_goal(user.id, goal.id)

            # Record attempts with time
            PracticeRepository.update_progress_on_attempt(
                user_id=user.id,
                goal_id=goal.id,
                content_type="interview_questions",
                time_spent_seconds=120,
                marked_for_revision=True,
            )

            PracticeRepository.update_progress_on_attempt(
                user_id=user.id,
                goal_id=goal.id,
                content_type="interview_questions",
                time_spent_seconds=180,
                marked_for_revision=False,
            )

            # Record calendar activity
            PracticeRepository.record_activity_entry(
                user_id=user.id,
                goal_id=goal.id,
                items_count=2,
                time_spent_seconds=300,
            )

            summary = ProgressService.get_dashboard_summary(user.id)
            assert summary["overall_metrics"]["total_items_completed"] == 2
            assert summary["overall_metrics"]["total_practice_time_seconds"] == 300
            assert summary["overall_metrics"]["total_practice_time_minutes"] == 5.0
            assert len(summary["recent_activity_calendar"]) >= 1
            assert summary["recent_activity_calendar"][0]["items_completed"] == 2
