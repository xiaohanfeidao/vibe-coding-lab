---
name: fullstack-agent-scaffold
description: Scaffolds production-grade full-stack applications with AI agent capabilities. Use when starting a new full-stack project that needs a React frontend (web-app + admin-app), FastAPI backend, and AgentScope Runtime multi-agent integration. Use when building applications that combine traditional web UI with intelligent agent workflows.
---

# Full-Stack Agent Scaffold

Build production-grade full-stack applications with embedded AI agent capabilities. This skill provides a battle-tested scaffold combining React frontends, FastAPI backend, and AgentScope Runtime multi-agent framework — so you start with working auth, API routing, agent orchestration, and deployment instead of wiring them from scratch.

## When to Use

- Starting a new full-stack project that needs both web UI and AI agent features
- Building an application where users interact with intelligent agents through a web interface
- Creating a multi-tenant system with separate front-office (web-app) and back-office (admin-app) frontends
- Projects requiring JWT authentication, role-based menus, and agent-driven workflows
- Any project that needs FastAPI + React + AgentScope Runtime as the core stack

**When NOT to use:** Static websites, simple APIs without a frontend, projects that don't need AI agent capabilities, or when a simpler stack (e.g., Next.js alone) suffices.

## Architecture Overview

Four independent services with distinct technology stacks. FastAPI and AgentScope Runtime are completely separate — no shared code, no shared framework, no direct communication.

**Core Principles:**
1. **FastAPI only handles memory service and REST APIs** — auth, menus, memory CRUD, health checks
2. **AgentScope Runtime handles all agent logic** — runs via its own `AgentApp` with built-in HTTP server, SSE streaming, session management, and state persistence
3. **Wrapping AgentScope in FastAPI is strictly prohibited** — they are two independent technology stacks
4. **If agent-server needs REST endpoints, define them in AgentScope Runtime** via `@agent_app.endpoint()` decorator — AgentScope Runtime fully supports custom REST APIs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Docker / K8s                                     │
│                                                                           │
│  ┌──────────┐  ┌──────────┐     ┌──────────────────┐     ┌──────────────┐  │
│  │ web-app  │  │admin-app │     │   api-server     │     │  agent-server│  │
│  │ :5173    │  │ :5174    │     │   (FastAPI)      │     │ (AgentScope  │  │
│  │ React    │  │ React    │     │   :8000          │     │  Runtime)    │  │
│  │ Arco     │  │ Arco     │◄────►│  Auth / Menu    │     │   :8090      │  │
│  └────┬─────┘  │ +Auth    │     │  Memory Service  │     │              │  │
│       │        └──────────┘     │  /api/v1/web/   │     │ AgentApp     │  │
│       │                          │  /api/v1/admin/ │     │ /process     │  │
│       │                          └──────────────────┘     │ @endpoint   │  │
│       │                                                    │ StateService│  │
│       └────────────────────────────────────────────────────┤ SessionHist │  │
│                          web-app ↔ agent-server (direct)   │ OpenAI SDK  │  │
│                                                           └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Technology Stack Separation:**

| Service | Framework | Port | Responsibility |
|---------|-----------|------|----------------|
| api-server | FastAPI | 8000 | Auth, menus, memory CRUD, health checks |
| agent-server | AgentScope Runtime (AgentApp) | 8090 | Agent chat, tool execution, session state, SSE streaming |
| web-app | React + Vite | 5173 | Public-facing portal, direct agent interaction |
| admin-app | React + Vite | 5174 | Back-office management, auth-protected |

**Communication Paths:**
1. **web-app ↔ agent-server** (:8090): Frontend directly calls AgentScope Runtime `/process` endpoint (SSE streaming)
2. **web-app ↔ api-server** (:8000): Health checks, menu retrieval, memory queries
3. **admin-app ↔ api-server** (:8000): JWT authentication, memory management, system configuration
4. **api-server ↔ agent-server**: **No direct communication** — completely independent

## Tech Stack

### api-server (Python — FastAPI)

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

