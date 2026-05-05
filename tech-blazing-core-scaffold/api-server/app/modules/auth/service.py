from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config.settings import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12),
    ).decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.auth.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.auth.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])


def authenticate_user(username: str, password: str) -> bool:
    if username != settings.auth.admin_username:
        return False
    if not settings.auth.admin_password_hash:
        return False
    return verify_password(password, settings.auth.admin_password_hash)
