from typing import List, Dict, Any
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import NotFoundError, ValidationError


class GoalService:
    """Service managing goals, user goal activation, and level information."""

    @staticmethod
    def get_all_goals() -> List[Dict[str, Any]]:
        goals = GoalRepository.get_all_active_goals()
        return [g.to_dict(include_levels=True) for g in goals]

    @staticmethod
    def get_goal_by_slug(goal_slug: str) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")
        return goal.to_dict(include_levels=True)

    @staticmethod
    def select_user_goals(user_id: str, goal_slugs: List[str]) -> List[Dict[str, Any]]:
        """
        Activate one or multiple goals for a user.
        Initializes default target and UserGoal record.
        """
        if not goal_slugs:
            raise ValidationError("Please select at least one goal.")

        activated_goals = []
        for slug in goal_slugs:
            goal = GoalRepository.get_by_slug(slug)
            if not goal:
                raise NotFoundError(f"Goal '{slug}' is not a valid goal.")

            user_goal = UserRepository.get_or_create_user_goal(user_id, goal.id)
            user_goal.is_active = True

            # Ensure default daily target exists
            daily_target = UserRepository.get_daily_target(user_id, goal.id)
            if not daily_target:
                UserRepository.upsert_daily_target(
                    user_id=user_id,
                    goal_id=goal.id,
                    target_quantity=goal.default_target_quantity,
                    target_type=goal.target_unit,
                )

            activated_goals.append(user_goal.to_dict())

        return activated_goals

    @staticmethod
    def get_user_goals(user_id: str) -> List[Dict[str, Any]]:
        user_goals = UserRepository.get_user_goals(user_id)
        return [ug.to_dict() for ug in user_goals]
