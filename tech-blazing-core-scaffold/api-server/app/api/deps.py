from __future__ import annotations

from fastapi import Depends, Request

from app.core.exceptions import UnauthorizedException
from app.modules.auth.service import decode_token


async def get_current_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise UnauthorizedException(message="缺少认证令牌")

    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedException(message="无效的访问令牌")
        return payload
    except UnauthorizedException:
        raise
    except Exception:
        raise UnauthorizedException(message="访问令牌已过期或无效")
