import pytest


class TestModulesAPI:
    def test_pronunciation_words_api(self, client):
        res = client.get("/api/v1/pronunciation/words?level=1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) > 0
        word_item = data["data"][0]
        assert "word" in word_item
        assert "easy_pronunciation" in word_item
        assert "syllables" in word_item

    def test_interview_questions_api(self, client):
        res = client.get("/api/v1/interviews/questions?level=1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) > 0
        q_item = data["data"][0]
        assert "question" in q_item
        assert "category" in q_item

    def test_presentation_tasks_api(self, client):
        res = client.get("/api/v1/presentations/tasks?level=1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) > 0

    def test_communication_exercises_api(self, client):
        res = client.get("/api/v1/communication/exercises?level=1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) > 0

    def test_gd_questions_api(self, client):
        res = client.get("/api/v1/gd/questions?level=1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) > 0
