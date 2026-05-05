from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_web_menus(async_client):
    response = await async_client.get("/api/v1/web/menus")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]) > 0
    assert data["data"][0]["key"] == "home"
    assert data["data"][0]["title"] == "首页"


@pytest.mark.asyncio
async def test_admin_menus(async_client):
    response = await async_client.get("/api/v1/admin/menus")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]) > 0
    assert data["data"][0]["key"] == "dashboard"


@pytest.mark.asyncio
async def test_admin_menus_has_children(async_client):
    response = await async_client.get("/api/v1/admin/menus")
    data = response.json()
    system_menu = next((m for m in data["data"] if m["key"] == "system"), None)
    assert system_menu is not None
    assert system_menu.get("children") is not None
    assert len(system_menu["children"]) > 0
