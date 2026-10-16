from datetime import datetime, timezone
from typing import List, Optional
from app.extensions import db
from app.models.user import User, UserGoal, DailyTarget, ActivityHistory
from app.models.goal import Goal
from app.utils.anonymous_id import generate_anonymous_id, normalize_anonymous_id


class UserRepository:
    """Data access layer for Anonymous Users, UserGoals, and Targets."""

    @staticmethod
    def get_by_anonymous_id(anonymous_id: str) -> Optional[User]:
        normalized = normalize_anonymous_id(anonymous_id)
        return db.session.query(User).filter_by(anonymous_id=normalized).first()

    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        return db.session.query(User).filter_by(id=user_id).first()

    @classmethod
    def create_anonymous_user(cls) -> User:
        """Generate a unique anonymous ID and persist the user."""
        max_attempts = 10
        for _ in range(max_attempts):
            anon_id = generate_anonymous_id()
            if not cls.get_by_anonymous_id(anon_id):
                user = User(anonymous_id=anon_id)
                db.session.add(user)
                db.session.commit()
                return user
        raise RuntimeError("Failed to generate unique anonymous ID after multiple attempts.")

    @staticmethod
    def update_last_active(user: User) -> None:
        user.last_active_at = datetime.now(timezone.utc)
        db.session.commit()

    @staticmethod
    def get_user_goals(user_id: str) -> List[UserGoal]:
        return (
            db.session.query(UserGoal)
            .filter_by(user_id=user_id, is_active=True)
            .join(Goal)
            .order_by(Goal.display_order)
            .all()
        )

    @staticmethod
    def get_user_goal_by_slug(user_id: str, goal_slug: str) -> Optional[UserGoal]:
        return (
            db.session.query(UserGoal)
            .join(Goal)
            .filter(UserGoal.user_id == user_id, Goal.slug == goal_slug)
            .first()
        )

    @staticmethod
    def get_or_create_user_goal(user_id: str, goal_id: str) -> UserGoal:
        ug = db.session.query(UserGoal).filter_by(user_id=user_id, goal_id=goal_id).first()
        if not ug:
            ug = UserGoal(user_id=user_id, goal_id=goal_id, current_level=1, starting_level=1, assessment_status="not_started")
            db.session.add(ug)
            db.session.commit()
        return ug

    @staticmethod
    def get_daily_target(user_id: str, goal_id: str) -> Optional[DailyTarget]:
        return db.session.query(DailyTarget).filter_by(user_id=user_id, goal_id=goal_id).first()

    @staticmethod
    def upsert_daily_target(user_id: str, goal_id: str, target_quantity: int, target_type: str = "items") -> DailyTarget:
        dt = db.session.query(DailyTarget).filter_by(user_id=user_id, goal_id=goal_id).first()
        if dt:
            dt.target_quantity = target_quantity
            if target_type:
                dt.target_type = target_type
            dt.updated_at = datetime.now(timezone.utc)
        else:
            dt = DailyTarget(user_id=user_id, goal_id=goal_id, target_quantity=target_quantity, target_type=target_type)
            db.session.add(dt)
        db.session.commit()
        return dt
