import pytest


class TestAuthAPI:
    def test_anonymous_registration_endpoint(self, client):
        res = client.post("/api/v1/auth/anonymous")
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert "anonymous_id" in data["data"]
        assert len(data["data"]["anonymous_id"]) == 8
        assert "access_token" in data["data"]

    def test_anonymous_login_endpoint(self, client):
        # 1. Create account
        reg_res = client.post("/api/v1/auth/anonymous")
        anon_id = reg_res.get_json()["data"]["anonymous_id"]

        # 2. Login
        login_res = client.post("/api/v1/auth/login", json={"anonymous_id": anon_id})
        assert login_res.status_code == 200
        data = login_res.get_json()
        assert data["success"] is True
        assert data["data"]["anonymous_id"] == anon_id
        assert "access_token" in data["data"]

    def test_anonymous_login_invalid_format(self, client):
        res = client.post("/api/v1/auth/login", json={"anonymous_id": "INVALID!"})
        assert res.status_code == 400
        data = res.get_json()
        assert data["success"] is False
        assert data["error"]["code"] == "VALIDATION_ERROR"

    def test_anonymous_login_not_found(self, client):
        res = client.post("/api/v1/auth/login", json={"anonymous_id": "ZZZZZZZZ"})
        assert res.status_code == 404
        data = res.get_json()
        assert data["success"] is False

    def test_get_me_endpoint(self, client, test_user):
        res = client.get("/api/v1/auth/me", headers=test_user["headers"])
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["anonymous_id"] == test_user["anonymous_id"]
