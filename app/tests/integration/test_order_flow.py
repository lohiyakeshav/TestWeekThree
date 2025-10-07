import pytest
from fastapi.testclient import TestClient
from app.tests.conftest import client, admin_token, user_token, admin_user, regular_user


class DummyCallRecorder:
    def __init__(self):
        self.calls = []
    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))

class TestOrderFlow:
    def test_create_successful_order(self, client, admin_token):
        response = client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data

    def test_create_failed_order(self, client, admin_token):
        response = client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data

    def test_background_email_task_invoked_on_success(self, client, admin_token, monkeypatch):
        # Arrange: monkeypatch EmailService to capture background task invocation
        from app.services import email_service as email_module
        success_recorder = DummyCallRecorder()
        failure_recorder = DummyCallRecorder()
        monkeypatch.setattr(email_module.EmailService, "send_success_email", success_recorder)
        monkeypatch.setattr(email_module.EmailService, "send_failure_email", failure_recorder)

        # Act
        response = client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": True}
        )
        assert response.status_code == 200

        # BackgroundTasks in TestClient execute after response by Starlette's TestClient
        # Validate that our recorder was scheduled and executed
        assert len(success_recorder.calls) == 1
        # First arg is the email string
        assert isinstance(success_recorder.calls[0][0][0], str)
        assert len(failure_recorder.calls) == 0

    def test_background_email_task_invoked_on_failure(self, client, admin_token, monkeypatch):
        from app.services import email_service as email_module
        success_recorder = DummyCallRecorder()
        failure_recorder = DummyCallRecorder()
        monkeypatch.setattr(email_module.EmailService, "send_success_email", success_recorder)
        monkeypatch.setattr(email_module.EmailService, "send_failure_email", failure_recorder)

        response = client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": False}
        )
        assert response.status_code == 200

        assert len(failure_recorder.calls) == 1
        assert isinstance(failure_recorder.calls[0][0][0], str)
        assert len(success_recorder.calls) == 0

    def test_get_orders_as_admin(self, client, admin_token):
        # Create a test order first
        client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": True}
        )
        
        response = client.get(
            "/orders/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert len(data["orders"]) >= 1

    def test_get_orders_as_user(self, client, user_token):
        response = client.get(
            "/orders/",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        # User should only see their own orders
        assert len(data["orders"]) == 0  # No orders created by this user yet

    def test_order_rollback_simulation(self, client, admin_token):
        # Test that failed orders are still created (simulation)
        response = client.post(
            "/orders/create",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"success": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