### agent-server (Python — AgentScope Runtime)

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| agentscope | latest | Multi-agent framework |
| agentscope-runtime | latest | Official runtime (AgentApp, StateService, SessionHistory) |
| pyyaml | 6+ | Parse agent_config.yml |
| pydantic | 2+ | Data validation |

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

## Project Structure

```
project-root/
├── pnpm-workspace.yaml
├── package.json
├── docker-compose.yml
├── .gitignore
│
├── api-server/                       # FastAPI — memory service and REST APIs only
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
│   │   │   └── memory/               # Memory service (CRUD for agent conversation data)
│   │   │       ├── schema.py
│   │   │       ├── service.py
│   │   │       └── router.py
│   │   └── utils/
│   │       └── pagination.py
│   └── tests/
│
├── agent-server/                     # AgentScope Runtime (independent, NO FastAPI)
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── config/
│   │   └── agent_config.yml          # AgentScope-specific configuration
│   ├── scripts/
│   │   ├── start.py                  # AgentScope Runtime launcher
│   │   ├── start.sh
│   │   └── start.bat
│   ├── app_agent.py                  # AgentApp entry point (init/query/shutdown)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   └── settings.py           # AgentScope configuration models
│   │   ├── agents/                   # Agent definitions
│   │   │   ├── __init__.py
│   │   │   ├── assistant.py          # Default ReActAgent
│   │   │   ├── planner.py            # Planning Agent
│   │   │   └── researcher.py         # Research Agent
│   │   ├── tools/                    # Custom tools
│   │   │   ├── __init__.py
│   │   │   ├── weather.py
│   │   │   ├── knowledge.py          # RAG retrieval tool
│   │   │   └── database.py           # Database query tool
│   │   ├── pipelines/                # Multi-agent workflows
│   │   │   ├── __init__.py
│   │   │   ├── chat_pipeline.py      # Single agent chat
│   │   │   ├── research_pipeline.py  # Multi-agent collaboration
│   │   │   └── review_pipeline.py    # Parallel review
│   │   ├── memory/                   # Agent memory management
│   │   │   ├── __init__.py
│   │   │   └── memory_manager.py     # Memory compression + long-term memory
│   │   └── rag/                      # RAG knowledge base
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
│       │   ├── client.ts             # Axios instance (api-server :8000)
│       │   ├── agent-client.ts       # AgentScope Runtime client (:8090)
│       │   └── modules/
│       │       ├── health.ts
│       │       ├── menu.ts
│       │       ├── memory.ts         # Memory service API
│       │       └── agent.ts          # Agent chat API (direct to AgentScope Runtime)
│       ├── components/Layout/
│       │   └── AppLayout.tsx         # Header + Menu + Content + Footer
│       ├── pages/
│       │   ├── Home/
│       │   ├── Features/
│       │   ├── About/
│       │   ├── Contact/
│       │   └── AgentChat/            # Agent interaction page (direct to AgentScope Runtime)
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
│       │       └── memory.ts         # Memory management API
│       ├── components/Layout/
│       │   └── AdminLayout.tsx       # Sider + Menu + Header + Content
│       ├── pages/
│       │   ├── Login/
│       │   ├── Dashboard/
│       │   ├── System/
│       │   ├── Users/
│       │   └── MemoryManager/        # Memory data management
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

1.7 AgentScope Runtime (independent service, NO FastAPI dependency)
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

FastAPI provides memory service for querying and managing AgentScope conversation memory data:

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
from fastapi import APIRouter
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

### Phase 1.8: AgentScope Runtime (Independent Service)

AgentScope Runtime runs as an independent service via the official `AgentApp`, completely separate from FastAPI. It provides Agent-as-a-Service (AaaS) with built-in SSE streaming, session management, state persistence, and OpenAI-compatible endpoints. No FastAPI code is used in agent-server.

**Key AgentScope Runtime features:**
- `AgentApp` — lifecycle hub with `@init`, `@query`, `@shutdown` decorators
- Built-in HTTP server on port 8090, `/process` endpoint for SSE streaming
- `InMemoryStateService` / `InMemorySessionHistoryService` — built-in state and session management
- `@agent_app.endpoint()` — custom REST API endpoints (health check, session list, etc.)
- OpenAI SDK compatible — `/compatible-mode/v1` endpoint
- Built-in Web UI — `agent_app.run(web_ui=True)`
- `LocalDeployManager` / `K8sDeployManager` — production deployment

```toml
# agent-server/pyproject.toml
[project]
name = "agent-server"
dependencies = [
    "agentscope",
    "agentscope-runtime",
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
  port: 8090

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
    name: "Friday"
    sys_prompt: "You are a helpful AI assistant named Friday."
    model: "dashscope"
    max_iters: 10
    tools:
      - execute_python_code
    compression:
      enable: true
      trigger_threshold: 8000
      keep_recent: 3

  planner:
    name: "Planner"
    sys_prompt: "You are a task planner."
    model: "dashscope"
    max_iters: 5

session:
  state_service: "in_memory"
  session_history_service: "in_memory"

logging:
  level: INFO
```

```python
# agent-server/app_agent.py
import os

from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, execute_python_code
from agentscope.pipeline import stream_printing_messages

from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.adapters.agentscope.memory import (
    AgentScopeSessionHistoryMemory,
)
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import (
    InMemorySessionHistoryService,
)

agent_app = AgentApp(
    app_name="Friday",
    app_description="A helpful AI assistant",
)


@agent_app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()
    await self.state_service.start()
    await self.session_service.start()


@agent_app.query(framework="agentscope")
async def query_func(self, msgs, request: AgentRequest = None, **kwargs):
    session_id = request.session_id
    user_id = request.user_id

    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="Friday",
        model=DashScopeChatModel(
            "qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            stream=True,
        ),
        sys_prompt="You're a helpful assistant named Friday.",
        toolkit=toolkit,
        memory=AgentScopeSessionHistoryMemory(
            service=self.session_service,
            session_id=session_id,
            user_id=user_id,
        ),
    )
    agent.set_console_output_enabled(enabled=False)

    if state:
        agent.load_state_dict(state)

    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last

    state = agent.state_dict()
    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=state,
    )


