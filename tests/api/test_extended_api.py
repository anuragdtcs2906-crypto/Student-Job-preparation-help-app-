import pytest


class TestExtendedAPI:
    def test_health_check(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "healthy"

    def test_goal_levels_and_progression_status_api(self, client, test_user):
        # 1. Get levels
        res = client.get("/api/v1/goals/interview/levels")
        assert res.status_code == 200
        data = res.get_json()
        assert len(data["data"]) == 5

        # 2. Get level details
        lvl_res = client.get("/api/v1/goals/interview/levels/2")
        assert lvl_res.status_code == 200
        assert lvl_res.get_json()["data"]["level_number"] == 2

        # 3. Check progression status
        client.post(
            "/api/v1/goals/select",
            headers=test_user["headers"],
            json={"goal_slugs": ["interview"]},
        )
        status_res = client.get(
            "/api/v1/goals/interview/progression-status",
            headers=test_user["headers"],
        )
        assert status_res.status_code == 200
        assert "eligible" in status_res.get_json()["data"]

    def test_single_item_routes(self, client):
        # Pronunciation single item
        w_list = client.get("/api/v1/pronunciation/words?limit=1").get_json()["data"]
        if w_list:
            w_res = client.get(f"/api/v1/pronunciation/words/{w_list[0]['id']}")
            assert w_res.status_code == 200
            assert w_res.get_json()["data"]["id"] == w_list[0]["id"]

        # Interview single item
        q_list = client.get("/api/v1/interviews/questions?limit=1").get_json()["data"]
        if q_list:
            q_res = client.get(f"/api/v1/interviews/questions/{q_list[0]['id']}")
            assert q_res.status_code == 200

        # Presentation single item
        p_list = client.get("/api/v1/presentations/tasks?limit=1").get_json()["data"]
        if p_list:
            p_res = client.get(f"/api/v1/presentations/tasks/{p_list[0]['id']}")
            assert p_res.status_code == 200

        # Communication single item
        c_list = client.get("/api/v1/communication/exercises?limit=1").get_json()["data"]
        if c_list:
            c_res = client.get(f"/api/v1/communication/exercises/{c_list[0]['id']}")
            assert c_res.status_code == 200

        # GD single item
        g_list = client.get("/api/v1/gd/questions?limit=1").get_json()["data"]
        if g_list:
            g_res = client.get(f"/api/v1/gd/questions/{g_list[0]['id']}")
            assert g_res.status_code == 200
