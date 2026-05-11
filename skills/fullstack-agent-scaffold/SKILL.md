---
name: fullstack-agent-scaffold
description: Scaffolds production-grade full-stack applications with AI agent capabilities. Use when starting a new full-stack project that needs a React frontend (web-app + admin-app), FastAPI backend, and AgentScope multi-agent integration. Use when building applications that combine traditional web UI with intelligent agent workflows.
---

# Full-Stack Agent Scaffold

Build production-grade full-stack applications with embedded AI agent capabilities. This skill provides a battle-tested scaffold combining React frontends, FastAPI backend, and AgentScope multi-agent framework — so you start with working auth, API routing, agent orchestration, and deployment instead of wiring them from scratch.

## When to Use

- Starting a new full-stack project that needs both web UI and AI agent features
- Building an application where users interact with intelligent agents through a web interface
- Creating a multi-tenant system with separate front-office (web-app) and back-office (admin-app) frontends
- Projects requiring JWT authentication, role-based menus, and agent-driven workflows
- Any project that needs FastAPI + React + AgentScope as the core stack

**When NOT to use:** Static websites, simple APIs without a frontend, projects that don't need AI agent capabilities, or when a simpler stack (e.g., Next.js alone) suffices.

## Architecture Overview

四层独立架构：前端（web-app / admin-app）、API 后端（FastAPI）、智能体层（AgentScope）三者完全解耦，FastAPI 与 AgentScope 之间无任何直接通信。

**核心原则：FastAPI 只做记忆服务和 REST 接口，Agent 相关功能全部由 AgentScope 独立承担，禁止 FastAPI 包装 AgentScope。**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Docker / K8s                                     │
│                                                                           │
│  ┌──────────┐  ┌──────────┐     ┌──────────────────┐     ┌──────────────┐  │
│  │ web-app  │  │admin-app │     │   api-server     │     │  AgentScope  │  │
│  │ :5173    │  │ :5174    │     │   (FastAPI)      │     │  Server      │  │
│  │ React    │  │ React    │     │   :8000          │     │   :8080      │  │
│  │ Arco     │  │ Arco     │◄────►│  Auth / Menu    │     │              │  │
│  └────┬─────┘  │ +Auth    │     │  Memory Service  │     │ ReActAgent   │  │
│       │        └──────────┘     │  /api/v1/web/   │     │ MsgHub       │  │
│       │                          │  /api/v1/admin/ │     │ Pipeline     │  │
│       │                          └──────────────────┘     │ Toolkit      │  │
│       │                                                    │ Session      │  │
│       └────────────────────────────────────────────────────┘              │
│                          web-app ↔ AgentScope (直接通信)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**架构说明：**
- **web-app**：前台门户，面向终端用户，直接与 AgentScope 通信进行 AI 交互
- **admin-app**：后台管理，面向管理员，通过 FastAPI 管理系统配置和监控数据
- **api-server（FastAPI）**：仅负责认证、菜单、记忆服务、数据持久化等 REST 接口，**不涉及任何 Agent 逻辑**
- **AgentScope Server**：独立运行的智能体服务，处理所有 AI 推理、工具调用、多智能体协作、会话管理

**通信关系：**
1. **web-app ↔ AgentScope**：前端直接调用 AgentScope Server API（WebSocket / HTTP :8080）
2. **admin-app ↔ api-server**：通过 `/api/v1/admin/` 路径通信（需要 JWT 认证）
3. **web-app ↔ api-server**：通过 `/api/v1/web/` 路径通信（健康检查、菜单获取、记忆查询等）
4. **api-server ↔ AgentScope**：**无直接通信**，两者完全独立

## Tech Stack

### api-server (Python Backend)

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Runtime |
| FastAPI | 0.115+ | Web framework |
| Uvicorn | 0.34+ | ASGI server |
| Gunicorn | 23+ | Multi-process manager |
| PyYAML | 6+ | Parse application.yml |
| Pydantic | 2+ | Data validation & Settings |
| Pydantic Settings | 2+ | Configuration models |
| slowapi | 0.1+ | API rate limiting |
| PyJWT | 2.9+ | JWT token generation & verification |
| passlib | 1.7+ | Password hashing (bcrypt) |
| httpx | 0.28+ | Async HTTP client (testing) |
| pytest | 8+ | Test framework |
| pytest-asyncio | 0.24+ | Async test support |
| ruff | 0.8+ | Linter + Formatter |

### web-app & admin-app (React Frontend)

| Dependency | Version | Purpose |
|---|---|---|
| Node.js | 18+ | Runtime |
| React | 18+ | UI framework |
| TypeScript | 5+ | Type system |
| Vite | 6+ | Build tool |
| @arco-design/web-react | 2.67+ | UI component library |
| React Router | 7+ | Routing |
| Axios | 1+ | HTTP client |
| Vitest | 3+ | Unit testing |

### AgentScope (AI Agent Layer)

| Component | Purpose |
|---|---|
| ReActAgent | Reasoning-Acting agent with tool use, memory, RAG |
| MsgHub | Publish-subscribe multi-agent communication |
| SequentialPipeline | Sequential agent execution |
| FanoutPipeline | Parallel agent execution |
| Toolkit | Tool registration and MCP integration |
| InMemoryMemory / RedisMemory | Working memory backends |
| KnowledgeBase | RAG with vector store integration |
| JSONSession / RedisSession | Conversation state persistence |
| OpenTelemetry | Tracing and observability |

## Project Structure