@agent_app.shutdown
async def shutdown_func(self):
    await self.state_service.stop()
    await self.session_service.stop()


@agent_app.endpoint("/health")
async def health_check(request: AgentRequest = None):
    return {"status": "ok"}


@agent_app.endpoint("/sessions")
async def list_sessions(request: AgentRequest = None):
    return {"sessions": []}


if __name__ == "__main__":
    agent_app.run(host="0.0.0.0", port=8090)
```

Start command:

```bash
cd agent-server
pip install -e ".[dev]"
python app_agent.py
```

After launch, the service listens on `http://localhost:8090/process` with SSE streaming.

Test with curl:

```bash
curl -N \
  -X POST "http://localhost:8090/process" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [
          { "type": "text", "text": "What is the capital of France?" }
        ]
      }
    ]
  }'
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
      "/agent": { target: "http://localhost:8090", changeOrigin: true },
    },
  },
});
```

**Step 2.2 — API layer (dual client: api-server + agent-server)**

```typescript
// src/api/client.ts — api-server client (memory service, menus, etc.)
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
// src/api/agent-client.ts — AgentScope Runtime client (direct, NO FastAPI proxy)
const AGENT_BASE_URL = import.meta.env.VITE_AGENT_BASE_URL ?? "http://localhost:8090";

export interface AgentChatRequest {
  input: Array<{
    role: string;
    content: Array<{ type: string; text: string }>;
  }>;
  session_id?: string;
  user_id?: string;
}

export async function chatWithAgent(
  message: string,
  sessionId?: string,
): Promise<ReadableStream<Uint8Array>> {
  const request: AgentChatRequest = {
    input: [
      {
        role: "user",
        content: [{ type: "text", text: message }],
      },
    ],
    session_id: sessionId,
  };

  const response = await fetch(`${AGENT_BASE_URL}/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Agent service error: ${response.status}`);
  }

  return response.body!;
}

export async function checkAgentHealth(): Promise<{ status: string }> {
  const res = await fetch(`${AGENT_BASE_URL}/health`);
  return res.json();
}

export async function listAgentSessions(): Promise<{ sessions: unknown[] }> {
  const res = await fetch(`${AGENT_BASE_URL}/sessions`);
  return res.json();
}

export function parseSSEStream(stream: ReadableStream<Uint8Array>) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();

  return {
    async *[Symbol.asyncIterator]() {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        const lines = text.split("\n").filter((line) => line.startsWith("data: "));
        for (const line of lines) {
          try {
            yield JSON.parse(line.slice(6));
          } catch {
            continue;
          }
        }
      }
    },
  };
}
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

Agent chat component using SSE:

```tsx
import { chatWithAgent, parseSSEStream } from "@/api/agent-client";

