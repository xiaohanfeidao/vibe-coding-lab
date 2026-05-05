from __future__ import annotations

from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    key: str
    title: str
    icon: str | None = None
    path: str | None = None
    children: list["MenuItem"] | None = None
    sort: int = 0
