from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_web_health_check(async_client):
    response = await async_client.get("/api/v1/web/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "ok"
    assert data["data"]["status"] == "healthy"


@pytest.mark.asyncio
async def test_admin_health_check(async_client):
    response = await async_client.get("/api/v1/admin/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "version" in data["data"]