export function AgentChatView() {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);

  async function handleSend() {
    if (!input.trim() || streaming) return;
    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setStreaming(true);

    try {
      const stream = await chatWithAgent(input, sessionId);
      let assistantContent = "";
      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      for await (const chunk of parseSSEStream(stream)) {
        if (chunk.object === "content" && chunk.text) {
          assistantContent += chunk.text;
          setMessages((prev) => [
            ...prev.slice(0, -1),
            { role: "assistant", content: assistantContent },
          ]);
        }
      }
    } catch (err) {
      Message.error("Agent service connection failed");
    } finally {
      setStreaming(false);
    }
  }
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
    ports: ["8090:8090"]
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes: [./agent-server/config:/app/config]
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
```

## AgentScope Runtime Integration Patterns

**Important: All patterns below are implemented in agent-server using AgentScope Runtime only. No FastAPI code is involved. The frontend calls AgentScope Runtime API directly.**

### Pattern 1: Single Agent Chat (Simplest)

User sends a message, one ReActAgent processes it via `/process`:

```
web-app → POST http://agent-server:8090/process → ReActAgent → SSE Response
```

### Pattern 2: Multi-Agent Pipeline

User request flows through specialized agents sequentially:

```
web-app → POST http://agent-server:8090/process → PlannerAgent → ResearcherAgent → WriterAgent → SSE Response
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

Same request dispatched to multiple agents concurrently:

```
web-app → POST http://agent-server:8090/process → Fanout → [CodeReviewer, SecurityAuditor, TestEngineer] → Merge → SSE Response
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

### Pattern 4: SSE Streaming (Built-in)

AgentScope Runtime provides built-in SSE streaming via the `/process` endpoint. No manual implementation needed — just use `stream_printing_messages` in the `@query` handler:

```python
@agent_app.query(framework="agentscope")
async def query_func(self, msgs, request: AgentRequest = None, **kwargs):
    agent = ReActAgent(...)
    async for msg, last in stream_printing_messages(
        agents=[agent], coroutine_task=agent(msgs),
    ):
        yield msg, last
```

Frontend consumption:

```typescript
import { chatWithAgent, parseSSEStream } from "@/api/agent-client";

const stream = await chatWithAgent(message, sessionId);
for await (const chunk of parseSSEStream(stream)) {
  if (chunk.object === "content" && chunk.text) {
    appendToChat(chunk.text);
  }
}
```

### Pattern 5: Custom REST Endpoints

AgentScope Runtime supports custom REST endpoints via `@agent_app.endpoint()` decorator — no FastAPI needed:

```python
@agent_app.endpoint("/health")
async def health_check(request: AgentRequest = None):
    return {"status": "ok", "app": "Friday"}

@agent_app.endpoint("/sessions")
async def list_sessions(request: AgentRequest = None):
    return {"sessions": [...]}

@agent_app.endpoint("/stream_sync")
def stream_sync_handler(request: AgentRequest):
    for i in range(5):
        yield f"chunk {i}\n"
```

### Pattern 6: Tool Integration

Register custom tools for agents to call (registered in agent-server):

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

### Pattern 7: MCP Tool Integration

Connect agents to external MCP servers (integrated in agent-server):

```python
# agent-server/app/tools/mcp_tools.py
from agentscope.mcp import HttpStatelessClient