```
project-root/
├── pnpm-workspace.yaml
├── package.json
├── docker-compose.yml
├── .gitignore
│
├── api-server/                       # FastAPI — 仅做记忆服务和 REST 接口
│   ├── pyproject.toml
│   ├── gunicorn.conf.py
│   ├── Dockerfile
│   ├── config/
│   │   ├── application.yml
│   │   ├── application-dev.yml
│   │   └── application-prod.yml      # .gitignored
│   ├── scripts/
│   │   ├── start.py                  # Cross-platform launcher
│   │   ├── start.sh
│   │   └── start.bat
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app factory
│   │   ├── config/
│   │   │   ├── loader.py             # YAML loader + env var resolution
│   │   │   └── settings.py           # Pydantic Settings models
│   │   ├── core/
│   │   │   ├── exceptions.py         # Unified exception hierarchy
│   │   │   ├── middleware.py         # Request timing + security headers
│   │   │   ├── response.py          # Unified response format
│   │   │   └── security.py          # Security utilities
│   │   ├── api/
│   │   │   ├── deps.py              # Dependency injection
│   │   │   └── v1/
│   │   │       ├── router.py         # v1 route aggregation
│   │   │       ├── web/
│   │   │       │   └── router.py     # /api/v1/web/ routes
│   │   │       └── admin/
│   │   │           └── router.py     # /api/v1/admin/ routes
│   │   ├── modules/
│   │   │   ├── health/               # Health check
│   │   │   ├── auth/                 # JWT authentication
│   │   │   │   ├── schema.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── menu/                 # Menu configuration
│   │   │   │   ├── schema.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   └── memory/               # 记忆服务（AgentScope 的记忆后端）
│   │   │       ├── schema.py         # Memory request/response models
│   │   │       ├── service.py        # Memory CRUD logic
│   │   │       └── router.py         # /api/v1/web/memory/ + /admin/memory/
│   │   └── utils/
│   │       └── pagination.py
│   └── tests/
│
├── agent-server/                     # AgentScope 独立服务（与 FastAPI 无关）
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── config/
│   │   └── agent_config.yml          # AgentScope 专属配置
│   ├── scripts/
│   │   ├── start.py                  # AgentScope Server 启动脚本
│   │   ├── start.sh
│   │   └── start.bat
│   ├── app/
│   │   ├── __init__.py
│   │   ├── server.py                 # AgentScope HTTP/WS Server 入口
│   │   ├── config/
│   │   │   └── settings.py           # AgentScope 配置模型
│   │   ├── agents/                   # Agent 定义
│   │   │   ├── __init__.py
│   │   │   ├── assistant.py          # 默认 ReActAgent
│   │   │   ├── planner.py            # 规划 Agent
│   │   │   └── researcher.py         # 研究 Agent
│   │   ├── tools/                    # 自定义工具
│   │   │   ├── __init__.py
│   │   │   ├── weather.py
│   │   │   ├── knowledge.py          # RAG 检索工具
│   │   │   └── database.py           # 数据库查询工具
│   │   ├── pipelines/                # 多 Agent 工作流
│   │   │   ├── __init__.py
│   │   │   ├── chat_pipeline.py      # 单 Agent 对话
│   │   │   ├── research_pipeline.py  # 多 Agent 协作
│   │   │   └── review_pipeline.py    # 并行审查
│   │   ├── memory/                   # Agent 记忆管理
│   │   │   ├── __init__.py
│   │   │   └── memory_manager.py     # 记忆压缩 + 长期记忆
│   │   ├── session/                  # 会话管理
│   │   │   ├── __init__.py
│   │   │   └── session_manager.py    # JSON / Redis 会话
│   │   └── rag/                      # RAG 知识库
│   │       ├── __init__.py
│   │       └── knowledge_base.py
│   └── tests/
│
├── web-app/                          # Front-office (public-facing)
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── api/
│       │   ├── client.ts             # Axios instance (api-server)
│       │   ├── agent-client.ts       # AgentScope Server client (WS/HTTP)
│       │   └── modules/
│       │       ├── health.ts
│       │       ├── menu.ts
│       │       ├── memory.ts         # 记忆服务 API
│       │       └── agent.ts          # Agent chat API (直连 AgentScope)
│       ├── components/Layout/
│       │   └── AppLayout.tsx         # Header + Menu + Content + Footer
│       ├── pages/
│       │   ├── Home/
│       │   ├── Features/
│       │   ├── About/
│       │   ├── Contact/
│       │   └── AgentChat/            # Agent 交互页面（直连 AgentScope）
│       ├── router/
│       ├── styles/
│       │   ├── arco-theme.css        # Arco Design Token overrides
│       │   └── global.css
│       └── types/
│           └── api.d.ts
│
├── admin-app/                        # Back-office (management)
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── api/
│       │   ├── client.ts             # Axios + Token management + 401 refresh
│       │   ├── auth.ts               # Login/logout/refresh/me
│       │   └── modules/
│       │       ├── health.ts
│       │       ├── menu.ts
│       │       └── memory.ts         # 记忆管理 API
│       ├── components/Layout/
│       │   └── AdminLayout.tsx       # Sider + Menu + Header + Content
│       ├── pages/
│       │   ├── Login/
│       │   ├── Dashboard/
│       │   ├── System/
│       │   ├── Users/
│       │   └── MemoryManager/        # 记忆数据管理
│       ├── router/
│       ├── styles/
│       └── types/
│
└── shared/                           # Shared frontend code (optional)
    └── .gitkeep
```

## Core Process

### Phase 1: Foundation — Backend + Agent Layer

```
1.1 Initialize monorepo ──→ 1.2 api-server scaffold ──→ 1.3 Config loader
                                                           │
1.5 Memory module ←── 1.4 Core modules ←──────────────────┘
         │
         ▼
1.6 Health + Menu + Pagination + Rate limiting

1.7 AgentScope Server (独立服务，与 FastAPI 无关)
```

**Step 1.1 — Initialize pnpm monorepo**

```yaml
# pnpm-workspace.yaml
packages:
  - "web-app"
  - "admin-app"
```

