import pytest
from fastapi.testclient import TestClient
from app.tests.conftest import client, admin_token, user_token, admin_user, regular_user

class TestAuthFlow:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

    def test_login_success(self, client, admin_user):
        response = client.post("/auth/login", json={"username": "admin", "password": "Admin123"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_info" in data
        assert data["user_info"]["username"] == "admin"
        assert data["user_info"]["role"] == "admin"

    def test_get_current_user(self, client, admin_token):
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "admin"

    def test_get_current_user_invalid_token(self, client):
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401

    def test_password_complexity_validation(self, client):
        # Test weak password
        response = client.post("/auth/register", json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "weak",
            "role": "user"
        })
        assert response.status_code == 400
        assert "Password must be at least 8 characters" in response.json()["detail"]
