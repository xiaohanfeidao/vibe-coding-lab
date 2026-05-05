# Implementation Plan: tech-blazing-core-scaffold

## Overview

构建一套全栈项目脚手架模板，包含 api-server（Python FastAPI）、web-app（React + Arco Design）和 admin-app（React + Arco Design）三个子项目，采用 pnpm monorepo 管理。按依赖图从底向上、垂直切片方式拆分任务。

## Architecture Decisions

- **Monorepo 结构**：pnpm workspace 管理前端子项目，api-server 独立 Python 项目
- **API 路径分离**：`/api/v1/web/`（前台）和 `/api/v1/admin/`（后台）独立路由
- **认证方案**：JWT（HS256）+ bcrypt 密码哈希，Token 存内存不用 localStorage
- **UI 组件库**：Arco Design 全量采用，不自建基础组件
- **限流存储**：内存存储（slowapi），后续可切换 Redis
- **Docker 部署**：docker-compose 编排三个服务，前端 Nginx + 后端 Gunicorn

## Dependency Graph

```
Monorepo root (pnpm-workspace.yaml, .gitignore, package.json)
    │
    ├── api-server/
    │       │
    │       ├── pyproject.toml + 依赖声明
    │       │       │
    │       ├── config/ (application*.yml)
    │       │       │
    │       ├── app/config/ (loader.py → settings.py)
    │       │       │
    │       ├── app/core/ (exceptions, response, middleware, security)
    │       │       │
    │       ├── app/api/v1/ (router 结构: web/ + admin/)
    │       │       │
    │       ├── app/modules/health/ ──────────────────┐
    │       │       │                                  │
    │       ├── app/modules/auth/ ← depends on core    │
    │       │       │                                  │
    │       ├── app/utils/ (pagination.py)             │
    │       │                                          │
    │       ├── gunicorn.conf.py                       │
    │       │                                          │
    │       └── tests/                                 │
    │                                                  │
    ├── web-app/ ← depends on api-server health ───────┘
    │       │
    │       ├── 项目脚手架 (Vite + React + Arco)
    │       ├── api/client.ts + api/modules/health.ts
    │       ├── components/Layout/ (Arco Layout)
    │       ├── pages/Home/ (健康检查展示)
    │       ├── router/ + styles/ + types/
    │       └── tests/
    │
    ├── admin-app/ ← depends on api-server auth + health
    │       │
    │       ├── 项目脚手架 (Vite + React + Arco)
    │       ├── api/client.ts (含 Token 拦截器) + api/auth.ts + api/modules/health.ts
    │       ├── components/Layout/ (Arco Layout + Sider + Menu)
    │       ├── pages/Login/ (认证逻辑)
    │       ├── pages/Dashboard/ (受保护页面)
    │       ├── router/ (路由守卫) + styles/ + types/
    │       └── tests/
    │
    └── Docker/ ← depends on all three sub-projects
            │
            ├── docker-compose.yml
            ├── api-server/Dockerfile
            ├── web-app/Dockerfile + nginx.conf
            └── admin-app/Dockerfile + nginx.conf
```

## Task List

### Phase 1: Foundation — Monorepo + API Server Core

---

## Task 1: 初始化 Monorepo 根目录

**Description:** 创建 `tech-blazing-core-scaffold/` 根目录，配置 pnpm workspace、根 package.json、.gitignore，建立 monorepo 基础结构。

**Acceptance criteria:**
- [ ] `tech-blazing-core-scaffold/` 目录已创建
- [ ] `pnpm-workspace.yaml` 正确声明 web-app 和 admin-app
- [ ] 根 `package.json` 包含 workspace 级脚本（dev/build/test/lint）
- [ ] `.gitignore` 覆盖 Python/Node.js/Docker/IDE/敏感文件
- [ ] `shared/.gitkeep` 已创建

**Verification:**
- [ ] `cd tech-blazing-core-scaffold && pnpm install` 无报错

**Dependencies:** None

**Files likely touched:**
- `tech-blazing-core-scaffold/pnpm-workspace.yaml`
- `tech-blazing-core-scaffold/package.json`
- `tech-blazing-core-scaffold/.gitignore`
- `tech-blazing-core-scaffold/shared/.gitkeep`

**Estimated scope:** S (1-2 files)

---

