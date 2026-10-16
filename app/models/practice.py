import uuid
from datetime import datetime, timezone
from app.extensions import db


class PracticeSession(db.Model):
    """
    Practice session entity measuring actual engagement and time spent without forced duration pressure.
    """

    __tablename__ = "practice_sessions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type = db.Column(db.String(50), nullable=False)  # pronunciation, interview, presentation, communication, gd
    session_start = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    session_end = db.Column(db.DateTime(timezone=True), nullable=True)
    duration_seconds = db.Column(db.Integer, default=0, nullable=False)
    items_target = db.Column(db.Integer, default=0, nullable=False)
    items_completed = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(30), default="active", nullable=False)  # active, completed, abandoned
    session_metadata = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="practice_sessions")
    goal = db.relationship("Goal", lazy="joined")
    attempts = db.relationship("PracticeAttempt", back_populates="session", cascade="all, delete-orphan", lazy="selectin")

    def to_dict(self, include_attempts: bool = False):
        data = {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "activity_type": self.activity_type,
            "session_start": self.session_start.isoformat() if self.session_start else None,
            "session_end": self.session_end.isoformat() if self.session_end else None,
            "duration_seconds": self.duration_seconds,
            "duration_minutes": round(self.duration_seconds / 60, 1),
            "items_target": self.items_target,
            "items_completed": self.items_completed,
            "status": self.status,
            "session_metadata": self.session_metadata,
        }
        if include_attempts and self.attempts:
            data["attempts"] = [a.to_dict() for a in self.attempts]
        return data


class PracticeAttempt(db.Model):
    """
    Individual attempt or completion of a specific content item within a session.
    """

    __tablename__ = "practice_attempts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), db.ForeignKey("practice_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    content_type = db.Column(db.String(50), nullable=False)  # pronunciation_words, interview_questions, presentation_tasks, communication_exercises, gd_questions
    content_id = db.Column(db.String(36), nullable=False, index=True)
    user_input = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=True, nullable=False)
    marked_for_revision = db.Column(db.Boolean, default=False, nullable=False)
    time_spent_seconds = db.Column(db.Integer, default=0, nullable=False)
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    session = db.relationship("PracticeSession", back_populates="attempts")
    user = db.relationship("User", back_populates="practice_attempts")
    goal = db.relationship("Goal", lazy="joined")
    feedback = db.relationship("AIFeedback", back_populates="practice_attempt", uselist=False, cascade="all, delete-orphan", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "goal_slug": self.goal.slug if self.goal else None,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "user_input": self.user_input,
            "is_completed": self.is_completed,
            "marked_for_revision": self.marked_for_revision,
            "time_spent_seconds": self.time_spent_seconds,
            "score": self.score,
            "feedback": self.feedback.to_dict() if self.feedback else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class UserProgress(db.Model):
    """
    Cumulative progress metrics per goal for a user.
    """

    __tablename__ = "user_progress"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    total_items_completed = db.Column(db.Integer, default=0, nullable=False)
    total_practice_time_seconds = db.Column(db.Integer, default=0, nullable=False)
    words_practiced = db.Column(db.Integer, default=0, nullable=False)
    questions_practiced = db.Column(db.Integer, default=0, nullable=False)
    tasks_practiced = db.Column(db.Integer, default=0, nullable=False)
    exercises_practiced = db.Column(db.Integer, default=0, nullable=False)
    revision_queue_count = db.Column(db.Integer, default=0, nullable=False)
    last_practiced_at = db.Column(db.DateTime(timezone=True), nullable=True)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="progress_records")
    goal = db.relationship("Goal", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "goal_id", name="uq_user_goal_progress"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "total_items_completed": self.total_items_completed,
            "total_practice_time_seconds": self.total_practice_time_seconds,
            "total_practice_time_minutes": round(self.total_practice_time_seconds / 60, 1),
            "words_practiced": self.words_practiced,
            "questions_practiced": self.questions_practiced,
            "tasks_practiced": self.tasks_practiced,
            "exercises_practiced": self.exercises_practiced,
            "revision_queue_count": self.revision_queue_count,
            "last_practiced_at": self.last_practiced_at.isoformat() if self.last_practiced_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserRecommendation(db.Model):
    """
    Personalized practice item recommended by the recommendation engine.
    """

    __tablename__ = "user_recommendations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    content_type = db.Column(db.String(50), nullable=False)  # pronunciation_words, interview_questions, etc.
    content_id = db.Column(db.String(36), nullable=False)
    reason = db.Column(db.String(50), nullable=False)  # new_level, difficult_item, spaced_revision, target_fulfillment
    reason_label = db.Column(db.String(100), nullable=True)  # User-friendly explanation (e.g. "Focus Area for Level 2")
    priority = db.Column(db.Integer, default=1, nullable=False)
    is_consumed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="recommendations")
    goal = db.relationship("Goal", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "reason": self.reason,
            "reason_label": self.reason_label,
            "priority": self.priority,
            "is_consumed": self.is_consumed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
