import pytest


class TestPracticeAPI:
    def test_practice_session_lifecycle(self, client, test_user):
        # 1. Start session
        start_res = client.post(
            "/api/v1/practice/sessions/start",
            headers=test_user["headers"],
            json={"goal_slug": "pronunciation", "target_count": 5},
        )
        assert start_res.status_code == 201
        session_id = start_res.get_json()["data"]["id"]

        # 2. Get active session
        active_res = client.get(
            "/api/v1/practice/sessions/active/pronunciation",
            headers=test_user["headers"],
        )
        assert active_res.status_code == 200
        assert active_res.get_json()["data"]["id"] == session_id

        # 3. Submit attempt
        attempt_res = client.post(
            "/api/v1/practice/attempts",
            headers=test_user["headers"],
            json={
                "session_id": session_id,
                "content_type": "pronunciation_words",
                "content_id": "test-word-1",
                "user_input": "KUMF-ter-bul",
                "is_completed": True,
                "marked_for_revision": True,
                "time_spent_seconds": 30,
                "request_ai_feedback": False,
            },
        )
        assert attempt_res.status_code == 200
        assert attempt_res.get_json()["data"]["is_completed"] is True

        # 4. Complete session
        complete_res = client.post(
            f"/api/v1/practice/sessions/{session_id}/complete",
            headers=test_user["headers"],
            json={"duration_seconds": 45},
        )
        assert complete_res.status_code == 200
        assert complete_res.get_json()["data"]["status"] == "completed"
