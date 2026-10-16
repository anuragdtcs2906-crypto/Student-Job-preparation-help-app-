import uuid
from datetime import datetime, timezone
from app.extensions import db


class AIFeedback(db.Model):
    """
    Validated AI structured feedback record for practice attempts and open-ended assessments.
    Enforces supportive, confidence-building tone.
    """

    __tablename__ = "ai_feedback"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type = db.Column(db.String(50), nullable=False)  # practice_attempt, assessment_attempt
    source_id = db.Column(db.String(36), nullable=False, index=True)
    practice_attempt_id = db.Column(db.String(36), db.ForeignKey("practice_attempts.id", ondelete="CASCADE"), nullable=True)

    strengths = db.Column(db.JSON, nullable=False)  # List of positive, identified strengths
    areas_to_improve = db.Column(db.JSON, nullable=False)  # List of constructive actionable pointers
    feedback_text = db.Column(db.Text, nullable=False)  # Supportive narrative feedback
    recommended_practice = db.Column(db.JSON, nullable=True)  # Specific practice focus
    confidence_message = db.Column(db.Text, nullable=False)  # Encouraging closing statement
    model_used = db.Column(db.String(50), default="gpt-4o-mini", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    practice_attempt = db.relationship("PracticeAttempt", back_populates="feedback")
    user = db.relationship("User")
    goal = db.relationship("Goal", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "strengths": self.strengths or [],
            "areas_to_improve": self.areas_to_improve or [],
            "feedback": self.feedback_text,
            "recommended_practice": self.recommended_practice or [],
            "confidence_message": self.confidence_message,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