```json
// package.json (root)
{
  "name": "project-root",
  "private": true,
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint"
  }
}
```

**Step 1.2 — api-server scaffold**

```bash
cd api-server
pip install -e ".[dev]"
```

```toml
# pyproject.toml key dependencies
[project]
dependencies = [
    "fastapi>=0.115",
    "uvicorn>=0.34",
    "gunicorn>=23",
    "pyyaml>=6",
    "pydantic>=2",
    "pydantic-settings>=2",
    "slowapi>=0.1",
    "pyjwt>=2.9",
    "passlib[bcrypt]>=1.7",
    "httpx>=0.28",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-asyncio>=0.24", "ruff>=0.8"]
```

**Step 1.3 — Configuration loader**

All configuration from `application.yml`, no hardcoded values:

```yaml
# config/application.yml
app:
  name: project-name
  version: "0.1.0"
  debug: false

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  worker_class: "uvicorn.workers.UvicornWorker"

auth:
  secret_key: "${AUTH_SECRET_KEY:change-me-in-production}"
  algorithm: "HS256"
  access_token_expire_minutes: 30
  refresh_token_expire_days: 7

memory:
  backend: "sqlalchemy"
  sqlalchemy_url: "sqlite:///memory.db"
  redis_host: "${REDIS_HOST:localhost}"
  redis_port: 6379
  redis_db: 0

cors:
  origins:
    - "http://localhost:5173"
    - "http://localhost:5174"

rate_limit:
  enabled: true
  default: "60/minute"
  auth: "10/minute"
  memory: "30/minute"

logging:
  level: INFO
  format: json

menus:
  web:
    - key: home
      title: "Home"
      icon: "icon-home"
      path: "/"
      sort: 1
    - key: agent
      title: "AI Assistant"
      icon: "icon-robot"
      path: "/agent"
      sort: 2
  admin:
    - key: dashboard
      title: "Dashboard"
      icon: "icon-dashboard"
      path: "/admin/dashboard"
      sort: 1
    - key: memory-manager
      title: "Memory Manager"
      icon: "icon-storage"
      path: "/admin/memory"
      sort: 2
```

Environment override pattern:

```yaml
# config/application-dev.yml
app:
  debug: true
memory:
  backend: "sqlalchemy"
  sqlalchemy_url: "sqlite:///memory-dev.db"
logging:
  level: DEBUG
  format: text
```

**Step 1.4 — Core modules**

Unified response format:

```python
# app/core/response.py
def success_response(data=None, message="ok", code=0):
    return {"code": code, "message": message, "data": data}
```

Security headers middleware (6 headers):

```python
# app/core/middleware.py
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
```

**Step 1.5 — Auth module**

JWT (HS256) + bcrypt, endpoints under `/api/v1/admin/auth/`:

| Endpoint | Method | Auth | Rate Limit |
|---|---|---|---|
| `/login` | POST | None | 10/min |
| `/refresh` | POST | None | 10/min |
| `/logout` | POST | Bearer | - |
| `/me` | GET | Bearer | - |

**Step 1.6 — Memory module**

FastAPI 提供记忆服务，供前端查询和管理 AgentScope 的对话记忆数据：

```python
# app/modules/memory/service.py
from app.config.settings import settings


class MemoryService:
    def __init__(self):
        self._backend = settings.memory.backend

    async def get_memories(self, session_id: str, limit: int = 50):
        pass

    async def get_memory_by_id(self, memory_id: str):
        pass

    async def delete_memory(self, memory_id: str):
        pass

    async def search_memories(self, query: str, limit: int = 10):
        pass


memory_service = MemoryService()
```

```python
# app/modules/memory/router.py
from fastapi import APIRouter, Depends
from app.modules.memory.schema import MemoryQuery, MemoryResponse
from app.modules.memory.service import memory_service

web_router = APIRouter(prefix="/memory", tags=["web-memory"])
admin_router = APIRouter(prefix="/memory", tags=["admin-memory"])


@web_router.get("/{session_id}", response_model=MemoryResponse)
async def get_memories(session_id: str, limit: int = 50):
    return await memory_service.get_memories(session_id, limit)


@web_router.get("/search")
async def search_memories(query: str, limit: int = 10):
    return await memory_service.search_memories(query, limit)


@admin_router.get("/")
async def list_all_sessions():
    pass


@admin_router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    pass
```

**Step 1.7 — Remaining modules**

Health check, menu, pagination, rate limiting — follow the existing scaffold patterns.

### Phase 1.8: AgentScope Server (独立服务)

AgentScope 作为独立服务运行，与 FastAPI 完全无关。前端（web-app）直接与 AgentScope Server 通信。

```toml
# agent-server/pyproject.toml
[project]
name = "agent-server"
dependencies = [
    "agentscope",
    "uvicorn>=0.34",
    "pyyaml>=6",
    "pydantic>=2",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-asyncio>=0.24", "ruff>=0.8"]
```

```yaml
# agent-server/config/agent_config.yml
server:
  host: "0.0.0.0"
  port: 8080

models:
  default: "dashscope"
  dashscope:
    model_name: "qwen-plus"
    api_key: "${DASHSCOPE_API_KEY:}"
  openai:
    model_name: "gpt-4o"
    api_key: "${OPENAI_API_KEY:}"
  anthropic:
    model_name: "claude-sonnet-4-20250514"
    api_key: "${ANTHROPIC_API_KEY:}"

agents:
  assistant:
    sys_prompt: "You are a helpful AI assistant."
    model: "dashscope"
    max_iters: 10
    memory:
      backend: "in_memory"
    compression:
      enable: true
      trigger_threshold: 8000
      keep_recent: 3

  planner:
    sys_prompt: "You are a task planner."
    model: "dashscope"
    max_iters: 5

session:
  backend: "json"
  save_dir: "./sessions"

rag:
  embedding_model: "dashscope"
  store: "milvus_lite"
  collection_name: "knowledge"

mcp:
  servers: []

logging:
  level: INFO
```

