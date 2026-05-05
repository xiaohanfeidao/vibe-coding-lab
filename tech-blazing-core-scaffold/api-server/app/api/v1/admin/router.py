from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.response import success_response
from app.main import limiter
from app.modules.auth.router import auth_router

admin_router = APIRouter()
admin_router.include_router(auth_router)


@admin_router.get("/health")
@limiter.limit("60/minute")
async def admin_health_check(request: Request):
    return success_response(data={"status": "healthy"})
