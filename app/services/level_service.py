from typing import List, Dict, Any, Optional
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.repositories.practice_repository import PracticeRepository
from app.utils.exceptions import NotFoundError


class LevelService:
    """Service managing level information and progression eligibility."""

    @staticmethod
    def get_goal_levels(goal_slug: str) -> List[Dict[str, Any]]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")
        levels = GoalRepository.get_levels_for_goal(goal.id)
        return [lvl.to_dict() for lvl in levels]

    @staticmethod
    def get_level_details(goal_slug: str, level_number: int) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")
        level = GoalRepository.get_level(goal.id, level_number)
        if not level:
            raise NotFoundError(f"Level {level_number} not found for goal '{goal_slug}'.")

        config = GoalRepository.get_level_config_for_level(goal.id, level_number)
        data = level.to_dict()
        if config:
            data["configuration"] = config.to_dict()
        return data

    @staticmethod
    def check_progression_eligibility(user_id: str, goal_slug: str) -> Dict[str, Any]:
        """
        Check if user is eligible to attempt the level progression assessment.
        Requirements: User has practiced a baseline amount in their current level.
        """
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        user_goal = UserRepository.get_user_goal_by_slug(user_id, goal_slug)
        if not user_goal:
            return {"eligible": False, "reason": "Goal not yet started."}

        current_level = user_goal.current_level
        if current_level >= 5:
            return {
                "eligible": False,
                "current_level": 5,
                "is_max_level": True,
                "message": "Congratulations! You have reached the highest mastery level for this goal.",
            }

        progress = PracticeRepository.get_or_create_user_progress(user_id, goal.id)
        # Recommendation: At least 3 practice items completed to attempt progression check
        min_items_recommended = 3
        can_attempt = progress.total_items_completed >= min_items_recommended

        return {
            "eligible": can_attempt,
            "current_level": current_level,
            "next_level": current_level + 1,
            "items_completed": progress.total_items_completed,
            "items_required": min_items_recommended,
            "message": (
                "Ready for your Level Progression Check!"
                if can_attempt
                else f"Complete at least {min_items_recommended - progress.total_items_completed} more practice exercises before your progress check."
            ),
        }
