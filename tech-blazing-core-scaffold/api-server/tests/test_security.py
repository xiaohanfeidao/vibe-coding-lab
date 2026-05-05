from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_security_headers_present(async_client):
    response = await async_client.get("/api/v1/web/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "strict-transport-security" in response.headers
    assert "content-security-policy" in response.headers
    assert "referrer-policy" in response.headers


@pytest.mark.asyncio
async def test_response_timing_header(async_client):
    response = await async_client.get("/api/v1/web/health")
    assert "x-response-time" in response.headers


@pytest.mark.asyncio
async def test_cors_allows_configured_origin(async_client):
    response = await async_client.options(
        "/api/v1/web/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
async def test_cors_blocks_unknown_origin(async_client):
    response = await async_client.options(
        "/api/v1/web/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" not in response.headers
