# 启动指南

## 环境差异

| 特性 | 本地开发 (Win/Mac) | 生产环境 (Linux/Docker) |
|------|-------------------|----------------------|
| ASGI 服务器 | uvicorn（单进程 + 热重载） | gunicorn（多进程） |
| 热重载 | ✅ `--reload` | ❌ |
| Worker 数量 | 1 | CPU × 2 + 1 |
| 配置文件 | application-dev.yml | application-prod.yml |
| 日志格式 | text（可读） | json（结构化） |
| Debug 模式 | true | false |

## 快速启动

### 方式一：智能启动脚本（推荐）

```bash
cd api-server
python scripts/start.py
```

脚本自动检测：
- 操作系统 → Windows 用 uvicorn，Linux 用 gunicorn
- 环境变量 `APP_PROFILE` → 未设置则默认 dev
- 环境变量 `WORKERS` → 未设置则默认 CPU × 2 + 1

### 方式二：手动启动

**本地开发（Win/Mac/Linux 通用）：**

```bash
cd api-server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**生产环境（仅 Linux）：**

```bash
cd api-server
gunicorn app.main:app -c gunicorn.conf.py
```

**Docker 部署（任何 OS）：**

```bash
docker-compose up --build
```

### 方式三：环境变量控制

```bash
# 开发环境（默认）
APP_PROFILE=dev python scripts/start.py

# 生产环境
APP_PROFILE=prod python scripts/start.py

# 指定 worker 数量
WORKERS=8 APP_PROFILE=prod python scripts/start.py
```

## 前端启动

```bash
# web-app（前台门户）
cd web-app && pnpm dev

# admin-app（后台管理）
cd admin-app && pnpm dev
```

## 常见问题

### Q: Windows 下 gunicorn 报错？
A: gunicorn 不支持 Windows。使用 `python scripts/start.py` 或 `uvicorn` 代替。

### Q: 如何确认当前使用的是哪个配置？
A: 查看启动日志，会打印 `APP_PROFILE=dev/prod` 和 `workers=N`。

### Q: Docker 中为什么能用 gunicorn？
A: Docker 容器内是 Linux 环境，gunicorn 可以正常运行。
