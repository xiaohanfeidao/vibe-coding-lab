from __future__ import annotations

from app.config.settings import settings
from app.modules.menu.schema import MenuItem


def get_web_menus() -> list[MenuItem]:
    raw = settings.menus.get("web", [])
    return [MenuItem(**item) for item in raw]


def get_admin_menus() -> list[MenuItem]:
    raw = settings.menus.get("admin", [])
    return [MenuItem(**item) for item in raw]