```python
# agent-server/app/server.py
import agentscope
from agentscope.agent import ReActAgent
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.session import JSONSession
from agentscope.message import Msg

from app.config.settings import AgentSettings

settings = AgentSettings.load()


agentscope.init(
    project="agent-server",
    logging_level=settings.logging.level,
)


class AgentScopeServer:
    def __init__(self):
        self._agents: dict[str, ReActAgent] = {}
        self._toolkit = Toolkit()
        self._session = JSONSession(save_dir=settings.session.save_dir)

    def _create_model(self, model_name: str | None = None):
        name = model_name or settings.models.default
        cfg = settings.models.get(name)
        from agentscope.model import (
            OpenAIChatModel,
            DashScopeChatModel,
            AnthropicChatModel,
        )
        match name:
            case "dashscope":
                return DashScopeChatModel(
                    model_name=cfg.model_name, api_key=cfg.api_key,
                )
            case "openai":
                return OpenAIChatModel(
                    model_name=cfg.model_name, api_key=cfg.api_key,
                )
            case "anthropic":
                return AnthropicChatModel(
                    model_name=cfg.model_name, api_key=cfg.api_key,
                )

    def get_or_create_agent(self, session_id: str, agent_name: str = "assistant") -> ReActAgent:
        key = f"{session_id}:{agent_name}"
        if key not in self._agents:
            cfg = settings.agents.get(agent_name)
            self._agents[key] = ReActAgent(
                name=agent_name,
                sys_prompt=cfg.sys_prompt,
                model=self._create_model(cfg.model),
                toolkit=self._toolkit,
                memory=InMemoryMemory(),
                max_iters=cfg.max_iters,
            )
        return self._agents[key]

    async def chat(self, session_id: str, user_message: str, agent_name: str = "assistant"):
        agent = self.get_or_create_agent(session_id, agent_name)
        msg = Msg(name="user", content=user_message, role="user")
        response = await agent(msg)
        return response

    async def chat_stream(self, session_id: str, user_message: str, agent_name: str = "assistant"):
        agent = self.get_or_create_agent(session_id, agent_name)
        msg = Msg(name="user", content=user_message, role="user")
        response = await agent(msg)
        async for chunk in response.stream():
            yield chunk

    async def save_session(self, session_id: str):
        for key, agent in self._agents.items():
            if key.startswith(f"{session_id}:"):
                await self._session.save_session_state(session_id, agent=agent)

    async def load_session(self, session_id: str):
        pass


server = AgentScopeServer()
```

```python
# agent-server/app/server.py (HTTP/WS 路由部分)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

agent_app = FastAPI(title="AgentScope Server")


class ChatRequest(BaseModel):
    session_id: str
    message: str
    agent_name: str = "assistant"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@agent_app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await server.chat(request.session_id, request.message, request.agent_name)
    return ChatResponse(reply=response.content, session_id=request.session_id)


@agent_app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_stream():
        async for chunk in server.chat_stream(
            request.session_id, request.message, request.agent_name
        ):
            import json
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@agent_app.get("/health")
async def health():
    return {"status": "ok"}


@agent_app.post("/session/save")
async def save_session(session_id: str):
    await server.save_session(session_id)
    return {"status": "saved"}
```

启动命令：

```bash
cd agent-server
pip install -e ".[dev]"
uvicorn app.server:agent_app --host 0.0.0.0 --port 8080 --reload
```

### Phase 2: web-app (Front-Office)

**Step 2.1 — Vite + React + Arco Design scaffold**

```bash
cd web-app && pnpm install
```

Key config:

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": { target: "http://localhost:8000", changeOrigin: true },
      "/agent": { target: "http://localhost:8080", changeOrigin: true },
    },
  },
});
```

**Step 2.2 — API layer (双客户端：api-server + agent-server)**

```typescript
// src/api/client.ts — api-server 客户端（记忆服务、菜单等）
import axios from "axios";
import { Message } from "@arco-design/web-react";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  timeout: 30000,
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    Message.error(error.response?.data?.message ?? "Request failed");
    return Promise.reject(error);
  },
);

export default apiClient;
```

```typescript
// src/api/agent-client.ts — AgentScope Server 客户端（直连，不经过 FastAPI）
import axios from "axios";
import { Message } from "@arco-design/web-react";

const agentClient = axios.create({
  baseURL: import.meta.env.VITE_AGENT_BASE_URL ?? "http://localhost:8080",
  timeout: 120000,
});

agentClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    Message.error("Agent 服务连接失败");
    return Promise.reject(error);
  },
);

export async function chatWithAgent(
  sessionId: string,
  message: string,
  agentName: string = "assistant",
) {
  return agentClient.post("/chat", { session_id: sessionId, message, agent_name: agentName });
}

export async function streamChatWithAgent(
  sessionId: string,
  message: string,
  agentName: string = "assistant",
): Promise<ReadableStream> {
  const response = await fetch(
    `${import.meta.env.VITE_AGENT_BASE_URL ?? "http://localhost:8080"}/chat/stream`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message, agent_name: agentName }),
    },
  );
  return response.body!;
}

export default agentClient;
```

**Step 2.3 — Layout + pages + agent chat page**

Use Arco Design exclusively. Every data page handles three states:

```tsx
import { Skeleton, Result, Empty, Button } from "@arco-design/web-react";

export function AgentChatPage() {
  const { data, isLoading, error, refetch } = useAgentStatus();

  if (isLoading) return <Skeleton animation />;
  if (error) return (
    <Result status="error" title="Connection failed"
      subTitle={error.message}
      extra={<Button type="primary" onClick={refetch}>Retry</Button>} />
  );
  if (!data) return <Empty description="No data" />;

  return <AgentChatView data={data} />;
}
```

### Phase 3: admin-app (Back-Office)

**Step 3.1 — Same Vite + React + Arco scaffold (port 5174)**

**Step 3.2 — Token management (memory, NOT localStorage)**

```typescript
// src/api/client.ts
let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}

