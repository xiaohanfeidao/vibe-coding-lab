#!/bin/bash
set -e

cd "$(dirname "$0")/.."

export APP_PROFILE="${APP_PROFILE:-dev}"
export SERVER_HOST="${SERVER_HOST:-127.0.0.1}"
export SERVER_PORT="${SERVER_PORT:-8000}"

echo "============================================================"
echo "Tech Blazing Core Scaffold - API Server"
echo "============================================================"
echo "Profile:    $APP_PROFILE"
echo "Host:       $SERVER_HOST"
echo "Port:       $SERVER_PORT"

if [ "$APP_PROFILE" = "dev" ]; then
    echo "Mode:       uvicorn (single process + reload)"
    echo "============================================================"
    python -m uvicorn app.main:app --reload --host "$SERVER_HOST" --port "$SERVER_PORT"
else
    echo "Mode:       gunicorn (multi process)"
    echo "============================================================"
    exec gunicorn app.main:app -c gunicorn.conf.py
fi
