import pytest


class TestProgressDashboardAPI:
    def test_dashboard_api(self, client, test_user):
        # Select goal
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["pronunciation", "interview"]},
        )

        res = client.get("/api/v1/dashboard", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "overall_metrics" in data["data"]
        assert len(data["data"]["goals"]) == 2

    def test_goal_progress_details_api(self, client, test_user):
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["presentation"]},
        )

        res = client.get("/api/v1/progress/presentation", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["goal"]["slug"] == "presentation"
        assert "recommendations" in data["data"]

    def test_recommendations_endpoint(self, client, test_user):
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["communication"]},
        )

        res = client.get("/api/v1/recommendations/communication", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
