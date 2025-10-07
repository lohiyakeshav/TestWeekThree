import pytest
from fastapi.testclient import TestClient
from app.tests.conftest import client, admin_token, user_token, admin_user, regular_user

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