mcp_client = HttpStatelessClient(url="http://mcp-server:3000/sse")
await toolkit.add_mcp_tools(mcp_client)
```

### Pattern 8: OpenAI SDK Compatibility

AgentScope Runtime supports OpenAI SDK compatible endpoint at `/compatible-mode/v1`:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8090/compatible-mode/v1")

response = client.responses.create(
    model="any_name",
    input="What is the weather today?",
)

print(response)
```

## Code Style

### Python (api-server — FastAPI)

- Use `from __future__ import annotations` for all files
- All config from `application.yml`, no hardcoded values
- All I/O operations use `async def`
- Type annotations on all public function signatures
- Ruff: line width 120, double quotes, 4-space indent
- All API input validated via Pydantic models

### Python (agent-server — AgentScope Runtime)

- Use `from __future__ import annotations` for all files
- All config from `agent_config.yml`, no hardcoded values
- Use `AgentApp` lifecycle pattern (`@init`, `@query`, `@shutdown`)
- Custom REST endpoints via `@agent_app.endpoint()`
- Never import FastAPI in agent-server code
- Ruff: line width 120, double quotes, 4-space indent

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
- **AgentScope Runtime and FastAPI must be fully isolated — wrapping AgentScope in FastAPI is prohibited**
- **agent-server must never import FastAPI — use AgentScope Runtime's `@agent_app.endpoint()` for custom REST APIs**

## Commands

```bash
# api-server (FastAPI — memory service and REST APIs only)
cd api-server && pip install -e ".[dev]"
cd api-server && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd api-server && gunicorn app.main:app -c gunicorn.conf.py
cd api-server && pytest tests/ -v
cd api-server && ruff check . && ruff format --check .

# agent-server (AgentScope Runtime — independent agent service)
cd agent-server && pip install -e ".[dev]"
cd agent-server && python app_agent.py
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
| "I'll wrap AgentScope in FastAPI for convenience" | **Prohibited!** AgentScope Runtime has its own HTTP server with built-in SSE streaming, session management, and `@endpoint()` for custom REST APIs. FastAPI wrapping causes coupling and makes independent scaling impossible. |
| "AgentScope doesn't support custom REST endpoints" | **False!** AgentScope Runtime supports `@agent_app.endpoint()` decorator for custom REST APIs, plus built-in `/process` (SSE), `/health`, and OpenAI-compatible `/compatible-mode/v1` endpoints. |
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
- **`import fastapi` or `from fastapi import ...` in agent-server code (prohibited — use AgentScope Runtime)**
- **web-app proxying AgentScope calls through FastAPI (prohibited — frontend must connect directly to AgentScope Runtime :8090)**
- **Manually creating HTTP routes in agent-server instead of using `@agent_app.endpoint()` (use AgentScope Runtime's built-in mechanism)**

## Verification

After completing the scaffold, confirm:

- [ ] `cd api-server && uvicorn app.main:app --reload` starts on port 8000, `/docs` shows Swagger UI
- [ ] `cd api-server && gunicorn app.main:app -c gunicorn.conf.py` starts with multiple workers
- [ ] `application.yml` loads correctly, `application-dev.yml` overrides work
- [ ] `/api/v1/web/health` and `/api/v1/admin/health` return 200
- [ ] `/api/v1/admin/auth/login` returns JWT tokens, `/me` requires Bearer token
- [ ] `/api/v1/web/memory/{session_id}` returns memory data
- [ ] `cd agent-server && python app_agent.py` starts on port 8090
- [ ] `http://localhost:8090/health` returns `{"status": "ok"}`
- [ ] `http://localhost:8090/process` accepts POST and returns SSE events
- [ ] `http://localhost:8090/sessions` returns session list
- [ ] `cd web-app && pnpm dev` starts on port 5173, pages render correctly
- [ ] `cd admin-app && pnpm dev` starts on port 5174, login flow works
- [ ] web-app can directly call AgentScope Runtime (port 8090) `/process` for agent chat
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
- [ ] **No `import fastapi` in agent-server code (fully independent)**
- [ ] **web-app connects directly to AgentScope Runtime via agent-client.ts (no FastAPI proxy)**
- [ ] `docker-compose up --build` starts all four services
- [ ] Admin tokens stored in memory, not localStorage

---

