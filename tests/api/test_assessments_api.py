import pytest


class TestAssessmentsAPI:
    def test_get_diagnostic_assessment(self, client):
        res = client.get("/api/v1/assessments/pronunciation/diagnostic")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "questions" in data["data"]
        assert len(data["data"]["questions"]) == 5

    def test_submit_diagnostic_assessment(self, client, test_user):
        # 1. Fetch questions
        get_res = client.get("/api/v1/assessments/interview/diagnostic")
        questions = get_res.get_json()["data"]["questions"]

        # 2. Submit answers
        answers = [{"question_id": q["id"], "user_response": "B"} for q in questions]
        sub_res = client.post(
            "/api/v1/assessments/interview/submit",
            headers=test_user["headers"],
            json={"answers": answers},
        )
        assert sub_res.status_code == 200
        data = sub_res.get_json()
        assert data["success"] is True
        assert "calculated_level" in data["data"]
        assert "strengths" in data["data"]
        assert "supportive_summary" in data["data"]

    def test_get_assessment_history(self, client, test_user):
        res = client.get("/api/v1/assessments/interview/history", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
