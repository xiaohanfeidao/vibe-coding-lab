@echo off
cd /d "%~dp0\.."

if not defined APP_PROFILE set APP_PROFILE=dev
if not defined SERVER_HOST set SERVER_HOST=127.0.0.1
if not defined SERVER_PORT set SERVER_PORT=8000

echo ============================================================
echo Tech Blazing Core Scaffold - API Server
echo ============================================================
echo OS:         Windows
echo Profile:    %APP_PROFILE%
echo Host:       %SERVER_HOST%
echo Port:       %SERVER_PORT%
echo Mode:       uvicorn (single process)
echo ============================================================

if "%APP_PROFILE%"=="dev" (
    python -m uvicorn app.main:app --reload --host %SERVER_HOST% --port %SERVER_PORT%
) else (
    python -m uvicorn app.main:app --host %SERVER_HOST% --port %SERVER_PORT% --workers 4
)