## AgentScope Deep Integration Guide

### 1. Core Agent Types

AgentScope provides multiple agent types for different scenarios:

| Agent Type | Use Case | Core Features |
|-----------|---------|---------|
| **ReActAgent** | Standard chat, tool calling, reasoning tasks | ReAct reasoning loop, automatic tool selection, memory compression |
| **RealtimeAgent** | Real-time chat, voice assistants | WebSocket streaming, low-latency response |
| **A2AAgent** | Inter-agent communication, multi-agent collaboration | A2A protocol support, cross-agent message passing |
| **UserAgent** | Human-in-the-loop, user input proxy | Collect user input, pass to other agents |

#### ReActAgent Core Configuration

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
    plan_notebook=PlanNotebook(),
    compression_config=ReActAgent.CompressionConfig(
        enable=True,
        agent_token_counter=token_counter,
        trigger_threshold=8000,
        keep_recent=3,
    ),
)
```

#### RealtimeAgent Configuration

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

queue = asyncio.Queue()
await agent.start(queue)

await agent.put_message("Hello!")
```

### 2. Memory System

AgentScope supports a multi-layer memory architecture:

#### Working Memory

```python
# In-memory storage (development)
from agentscope.memory import InMemoryMemory
memory = InMemoryMemory()

# Redis storage (production)
from agentscope.memory import RedisMemory
memory = RedisMemory(
    host="localhost",
    port=6379,
    db=0,
)

# SQLAlchemy storage
from agentscope.memory import SqlAlchemyMemory
memory = SqlAlchemyMemory(
    url="sqlite:///memory.db",
)
```

#### Long-Term Memory

```python
# ReMe personal long-term memory
from agentscope.memory import ReMePersonalLongTermMemory
ltm = ReMePersonalLongTermMemory(
    api_key=os.getenv("REME_API_KEY"),
    user_id="user-123",
)

# Mem0 long-term memory
from agentscope.memory import Mem0LongTermMemory
ltm = Mem0LongTermMemory(
    api_key=os.getenv("MEM0_API_KEY"),
)

# Integrate long-term memory into Agent
agent = ReActAgent(
    name="assistant",
    model=model,
    memory=InMemoryMemory(),
    long_term_memory=ltm,
)
```

### 3. MsgHub Multi-Agent Communication

MsgHub provides flexible multi-agent orchestration:

```python
from agentscope.pipeline import MsgHub
from agentscope.message import Msg

async def collaborative_task():
    planner = ReActAgent(name="planner", sys_prompt="Plan tasks...", model=...)
    researcher = ReActAgent(name="researcher", sys_prompt="Research information...", model=...)
    writer = ReActAgent(name="writer", sys_prompt="Write reports...", model=...)

    msg = Msg(name="user", content="Write an AI trends report", role="user")

    # Mode 1: Auto-broadcast
    async with MsgHub(participants=[planner, researcher, writer]) as hub:
        await planner(msg)
        await researcher()
        result = await writer()

    # Mode 2: Manual broadcast control
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

### 4. Tool Integration

#### Custom Tool Registration

```python
from agentscope.tool import Toolkit

toolkit = Toolkit()

@toolkit.register_tool
def fetch_weather(city: str) -> dict:
    """Fetch weather information for a given city."""
    return weather_api.get(city)

@toolkit.register_tool
def search_knowledge(query: str, limit: int = 5) -> list[dict]:
    """Search the knowledge base for relevant documents."""
    return knowledge_base.retrieve(query, limit)

@toolkit.register_tool
def execute_python(code: str) -> str:
    """Execute Python code and return the result."""
    import subprocess
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout or result.stderr
```

#### MCP Tool Integration

```python
from agentscope.mcp import HttpStatelessClient, HttpStatefulClient

# Stateless MCP client
stateless_client = HttpStatelessClient(url="http://mcp-server:3000/sse")
await toolkit.add_mcp_tools(stateless_client)

# Stateful MCP client
stateful_client = HttpStatefulClient(url="http://mcp-server:3000/sse")
async with stateful_client.create_session() as session:
    await toolkit.add_mcp_tools(session)
