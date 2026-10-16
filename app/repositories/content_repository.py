from typing import List, Optional, Type
from app.extensions import db
from app.models.content import (
    PronunciationWord,
    InterviewQuestion,
    PresentationTask,
    CommunicationExercise,
    GDQuestion,
)


class ContentRepository:
    """Data access layer for all 5 goal content datasets."""

    # 1. Pronunciation Words
    @staticmethod
    def get_pronunciation_words(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[PronunciationWord]:
        query = db.session.query(PronunciationWord).filter_by(is_active=True)
        if level is not None:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        return query.order_by(PronunciationWord.revision_priority.desc(), PronunciationWord.word).offset(offset).limit(limit).all()

    @staticmethod
    def get_pronunciation_word_by_id(word_id: str) -> Optional[PronunciationWord]:
        return db.session.query(PronunciationWord).filter_by(id=word_id).first()

    # 2. Interview Questions
    @staticmethod
    def get_interview_questions(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[InterviewQuestion]:
        query = db.session.query(InterviewQuestion).filter_by(is_active=True)
        if level is not None:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        return query.order_by(InterviewQuestion.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_interview_question_by_id(question_id: str) -> Optional[InterviewQuestion]:
        return db.session.query(InterviewQuestion).filter_by(id=question_id).first()

    # 3. Presentation Tasks
    @staticmethod
    def get_presentation_tasks(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[PresentationTask]:
        query = db.session.query(PresentationTask).filter_by(is_active=True)
        if level is not None:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        return query.order_by(PresentationTask.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_presentation_task_by_id(task_id: str) -> Optional[PresentationTask]:
        return db.session.query(PresentationTask).filter_by(id=task_id).first()

    # 4. Clear English / Communication Exercises
    @staticmethod
    def get_communication_exercises(
        level: Optional[int] = None,
        category: Optional[str] = None,
        exercise_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[CommunicationExercise]:
        query = db.session.query(CommunicationExercise).filter_by(is_active=True)
        if level is not None:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        if exercise_type:
            query = query.filter_by(exercise_type=exercise_type)
        return query.order_by(CommunicationExercise.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_communication_exercise_by_id(exercise_id: str) -> Optional[CommunicationExercise]:
        return db.session.query(CommunicationExercise).filter_by(id=exercise_id).first()

    # 5. GD & Professional Communication
    @staticmethod
    def get_gd_questions(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[GDQuestion]:
        query = db.session.query(GDQuestion).filter_by(is_active=True)
        if level is not None:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        return query.order_by(GDQuestion.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_gd_question_by_id(gd_id: str) -> Optional[GDQuestion]:
        return db.session.query(GDQuestion).filter_by(id=gd_id).first()
