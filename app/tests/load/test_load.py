import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from app.tests.conftest import client, admin_token

class TestLoadTesting:
    def test_light_concurrent_order_creation(self, client, admin_token):
        """Lightweight concurrency sanity check"""
        def create_order():
            response = client.post(
                "/orders/create",
                headers={"Authorization": f"Bearer {admin_token}"},
                json={"success": True}
            )
            return response.status_code == 200

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_order) for _ in range(3)]
            results = [future.result() for future in futures]

        assert all(results)
        assert len(results) == 3
