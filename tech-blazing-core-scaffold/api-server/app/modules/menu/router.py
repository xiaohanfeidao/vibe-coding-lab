from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.response import success_response
from app.main import limiter
from app.modules.menu.service import get_admin_menus, get_web_menus

menu_router = APIRouter()


@menu_router.get("/web/menus")
@limiter.limit("60/minute")
async def web_menus(request: Request):
    menus = get_web_menus()
    return success_response(data=[m.model_dump(exclude_none=True) for m in menus])


@menu_router.get("/admin/menus")
@limiter.limit("60/minute")
async def admin_menus(request: Request):
    menus = get_admin_menus()
    return success_response(data=[m.model_dump(exclude_none=True) for m in menus])