## Task 2: 初始化 api-server 项目结构与依赖

**Description:** 创建 `api-server/` 子项目，配置 pyproject.toml（含全部依赖声明）、目录结构骨架、application.yml 配置文件。

**Acceptance criteria:**
- [ ] `api-server/pyproject.toml` 包含所有 Python 依赖（FastAPI, Uvicorn, Gunicorn, PyYAML, Pydantic, slowapi, PyJWT, passlib, httpx, pytest, ruff）
- [ ] `api-server/app/` 目录结构完整（`__init__.py` 链条：app/, app/config/, app/core/, app/api/, app/api/v1/, app/api/v1/web/, app/api/v1/admin/, app/modules/, app/modules/health/, app/modules/auth/, app/utils/）
- [ ] `api-server/config/application.yml` 包含完整配置（app/server/auth/cors/rate_limit/logging）
- [ ] `api-server/config/application-dev.yml` 开发环境覆盖
- [ ] `api-server/config/application-prod.yml` 占位（加入 .gitignore）
- [ ] `pip install -e ".[dev]"` 可成功安装

**Verification:**
- [ ] `cd api-server && pip install -e ".[dev]"` 无报错
- [ ] `cd api-server && ruff check .` 无错误

**Dependencies:** Task 1

**Files likely touched:**
- `api-server/pyproject.toml`
- `api-server/app/__init__.py`
- `api-server/app/config/__init__.py`
- `api-server/app/core/__init__.py`
- `api-server/app/api/__init__.py`
- `api-server/app/api/v1/__init__.py`
- `api-server/app/api/v1/web/__init__.py`
- `api-server/app/api/v1/admin/__init__.py`
- `api-server/app/modules/__init__.py`
- `api-server/app/modules/health/__init__.py`
- `api-server/app/modules/auth/__init__.py`
- `api-server/app/utils/__init__.py`
- `api-server/config/application.yml`
- `api-server/config/application-dev.yml`
- `api-server/config/application-prod.yml`

**Estimated scope:** M (3-5 files)

---

## Task 3: 实现 application.yml 配置加载器与 Settings 模型

**Description:** 实现 `app/config/loader.py`（YAML 加载 + 环境覆盖 + 深度合并）和 `app/config/settings.py`（Pydantic Settings 模型），让整个应用可从配置文件读取所有设置。

**Acceptance criteria:**
- [ ] `loader.py` 可加载 `application.yml` 并支持 `application-{profile}.yml` 环境覆盖
- [ ] `loader.py` 支持环境变量占位符 `${ENV_VAR:default}` 解析
- [ ] `settings.py` 定义 AppSettings、ServerSettings、AuthSettings、CorsSettings、RateLimitSettings、LoggingSettings
- [ ] `settings.py` 从 loader 输出构建 Pydantic Settings 实例
- [ ] 配置加载测试通过

**Verification:**
- [ ] `cd api-server && pytest tests/test_config.py -v` 全部通过

**Dependencies:** Task 2

**Files likely touched:**
- `api-server/app/config/loader.py`
- `api-server/app/config/settings.py`
- `api-server/tests/__init__.py`
- `api-server/tests/conftest.py`
- `api-server/tests/test_config.py`

**Estimated scope:** M (3-5 files)

---

## Task 4: 实现核心模块（exceptions / response / middleware / security）

**Description:** 实现 api-server 的核心基础设施：统一异常定义、统一响应格式、请求计时中间件、安全头中间件、CORS 配置。

**Acceptance criteria:**
- [ ] `exceptions.py` 定义 AppException 及常用子类
- [ ] `response.py` 提供统一响应函数 `success_response()` / `error_response()`
- [ ] `middleware.py` 实现 RequestTimingMiddleware（X-Response-Time + 结构化日志）
- [ ] `middleware.py` 实现 SecurityHeadersMiddleware（6 个安全头）
- [ ] `security.py` 提供 CORS 配置初始化函数（从 settings 读取 origins）
- [ ] 全局异常处理器注册（生产环境不暴露堆栈）

**Verification:**
- [ ] `cd api-server && pytest tests/ -v` 通过（含安全头测试）

**Dependencies:** Task 3

**Files likely touched:**
- `api-server/app/core/exceptions.py`
- `api-server/app/core/response.py`
- `api-server/app/core/middleware.py`
- `api-server/app/core/security.py`
- `api-server/tests/test_security.py`

