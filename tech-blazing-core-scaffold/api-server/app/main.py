from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config.settings import settings
from app.core.exceptions import AppException, app_exception_handler, global_exception_handler
from app.core.middleware import RequestTimingMiddleware, SecurityHeadersMiddleware
from app.core.response import success_response

limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.rate_limit.enabled,
    default_limits=[settings.rate_limit.default],
)


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.name,
        version=settings.version,
        debug=settings.debug,
    )

    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_exception_handler(AppException, app_exception_handler)
    application.add_exception_handler(Exception, global_exception_handler)

    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(RequestTimingMiddleware)

    from fastapi.middleware.cors import CORSMiddleware

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.v1.router import v1_router

    application.include_router(v1_router, prefix="/api")

    @application.get("/", include_in_schema=False)
    @limiter.limit(settings.rate_limit.default)
    async def root(request: Request):
        return success_response(data={"message": "tech-blazing-core-scaffold API", "version": settings.version})

    return application


app = create_app()