```

### 5. RAG Integration

AgentScope provides complete RAG support:

```python
from agentscope.rag import KnowledgeBase, Document
from agentscope.rag._store import MilvusLiteStore, QdrantStore
from agentscope.embedding import DashScopeEmbedding

# Create vector store
store = MilvusLiteStore(
    collection_name="documents",
    dimension=1024,
)

# Create embedding model
embedding = DashScopeEmbedding(
    model_name="text-embedding-v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# Create knowledge base
kb = KnowledgeBase(
    embedding_store=store,
    embedding_model=embedding,
)

# Add documents
documents = [
    Document(content="Document content 1", metadata={"source": "file1.pdf"}),
    Document(content="Document content 2", metadata={"source": "file2.pdf"}),
]
await kb.add_documents(documents)

# Retrieve knowledge
results = await kb.retrieve("query content", limit=3)

# Register knowledge base as a tool
@toolkit.register_tool
def retrieve_knowledge(query: str, limit: int = 5) -> str:
    """Retrieve relevant information from the knowledge base."""
    docs = await kb.retrieve(query, limit)
    return "\n\n".join([d.content for d in docs])
```

### 6. Session Management

AgentScope Runtime provides built-in session management via `InMemorySessionHistoryService` and `InMemoryStateService`. For production, use Redis-backed services:

```python
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import InMemorySessionHistoryService

@agent_app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()
    await self.state_service.start()
    await self.session_service.start()
```

### 7. Evaluation Framework

```python
from agentscope.evaluate import GeneralEvaluator
from agentscope.evaluate._metric_base import MetricBase

class CorrectnessMetric(MetricBase):
    async def compute(self, solution, reference) -> float:
        return similarity_score(solution.output, reference.output)

evaluator = GeneralEvaluator(
    tasks=[
        {"input": "Question 1", "reference": {"output": "Answer 1"}},
        {"input": "Question 2", "reference": {"output": "Answer 2"}},
    ],
    metrics=[CorrectnessMetric()],
    agent=agent,
)

results = await evaluator.run()
print(f"Accuracy: {results['correctness']:.2f}")
```

### 8. Real-Time Voice Capabilities

```python
from agentscope.realtime import DashScopeRealtimeModel
from agentscope.tts import DashScopeCosyVoiceTTSModel

realtime_model = DashScopeRealtimeModel(
    model_name="qwen3-omni-flash-realtime",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

tts_model = DashScopeCosyVoiceTTSModel(
    model_name="cosyvoice-300m",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

agent = RealtimeAgent(
    name="voice-assistant",
    sys_prompt="You are a voice assistant.",
    model=realtime_model,
    tts_model=tts_model,
)
```

### 9. Deployment Modes

#### Local Development

```bash
pip install agentscope agentscope-runtime
```

#### AgentScope Runtime Deployment

```python
from agentscope_runtime.engine.deployers import LocalDeployManager

async def main():
    await agent_app.deploy(LocalDeployManager(host="0.0.0.0", port=8090))
```

#### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app_agent.py"]
```

#### Environment Variable Configuration

```bash
# .env file
DASHSCOPE_API_KEY=your-dashscope-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 10. AgentScope Best Practices

| Practice | Description |
|-----|------|
| **Use AgentApp lifecycle** | Register `@init`, `@query`, `@shutdown` hooks for proper resource management |
| **Async-first** | All Agent operations use `async/await` |
| **Externalized config** | Model configs and API keys managed via `agent_config.yml` + environment variables |
| **Session isolation** | Each user session uses a unique session_id / user_id |
| **Built-in SSE streaming** | AgentScope Runtime provides SSE streaming via `/process` endpoint automatically |
| **Custom endpoints via @endpoint** | Use `@agent_app.endpoint()` for custom REST APIs, never import FastAPI |
| **Error handling** | Catch Agent exceptions and return user-friendly error messages |
| **Memory compression** | Enable memory compression to avoid context window overflow |
| **Multi-model support** | Support multiple providers: DashScope, OpenAI, Anthropic |
| **Observability** | AgentScope Runtime has built-in OpenTelemetry tracing |