**Estimated scope:** M (3-5 files)

---

## Task 5: 实现 FastAPI 应用工厂与健康检查端点

**Description:** 实现 `app/main.py`（应用工厂，注册中间件/路由/异常处理器）、路由结构（v1/web/admin）、健康检查模块，使 API 服务可启动并提供健康检查。

**Acceptance criteria:**
- [ ] `app/main.py` 使用工厂模式创建 FastAPI 应用
- [ ] 中间件注册顺序正确：SecurityHeaders → RequestTiming → CORS
- [ ] `/api/v1/web/health` 返回 `{ "code": 0, "message": "ok", "data": { "status": "healthy" } }`
- [ ] `/api/v1/admin/health` 返回相同格式
- [ ] `http://localhost:8000/docs` 可访问 Swagger 文档
- [ ] `uvicorn app.main:app --reload` 可启动

**Verification:**
- [ ] `cd api-server && uvicorn app.main:app --reload` 启动无报错
- [ ] `curl http://localhost:8000/api/v1/web/health` 返回 200
- [ ] `cd api-server && pytest tests/test_health.py -v` 全部通过

**Dependencies:** Task 4

**Files likely touched:**
- `api-server/app/main.py`
- `api-server/app/api/v1/router.py`
- `api-server/app/api/v1/web/router.py`
- `api-server/app/api/v1/admin/router.py`
- `api-server/app/api/deps.py`
- `api-server/app/modules/health/schema.py`
- `api-server/app/modules/health/router.py`
- `api-server/tests/test_health.py`

**Estimated scope:** M (3-5 files)

---

## Task 6: 实现 Gunicorn 多进程配置与启动脚本

**Description:** 实现 `gunicorn.conf.py`（多进程配置，从 application.yml 读取参数）和 `scripts/start.sh` 启动脚本。

**Acceptance criteria:**
- [ ] `gunicorn.conf.py` 配置 workers/worker_class/max_requests/keepalive/preload_app
- [ ] workers 默认值 = CPU × 2 + 1
- [ ] `scripts/start.sh` 可执行
- [ ] `gunicorn app.main:app -c gunicorn.conf.py` 可多进程启动

**Verification:**
- [ ] `cd api-server && gunicorn app.main:app -c gunicorn.conf.py` 启动无报错
- [ ] 多 worker 进程可见（`ps aux | grep gunicorn`）

**Dependencies:** Task 5

**Files likely touched:**
- `api-server/gunicorn.conf.py`
- `api-server/scripts/start.sh`

**Estimated scope:** S (1-2 files)

---

## Task 7: 实现分页工具与 API 限流

**Description:** 实现 `app/utils/pagination.py`（通用分页参数与响应模型）和 slowapi 限流集成。

**Acceptance criteria:**
- [ ] `PaginationParams` Pydantic 模型（page/page_size，默认 1/20）
- [ ] `PaginatedResponse` 泛型响应模型（items/total/page/page_size）
- [ ] slowapi Limiter 初始化并注册到 FastAPI app
- [ ] 通用 API 限流 60/min，认证端点限流 10/min
- [ ] 超限返回 429

**Verification:**
- [ ] `cd api-server && pytest tests/ -v` 通过
- [ ] 手动验证限流：连续请求超限后返回 429

**Dependencies:** Task 5

**Files likely touched:**
- `api-server/app/utils/pagination.py`
- `api-server/app/main.py`（注册 limiter）
- `api-server/app/core/middleware.py`（限流集成）

**Estimated scope:** S (1-2 files)

### Checkpoint: Foundation

- [ ] `cd api-server && pytest tests/ -v` 全部通过
- [ ] `cd api-server && ruff check .` 无错误
- [ ] `uvicorn app.main:app --reload` 启动正常，Swagger 可访问
- [ ] `/api/v1/web/health` 和 `/api/v1/admin/health` 返回正确
- [ ] 安全响应头存在
- [ ] Gunicorn 多进程启动正常
- [ ] **Review with human before proceeding**

---

### Phase 2: Frontend — web-app

---

## Task 8: 初始化 web-app 项目脚手架

**Description:** 使用 Vite 创建 React + TypeScript 项目，安装 Arco Design 及全部前端依赖，配置 ESLint/Prettier/Vitest。

