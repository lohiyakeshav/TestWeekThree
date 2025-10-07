import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from app.tests.conftest import client, admin_token

class TestLoadTesting:
    def test_concurrent_order_creation(self, client, admin_token):
        """Test creating multiple orders concurrently"""
        def create_order():
            response = client.post(
                "/orders/create",
                headers={"Authorization": f"Bearer {admin_token}"},
                json={"success": True}
            )
            return response.status_code == 200
        
        # Create 10 orders concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_order) for _ in range(10)]
            results = [future.result() for future in futures]
        
        assert all(results)
        assert len(results) == 10

    def test_concurrent_login_attempts(self, client):
        """Test multiple login attempts concurrently"""
        def login():
            response = client.post("/auth/login", json={"username": "admin", "password": "Admin123"})
            return response.status_code == 200
        
        # Test 5 concurrent logins
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(login) for _ in range(5)]
            results = [future.result() for future in futures]
        
        assert all(results)
        assert len(results) == 5

    def test_high_frequency_order_requests(self, client, admin_token):
        """Test high frequency order creation requests"""
        start_time = time.time()
        success_count = 0
        
        # Create 50 orders rapidly
        for i in range(50):
            response = client.post(
                "/orders/create",
                headers={"Authorization": f"Bearer {admin_token}"},
                json={"success": i % 2 == 0}  # Alternate success/failure
            )
            if response.status_code == 200:
                success_count += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time (less than 10 seconds)
        assert duration < 10
        assert success_count == 50

    def test_concurrent_user_registration(self, client):
        """Test concurrent user registration"""
        def register_user(user_id):
            response = client.post("/auth/register", json={
                "username": f"user{user_id}",
                "email": f"user{user_id}@test.com",
                "password": "User123",
                "role": "user"
            })
            return response.status_code == 200
        
        # Register 5 users concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_user, i) for i in range(5)]
            results = [future.result() for future in futures]
        
        assert all(results)
        assert len(results) == 5

    def test_mixed_workload(self, client, admin_token):
        """Test mixed workload of different operations"""
        def mixed_operation(op_type, op_id):
            if op_type == "order":
                response = client.post(
                    "/orders/create",
                    headers={"Authorization": f"Bearer {admin_token}"},
                    json={"success": True}
                )
            elif op_type == "get_orders":
                response = client.get(
                    "/orders/",
                    headers={"Authorization": f"Bearer {admin_token}"}
                )
            elif op_type == "health":
                response = client.get("/health")
            else:
                return False
            
            return response.status_code == 200
        
        operations = ["order", "get_orders", "health"] * 10  # 30 operations total
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(mixed_operation, op, i) 
                for i, op in enumerate(operations)
            ]
            results = [future.result() for future in futures]
        
        assert all(results)
        assert len(results) == 30
