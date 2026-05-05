from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, code: int = 500, message: str = "Internal Server Error", data: object = None):
        self.code = code
        self.message = message
        self.data = data


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(code=404, message=message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(code=401, message=message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(code=403, message=message)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(code=422, message=message)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": exc.data},
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Internal Server Error", "data": None},
    )
