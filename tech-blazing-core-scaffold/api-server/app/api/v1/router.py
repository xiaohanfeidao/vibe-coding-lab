from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.web.router import web_router
from app.api.v1.admin.router import admin_router
from app.modules.menu.router import menu_router

v1_router = APIRouter()
v1_router.include_router(web_router, prefix="/v1/web", tags=["web"])
v1_router.include_router(admin_router, prefix="/v1/admin", tags=["admin"])
v1_router.include_router(menu_router, prefix="/v1", tags=["menu"])