**Acceptance criteria:**
- [ ] `web-app/` 项目通过 Vite 创建，React 18 + TypeScript 5
- [ ] `@arco-design/web-react` 已安装
- [ ] `vitest` + `@testing-library/react` + `@testing-library/jest-dom` + `jsdom` 已安装
- [ ] `vite.config.ts` 配置开发代理（/api → localhost:8000）
- [ ] `tsconfig.json` + `tsconfig.app.json` + `tsconfig.node.json` 配置正确
- [ ] ESLint + Prettier 配置就绪
- [ ] `pnpm dev` 可启动开发服务器

**Verification:**
- [ ] `cd web-app && pnpm dev` 启动无报错
- [ ] `cd web-app && pnpm lint` 无错误
- [ ] `cd web-app && pnpm typecheck` 无错误

**Dependencies:** Task 1

**Files likely touched:**
- `web-app/package.json`
- `web-app/vite.config.ts`
- `web-app/tsconfig.json`
- `web-app/tsconfig.app.json`
- `web-app/tsconfig.node.json`
- `web-app/index.html`
- `web-app/eslint.config.js`
- `web-app/.prettierrc`

**Estimated scope:** M (3-5 files)

---

## Task 9: 实现 web-app API 层与类型定义

**Description:** 实现 `api/client.ts`（Axios 实例 + 拦截器 + Arco Message 错误提示）、`api/modules/health.ts`（健康检查 API）、`types/api.d.ts`（统一响应类型）。

**Acceptance criteria:**
- [ ] `api/client.ts` 创建 Axios 实例，baseURL 从 `VITE_API_BASE_URL` 读取
- [ ] 响应拦截器解包 `ApiResponse<T>` 格式
- [ ] 错误拦截器使用 Arco `Message.error()` 全局提示
- [ ] `api/modules/health.ts` 封装 `getHealth()` 方法
- [ ] `types/api.d.ts` 定义 `ApiResponse<T>` 类型

**Verification:**
- [ ] `cd web-app && pnpm typecheck` 无错误
- [ ] `cd web-app && pnpm test` 通过（client 单元测试）

**Dependencies:** Task 8

**Files likely touched:**
- `web-app/src/api/client.ts`
- `web-app/src/api/modules/health.ts`
- `web-app/src/types/api.d.ts`
- `web-app/src/vite-env.d.ts`

**Estimated scope:** S (1-2 files)

---

## Task 10: 实现 web-app 门户网站布局、路由与页面

**Description:** 实现 Arco Layout 门户网站风格布局、React Router 路由配置、多页面（首页/功能/关于/联系我们）、Arco 主题 CSS、全局样式。web-app 采用门户网站风格，包含顶部导航栏、Hero 区域、功能卡片、关于区域、页脚等典型门户元素。

**Acceptance criteria:**
- [ ] `AppLayout.tsx` 使用 Arco `<Layout>` + `<Header>`（含顶部导航 Menu）+ `<Content>` + `<Footer>`
- [ ] 路由配置：`/` → Home, `/features` → Features, `/about` → About, `/contact` → Contact
- [ ] `Home.tsx` 门户首页风格：Hero Banner + 功能亮点 Card 网格 + 数据展示（调用健康检查 API）
- [ ] `Features.tsx` 功能介绍页：Arco Card + Descriptions 展示平台功能
- [ ] `About.tsx` 关于页：Arco Card 展示项目信息
- [ ] `Contact.tsx` 联系页：Arco Form 表单（占位，不实际发送）
- [ ] 所有数据展示页面使用 Container/Presentation 分离 + 三态处理
- [ ] `arco-theme.css` 覆盖品牌色 Token
- [ ] `global.css` 全局样式（门户风格排版）
- [ ] `useRequest.ts` 通用请求 Hook
- [ ] 响应式：移动端导航折叠为 Arco Dropdown

**Verification:**
- [ ] `cd web-app && pnpm dev` 启动后页面可访问
- [ ] 启动 api-server 后，web-app 首页 Hero 区域展示系统状态数据
- [ ] 顶部导航可切换页面，路由正常
- [ ] 移动端导航折叠正常
- [ ] `cd web-app && pnpm test` 通过

**Dependencies:** Task 9, Task 5（api-server 健康检查端点）

