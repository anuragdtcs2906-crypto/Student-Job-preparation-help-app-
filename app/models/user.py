import uuid
from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    """
    Anonymous user model.
    No PII (no name, email, phone, college) is stored.
    The anonymous_id is the primary identifier.
    """

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    anonymous_id = db.Column(db.String(16), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_active_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user_goals = db.relationship(
        "UserGoal", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    daily_targets = db.relationship(
        "DailyTarget", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    activity_history = db.relationship(
        "ActivityHistory", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    practice_sessions = db.relationship(
        "PracticeSession", back_populates="user", cascade="all, delete-orphan"
    )
    practice_attempts = db.relationship(
        "PracticeAttempt", back_populates="user", cascade="all, delete-orphan"
    )
    progress_records = db.relationship(
        "UserProgress", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    recommendations = db.relationship(
        "UserRecommendation", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "anonymous_id": self.anonymous_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_active_at": self.last_active_at.isoformat() if self.last_active_at else None,
            "is_active": self.is_active,
        }


class UserGoal(db.Model):
    """
    Goal selected by a user.
    Levels and progress are tracked independently per goal.
    """

    __tablename__ = "user_goals"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    current_level = db.Column(db.Integer, default=1, nullable=False)
    starting_level = db.Column(db.Integer, default=1, nullable=False)
    assessment_status = db.Column(db.String(20), default="not_started", nullable=False)  # not_started, in_progress, completed
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="user_goals")
    goal = db.relationship("Goal", back_populates="user_goals", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "goal_id", name="uq_user_goal"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "goal_name": self.goal.name if self.goal else None,
            "current_level": self.current_level,
            "starting_level": self.starting_level,
            "assessment_status": self.assessment_status,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyTarget(db.Model):
    """
    User-configured daily practice quantity for a specific goal.
    Quantity-based, not time-forced.
    """

    __tablename__ = "daily_targets"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    target_quantity = db.Column(db.Integer, nullable=False, default=10)
    target_type = db.Column(db.String(30), nullable=False, default="items")  # words, questions, tasks, exercises
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="daily_targets")
    goal = db.relationship("Goal", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "goal_id", name="uq_user_goal_daily_target"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "target_quantity": self.target_quantity,
            "target_type": self.target_type,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ActivityHistory(db.Model):
    """
    Daily practice activity record for calendar and trend visualizations.
    Tracks items completed and actual practice time without judgmental streaks.
    """

    __tablename__ = "activity_history"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_date = db.Column(db.Date, nullable=False, index=True)
    items_completed = db.Column(db.Integer, default=0, nullable=False)
    time_spent_seconds = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="activity_history")
    goal = db.relationship("Goal", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "goal_id", "activity_date", name="uq_user_goal_activity_date"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "activity_date": self.activity_date.isoformat() if self.activity_date else None,
            "items_completed": self.items_completed,
            "time_spent_seconds": self.time_spent_seconds,
            "time_spent_minutes": round(self.time_spent_seconds / 60, 1),
        }
