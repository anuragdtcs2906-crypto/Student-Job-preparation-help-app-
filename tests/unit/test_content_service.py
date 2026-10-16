import pytest
from app.services.content_service import ContentService
from app.utils.exceptions import NotFoundError


class TestContentServiceUnit:
    def test_pronunciation_words_lookup(self, app):
        with app.app_context():
            words = ContentService.get_pronunciation_words(level=1)
            assert len(words) > 0
            word_id = words[0]["id"]
            single_word = ContentService.get_pronunciation_word_by_id(word_id)
            assert single_word["id"] == word_id

            with pytest.raises(NotFoundError):
                ContentService.get_pronunciation_word_by_id("non-existent-id")

    def test_interview_questions_lookup(self, app):
        with app.app_context():
            qs = ContentService.get_interview_questions(level=1)
            assert len(qs) > 0
            q_id = qs[0]["id"]
            single_q = ContentService.get_interview_question_by_id(q_id)
            assert single_q["id"] == q_id

            with pytest.raises(NotFoundError):
                ContentService.get_interview_question_by_id("non-existent-id")

    def test_presentation_tasks_lookup(self, app):
        with app.app_context():
            tasks = ContentService.get_presentation_tasks(level=1)
            assert len(tasks) > 0
            task_id = tasks[0]["id"]
            single_task = ContentService.get_presentation_task_by_id(task_id)
            assert single_task["id"] == task_id

            with pytest.raises(NotFoundError):
                ContentService.get_presentation_task_by_id("non-existent-id")

    def test_communication_exercises_lookup(self, app):
        with app.app_context():
            exercises = ContentService.get_communication_exercises(level=1)
            assert len(exercises) > 0
            ex_id = exercises[0]["id"]
            single_ex = ContentService.get_communication_exercise_by_id(ex_id)
            assert single_ex["id"] == ex_id

            with pytest.raises(NotFoundError):
                ContentService.get_communication_exercise_by_id("non-existent-id")

    def test_gd_questions_lookup(self, app):
        with app.app_context():
            gds = ContentService.get_gd_questions(level=1)
            assert len(gds) > 0
            gd_id = gds[0]["id"]
            single_gd = ContentService.get_gd_question_by_id(gd_id)
            assert single_gd["id"] == gd_id

            with pytest.raises(NotFoundError):
                ContentService.get_gd_question_by_id("non-existent-id")
