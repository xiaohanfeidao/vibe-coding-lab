from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_current_user
from app.core.exceptions import UnauthorizedException
from app.core.response import success_response
from app.main import limiter
from app.modules.auth.schema import LoginRequest, RefreshRequest, TokenResponse, UserResponse
from app.modules.auth.service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest):
    if not authenticate_user(body.username, body.password):
        raise UnauthorizedException(message="用户名或密码错误")

    token_data = {"sub": body.username, "role": "admin"}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return success_response(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token).model_dump(),
    )


@auth_router.post("/refresh")
@limiter.limit("10/minute")
async def refresh(request: Request, body: RefreshRequest):
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException(message="无效的刷新令牌")
        token_data = {"sub": payload["sub"], "role": payload.get("role", "admin")}
        access_token = create_access_token(token_data)
        return success_response(
            data=TokenResponse(access_token=access_token, refresh_token=body.refresh_token).model_dump(),
        )
    except UnauthorizedException:
        raise
    except Exception:
        raise UnauthorizedException(message="刷新令牌已过期或无效")


@auth_router.post("/logout")
@limiter.limit("60/minute")
async def logout(request: Request):
    return success_response(data=None, message="已登出")


@auth_router.get("/me")
@limiter.limit("60/minute")
async def get_current_user_info(request: Request, current_user: dict = Depends(get_current_user)):
    return success_response(
        data=UserResponse(username=current_user["sub"], role=current_user.get("role", "admin")).model_dump(),
    )