**Files likely touched:**
- `web-app/src/main.tsx`
- `web-app/src/App.tsx`
- `web-app/src/components/Layout/AppLayout.tsx`
- `web-app/src/components/Layout/AppLayout.test.tsx`
- `web-app/src/components/Layout/index.ts`
- `web-app/src/pages/Home/Home.tsx`
- `web-app/src/pages/Home/Home.test.tsx`
- `web-app/src/pages/Home/index.ts`
- `web-app/src/pages/Features/Features.tsx`
- `web-app/src/pages/Features/index.ts`
- `web-app/src/pages/About/About.tsx`
- `web-app/src/pages/About/index.ts`
- `web-app/src/pages/Contact/Contact.tsx`
- `web-app/src/pages/Contact/index.ts`
- `web-app/src/router/index.tsx`
- `web-app/src/hooks/useRequest.ts`
- `web-app/src/styles/global.css`
- `web-app/src/styles/arco-theme.css`
- `web-app/src/utils/index.ts`

**Estimated scope:** L (5-8 files) — 门户网站多页面，但每个页面结构清晰

### Checkpoint: web-app

- [ ] `cd web-app && pnpm test` 全部通过
- [ ] `cd web-app && pnpm lint` 无错误
- [ ] web-app 首页门户风格正常展示（Hero + 功能卡片 + 系统状态）
- [ ] 顶部导航可切换页面（首页/功能/关于/联系）
- [ ] 三态（loading/error/empty）正常工作
- [ ] Arco Design 组件正确渲染
- [ ] 移动端响应式正常

---

### Phase 3: Auth — api-server 认证模块

---

## Task 11: 实现 api-server 认证模块

**Description:** 实现 JWT 认证完整流程：登录/登出/刷新 Token/获取当前用户，包括密码哈希、Token 生成/校验、认证依赖注入。

**Acceptance criteria:**
- [ ] `modules/auth/schema.py` 定义 LoginRequest/LoginResponse/TokenResponse/UserResponse
- [ ] `modules/auth/service.py` 实现密码校验（bcrypt）、Token 生成/校验（PyJWT）、刷新逻辑
- [ ] `modules/auth/router.py` 注册 4 个端点：login/logout/refresh/me
- [ ] `/api/v1/admin/auth/login` 接受用户名/密码，返回 access_token + refresh_token
- [ ] `/api/v1/admin/auth/refresh` 接受 refresh_token，返回新 access_token
- [ ] `/api/v1/admin/auth/me` 需 Bearer Token，返回用户信息
- [ ] `app/api/deps.py` 提供 `get_current_user()` 依赖注入
- [ ] 初始管理员账号从 application.yml 读取，首次启动自动创建
- [ ] 认证端点限流 10/min

**Verification:**
- [ ] `cd api-server && pytest tests/test_auth.py -v` 全部通过
- [ ] 手动验证：POST login → GET me → POST refresh → POST logout

**Dependencies:** Task 5, Task 7

**Files likely touched:**
- `api-server/app/modules/auth/schema.py`
- `api-server/app/modules/auth/service.py`
- `api-server/app/modules/auth/router.py`
- `api-server/app/api/deps.py`
- `api-server/app/api/v1/admin/router.py`
- `api-server/app/main.py`（注册 auth 路由）
- `api-server/tests/test_auth.py`

**Estimated scope:** M (3-5 files)

### Checkpoint: Auth

- [ ] `cd api-server && pytest tests/ -v` 全部通过
- [ ] 登录/刷新/获取用户信息端点正常工作
- [ ] 无 Token 访问受保护端点返回 401
- [ ] 限流生效

---

### Phase 3.5: Menu — api-server 菜单模块

---

## Task 11.5: 实现 api-server 菜单模块

**Description:** 实现后台管理菜单 API，返回当前用户可访问的菜单树结构。菜单数据从 application.yml 配置读取，支持按角色区分前台/后台菜单。此模块为 admin-app 侧边栏菜单和 web-app 顶部导航提供数据源。