apiClient.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

apiClient.interceptors.response.use(null, async (error) => {
  if (error.response?.status === 401 && refreshToken) {
    const { data } = await axios.post("/api/v1/admin/auth/refresh", {
      refresh_token: refreshToken,
    });
    setTokens(data.data.access_token, data.data.refresh_token);
    error.config.headers.Authorization = `Bearer ${accessToken}`;
    return axios(error.config);
  }
  clearTokens();
  window.location.href = "/login";
  return Promise.reject(error);
});
```

**Step 3.3 — AdminLayout + Login + Dashboard + MemoryManager**

### Phase 4: Docker + Deployment

```yaml
# docker-compose.yml
version: "3.8"
services:
  api-server:
    build: { context: ./api-server, dockerfile: Dockerfile }
    ports: ["8000:8000"]
    environment:
      - APP_PROFILE=prod
      - AUTH_SECRET_KEY=${AUTH_SECRET_KEY}
    volumes: [./api-server/config:/app/config]
    restart: unless-stopped

  agent-server:
    build: { context: ./agent-server, dockerfile: Dockerfile }
    ports: ["8080:8080"]
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes: [./agent-server/config:/app/config, agent-sessions:/app/sessions]
    restart: unless-stopped

  web-app:
    build: { context: ./web-app, dockerfile: Dockerfile }
    ports: ["3000:80"]
    depends_on: [api-server, agent-server]
    restart: unless-stopped

  admin-app:
    build: { context: ./admin-app, dockerfile: Dockerfile }
    ports: ["3001:80"]
    depends_on: [api-server]
    restart: unless-stopped

volumes:
  agent-sessions:
```

## AgentScope Integration Patterns

**重要：以下所有模式均在 agent-server 中实现，与 FastAPI 无关。前端直接调用 AgentScope Server API。**

### Pattern 1: Single Agent Chat (Simplest)

User sends a message, one ReActAgent processes it：

```
web-app → POST http://agent-server:8080/chat → ReActAgent → Response
```

### Pattern 2: Multi-Agent Pipeline

User request flows through specialized agents sequentially：

```
web-app → POST http://agent-server:8080/chat → PlannerAgent → ResearcherAgent → WriterAgent → Response
```

```python
# agent-server/app/pipelines/research_pipeline.py
from agentscope.pipeline import MsgHub, sequential_pipeline
from agentscope.message import Msg

async def research_pipeline(session_id: str, user_message: str):
    planner = ReActAgent(name="planner", sys_prompt="Break down tasks...", model=...)
    researcher = ReActAgent(name="researcher", sys_prompt="Research topics...", model=...)
    writer = ReActAgent(name="writer", sys_prompt="Write summaries...", model=...)

    msg = Msg(name="user", content=user_message, role="user")

    async with MsgHub(participants=[planner, researcher, writer]) as hub:
        result = await sequential_pipeline([planner, researcher, writer], msg)

    return result.content
```

### Pattern 3: Parallel Agent Fan-out

Same request dispatched to multiple agents concurrently：

```
web-app → POST http://agent-server:8080/chat → Fanout → [CodeReviewer, SecurityAuditor, TestEngineer] → Merge → Response
```

```python
# agent-server/app/pipelines/review_pipeline.py
from agentscope.pipeline import fanout_pipeline
from agentscope.message import Msg

async def review_pipeline(session_id: str, code: str):
    reviewer = ReActAgent(name="code-reviewer", ...)
    auditor = ReActAgent(name="security-auditor", ...)
    tester = ReActAgent(name="test-engineer", ...)

    msg = Msg(name="user", content=code, role="user")
    results = await fanout_pipeline([reviewer, auditor, tester], msg, enable_gather=True)
    return results
```

### Pattern 4: SSE Streaming

Stream agent responses to the frontend in real-time（前端直连 AgentScope Server）：

```python
# agent-server/app/server.py
@agent_app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_stream():
        async for chunk in server.chat_stream(
            request.session_id, request.message, request.agent_name
        ):
            import json
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

```typescript
// web-app 前端直连 AgentScope Server
import { streamChatWithAgent } from "@/api/agent-client";

const stream = await streamChatWithAgent(sessionId, message);
const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const text = new TextDecoder().decode(value);
  text.split("\n").filter(line => line.startsWith("data: ")).forEach(line => {
    const chunk = JSON.parse(line.slice(6));
    appendToChat(chunk.content);
  });
}
```

### Pattern 5: Tool Integration

Register custom tools for agents to call（在 agent-server 中注册）：

```python
# agent-server/app/tools/weather.py
from agentscope.tool import Toolkit

toolkit = Toolkit()

@toolkit.register_tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the internal database for matching records."""
    return db.search(query, limit)

@toolkit.register_tool
def get_user_info(user_id: str) -> dict:
    """Retrieve user profile information."""
    return user_service.get_profile(user_id)
```

### Pattern 6: MCP Tool Integration

Connect agents to external MCP servers（在 agent-server 中集成）：

```python
# agent-server/app/tools/mcp_tools.py
from agentscope.mcp import HttpStatelessClient

mcp_client = HttpStatelessClient(url="http://mcp-server:3000/sse")
await toolkit.add_mcp_tools(mcp_client)
```

## Code Style

### Python (api-server)

- Use `from __future__ import annotations` for all files
- All config from `application.yml`, no hardcoded values
- All I/O operations use `async def`
- Type annotations on all public function signatures
- Ruff: line width 120, double quotes, 4-space indent
- All API input validated via Pydantic models

