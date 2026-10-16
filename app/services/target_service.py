from typing import List, Dict, Any, Optional
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import NotFoundError, ValidationError


class TargetService:
    """Service managing user-configured daily practice quantities."""

    @staticmethod
    def get_user_targets(user_id: str) -> List[Dict[str, Any]]:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return [dt.to_dict() for dt in user.daily_targets if dt.is_active]

    @staticmethod
    def update_daily_target(
        user_id: str,
        goal_slug: str,
        target_quantity: int,
        target_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        if target_quantity < 1 or target_quantity > 100:
            raise ValidationError("Target quantity must be between 1 and 100 items.")

        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        # Ensure goal is activated for user
        UserRepository.get_or_create_user_goal(user_id, goal.id)

        target_type = target_type or goal.target_unit
        dt = UserRepository.upsert_daily_target(
            user_id=user_id,
            goal_id=goal.id,
            target_quantity=target_quantity,
            target_type=target_type,
        )
        return dt.to_dict()
