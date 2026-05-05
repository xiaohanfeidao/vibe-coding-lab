#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=== 1. 安装 admin-app 依赖 ==="
cd admin-app
npm install

echo "=== 2. 验证 admin-app 构建 ==="
npx vite build

echo "=== 3. 验证 api-server 测试 ==="
cd ../api-server
python -m pytest tests/ -v

echo "=== 4. 启动 api-server ==="
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

echo "=== 5. 启动 web-app (新终端) ==="
cd ../web-app && pnpm dev &

echo "=== 6. 启动 admin-app (新终端) ==="
cd ../admin-app && pnpm dev &

wait