### TypeScript (web-app & admin-app)

- Strict mode: `"strict": true`
- Function components + Hooks only, no class components
- **All UI components from Arco Design, no custom base components**
- Arco components imported on-demand: `import { Button } from "@arco-design/web-react"`
- Components PascalCase (`HomePage.tsx`), utilities camelCase (`useRequest.ts`)
- Named exports, default export only for entry files
- ESLint + Prettier: single quotes, trailing commas, 2-space indent, line width 100

## Frontend Architecture

### Arco Design Usage Rules

| Need | Use Arco Component | Never Build |
|---|---|---|
| Layout | `<Layout>` / `<Layout.Sider>` / `<Layout.Content>` | Custom layout |
| Navigation | `<Menu>` / `<Breadcrumb>` | Custom navbar |
| Forms | `<Form>` / `<Input>` / `<Select>` | Custom form controls |
| Data display | `<Table>` / `<Card>` / `<Descriptions>` / `<Statistic>` | Custom data components |
| Feedback | `<Message>` / `<Modal>` / `<Drawer>` | Custom modals |
| Loading | `<Skeleton animation />` | Custom spinner |
| Empty state | `<Empty />` | Custom empty state |
| Error state | `<Result status="error" />` | Custom error page |

### Three-State Requirement

Every data display component MUST handle:

```tsx
if (isLoading) return <Skeleton animation />;
if (error) return <Result status="error" title="Failed" extra={<Button onClick={refetch}>Retry</Button>} />;
if (!data || data.length === 0) return <Empty description="No data" />;
return <DataView data={data} />;
```

### State Management (Simplest First)

| Level | Approach | Use When |
|---|---|---|
| Local state | `useState` | Form inputs, modal toggles |
| Lifted state | Parent component | 2-3 sibling components sharing |
| URL state | `searchParams` | Filters, pagination, shareable state |
| Context | React Context | Theme, locale (read-heavy) |
| Server state | Custom Hook + Axios | Remote data fetching |
| Global store | Reserved for future | Complex global client state |

## Security Requirements

- All API input validated via Pydantic models at route boundary
- Security response headers on every response (6 headers)
- CORS origins from config file, never `*`
- Rate limiting: general 60/min, auth 10/min, memory 30/min
- Production: no stack traces in error responses
- Sensitive config via env vars: `${ENV_VAR:default}`
- `.gitignore` must include: `application-prod.yml`, `*.pem`, `*.key`, `.env`
- No sensitive data in logs or API responses
- Admin Token stored in JS memory, NOT localStorage
- 401 auto-refresh with fallback to login page
- **AgentScope Server 与 FastAPI 完全隔离，禁止在 FastAPI 中包装 AgentScope**

## Commands

```bash
# api-server (FastAPI — 仅做记忆服务和 REST 接口)
cd api-server && pip install -e ".[dev]"
cd api-server && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd api-server && gunicorn app.main:app -c gunicorn.conf.py
cd api-server && pytest tests/ -v
cd api-server && ruff check . && ruff format --check .

# agent-server (AgentScope — 独立智能体服务)
cd agent-server && pip install -e ".[dev]"
cd agent-server && uvicorn app.server:agent_app --reload --host 0.0.0.0 --port 8080
cd agent-server && pytest tests/ -v
cd agent-server && ruff check . && ruff format --check .

# web-app
cd web-app && pnpm install
cd web-app && pnpm dev
cd web-app && pnpm build
cd web-app && pnpm test
cd web-app && pnpm lint

# admin-app
cd admin-app && pnpm install
cd admin-app && pnpm dev
cd admin-app && pnpm build
cd admin-app && pnpm test
cd admin-app && pnpm lint

# Root (monorepo)
pnpm install
pnpm -r --parallel dev
pnpm -r build
pnpm -r test

# Docker
docker-compose up --build
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll wrap AgentScope in FastAPI for convenience" | **禁止！** FastAPI 与 AgentScope 必须完全独立。AgentScope 有自己的 HTTP Server，前端直连。FastAPI 包装会导致耦合、难以独立扩展和部署。 |
| "I'll add agent integration later" | Agent integration affects frontend architecture (dual client), session management, and deployment. Retrofitting is 5x harder than building it in from the start. |
| "We don't need the admin-app yet" | Admin-app provides auth, memory management, and system monitoring. You need it from day one. |
| "I'll just use localStorage for tokens" | localStorage is vulnerable to XSS. Memory-only tokens with refresh flow is the production standard. |
| "Arco Design limits my creativity" | Arco Design provides production-quality, accessible components. Custom components introduce bugs and accessibility gaps. Override theme tokens instead. |
| "I don't need streaming for agent responses" | Agent responses take 5-30 seconds. Without streaming, users think the app is frozen. SSE streaming is essential for agent UX. |
| "One model provider is enough" | Model providers have outages and rate limits. Supporting multiple providers (DashScope, OpenAI, Anthropic) via config ensures availability. |
| "I'll skip the three-state handling for now" | Every missing loading/error/empty state is a blank screen or crash for users. Arco provides these components — use them. |
| "I can hardcode the model config" | Model configs change per environment (dev uses cheaper models, prod uses best). agent_config.yml with env var injection is the only safe pattern. |

## Red Flags

- `.pip_packages/` or `node_modules/` committed to Git
- API keys or secrets in source code or config files (use env vars)
- `localStorage` or `sessionStorage` for JWT tokens
- Custom base components that duplicate Arco Design functionality
- Missing loading, error, or empty states on any data page
- Synchronous blocking calls in FastAPI request handlers
- CORS configured with `*` in production
- Missing security response headers
- Unpaginated list endpoints returning full datasets
- Agent responses without streaming (SSE)
- Hardcoded model names or API keys in agent-server code
- No session persistence for agent conversations
- **FastAPI 代码中 import agentscope（禁止！两者必须完全独立）**
- **web-app 通过 FastAPI 代理调用 AgentScope（禁止！前端直连 AgentScope Server）**

## Verification

After completing the scaffold, confirm:

- [ ] `cd api-server && uvicorn app.main:app --reload` starts, `/docs` shows Swagger UI
- [ ] `cd api-server && gunicorn app.main:app -c gunicorn.conf.py` starts with multiple workers
- [ ] `application.yml` loads correctly, `application-dev.yml` overrides work
- [ ] `/api/v1/web/health` and `/api/v1/admin/health` return 200
- [ ] `/api/v1/admin/auth/login` returns JWT tokens, `/me` requires Bearer token
- [ ] `/api/v1/web/memory/{session_id}` returns memory data
- [ ] `cd agent-server && uvicorn app.server:agent_app --reload --port 8080` starts
- [ ] `http://localhost:8080/health` returns 200
- [ ] `http://localhost:8080/chat` returns agent responses
- [ ] `http://localhost:8080/chat/stream` returns SSE events
- [ ] `cd web-app && pnpm dev` starts on port 5173, pages render correctly
- [ ] `cd admin-app && pnpm dev` starts on port 5174, login flow works
- [ ] web-app can directly call AgentScope Server (port 8080) for agent chat
- [ ] web-app can call api-server (port 8000) for health check and memory queries
- [ ] `cd api-server && pytest tests/ -v` all pass
- [ ] `cd agent-server && pytest tests/ -v` all pass
- [ ] `cd web-app && pnpm test` all pass
- [ ] `cd admin-app && pnpm test` all pass
- [ ] `cd api-server && ruff check .` no errors
- [ ] `cd agent-server && ruff check .` no errors
- [ ] API responses include security headers
- [ ] CORS only allows configured origins
- [ ] Rate limiting returns 429 when exceeded
- [ ] All data pages handle loading/error/empty states
- [ ] AgentScope agents can be created and respond to messages
- [ ] Agent session state persists across requests
- [ ] **api-server 代码中无任何 `import agentscope`（完全独立）**
- [ ] **web-app 通过 agent-client.ts 直连 AgentScope Server（不经过 FastAPI）**
- [ ] `docker-compose up --build` starts all four services
- [ ] Admin tokens stored in memory, not localStorage

