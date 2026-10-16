import uuid
from datetime import datetime, timezone
from app.extensions import db


class Goal(db.Model):
    """
    Supported learning goal entity (e.g., pronunciation, interview, presentation).
    """

    __tablename__ = "goals"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    target_unit = db.Column(db.String(30), default="items", nullable=False)  # words, questions, tasks, exercises
    default_target_quantity = db.Column(db.Integer, default=10, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    levels = db.relationship("Level", back_populates="goal", cascade="all, delete-orphan", order_by="Level.level_number")
    level_configurations = db.relationship("LevelConfiguration", back_populates="goal", cascade="all, delete-orphan")
    user_goals = db.relationship("UserGoal", back_populates="goal")
    assessments = db.relationship("Assessment", back_populates="goal")
    assessment_questions = db.relationship("AssessmentQuestion", back_populates="goal")

    def to_dict(self, include_levels: bool = True):
        data = {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "target_unit": self.target_unit,
            "default_target_quantity": self.default_target_quantity,
            "display_order": self.display_order,
            "is_active": self.is_active,
        }
        if include_levels and self.levels:
            data["levels"] = [level.to_dict() for level in self.levels]
        return data


class Level(db.Model):
    """
    Goal-specific proficiency level (1 to 5).
    Configurable via database.
    """

    __tablename__ = "levels"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4, 5
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    required_mastery_percentage = db.Column(db.Float, default=75.0, nullable=False)
    content_focus = db.Column(db.JSON, nullable=True)  # List of focus categories/skills
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    goal = db.relationship("Goal", back_populates="levels")

    __table_args__ = (
        db.UniqueConstraint("goal_id", "level_number", name="uq_goal_level_number"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "level_number": self.level_number,
            "title": self.title,
            "description": self.description,
            "required_mastery_percentage": self.required_mastery_percentage,
            "content_focus": self.content_focus or [],
        }


class LevelConfiguration(db.Model):
    """
    Deterministic rules and thresholds for assessment level mapping and progression.
    """

    __tablename__ = "level_configurations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_level = db.Column(db.Integer, nullable=False)
    min_score_percent = db.Column(db.Float, nullable=False)
    max_score_percent = db.Column(db.Float, nullable=False)
    criteria_description = db.Column(db.Text, nullable=False)
    strengths_summary = db.Column(db.Text, nullable=True)
    practice_focus = db.Column(db.Text, nullable=True)
    supportive_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    goal = db.relationship("Goal", back_populates="level_configurations")

    __table_args__ = (
        db.UniqueConstraint("goal_id", "assigned_level", name="uq_goal_assigned_level_config"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "assigned_level": self.assigned_level,
            "min_score_percent": self.min_score_percent,
            "max_score_percent": self.max_score_percent,
            "criteria_description": self.criteria_description,
            "strengths_summary": self.strengths_summary,
            "practice_focus": self.practice_focus,
            "supportive_message": self.supportive_message,
        }