**Acceptance criteria:**
- [ ] `modules/menu/schema.py` 定义 MenuItem 模型（key/title/icon/path/children/sort）
- [ ] `modules/menu/service.py` 从 application.yml 加载菜单配置，支持按角色过滤
- [ ] `/api/v1/admin/menus` 返回后台管理菜单树（需认证）
- [ ] `/api/v1/web/menus` 返回前台门户导航菜单（无需认证）
- [ ] `config/application.yml` 新增 `menus` 配置节，包含前台和后台菜单定义
- [ ] 菜单支持多级嵌套（children 字段）

**Verification:**
- [ ] `cd api-server && pytest tests/test_menu.py -v` 全部通过
- [ ] GET `/api/v1/web/menus` 返回前台导航菜单
- [ ] GET `/api/v1/admin/menus`（带 Token）返回后台侧边栏菜单

**Dependencies:** Task 5, Task 11

**Files likely touched:**
- `api-server/app/modules/menu/__init__.py`
- `api-server/app/modules/menu/schema.py`
- `api-server/app/modules/menu/service.py`
- `api-server/app/modules/menu/router.py`
- `api-server/app/api/v1/admin/router.py`
- `api-server/app/api/v1/web/router.py`
- `api-server/config/application.yml`
- `api-server/tests/test_menu.py`

**Estimated scope:** M (3-5 files)

---

### Phase 4: Frontend — admin-app

---

## Task 12: 初始化 admin-app 项目脚手架

**Description:** 与 Task 8 对称，创建 admin-app 项目，安装相同依赖，额外配置 Token 管理相关结构。

**Acceptance criteria:**
- [ ] `admin-app/` 项目通过 Vite 创建，React 18 + TypeScript 5
- [ ] `@arco-design/web-react` 已安装
- [ ] 测试依赖已安装
- [ ] `vite.config.ts` 配置开发代理（/api → localhost:8000）
- [ ] `pnpm dev` 可启动开发服务器

**Verification:**
- [ ] `cd admin-app && pnpm dev` 启动无报错
- [ ] `cd admin-app && pnpm lint` 无错误

**Dependencies:** Task 1

**Files likely touched:**
- `admin-app/package.json`
- `admin-app/vite.config.ts`
- `admin-app/tsconfig.json`
- `admin-app/tsconfig.app.json`
- `admin-app/tsconfig.node.json`
- `admin-app/index.html`
- `admin-app/eslint.config.js`
- `admin-app/.prettierrc`

**Estimated scope:** M (3-5 files)

---

## Task 13: 实现 admin-app API 层与 Token 管理

**Description:** 实现 `api/client.ts`（含 Token 自动附加 + 401 刷新拦截器）、`api/auth.ts`（login/logout/refresh/me）、`api/modules/health.ts`、Token 内存管理模块。

**Acceptance criteria:**
- [ ] `api/client.ts` 请求拦截器自动附加 `Authorization: Bearer <token>`
- [ ] `api/client.ts` 响应拦截器：401 时自动调用 refresh，刷新失败跳转登录页
- [ ] `api/auth.ts` 封装 login/logout/refresh/getCurrentUser
- [ ] Token 存储在 JavaScript 内存中（不使用 localStorage）
- [ ] `types/api.d.ts` 定义认证相关类型

**Verification:**
- [ ] `cd admin-app && pnpm typecheck` 无错误
- [ ] `cd admin-app && pnpm test` 通过（Token 管理单元测试）

**Dependencies:** Task 12, Task 11（api-server auth 端点）

**Files likely touched:**
- `admin-app/src/api/client.ts`
- `admin-app/src/api/auth.ts`
- `admin-app/src/api/modules/health.ts`
- `admin-app/src/types/api.d.ts`
- `admin-app/src/vite-env.d.ts`

**Estimated scope:** M (3-5 files)

---

## Task 14: 实现 admin-app 布局、路由守卫、登录页与菜单展示

**Description:** 实现 Arco 后台布局（Layout + Sider + Menu）、登录页（Arco Form + 认证逻辑）、路由守卫（未登录跳转登录页）、侧边栏菜单（从 API 动态加载）。登录后首页展示侧边栏菜单，菜单项可点击切换页面。

