from typing import Dict, Any, List, Optional
from datetime import date, timedelta
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.repositories.practice_repository import PracticeRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.recommendation.engine import RecommendationEngine
from app.utils.exceptions import NotFoundError


class ProgressService:
    """Service managing user progress dashboards, analytics, and activity calendars."""

    @staticmethod
    def get_dashboard_summary(user_id: str) -> Dict[str, Any]:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")

        user_goals = UserRepository.get_user_goals(user_id)
        active_goals_data = []
        total_time_seconds = 0
        total_items = 0

        for ug in user_goals:
            goal = ug.goal
            prog = PracticeRepository.get_or_create_user_progress(user_id, goal.id)
            target = UserRepository.get_daily_target(user_id, goal.id)
            target_qty = target.target_quantity if target else goal.default_target_quantity

            total_time_seconds += prog.total_practice_time_seconds
            total_items += prog.total_items_completed

            # Get recent recommendations
            recs = PracticeRepository.get_user_recommendations(user_id, goal.id, limit=3)

            active_goals_data.append({
                "goal_slug": goal.slug,
                "goal_name": goal.name,
                "current_level": ug.current_level,
                "starting_level": ug.starting_level,
                "assessment_status": ug.assessment_status,
                "daily_target": {
                    "quantity": target_qty,
                    "unit": goal.target_unit,
                },
                "progress": prog.to_dict(),
                "recommendation_count": len(recs),
            })

        # Activity calendar for last 14 days
        activity_history = PracticeRepository.get_activity_history(user_id, days=14)
        calendar = [entry.to_dict() for entry in activity_history]

        return {
            "anonymous_id": user.anonymous_id,
            "overall_metrics": {
                "total_items_completed": total_items,
                "total_practice_time_seconds": total_time_seconds,
                "total_practice_time_minutes": round(total_time_seconds / 60, 1),
                "active_goals_count": len(user_goals),
            },
            "goals": active_goals_data,
            "recent_activity_calendar": calendar,
        }

    @staticmethod
    def get_goal_progress_details(user_id: str, goal_slug: str) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        user_goal = UserRepository.get_user_goal_by_slug(user_id, goal_slug)
        if not user_goal:
            raise NotFoundError(f"Goal '{goal_slug}' is not activated for this user.")

        progress = PracticeRepository.get_or_create_user_progress(user_id, goal.id)
        daily_target = UserRepository.get_daily_target(user_id, goal.id)
        attempts = PracticeRepository.get_user_attempts_for_goal(user_id, goal.id, limit=20)
        revisions = PracticeRepository.get_revision_items(user_id, goal.id)
        assessment_history = AssessmentRepository.get_attempts_for_user(user_id, goal.id)
        activity_calendar = PracticeRepository.get_activity_history(user_id, goal.id, days=30)

        # Ensure recommendations exist
        recommendations = RecommendationEngine.generate_recommendations(user_id, goal_slug)

        return {
            "goal": goal.to_dict(include_levels=True),
            "user_goal": user_goal.to_dict(),
            "current_level": user_goal.current_level,
            "daily_target": daily_target.to_dict() if daily_target else {
                "target_quantity": goal.default_target_quantity,
                "target_type": goal.target_unit,
                "is_active": True,
            },
            "progress": progress.to_dict(),
            "revision_queue": [r.to_dict() for r in revisions],
            "recent_attempts": [a.to_dict() for a in attempts],
            "assessment_history": [ah.to_dict() for ah in assessment_history],
            "activity_calendar_30_days": [ac.to_dict() for ac in activity_calendar],
            "recommendations": recommendations,
        }
