from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.response import success_response
from app.main import limiter

web_router = APIRouter()


@web_router.get("/health")
@limiter.limit("60/minute")
async def web_health_check(request: Request):
    return success_response(data={"status": "healthy"})
