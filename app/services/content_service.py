from typing import List, Dict, Any, Optional
from app.repositories.content_repository import ContentRepository
from app.utils.exceptions import NotFoundError


class ContentService:
    """Service providing content queries and lookups for all 5 learning modules."""

    # 1. Pronunciation
    @staticmethod
    def get_pronunciation_words(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        words = ContentRepository.get_pronunciation_words(level, category, limit, offset)
        return [w.to_dict() for w in words]

    @staticmethod
    def get_pronunciation_word_by_id(word_id: str) -> Dict[str, Any]:
        word = ContentRepository.get_pronunciation_word_by_id(word_id)
        if not word:
            raise NotFoundError("Pronunciation word not found.")
        return word.to_dict()

    # 2. Interview
    @staticmethod
    def get_interview_questions(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        questions = ContentRepository.get_interview_questions(level, category, limit, offset)
        return [q.to_dict() for q in questions]

    @staticmethod
    def get_interview_question_by_id(question_id: str) -> Dict[str, Any]:
        q = ContentRepository.get_interview_question_by_id(question_id)
        if not q:
            raise NotFoundError("Interview question not found.")
        return q.to_dict()

    # 3. Presentation
    @staticmethod
    def get_presentation_tasks(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        tasks = ContentRepository.get_presentation_tasks(level, category, limit, offset)
        return [t.to_dict() for t in tasks]

    @staticmethod
    def get_presentation_task_by_id(task_id: str) -> Dict[str, Any]:
        task = ContentRepository.get_presentation_task_by_id(task_id)
        if not task:
            raise NotFoundError("Presentation task not found.")
        return task.to_dict()

    # 4. Clear English / Communication
    @staticmethod
    def get_communication_exercises(
        level: Optional[int] = None,
        category: Optional[str] = None,
        exercise_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        exercises = ContentRepository.get_communication_exercises(level, category, exercise_type, limit, offset)
        return [e.to_dict(include_solution=True) for e in exercises]

    @staticmethod
    def get_communication_exercise_by_id(exercise_id: str) -> Dict[str, Any]:
        exercise = ContentRepository.get_communication_exercise_by_id(exercise_id)
        if not exercise:
            raise NotFoundError("Communication exercise not found.")
        return exercise.to_dict(include_solution=True)

    # 5. GD & Professional Communication
    @staticmethod
    def get_gd_questions(
        level: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        gds = ContentRepository.get_gd_questions(level, category, limit, offset)
        return [g.to_dict() for g in gds]

    @staticmethod
    def get_gd_question_by_id(gd_id: str) -> Dict[str, Any]:
        gd = ContentRepository.get_gd_question_by_id(gd_id)
        if not gd:
            raise NotFoundError("Group discussion topic not found.")
        return gd.to_dict()
