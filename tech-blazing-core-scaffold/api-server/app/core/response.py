from __future__ import annotations

from typing import Any

from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "ok", code: int = 0) -> dict:
    return {"code": code, "message": message, "data": data}


def error_response(message: str = "error", code: int = -1, data: Any = None, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "data": data},
    )