**Acceptance criteria:**
- [ ] `AdminLayout.tsx` 使用 Arco `<Layout>` + `<Layout.Sider>` + `<Menu>`，侧边栏菜单从 `/api/v1/admin/menus` 动态加载
- [ ] 菜单项支持多级展开（SubMenu），点击菜单项切换路由
- [ ] 当前路由对应的菜单项自动高亮（selectedKeys 同步）
- [ ] 菜单折叠/展开切换（Sider collapsible）
- [ ] `Login.tsx` 使用 Arco `<Form>` + `<Input>` + `<Button>`，调用 auth API
- [ ] 路由守卫：未登录访问受保护路由时跳转登录页
- [ ] 登录成功后跳转 Dashboard
- [ ] 登出清除 Token 并跳转登录页
- [ ] `arco-theme.css` + `global.css` 样式就绪
- [ ] 菜单加载三态处理：Skeleton（加载中）/ 正常展示 / 错误提示

**Verification:**
- [ ] 启动 api-server + admin-app 后，登录页可正常登录
- [ ] 登录后侧边栏菜单正确展示（Dashboard/系统管理/用户管理等）
- [ ] 点击菜单项可切换页面，当前项高亮
- [ ] 未登录状态访问 Dashboard 被重定向到登录页
- [ ] `cd admin-app && pnpm test` 通过

**Dependencies:** Task 13, Task 11.5（菜单 API）

**Files likely touched:**
- `admin-app/src/main.tsx`
- `admin-app/src/App.tsx`
- `admin-app/src/components/Layout/AdminLayout.tsx`
- `admin-app/src/components/Layout/AdminLayout.test.tsx`
- `admin-app/src/components/Layout/index.ts`
- `admin-app/src/pages/Login/Login.tsx`
- `admin-app/src/pages/Login/index.ts`
- `admin-app/src/api/modules/menu.ts`
- `admin-app/src/router/index.tsx`
- `admin-app/src/hooks/useRequest.ts`
- `admin-app/src/styles/global.css`
- `admin-app/src/styles/arco-theme.css`
- `admin-app/src/utils/index.ts`

**Estimated scope:** L (5-8 files)

---

## Task 15: 实现 admin-app Dashboard 与菜单对应页面

**Description:** 实现 Dashboard 页面和菜单对应的占位页面（系统管理/用户管理等），展示后台管理系统的完整导航体验。Dashboard 使用 Arco Statistic/Card/Table 展示系统信息，其他页面为占位页面。

**Acceptance criteria:**
- [ ] `Dashboard.tsx` 使用 Arco `<Card>` + `<Statistic>` + `<Descriptions>` 展示系统信息
- [ ] Dashboard 调用健康检查 API 展示服务状态
- [ ] Dashboard 展示统计卡片：用户数/访问量/在线数/系统运行时间（mock 数据）
- [ ] 菜单对应的占位页面：`/admin/system`（系统管理）、`/admin/users`（用户管理）
- [ ] 占位页面使用 Arco `<Result title="开发中" />` 提示
- [ ] 三态处理：Skeleton/Result error/Empty
- [ ] 所有页面为受保护页面，需登录后访问

**Verification:**
- [ ] 登录后 Dashboard 页面正常展示系统状态和统计卡片
- [ ] 侧边栏菜单点击可切换到对应页面
- [ ] 占位页面展示"开发中"提示
- [ ] `cd admin-app && pnpm test` 通过

**Dependencies:** Task 14

**Files likely touched:**
- `admin-app/src/pages/Dashboard/Dashboard.tsx`
- `admin-app/src/pages/Dashboard/Dashboard.test.tsx`
- `admin-app/src/pages/Dashboard/index.ts`
- `admin-app/src/pages/System/System.tsx`
- `admin-app/src/pages/System/index.ts`
- `admin-app/src/pages/Users/Users.tsx`
- `admin-app/src/pages/Users/index.ts`
- `admin-app/src/router/index.tsx`（新增路由）

**Estimated scope:** M (3-5 files)

### Checkpoint: admin-app

- [ ] `cd admin-app && pnpm test` 全部通过
- [ ] `cd admin-app && pnpm lint` 无错误
- [ ] 登录 → Dashboard 完整流程正常
- [ ] 侧边栏菜单从 API 动态加载并正确展示
- [ ] 菜单点击切换页面，当前项高亮
- [ ] Token 过期后自动刷新
- [ ] 三态正常工作

---

### Phase 5: Docker & Integration

---

## Task 16: 实现 Docker 配置

**Description:** 实现 docker-compose.yml、各子项目 Dockerfile、前端 nginx.conf，使 `docker-compose up` 可一键启动全部服务。

