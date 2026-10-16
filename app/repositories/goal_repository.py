from typing import List, Optional
from app.extensions import db
from app.models.goal import Goal, Level, LevelConfiguration


class GoalRepository:
    """Data access layer for Goals, Levels, and LevelConfigurations."""

    @staticmethod
    def get_all_active_goals() -> List[Goal]:
        return db.session.query(Goal).filter_by(is_active=True).order_by(Goal.display_order).all()

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Goal]:
        return db.session.query(Goal).filter_by(slug=slug.lower(), is_active=True).first()

    @staticmethod
    def get_by_id(goal_id: str) -> Optional[Goal]:
        return db.session.query(Goal).filter_by(id=goal_id).first()

    @staticmethod
    def get_levels_for_goal(goal_id: str) -> List[Level]:
        return db.session.query(Level).filter_by(goal_id=goal_id).order_by(Level.level_number).all()

    @staticmethod
    def get_level(goal_id: str, level_number: int) -> Optional[Level]:
        return db.session.query(Level).filter_by(goal_id=goal_id, level_number=level_number).first()

    @staticmethod
    def get_level_configurations(goal_id: str) -> List[LevelConfiguration]:
        return (
            db.session.query(LevelConfiguration)
            .filter_by(goal_id=goal_id)
            .order_by(LevelConfiguration.assigned_level)
            .all()
        )

    @staticmethod
    def get_level_config_for_level(goal_id: str, level_number: int) -> Optional[LevelConfiguration]:
        return (
            db.session.query(LevelConfiguration)
            .filter_by(goal_id=goal_id, assigned_level=level_number)
            .first()
        )

    @staticmethod
    def match_level_from_score(goal_id: str, percentage: float) -> int:
        """
        Deterministic level calculation from database LevelConfiguration score thresholds.
        """
        configs = GoalRepository.get_level_configurations(goal_id)
        if not configs:
            # Standard default deterministic fallback
            if percentage >= 85.0:
                return 5
            elif percentage >= 70.0:
                return 4
            elif percentage >= 50.0:
                return 3
            elif percentage >= 30.0:
                return 2
            return 1

        for config in configs:
            if config.min_score_percent <= percentage <= config.max_score_percent:
                return config.assigned_level

        # Fallback to closest bounds
        if percentage >= 85.0:
            return 5
        return 1