---

## AgentScope 深度集成指南

### 1. 核心 Agent 类型

AgentScope 提供多种 Agent 类型，适用于不同场景：

| Agent 类型 | 适用场景 | 核心特性 |
|-----------|---------|---------|
| **ReActAgent** | 标准对话、工具调用、推理任务 | ReAct 推理循环、自动工具选择、记忆压缩 |
| **RealtimeAgent** | 实时聊天、语音助手 | WebSocket 流式、低延迟响应 |
| **A2AAgent** | 智能体间通信、多智能体协作 | A2A 协议支持、跨智能体消息传递 |
| **UserAgent** | 人机协作、用户输入代理 | 收集用户输入、传递给其他智能体 |

#### ReActAgent 核心配置

```python
from agentscope.agent import ReActAgent
from agentscope.memory import InMemoryMemory, RedisMemory
from agentscope.plan import PlanNotebook

agent = ReActAgent(
    name="assistant",
    sys_prompt="You are a helpful AI assistant.",
    model=DashScopeChatModel(model_name="qwen-plus", api_key="..."),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    max_iters=10,
    plan_notebook=PlanNotebook(),  # 可选：任务规划能力
    compression_config=ReActAgent.CompressionConfig(
        enable=True,
        agent_token_counter=token_counter,
        trigger_threshold=8000,
        keep_recent=3,
    ),
)
```

#### RealtimeAgent 配置

```python
from agentscope.agent import RealtimeAgent
from agentscope.realtime import DashScopeRealtimeModel

agent = RealtimeAgent(
    name="voice-assistant",
    sys_prompt="You are a real-time voice assistant.",
    model=DashScopeRealtimeModel(
        model_name="qwen3-omni-flash-realtime",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    ),
    toolkit=toolkit,
)

# 启动实时代理
queue = asyncio.Queue()
await agent.start(queue)

# 发送消息
await agent.put_message("Hello!")
```

### 2. 记忆系统

AgentScope 支持多层记忆架构：

#### 工作记忆 (Working Memory)

```python
# 内存存储（开发环境）
from agentscope.memory import InMemoryMemory
memory = InMemoryMemory()

# Redis 存储（生产环境）
from agentscope.memory import RedisMemory
memory = RedisMemory(
    host="localhost",
    port=6379,
    db=0,
)

# SQLAlchemy 存储
from agentscope.memory import SqlAlchemyMemory
memory = SqlAlchemyMemory(
    url="sqlite:///memory.db",
)
```

#### 长期记忆 (Long-Term Memory)

```python
# ReMe 个人长期记忆
from agentscope.memory import ReMePersonalLongTermMemory
ltm = ReMePersonalLongTermMemory(
    api_key=os.getenv("REME_API_KEY"),
    user_id="user-123",
)

# Mem0 长期记忆
from agentscope.memory import Mem0LongTermMemory
ltm = Mem0LongTermMemory(
    api_key=os.getenv("MEM0_API_KEY"),
)

# 将长期记忆集成到 Agent
agent = ReActAgent(
    name="assistant",
    model=model,
    memory=InMemoryMemory(),
    long_term_memory=ltm,
)
```

### 3. MsgHub 多智能体通信

MsgHub 提供灵活的多智能体编排能力：

