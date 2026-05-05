from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post(
        "/api/v1/admin/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    response = await async_client.post(
        "/api/v1/admin/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_username(async_client):
    response = await async_client.post(
        "/api/v1/admin/auth/login",
        json={"username": "nonexistent", "password": "admin123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(async_client):
    login_resp = await async_client.post(
        "/api/v1/admin/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await async_client.get(
        "/api/v1/admin/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "admin"
    assert data["data"]["role"] == "admin"


@pytest.mark.asyncio
async def test_get_current_user_no_token(async_client):
    response = await async_client.get("/api/v1/admin/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(async_client):
    login_resp = await async_client.post(
        "/api/v1/admin/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    refresh_token = login_resp.json()["data"]["refresh_token"]

    response = await async_client.post(
        "/api/v1/admin/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_logout(async_client):
    response = await async_client.post("/api/v1/admin/auth/logout")
    assert response.status_code == 200
