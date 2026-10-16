import uuid
from datetime import datetime, timezone
from app.extensions import db


class PronunciationWord(db.Model):
    """
    Pronunciation learning item (text-based learning module for V1).
    """

    __tablename__ = "pronunciation_words"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    word = db.Column(db.String(100), nullable=False, index=True)
    easy_pronunciation = db.Column(db.String(150), nullable=False)  # e.g., "AR-ki-tek-cher"
    syllables = db.Column(db.JSON, nullable=False)  # e.g. ["ar", "chi", "tec", "ture"]
    stress_info = db.Column(db.String(100), nullable=True)  # e.g. "Primary stress on first syllable (AR)"
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)  # beginner, intermediate, advanced
    level = db.Column(db.Integer, default=1, nullable=False, index=True)  # 1 to 5
    category = db.Column(db.String(80), nullable=False, index=True)  # Technical, Professional, Academic, Everyday
    example_sentence = db.Column(db.Text, nullable=False)
    meaning = db.Column(db.Text, nullable=True)
    revision_priority = db.Column(db.Integer, default=1, nullable=False)  # 1 (normal) to 5 (high)
    common_difficulty = db.Column(db.Text, nullable=True)  # Helpful tip for common stumbling blocks
    audio_url = db.Column(db.String(255), nullable=True)  # Reference audio URL for future/frontend use
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "easy_pronunciation": self.easy_pronunciation,
            "syllables": self.syllables,
            "stress_info": self.stress_info,
            "difficulty": self.difficulty,
            "level": self.level,
            "category": self.category,
            "example_sentence": self.example_sentence,
            "meaning": self.meaning,
            "revision_priority": self.revision_priority,
            "common_difficulty": self.common_difficulty,
            "audio_url": self.audio_url,
        }


class InterviewQuestion(db.Model):
    """
    Interview question module item.
    """

    __tablename__ = "interview_questions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)  # Introduction, HR, Behavioral, Situational, Project, Technical, Teamwork, Problem Solving, Communication
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False, index=True)  # 1 to 5
    expected_skill = db.Column(db.String(150), nullable=True)  # e.g. "STAR framework, concise problem description"
    evaluation_criteria = db.Column(db.JSON, nullable=True)  # list of key evaluation points
    sample_guidance = db.Column(db.Text, nullable=True)  # Helpful tip on framing response
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "category": self.category,
            "difficulty": self.difficulty,
            "level": self.level,
            "expected_skill": self.expected_skill,
            "evaluation_criteria": self.evaluation_criteria or [],
            "sample_guidance": self.sample_guidance,
        }


class PresentationTask(db.Model):
    """
    Presentation practice task module item.
    """

    __tablename__ = "presentation_tasks"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)  # Self-intro, Project pitch, Technical concept, Slide explanation, 1-min topic, 2-min topic, Intro/Conclusion, Q&A
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False, index=True)  # 1 to 5
    evaluation_criteria = db.Column(db.JSON, nullable=True)
    sample_outline = db.Column(db.JSON, nullable=True)  # Suggested structured outline points
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "category": self.category,
            "difficulty": self.difficulty,
            "level": self.level,
            "evaluation_criteria": self.evaluation_criteria or [],
            "sample_outline": self.sample_outline or [],
        }


class CommunicationExercise(db.Model):
    """
    Clear English & Communication practice exercise item.
    """

    __tablename__ = "communication_exercises"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exercise_type = db.Column(db.String(60), nullable=False)  # sentence_construction, vocabulary, sentence_improvement, everyday_communication, professional_communication, response_selection
    prompt = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=True)  # Multiple choices if applicable
    correct_answer = db.Column(db.JSON, nullable=True)  # Correct answer key or model answer
    explanation = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=False, index=True)
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False, index=True)  # 1 to 5
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self, include_solution: bool = False):
        data = {
            "id": self.id,
            "exercise_type": self.exercise_type,
            "prompt": self.prompt,
            "options": self.options,
            "category": self.category,
            "difficulty": self.difficulty,
            "level": self.level,
        }
        if include_solution:
            data["correct_answer"] = self.correct_answer
            data["explanation"] = self.explanation
        return data


class GDQuestion(db.Model):
    """
    Group Discussion & Professional Communication scenario item.
    """

    __tablename__ = "gd_questions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = db.Column(db.String(255), nullable=False)
    scenario = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)  # Opinion, Respectful Disagreement, Building on Points, Clarification, Summary, Conciseness, Workplace Teamwork
    difficulty = db.Column(db.String(30), default="intermediate", nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False, index=True)  # 1 to 5
    perspective_points = db.Column(db.JSON, nullable=True)  # Different perspectives for thoughtful discussion
    evaluation_criteria = db.Column(db.JSON, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "scenario": self.scenario,
            "category": self.category,
            "difficulty": self.difficulty,
            "level": self.level,
            "perspective_points": self.perspective_points or [],
            "evaluation_criteria": self.evaluation_criteria or [],
        }