**Acceptance criteria:**
- [ ] `docker-compose.yml` 编排 api-server + web-app + admin-app
- [ ] `api-server/Dockerfile` 基于 python:3.11-slim，Gunicorn 启动
- [ ] `web-app/Dockerfile` + `admin-app/Dockerfile` 多阶段构建（node:18-alpine → nginx:alpine）
- [ ] `web-app/nginx.conf` + `admin-app/nginx.conf` 配置 SPA 回退 + API 代理
- [ ] `docker-compose up` 可一键启动三个服务

**Verification:**
- [ ] `docker-compose up --build` 构建无报错
- [ ] `http://localhost:3000` 可访问 web-app
- [ ] `http://localhost:3001` 可访问 admin-app
- [ ] `http://localhost:8000/docs` 可访问 API 文档

**Dependencies:** Task 6, Task 10, Task 15

**Files likely touched:**
- `tech-blazing-core-scaffold/docker-compose.yml`
- `api-server/Dockerfile`
- `web-app/Dockerfile`
- `web-app/nginx.conf`
- `admin-app/Dockerfile`
- `admin-app/nginx.conf`

**Estimated scope:** M (3-5 files)

---

## Task 17: 全链路集成验证与最终检查

**Description:** 运行全部测试、lint、类型检查，验证所有 Success Criteria，确保三个子项目可独立运行且互相通信。

**Acceptance criteria:**
- [ ] `cd api-server && pytest tests/ -v` 全部通过
- [ ] `cd api-server && ruff check .` 无错误
- [ ] `cd web-app && pnpm test` 全部通过
- [ ] `cd web-app && pnpm lint` 无错误
- [ ] `cd admin-app && pnpm test` 全部通过
- [ ] `cd admin-app && pnpm lint` 无错误
- [ ] web-app 首页可调用 API 健康检查并展示
- [ ] admin-app 可登录并查看 Dashboard
- [ ] API 安全响应头存在
- [ ] CORS 仅允许配置域名
- [ ] 限流生效

**Verification:**
- [ ] 逐项验证 SPEC.md 中的全部 Success Criteria

**Dependencies:** Task 16

**Files likely touched:**
- 可能需修复测试或配置文件

**Estimated scope:** S (1-2 files)

### Checkpoint: Complete

- [ ] 全部 Success Criteria 满足
- [ ] 三个子项目可独立运行
- [ ] 前后端通信正常
- [ ] Docker 一键部署正常
- [ ] **Ready for review**

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Arco Design 与 React 19 不兼容 | High | 已降级到 React 18（Arco Design 当前适配版本） |
| PyJWT/passlib 版本冲突 | Medium | pyproject.toml 锁定兼容版本范围 |
| Windows 下 Gunicorn 不可用 | Medium | 开发环境用 uvicorn，Gunicorn 仅在 Linux/Docker 中使用 |
| slowapi 内存存储重启丢失限流状态 | Low | 脚手架阶段可接受，后续可切换 Redis |
| Docker 构建时间过长 | Low | 多阶段构建 + pip/pnpm 缓存优化 |

## Parallelization Opportunities

| 可并行 | 说明 |
|--------|------|
| Task 8 (web-app 脚手架) ↔ Task 2 (api-server 依赖) | 无依赖关系，可同时进行 |
| Task 12 (admin-app 脚手架) ↔ Task 11 (auth 模块) | admin-app 脚手架不依赖 auth，可先创建 |
| Task 9 (web-app API 层) ↔ Task 6 (Gunicorn 配置) | 完全独立 |
| Task 10 (web-app 门户页面) ↔ Task 11.5 (菜单 API) | web-app 门户页面不依赖菜单 API |

| 必须顺序 | 说明 |
|----------|------|
| Task 3 → Task 4 → Task 5 | 配置 → 核心 → 应用，强依赖链 |
| Task 11 → Task 11.5 | 菜单 API 依赖认证模块（admin 菜单需认证） |
| Task 11.5 → Task 14 | admin-app 菜单展示依赖菜单 API |
| Task 11 → Task 13 | admin-app Token 管理依赖 auth 端点 |
| Task 5 → Task 10 | web-app 首页依赖健康检查端点 |
| Task 15 → Task 16 | Docker 依赖所有子项目完成 |