```python
from agentscope.pipeline import MsgHub
from agentscope.message import Msg

async def collaborative_task():
    planner = ReActAgent(name="planner", sys_prompt="规划任务...", model=...)
    researcher = ReActAgent(name="researcher", sys_prompt="研究信息...", model=...)
    writer = ReActAgent(name="writer", sys_prompt="撰写报告...", model=...)

    msg = Msg(name="user", content="写一份AI趋势报告", role="user")

    # 方式1：自动广播模式
    async with MsgHub(participants=[planner, researcher, writer]) as hub:
        await planner(msg)
        await researcher()
        result = await writer()

    # 方式2：手动控制广播
    async with MsgHub(
        participants=[planner, researcher, writer],
        enable_auto_broadcast=False,
    ) as hub:
        plan_result = await planner(msg)
        await hub.broadcast(plan_result)
        
        research_result = await researcher()
        await hub.broadcast(research_result)
        
        final_result = await writer()
    
    return final_result
```

### 4. 工具集成

#### 自定义工具注册

```python
from agentscope.tool import Toolkit

toolkit = Toolkit()

@toolkit.register_tool
def fetch_weather(city: str) -> dict:
    """获取指定城市的天气信息。"""
    return weather_api.get(city)

@toolkit.register_tool
def search_knowledge(query: str, limit: int = 5) -> list[dict]:
    """搜索知识库获取相关文档。"""
    return knowledge_base.retrieve(query, limit)

@toolkit.register_tool
def execute_python(code: str) -> str:
    """执行 Python 代码并返回结果。"""
    import subprocess
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout or result.stderr
```

#### MCP 工具集成

```python
from agentscope.mcp import HttpStatelessClient, HttpStatefulClient

# 无状态 MCP 客户端
stateless_client = HttpStatelessClient(url="http://mcp-server:3000/sse")
await toolkit.add_mcp_tools(stateless_client)

# 有状态 MCP 客户端
stateful_client = HttpStatefulClient(url="http://mcp-server:3000/sse")
async with stateful_client.create_session() as session:
    await toolkit.add_mcp_tools(session)
```

### 5. RAG 集成

AgentScope 提供完整的 RAG 支持：

```python
from agentscope.rag import KnowledgeBase, Document
from agentscope.rag._store import MilvusLiteStore, QdrantStore
from agentscope.embedding import DashScopeEmbedding

# 创建向量存储
store = MilvusLiteStore(
    collection_name="documents",
    dimension=1024,
)

# 创建嵌入模型
embedding = DashScopeEmbedding(
    model_name="text-embedding-v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# 创建知识库
kb = KnowledgeBase(
    embedding_store=store,
    embedding_model=embedding,
)

# 添加文档
documents = [
    Document(content="文档内容1", metadata={"source": "file1.pdf"}),
    Document(content="文档内容2", metadata={"source": "file2.pdf"}),
]
await kb.add_documents(documents)

# 检索知识
results = await kb.retrieve("查询内容", limit=3)

# 将知识库作为工具注册
@toolkit.register_tool
def retrieve_knowledge(query: str, limit: int = 5) -> str:
    """检索知识库获取相关信息。"""
    docs = await kb.retrieve(query, limit)
    return "\n\n".join([d.content for d in docs])
```

### 6. 会话管理

```python
from agentscope.session import JSONSession, RedisSession

# JSON 文件会话存储
json_session = JSONSession(save_dir="./sessions")

# Redis 会话存储（生产环境）
redis_session = RedisSession(
    host="localhost",
    port=6379,
    db=1,
)

# 保存会话状态
await json_session.save_session_state(
    session_id="user-123",
    agent=agent,
)

# 加载会话状态
await json_session.load_session_state(
    session_id="user-123",
    agent=agent,
)
```

### 7. 评估框架

```python
from agentscope.evaluate import GeneralEvaluator
from agentscope.evaluate._metric_base import MetricBase

# 自定义评估指标
class CorrectnessMetric(MetricBase):
    async def compute(self, solution, reference) -> float:
        return similarity_score(solution.output, reference.output)

# 创建评估器
evaluator = GeneralEvaluator(
    tasks=[
        {"input": "问题1", "reference": {"output": "答案1"}},
        {"input": "问题2", "reference": {"output": "答案2"}},
    ],
    metrics=[CorrectnessMetric()],
    agent=agent,
)

# 运行评估
results = await evaluator.run()
print(f"准确率: {results['correctness']:.2f}")
```

### 8. 实时语音能力

```python
from agentscope.realtime import DashScopeRealtimeModel
from agentscope.tts import DashScopeCosyVoiceTTSModel

# 实时语音模型
realtime_model = DashScopeRealtimeModel(
    model_name="qwen3-omni-flash-realtime",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# TTS 模型
tts_model = DashScopeCosyVoiceTTSModel(
    model_name="cosyvoice-300m",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# 实时语音代理
agent = RealtimeAgent(
    name="voice-assistant",
    sys_prompt="你是一个语音助手，用中文回复。",
    model=realtime_model,
    tts_model=tts_model,
)
```

### 9. 部署模式

#### 本地开发

```bash
# 安装
pip install agentscope

# 或从本地源码安装
pip install -e C:/Workspace/source/git/agentscope
```

#### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### 环境变量配置

```bash
# .env 文件
DASHSCOPE_API_KEY=your-dashscope-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 10. AgentScope 最佳实践

| 实践 | 说明 |
|-----|------|
| **异步优先** | 所有 Agent 操作使用 `async/await` |
| **配置外置** | 模型配置、API Key 通过 `application.yml` + 环境变量管理 |
| **会话隔离** | 每个用户会话使用独立的 session_id |
| **流式响应** | 长响应使用 SSE 流式返回 |
| **错误处理** | 捕获 Agent 异常并返回友好错误信息 |
| **记忆压缩** | 启用内存压缩避免上下文窗口溢出 |
| **多模型支持** | 支持 DashScope、OpenAI、Anthropic 等多提供商 |
| **可观测性** | 集成 OpenTelemetry 进行追踪 |
