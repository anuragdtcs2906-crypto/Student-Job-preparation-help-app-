import uuid
from datetime import datetime, timezone
from app.extensions import db


class Assessment(db.Model):
    """
    Assessment metadata container (Initial Diagnostic or Level Progression Check).
    """

    __tablename__ = "assessments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = db.Column(db.Integer, nullable=True)  # Null for initial diagnostic, 1-5 for level progression checks
    title = db.Column(db.String(150), nullable=False)
    assessment_type = db.Column(db.String(30), nullable=False, default="initial")  # initial, level_progression
    description = db.Column(db.Text, nullable=True)
    total_points = db.Column(db.Integer, default=100, nullable=False)
    pass_percentage = db.Column(db.Float, default=75.0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    goal = db.relationship("Goal", back_populates="assessments")
    questions = db.relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan", order_by="AssessmentQuestion.display_order")
    attempts = db.relationship("AssessmentAttempt", back_populates="assessment", cascade="all, delete-orphan")

    def to_dict(self, include_questions: bool = False):
        data = {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "level_number": self.level_number,
            "title": self.title,
            "assessment_type": self.assessment_type,
            "description": self.description,
            "total_points": self.total_points,
            "pass_percentage": self.pass_percentage,
            "question_count": len(self.questions) if self.questions else 0,
        }
        if include_questions and self.questions:
            data["questions"] = [q.to_dict(include_solution=False) for q in self.questions]
        return data


class AssessmentQuestion(db.Model):
    """
    Individual assessment question.
    Types: multiple_choice, pronunciation_awareness, sentence_construction, open_ended.
    """

    __tablename__ = "assessment_questions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = db.Column(db.String(36), db.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=True, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = db.Column(db.Integer, nullable=True)
    assessment_type = db.Column(db.String(30), nullable=False, default="initial")
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(40), nullable=False)  # multiple_choice, syllable_count, stress_choice, fill_blank, open_ended
    options = db.Column(db.JSON, nullable=True)  # List of option strings or key-value options
    correct_answer = db.Column(db.JSON, nullable=True)  # Correct answer key/text/indices
    rubric = db.Column(db.JSON, nullable=True)  # Scoring guidelines / criteria
    category = db.Column(db.String(80), nullable=False)  # e.g. "Syllables", "Behavioral", "Clarity"
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)  # beginner, intermediate, advanced
    points = db.Column(db.Integer, default=10, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    assessment = db.relationship("Assessment", back_populates="questions")
    goal = db.relationship("Goal", back_populates="assessment_questions")
    answers = db.relationship("AssessmentAnswer", back_populates="question", cascade="all, delete-orphan")

    def to_dict(self, include_solution: bool = False):
        data = {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "category": self.category,
            "difficulty": self.difficulty,
            "points": self.points,
            "display_order": self.display_order,
        }
        if include_solution:
            data["correct_answer"] = self.correct_answer
            data["rubric"] = self.rubric
            data["explanation"] = self.explanation
        return data


class AssessmentAttempt(db.Model):
    """
    Records a user's attempt at an assessment.
    Stores score, category-wise breakdown, calculated starting/progression level, strengths, and areas to practice.
    """

    __tablename__ = "assessment_attempts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = db.Column(db.String(36), db.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = db.Column(db.String(36), db.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=True, index=True)
    assessment_type = db.Column(db.String(30), default="initial", nullable=False)
    score = db.Column(db.Float, default=0.0, nullable=False)
    total_points = db.Column(db.Float, default=100.0, nullable=False)
    percentage = db.Column(db.Float, default=0.0, nullable=False)
    calculated_level = db.Column(db.Integer, default=1, nullable=False)
    passed_progression = db.Column(db.Boolean, nullable=True)  # True if scored >= pass_percentage on progression assessment
    status = db.Column(db.String(30), default="completed", nullable=False)  # in_progress, completed
    category_breakdown = db.Column(db.JSON, nullable=True)  # {"Category": {"score": X, "total": Y, "percentage": Z}}
    strengths = db.Column(db.JSON, nullable=True)  # List of strength strings
    areas_to_improve = db.Column(db.JSON, nullable=True)  # List of areas recommended for practice
    supportive_summary = db.Column(db.Text, nullable=True)
    ai_feedback = db.Column(db.JSON, nullable=True)
    started_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    user = db.relationship("User")
    goal = db.relationship("Goal")
    assessment = db.relationship("Assessment", back_populates="attempts")
    answers = db.relationship("AssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan", lazy="selectin")

    def to_dict(self, include_answers: bool = False):
        data = {
            "id": self.id,
            "goal_slug": self.goal.slug if self.goal else None,
            "assessment_id": self.assessment_id,
            "assessment_type": self.assessment_type,
            "score": self.score,
            "total_points": self.total_points,
            "percentage": self.percentage,
            "calculated_level": self.calculated_level,
            "passed_progression": self.passed_progression,
            "status": self.status,
            "category_breakdown": self.category_breakdown or {},
            "strengths": self.strengths or [],
            "areas_to_improve": self.areas_to_improve or [],
            "supportive_summary": self.supportive_summary,
            "ai_feedback": self.ai_feedback,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
        if include_answers and self.answers:
            data["answers"] = [a.to_dict() for a in self.answers]
        return data


class AssessmentAnswer(db.Model):
    """
    User response to a specific assessment question.
    """

    __tablename__ = "assessment_answers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = db.Column(db.String(36), db.ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = db.Column(db.String(36), db.ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_response = db.Column(db.JSON, nullable=True)  # Option key, text, or multiple answers
    is_correct = db.Column(db.Boolean, nullable=True)
    score_awarded = db.Column(db.Float, default=0.0, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    attempt = db.relationship("AssessmentAttempt", back_populates="answers")
    question = db.relationship("AssessmentQuestion", back_populates="answers")

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "user_response": self.user_response,
            "is_correct": self.is_correct,
            "score_awarded": self.score_awarded,
            "feedback": self.feedback,
        }
