import pytest


class TestGoalsAPI:
    def test_list_all_goals(self, client):
        res = client.get("/api/v1/goals")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 5
        slugs = [g["slug"] for g in data["data"]]
        assert "pronunciation" in slugs
        assert "interview" in slugs
        assert "presentation" in slugs
        assert "communication" in slugs
        assert "gd" in slugs

    def test_get_single_goal(self, client):
        res = client.get("/api/v1/goals/interview")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["slug"] == "interview"
        assert len(data["data"]["levels"]) == 5

    def test_select_goals(self, client, test_user):
        res = client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["pronunciation", "interview"]},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 2

    def test_get_my_goals(self, client, test_user):
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["presentation"]},
        )
        res = client.get("/api/v1/goals/my-goals", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) >= 1

    def test_update_daily_target(self, client, test_user):
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["pronunciation"]},
        )
        res = client.put(
            "/api/v1/goals/pronunciation/targets",
            headers=test_user["headers"],
            json={"target_quantity": 15, "target_type": "words"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["target_quantity"] == 15
