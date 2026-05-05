from __future__ import annotations

import os

from pydantic import BaseModel, Field

from app.config.loader import load_config


class ServerSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    worker_class: str = "uvicorn.workers.UvicornWorker"


class AuthSettings(BaseModel):
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    admin_username: str = "admin"
    admin_password_hash: str = ""


class CorsSettings(BaseModel):
    origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])


class RateLimitSettings(BaseModel):
    enabled: bool = True
    default: str = "60/minute"
    auth: str = "10/minute"


class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "json"


class AppSettings(BaseModel):
    name: str = "tech-blazing-core-scaffold"
    version: str = "0.1.0"
    debug: bool = False
    server: ServerSettings = ServerSettings()
    auth: AuthSettings = AuthSettings()
    cors: CorsSettings = CorsSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    logging: LoggingSettings = LoggingSettings()
    menus: dict = Field(default_factory=dict)


def get_settings(profile: str | None = None) -> AppSettings:
    config = load_config(profile)
    return AppSettings(
        name=config.get("app", {}).get("name", "tech-blazing-core-scaffold"),
        version=config.get("app", {}).get("version", "0.1.0"),
        debug=config.get("app", {}).get("debug", False),
        server=ServerSettings(**config.get("server", {})),
        auth=AuthSettings(**config.get("auth", {})),
        cors=CorsSettings(**config.get("cors", {})),
        rate_limit=RateLimitSettings(**config.get("rate_limit", {})),
        logging=LoggingSettings(**config.get("logging", {})),
        menus=config.get("menus", {}),
    )


settings = get_settings(os.environ.get("APP_PROFILE"))
