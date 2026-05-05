# Spec: tech-blazing-core-scaffold

## Objective

构建一套全栈项目脚手架模板，后续所有新项目可基于此模板快速启动。脚手架包含三个子项目：

- **web-app**（前台页面工程）：面向终端用户的 Web 应用，基于 TypeScript + React + Vite 构建
- **admin-app**（后台页面工程）：面向管理员的运营后台，基于 TypeScript + React + Vite 构建
- **api-server**（API 系统）：提供 RESTful API 服务，基于 Python FastAPI 构建，支持多进程部署，通过 `application.yml` 管理配置

两个前端工程均通过 REST API 与 api-server 通信。本脚手架作为基础设施模板，提供开箱即用的项目结构、配置管理、开发工具链和基础功能模块。

### 用户故事

- 作为开发者，我可以 `clone` 此脚手架后立即启动三个子项目的开发服务器
- 作为开发者，我可以通过修改 `application.yml` 切换 API 系统的运行环境
- 作为开发者，我可以在前台和后台工程中调用 API 系统的接口并获取数据
- 作为运维人员，我可以通过 gunicorn 多进程方式部署 API 系统

## Tech Stack

### api-server（Python 后端）

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 运行时 |
| FastAPI | 0.115+ | Web 框架 |
| Uvicorn | 0.34+ | ASGI 服务器 |
| Gunicorn | 23+ | 多进程管理 |
| PyYAML | 6+ | 解析 application.yml |
| Pydantic | 2+ | 数据校验与 Settings 管理 |
| Pydantic Settings | 2+ | 配置模型 |
| httpx | 0.28+ | 异步 HTTP 客户端（测试用） |
| pytest | 8+ | 测试框架 |
| pytest-asyncio | 0.24+ | 异步测试支持 |
| ruff | 0.8+ | Linter + Formatter |
| slowapi | 0.1+ | API 限流 |
| PyJWT | 2.9+ | JWT Token 生成与校验 |
| passlib | 1.7+ | 密码哈希（bcrypt） |

### web-app & admin-app（TypeScript 前端）

| 依赖 | 版本 | 用途 |
|------|------|------|
| Node.js | 18+ | 运行时 |
| React | 18+ | UI 框架（Arco Design 当前适配版本） |
| TypeScript | 5+ | 类型系统 |
| Vite | 6+ | 构建工具 |
| @arco-design/web-react | 2.67+ | UI 组件库（字节 Arco Design） |
| React Router | 7+ | 路由 |
| Axios | 1+ | HTTP 客户端 |
| Vitest | 3+ | 单元测试 |
| @testing-library/react | 16+ | 组件测试 |
| @testing-library/jest-dom | 6+ | DOM 断言扩展 |
| jsdom | 25+ | 测试 DOM 环境 |
| ESLint | 9+ | 代码检查 |
| Prettier | 3+ | 代码格式化 |

### 工程级工具

| 工具 | 用途 |
|------|------|
| pnpm | Monorepo 包管理器 |
| pnpm workspace | 子项目依赖管理 |

## Commands

### api-server

```bash
# 安装依赖
cd api-server && pip install -e ".[dev]"

# 开发模式（单进程，热重载）
cd api-server && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式（多进程）
cd api-server && gunicorn app.main:app -c gunicorn.conf.py

# 运行测试
cd api-server && pytest tests/ -v

# 代码检查
cd api-server && ruff check . && ruff format --check .

# 自动修复
cd api-server && ruff check --fix . && ruff format .
```

### web-app

```bash
# 安装依赖
cd web-app && pnpm install

# 开发模式
cd web-app && pnpm dev

# 构建
cd web-app && pnpm build

# 预览构建产物
cd web-app && pnpm preview

# 运行测试
cd web-app && pnpm test

# 代码检查
cd web-app && pnpm lint

# 类型检查
cd web-app && pnpm typecheck
```

### admin-app

```bash
# 安装依赖
cd admin-app && pnpm install

# 开发模式
cd admin-app && pnpm dev

# 构建
cd admin-app && pnpm build

# 预览构建产物
cd admin-app && pnpm preview

# 运行测试
cd admin-app && pnpm test

# 代码检查
cd admin-app && pnpm lint

# 类型检查
cd admin-app && pnpm typecheck
```

### 根目录（Monorepo 级别）

```bash
# 安装所有前端依赖
pnpm install

# 同时启动所有子项目开发服务器
pnpm -r --parallel dev

# 同时构建所有前端项目
pnpm -r build

# 同时运行所有前端测试
pnpm -r test

# 同时运行所有前端 lint
pnpm -r lint
```

## Project Structure

```
tech-blazing-core-scaffold/
├── pnpm-workspace.yaml              # pnpm monorepo 工作区配置
├── package.json                     # 根级 package.json（workspace 脚本）
├── docker-compose.yml               # Docker 编排（api-server + web-app + admin-app）
├── .gitignore                       # Git 忽略规则
├── README.md                        # 项目说明
│
├── api-server/                      # Python FastAPI 后端
│   ├── pyproject.toml               # Python 项目配置 + 依赖
│   ├── gunicorn.conf.py             # Gunicorn 多进程配置
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI 应用工厂
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── loader.py            # application.yml 加载器
│   │   │   └── settings.py          # Pydantic Settings 模型
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py        # 全局异常定义
│   │   │   ├── middleware.py        # 中间件（CORS / 请求日志 / 限流）
│   │   │   ├── response.py         # 统一响应格式
│   │   │   └── security.py         # 安全工具（输入校验、安全头）
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # 依赖注入
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py        # v1 路由聚合
│   │   │       ├── web/             # 前台 API 路由
│   │   │       │   ├── __init__.py
│   │   │       │   └── router.py    # /api/v1/web/ 路由聚合
│   │   │       └── admin/           # 后台 API 路由
│   │   │           ├── __init__.py
│   │   │           └── router.py    # /api/v1/admin/ 路由聚合
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── health/              # 健康检查模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── schema.py        # 请求/响应 Pydantic 模型
│   │   │   │   └── router.py
│   │   │       └── auth/                # 认证模块（后台登录）
│   │   │       ├── __init__.py
│   │   │       ├── schema.py        # 登录请求/响应模型
│   │   │       ├── router.py        # 登录/登出/刷新 Token 端点
│   │   │       └── service.py       # 认证业务逻辑
│   │   └── menu/                # 菜单模块（前台/后台导航）
│   │       ├── __init__.py
│   │       ├── schema.py        # 菜单项模型（key/title/icon/path/children）
│   │       ├── service.py       # 菜单加载与角色过滤
│   │       └── router.py        # /api/v1/web/menus + /api/v1/admin/menus
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── pagination.py        # 通用分页工具
│   ├── config/
│   │   ├── application.yml          # 默认配置
│   │   ├── application-dev.yml      # 开发环境覆盖
│   │   └── application-prod.yml     # 生产环境覆盖
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest fixtures
│   │   ├── test_health.py           # 健康检查测试
│   │   ├── test_config.py           # 配置加载测试
│   │   ├── test_auth.py             # 认证模块测试
│   │   ├── test_menu.py             # 菜单模块测试
│   │   └── test_security.py         # 安全相关测试
│   ├── Dockerfile                   # API 服务 Docker 镜像
│   └── scripts/
│       └── start.sh                 # 多进程启动脚本
│
├── web-app/                         # 前台页面工程
│   ├── package.json
│   ├── Dockerfile                   # 前台 Docker 镜像（多阶段构建 + Nginx）
│   ├── nginx.conf                   # Nginx 配置（SPA 回退 + API 代理）
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── public/
│   │   └── favicon.ico
│   └── src/
│       ├── main.tsx                 # 应用入口（引入 @arco-design/web-react）
│       ├── App.tsx                  # 根组件
│       ├── vite-env.d.ts
│       ├── api/
│       │   ├── client.ts            # Axios 实例 + 拦截器
│       │   └── modules/
│       │       ├── health.ts        # 健康检查 API
│       │       └── menu.ts          # 前台导航菜单 API
│       ├── components/
│       │   └── Layout/
│       │       ├── AppLayout.tsx    # 基于 Arco Layout 的门户布局（Header+Menu+Content+Footer）
│       │       ├── AppLayout.test.tsx
│       │       └── index.ts
│       ├── hooks/
│       │   └── useRequest.ts        # 通用请求 Hook
│       ├── pages/
│       │   ├── Home/
│       │   │   ├── Home.tsx         # 门户首页（Hero Banner + 功能卡片 + 系统状态）
│       │   │   ├── Home.test.tsx
│       │   │   └── index.ts
│       │   ├── Features/
│       │   │   ├── Features.tsx     # 功能介绍页（Arco Card + Descriptions）
│       │   │   └── index.ts
│       │   ├── About/
│       │   │   ├── About.tsx        # 关于页（Arco Card 展示项目信息）
│       │   │   └── index.ts
│       │   └── Contact/
│       │       ├── Contact.tsx      # 联系页（Arco Form 占位）
│       │       └── index.ts
│       ├── router/
│       │   └── index.tsx            # 路由配置
│       ├── styles/
│       │   ├── global.css           # 全局样式
│       │   └── arco-theme.css       # Arco Design Token 覆盖（品牌色/圆角/间距）
│       ├── types/
│       │   └── api.d.ts             # API 响应类型定义
│       └── utils/
│           └── index.ts             # 工具函数
│
├── admin-app/                       # 后台页面工程
│   ├── package.json
│   ├── Dockerfile                   # 后台 Docker 镜像（多阶段构建 + Nginx）
│   ├── nginx.conf                   # Nginx 配置（SPA 回退 + API 代理）
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── public/
│   │   └── favicon.ico
│   └── src/
│       ├── main.tsx                 # 应用入口（引入 @arco-design/web-react）
│       ├── App.tsx                  # 根组件
│       ├── vite-env.d.ts
│       ├── api/
│       │   ├── client.ts            # Axios 实例 + 拦截器（含 Token 自动附加 + 401 刷新）
│       │   ├── auth.ts              # 认证 API（login/logout/refresh/me）
│       │   └── modules/
│       │       ├── health.ts        # 健康检查 API
│       │       └── menu.ts          # 后台菜单 API
│       ├── components/
│       │   └── Layout/
│       │       ├── AdminLayout.tsx  # 基于 Arco Layout + Sider + Menu 的后台布局（动态菜单）
│       │       ├── AdminLayout.test.tsx
│       │       └── index.ts
│       ├── hooks/
│       │   └── useRequest.ts        # 通用请求 Hook
│       ├── pages/
│       │   ├── Dashboard/
│       │   │   ├── Dashboard.tsx     # 仪表盘（Arco Statistic/Card + 健康检查 + Mock 统计）
│       │   │   ├── Dashboard.test.tsx
│       │   │   └── index.ts
│       │   ├── Login/
│       │   │   ├── Login.tsx         # 登录页（使用 Arco Form/Input/Button，含认证逻辑）
│       │   │   └── index.ts
│       │   ├── System/
│       │   │   ├── System.tsx        # 系统管理（占位：Arco Result "开发中"）
│       │   │   └── index.ts
│       │   └── Users/
│       │       ├── Users.tsx         # 用户管理（占位：Arco Result "开发中"）
│       │       └── index.ts
│       ├── router/
│       │   └── index.tsx            # 路由配置
│       ├── styles/
│       │   ├── global.css           # 全局样式
│       │   └── arco-theme.css       # Arco Design Token 覆盖
│       ├── types/
│       │   └── api.d.ts             # API 响应类型定义
│       └── utils/
│           └── index.ts             # 工具函数
│
└── shared/                          # 前端共享代码（可选扩展）
    └── .gitkeep
```

## Code Style

### Python (api-server)

```python
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    host: str = Field(default="0.0.0.0", alias="server.host")
    port: int = Field(default=8000, alias="server.port")
    workers: int = Field(default=4, alias="server.workers")
    worker_class: str = Field(
        default="uvicorn.workers.UvicornWorker",
        alias="server.worker_class",
    )


class AppSettings(BaseSettings):
    name: str = Field(default="tech-blazing-core-scaffold", alias="app.name")
    version: str = Field(default="0.1.0", alias="app.version")
    debug: bool = Field(default=False, alias="app.debug")
    server: ServerSettings = ServerSettings()


def load_config(profile: str | None = None) -> dict:
    config_dir = Path(__file__).resolve().parent.parent.parent / "config"
    base = yaml.safe_load((config_dir / "application.yml").read_text())
    if profile:
        override = config_dir / f"application-{profile}.yml"
        if override.exists():
            deep_merge(base, yaml.safe_load(override.read_text()))
    return base
```

**关键约定：**
- 使用 `from __future__ import annotations` 启用延迟注解
- 所有配置项从 `application.yml` 读取，不硬编码
- 函数优先使用 `async def`
- 类型注解覆盖所有公开函数签名
- 文件编码统一 UTF-8
- Ruff 规则：行宽 120，双引号，缩进 4 空格

### TypeScript (web-app & admin-app)

```typescript
import axios, { AxiosInstance, AxiosResponse } from "axios";
import { Message } from "@arco-design/web-react";

interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

function createApiClient(baseURL: string): AxiosInstance {
  const client = axios.create({ baseURL, timeout: 10000 });

  client.interceptors.response.use(
    (response: AxiosResponse<ApiResponse>) => response.data,
    (error) => {
      Message.error(error.response?.data?.message ?? "请求失败");
      return Promise.reject(error);
    },
  );

  return client;
}

export const apiClient = createApiClient(
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
);
```

**关键约定：**
- 严格模式：`"strict": true`
- 函数组件 + Hooks，不使用 class 组件
- **UI 组件全部使用 Arco Design，不自建基础组件**
- **Arco 组件按需引入**：`import { Button } from "@arco-design/web-react"`（Vite 自动 tree-shake）
- 文件命名：组件 PascalCase（`HomePage.tsx`），工具 camelCase（`useRequest.ts`）
- 导出使用命名导出，仅入口文件使用默认导出
- API 类型定义集中在 `types/api.d.ts`
- ESLint + Prettier：单引号，尾逗号，2 空格缩进，行宽 100

## Frontend Architecture & UI Engineering

> 参考 `skills/frontend-ui-engineering/SKILL.md`
> UI 组件库：[Arco Design](https://arco.design/) — 字节跳动企业级设计系统

### Arco Design 使用原则

**全量采用 Arco Design 组件体系，不自造轮子：**

| 需求 | 使用 Arco 组件 | 禁止自建 |
|------|---------------|----------|
| 布局 | `<Layout>` / `<Layout.Header>` / `<Layout.Content>` / `<Layout.Sider>` / `<Layout.Footer>` | 自建 Layout |
| 导航 | `<Menu>` / `<Breadcrumb>` / `<PageHeader>` | 自建导航栏 |
| 表单 | `<Form>` / `<Input>` / `<Select>` / `<DatePicker>` / `<Switch>` | 自建表单控件 |
| 数据展示 | `<Table>` / `<List>` / `<Card>` / `<Descriptions>` / `<Statistic>` | 自建数据组件 |
| 反馈 | `<Message>` / `<Notification>` / `<Modal>` / `<Drawer>` / `<Popconfirm>` | 自建弹窗/提示 |
| 加载态 | `<Skeleton>` / `<Spin>` | 自建加载指示器 |
| 空状态 | `<Empty>` | 自建空状态 |
| 错误态 | `<Result status="error">` | 自建错误页 |
| 分页 | `<Pagination>` / Table 内置分页 | 自建分页 |
| 侧边栏 | `<Layout.Sider>` + `<Menu>` | 自建侧边栏 |

**Arco Design 主题定制：**

```tsx
// 通过 CSS 变量覆盖主题（推荐方式）
// src/styles/arco-theme.css
:root {
  --arcoblue-6: #165dff;      /* 品牌主色 — 可按项目需求调整 */
  --arcoblue-5: #4080ff;
  --arcoblue-7: #0e42d2;
  --border-radius-medium: 4px;
  --border-radius-large: 8px;
}
```

- 主题定制通过 Arco Design Token（CSS 变量）实现，不修改组件源码
- 可使用 [Arco DesignLab](https://arco.design/themes) 生成完整主题包
- 颜色、圆角、间距、字重等均通过 Token 统一管控

### 组件架构

**文件组织原则：就近放置（Colocation）**

每个组件的相关文件放在同一目录下：

```
src/components/
  TaskList/
    TaskList.tsx          # 组件实现
    TaskList.test.tsx     # 测试
    use-task-list.ts      # 自定义 Hook（如有复杂状态）
    types.ts              # 组件专属类型（如需要）
    index.ts              # 导出
```

**组合优于配置 — 使用 Arco Layout 组合模式：**

```tsx
// ✅ Good: 使用 Arco Layout 组合
import { Layout } from "@arco-design/web-react";

const { Header, Content, Footer, Sider } = Layout;

<Layout>
  <Header>
    <Logo />
  </Header>
  <Layout>
    <Sider>
      <NavigationMenu />
    </Sider>
    <Content>
      <PageContent />
    </Content>
  </Layout>
  <Footer />
</Layout>

// ❌ Avoid: 过度配置
<Layout header={<Logo />} content={<PageContent />} variant="default" />
```

**分离数据获取与展示（Container / Presentation 分离）：**

```tsx
import { Skeleton, Result, Empty } from "@arco-design/web-react";

// Container: 处理数据获取和状态
export function HealthPageContainer() {
  const { data, isLoading, error, refetch } = useHealthCheck();

  if (isLoading) return <Skeleton animation />;
  if (error) return (
    <Result
      status="error"
      title="无法连接服务"
      subTitle={error.message}
      extra={<Button type="primary" onClick={refetch}>重试</Button>}
    />
  );
  if (!data) return <Empty description="暂无数据" />;

  return <HealthPage data={data} />;
}

// Presentation: 纯展示
export function HealthPage({ data }: { data: HealthData }) {
  return (
    <Card title="系统状态">
      <Descriptions
        data={[
          { label: "状态", value: data.status },
          { label: "版本", value: data.version },
        ]}
      />
    </Card>
  );
}
```

### 状态管理策略

按复杂度递增选择最简方案：

| 层级 | 方案 | 适用场景 |
|------|------|----------|
| Local state (`useState`) | 组件内 UI 状态 | 表单输入、弹窗开关 |
| Lifted state | 父组件管理 | 2-3 个兄弟组件共享 |
| URL state (`searchParams`) | 路由参数 | 筛选条件、分页、可分享状态 |
| Context | React Context | 主题、语言、全局配置（读多写少） |
| Server state | 自定义 Hook + Axios | 远程数据获取与缓存 |
| Global store | 预留扩展位 | 复杂全局客户端状态（后续按需引入） |

**规则：** Prop drilling 不超过 3 层。超过时引入 Context 或重构组件树。

### 设计系统规范 — Arco Design Token 体系

Arco Design 使用 Design Token 作为设计决策的唯一来源，通过 CSS 变量实现主题定制。

**Arco Design 核心设计原则：**

| 原则 | 说明 |
|------|------|
| 一致（Agreement） | 一致的规则保证整体协调 |
| 韵律（Rhythm） | 跳动的韵律构建字节的美感 |
| 清晰（Clear） | 清晰的指向亦是效率的提升 |
| 开放（Open） | 开放包容是解决问题的思路 |

**避免 AI 默认审美：**

| AI 默认模式 | 问题 | 正确做法 |
|-------------|------|----------|
| 全紫/靛蓝色调 | 千篇一律 | 使用 Arco Design 默认色板（arcoblue-6: #165dff）或项目定制主题 |
| 过度渐变 | 视觉噪声 | Arco Design 默认扁平风格 |
| 全部圆角 `rounded-2xl` | 忽略层级 | 使用 Arco border-radius 体系（small: 2px, medium: 4px, large: 8px） |
| 通用卡片网格 | 忽略信息优先级 | 使用 Arco Card + Descriptions 按信息层级组织 |
| 过大间距 | 破坏视觉层级 | 使用 Arco 间距体系 |

**Arco Design Token 间距体系：**

```css
:root {
  /* Arco Design 内置间距 Token */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-7: 28px;
  --spacing-8: 32px;
  --spacing-9: 36px;
  --spacing-10: 40px;
}
```

禁止使用不在 Arco 间距体系中的值（如 `13px`、`2.3rem`）。Arco 组件内部间距已按此体系对齐。

**Arco Design 排版层级：**

```css
:root {
  /* Arco 字体 Token */
  --font-size-body-1: 12px;    /* 辅助文字 */
  --font-size-body-2: 13px;    /* 正文（小） */
  --font-size-body-3: 14px;    /* 正文 */
  --font-size-title-1: 16px;   /* 小标题 */
  --font-size-title-2: 20px;   /* 标题 */
  --font-size-title-3: 24px;   /* 大标题 */
  --font-weight-400: 400;      /* 常规 */
  --font-weight-500: 500;      /* 中等 */
  --font-weight-700: 700;      /* 粗体 */
}
```

标题层级对应：
- h1 → `font-size-title-3`（24px，每页仅一个）
- h2 → `font-size-title-2`（20px，区域标题）
- h3 → `font-size-title-1`（16px，子区域标题）
- body → `font-size-body-3`（14px，正文）
- small → `font-size-body-1`（12px，辅助文字）

**Arco Design 颜色体系：**

```css
:root {
  /* Arco 品牌色 */
  --arcoblue-6: #165dff;       /* 主色 */
  --arcoblue-5: #4080ff;       /* 浅主色 */
  --arcoblue-7: #0e42d2;       /* 深主色 */

  /* Arco 功能色 */
  --green-6: #00b42a;          /* 成功 */
  --orange-6: #ff7d00;         /* 警告 */
  --red-6: #f53f3f;            /* 错误 */
  --cyan-6: #14c9c9;           /* 信息 */

  /* Arco 中性色 */
  --gray-1: #f7f8fa;           /* 背景 */
  --gray-2: #f2f3f5;           /* 填充 */
  --gray-3: #e5e6eb;           /* 边框 */
  --gray-4: #c9cdd4;           /* 填充/分割线 */
  --gray-5: #a9aeb8;           /* 禁用文字 */
  --gray-6: #86909c;           /* 辅助文字 */
  --gray-7: #6b7785;           /* 正文 */
  --gray-8: #4e5969;           /* 标题 */
  --gray-9: #272e3b;           /* 标题 */
  --gray-10: #1d2129;          /* 标题 */
}
```

- 使用 Arco 语义化颜色 Token，不使用原始 hex 值
- 确保对比度：正文 ≥ 4.5:1，大字 ≥ 3:1
- 不仅依赖颜色传达信息（同时使用图标、文字或图案）

### 无障碍（WCAG 2.1 AA）

Arco Design 组件内置无障碍支持（ARIA 属性、键盘导航），但仍需在业务层注意：

**键盘导航：**

```tsx
// ✅ Good: 使用 Arco Button（内置键盘支持）
<Button onClick={handleClick}>操作</Button>

// ❌ Bad: 不可聚焦
<div onClick={handleClick}>操作</div>
```

**ARIA 标签：**

```tsx
// 图标按钮需 aria-label
<Button icon={<IconClose />} aria-label="关闭对话框" />

// 表单使用 Arco Form + 规则校验
<Form.Item label="邮箱" field="email" rules={[{ required: true, type: "email" }]}>
  <Input placeholder="请输入邮箱" />
</Form.Item>
```

**焦点管理：** Arco Modal/Drawer 打开时自动聚焦，关闭时焦点返回触发元素。

### 必须处理的三态 — 使用 Arco 组件

每个数据展示组件必须处理以下三种状态：

```tsx
import { Skeleton, Result, Empty, Button } from "@arco-design/web-react";

export function DataPage() {
  const { data, isLoading, error, refetch } = useData();

  if (isLoading) return <Skeleton animation />;
  if (error) return (
    <Result
      status="error"
      title="加载失败"
      subTitle={error.message}
      extra={<Button type="primary" onClick={refetch}>重试</Button>}
    />
  );
  if (!data || data.length === 0) return <Empty description="暂无数据" />;

  return <DataList data={data} />;
}
```

- **Loading 态**：使用 Arco `<Skeleton animation />`，不用自定义 Spinner
- **Error 态**：使用 Arco `<Result status="error" />` + 重试按钮
- **Empty 态**：使用 Arco `<Empty />` + 说明文字

### 响应式设计

移动优先，逐步扩展。Arco Design 的 Grid 系统提供响应式支持：

```tsx
import { Grid } from "@arco-design/web-react";
const { Row, Col } = Grid;

<Row gutter={16}>
  <Col xs={24} sm={12} lg={8}>
    <Card>内容 1</Card>
  </Col>
  <Col xs={24} sm={12} lg={8}>
    <Card>内容 2</Card>
  </Col>
  <Col xs={24} sm={12} lg={8}>
    <Card>内容 3</Card>
  </Col>
</Row>
```

测试断点：320px、768px、1024px、1440px。

## Performance Requirements

> 参考 `skills/performance-optimization/SKILL.md`

### 性能预算

| 指标 | 目标 | 度量方式 |
|------|------|----------|
| API 响应时间 (p95) | < 200ms | 中间件请求日志 |
| API 响应时间 (p99) | < 500ms | 中间件请求日志 |
| JS 初始包体积 (gzip) | < 200KB | Vite 构建输出 |
| CSS 体积 (gzip) | < 50KB | Vite 构建输出 |
| LCP (前端) | ≤ 2.5s | Lighthouse |
| INP (前端) | ≤ 200ms | Lighthouse |
| CLS (前端) | ≤ 0.1 | Lighthouse |
| Time to Interactive | < 3.5s (4G) | Lighthouse |

### api-server 性能规范

**优化工作流：度量 → 定位 → 修复 → 验证 → 防护**

```
1. MEASURE  → 建立基线数据
2. IDENTIFY → 找到实际瓶颈（非假设）
3. FIX      → 针对性修复
4. VERIFY   → 再次度量，确认改善
5. GUARD    → 添加监控或测试防止回退
```

**请求耗时日志（内置中间件）：**

```python
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        logger.info(
            "%s %s → %d (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
```

**多进程性能考量：**

```python
# gunicorn.conf.py — 从 application.yml 读取配置
import multiprocessing

bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 5000
max_requests_jitter = 500
preload_app = True
```

- `workers` 默认值：CPU 核数 × 2 + 1（可被 application.yml 覆盖）
- `max_requests` + `max_requests_jitter`：防止内存泄漏，定期重启 worker
- `preload_app`：预加载应用代码，减少 worker 启动时间和内存占用

**列表端点必须分页：**

```python
from app.utils.pagination import PaginationParams, PaginatedResponse

@router.get("/items", response_model=PaginatedResponse[ItemOut])
async def list_items(pagination: PaginationParams = Depends()):
    return await item_service.list(pagination)
```

禁止无分页的全量数据返回。

**异步优先：**

- 所有 I/O 操作使用 `async def`
- 不在请求处理路径中引入同步阻塞调用
- 如必须使用同步库，通过 `asyncio.to_thread()` 在线程池中执行

### 前端性能规范

**路由级代码分割：**

```tsx
import { lazy, Suspense } from "react";
import { Skeleton } from "@arco-design/web-react";

const HomePage = lazy(() => import("./pages/Home"));
const DashboardPage = lazy(() => import("./pages/Dashboard"));

function App() {
  return (
    <Suspense fallback={<Skeleton animation />}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Suspense>
  );
}
```

**图片优化：**

- LCP 图片设置 `fetchpriority="high"`
- 非首屏图片使用 `loading="lazy"` + `decoding="async"`
- 所有 `<img>` 必须设置 `width` 和 `height` 属性（防止 CLS）

**避免不必要的重渲染：**

```tsx
// 稳定引用
const DEFAULT_OPTIONS = { sortBy: "date", order: "desc" } as const;

// 昂贵计算使用 useMemo
const stats = useMemo(() => calculateStats(data), [data]);

// 昂贵组件使用 React.memo
const ExpensiveList = React.memo(function ExpensiveList({ items }: Props) {
  return <ul>{items.map(/* ... */)}</ul>;
});
```

## Security Requirements

> 参考 `skills/security-and-hardening/SKILL.md`

### api-server 安全规范

#### 输入校验（所有 API 端点）

所有外部输入在系统边界（API 路由层）进行校验：

```python
from pydantic import BaseModel, Field

class HealthCheckQuery(BaseModel):
    verbose: bool = Field(default=False)

@router.get("/health")
async def health_check(query: HealthCheckQuery = Depends()):
    if query.verbose:
        return {"status": "healthy", "details": {...}}
    return {"status": "healthy"}
```

- 所有请求体使用 Pydantic 模型校验
- 所有查询参数使用 Pydantic 模型 + `Depends()` 校验
- 禁止直接从 `request.json()` 或 `request.query_params` 读取未校验数据

#### 安全响应头

```python
from starlette.middleware.base import BaseHTTPMiddleware

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

#### CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- `allow_origins` 从 `application.yml` 读取，不使用 `["*"]`
- 开发环境默认允许 `http://localhost:5173`（Vite 默认端口）
- 生产环境必须显式配置允许的域名

#### API 限流

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {"status": "healthy"}
```

- 通用 API：60 次/分钟
- 认证相关端点（后续扩展）：10 次/15分钟

#### 错误响应安全

```python
from app.core.exceptions import AppException

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal Server Error",
            "data": None,
        },
    )
```

- 生产环境不暴露堆栈跟踪
- 不向客户端返回内部错误细节
- 统一错误响应格式

#### 敏感信息管理

```
application.yml 结构：
├── application.yml         → 提交（不含敏感信息，仅默认值）
├── application-dev.yml     → 提交（开发环境非敏感配置）
├── application-prod.yml    → 不提交（生产环境含敏感配置，加入 .gitignore）
```

- 敏感配置（数据库密码、API Key 等）通过环境变量注入：`${ENV_VAR:default_value}`
- `.gitignore` 必须包含：`application-prod.yml`、`*.pem`、`*.key`、`.env`
- 禁止在日志中记录密码、Token 等敏感数据
- 禁止在 API 响应中返回敏感字段

#### application.yml 安全设计

```yaml
# config/application.yml
app:
  name: tech-blazing-core-scaffold
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

cors:
  origins:
    - "http://localhost:5173"
    - "http://localhost:5174"

rate_limit:
  enabled: true
  default: "60/minute"
  auth: "10/minute"

logging:
  level: INFO
  format: json
```

## Auth Module Specification

### 后台认证（admin-app → api-server）

后台管理系统预置完整的 JWT 认证流程：

**API 端点（`/api/v1/admin/auth/`）：**

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/admin/auth/login` | POST | 管理员登录，返回 access_token + refresh_token |
| `/api/v1/admin/auth/logout` | POST | 登出（可选：Token 黑名单） |
| `/api/v1/admin/auth/refresh` | POST | 刷新 access_token |
| `/api/v1/admin/auth/me` | GET | 获取当前用户信息 |

**认证流程：**

```
1. 管理员在 admin-app 登录页输入用户名/密码
2. POST /api/v1/admin/auth/login → 服务端校验 → 返回 JWT Token 对
3. admin-app 将 Token 存储在内存中（不存 localStorage）
4. 后续请求通过 Authorization: Bearer <token> 头携带
5. Token 过期前通过 /refresh 刷新
6. 登出时清除内存中的 Token
```

**Token 策略：**

- Access Token：短期有效（30 分钟，可配置）
- Refresh Token：长期有效（7 天，可配置）
- 签名算法：HS256
- 密钥从 `application.yml` 的 `auth.secret_key` 读取，生产环境通过环境变量注入
- 密码哈希：bcrypt（passlib）

**前端 Token 管理：**

```tsx
// admin-app: Token 存储在内存中，不使用 localStorage
let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
}

export function getAccessToken(): string | null {
  return accessToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
}
```

- Token 存储在 JavaScript 内存中，页面刷新时通过 refresh_token 恢复
- Axios 请求拦截器自动附加 `Authorization` 头
- 401 响应自动触发 refresh 流程，刷新失败跳转登录页

**初始管理员账号：**

- 通过 `application.yml` 配置初始管理员用户名/密码
- 密码以 bcrypt 哈希存储，不存明文
- 首次启动时自动创建初始管理员

### 前台 API 路径（`/api/v1/web/`）

前台 web-app 的 API 端点挂在 `/api/v1/web/` 路径下，当前阶段无需认证：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/web/health` | GET | 前台健康检查 |

后续扩展前台用户认证时，在 `/api/v1/web/auth/` 下添加对应端点。

## Menu Module Specification

### 菜单 API

菜单数据从 `application.yml` 配置读取，支持前台/后台不同菜单树，支持多级嵌套。

**API 端点：**

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/v1/web/menus` | GET | 无 | 获取前台门户导航菜单 |
| `/api/v1/admin/menus` | GET | Bearer Token | 获取后台管理侧边栏菜单 |

**菜单项模型：**

```python
class MenuItem(BaseModel):
    key: str
    title: str
    icon: str | None = None
    path: str | None = None
    children: list[MenuItem] | None = None
    sort: int = 0
```

**application.yml 菜单配置示例：**

```yaml
menus:
  web:
    - key: home
      title: 首页
      icon: icon-home
      path: /
      sort: 1
    - key: features
      title: 功能
      icon: icon-apps
      path: /features
      sort: 2
    - key: about
      title: 关于
      icon: icon-info-circle
      path: /about
      sort: 3
    - key: contact
      title: 联系我们
      icon: icon-phone
      path: /contact
      sort: 4
  admin:
    - key: dashboard
      title: 仪表盘
      icon: icon-dashboard
      path: /admin/dashboard
      sort: 1
    - key: system
      title: 系统管理
      icon: icon-settings
      sort: 2
      children:
        - key: system-config
          title: 系统配置
          path: /admin/system
          sort: 1
    - key: users
      title: 用户管理
      icon: icon-user-group
      path: /admin/users
      sort: 3
```

## Docker Configuration

### docker-compose.yml

```yaml
# docker-compose.yml — 根目录
version: "3.8"

services:
  api-server:
    build:
      context: ./api-server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APP_PROFILE=prod
      - AUTH_SECRET_KEY=${AUTH_SECRET_KEY}
    volumes:
      - ./api-server/config:/app/config
    restart: unless-stopped

  web-app:
    build:
      context: ./web-app
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - api-server
    restart: unless-stopped

  admin-app:
    build:
      context: ./admin-app
      dockerfile: Dockerfile
    ports:
      - "3001:80"
    depends_on:
      - api-server
    restart: unless-stopped
```

### api-server/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"

COPY app/ ./app/
COPY config/ ./config/
COPY gunicorn.conf.py ./
COPY scripts/ ./scripts/

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

### web-app/Dockerfile & admin-app/Dockerfile

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Nginx 配置要点：**
- SPA 路由回退：`try_files $uri $uri/ /index.html`
- API 代理：`/api/` 路径代理到 `api-server:8000`
- 静态资源缓存：JS/CSS 文件 `max-age=1y`（基于内容哈希）

## Testing Strategy

### api-server

| 维度 | 选择 |
|------|------|
| 框架 | pytest + pytest-asyncio |
| 测试位置 | `api-server/tests/` |
| 测试类型 | 单元测试 + API 集成测试 |
| 覆盖率目标 | 核心模块 ≥ 80% |
| 运行方式 | `cd api-server && pytest tests/ -v` |

**测试分层：**
- 单元测试：配置加载、工具函数、Pydantic 模型校验
- 集成测试：使用 `httpx.AsyncClient` 对 FastAPI 应用做端到端 API 测试
- 安全测试：CORS 配置、安全头、输入校验、限流
- 认证测试：登录/登出/刷新 Token 流程、Token 过期、无效 Token 拒绝
- conftest.py 提供 `async_client` fixture

**安全测试示例：**

```python
async def test_security_headers_present(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "strict-transport-security" in response.headers

async def test_cors_blocks_unknown_origin(async_client):
    response = await async_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" not in response.headers

async def test_input_validation_rejects_invalid(async_client):
    response = await async_client.post(
        "/api/v1/example",
        json={"invalid_field": "value"},
    )
    assert response.status_code == 422
```

### web-app & admin-app

| 维度 | 选择 |
|------|------|
| 框架 | Vitest + React Testing Library |
| 测试位置 | 组件同目录 `.test.tsx` 或 `__tests__/` |
| 测试类型 | 单元测试 + 组件测试 |
| 覆盖率目标 | 工具函数 ≥ 80%，组件 ≥ 60% |
| 运行方式 | `cd web-app && pnpm test` |

**测试分层：**
- 单元测试：工具函数、API client、Hooks
- 组件测试：Layout、页面组件渲染验证、三态（loading/error/empty）验证
- 无障碍测试：验证关键组件的 ARIA 属性和键盘可达性

**组件测试示例：**

```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Result, Button } from "@arco-design/web-react";

describe("Error Result", () => {
  it("renders error message and retry button", () => {
    const onRetry = vi.fn();
    render(
      <Result
        status="error"
        title="加载失败"
        extra={<Button type="primary" onClick={onRetry}>重试</Button>}
      />,
    );

    expect(screen.getByText("加载失败")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /重试/i })).toBeInTheDocument();
  });
});
```

## Boundaries

### Always do

- 运行测试后再提交代码
- 所有配置项从 `application.yml` 读取，不硬编码
- API 响应使用统一格式 `{ code, message, data }`
- 前端 API 调用统一通过 `api/client.ts` 的 Axios 实例
- Python 代码通过 Ruff 检查，TypeScript 代码通过 ESLint 检查
- 新增 API 端点需同步更新类型定义
- 遵循各子项目的目录结构约定
- **所有 API 端点输入必须通过 Pydantic 模型校验**
- **API 响应必须包含安全响应头**
- **CORS origins 从配置文件读取，不使用通配符 `*`**
- **前端组件必须处理 loading / error / empty 三态（使用 Arco Skeleton/Result/Empty）**
- **列表端点必须分页**
- **所有 I/O 操作使用 async**
- **后台 API 端点需要认证（/api/v1/admin/ 下的受保护路由）**
- **Token 存储在内存中，不使用 localStorage**

### Ask first

- 添加新的 Python/Node.js 依赖
- 修改 `application.yml` 的配置结构
- 更改 API 响应格式
- 修改多进程部署配置（worker 数量、worker_class）
- 添加数据库相关模块
- 修改 monorepo 工作区结构
- **添加新的认证流程或修改认证逻辑**
- **修改 CORS 配置**
- **修改限流策略**
- **添加文件上传处理**

### Never do

- 在代码中硬编码配置值（端口、主机名、密钥等）
- 在 `application.yml` 中存储敏感信息
- 跳过测试直接提交
- 在前端代码中直接使用 `fetch` 而非统一的 Axios 实例
- 在 api-server 中引入同步阻塞调用
- 删除健康检查端点
- **自建 Arco Design 已有的基础组件（Layout/Button/Form/Table 等）**
- **提交敏感信息到版本控制（API Key、密码、Token）**
- **在日志中记录敏感数据（密码、Token）**
- **信任客户端校验作为安全边界**
- **禁用安全响应头**
- **在前端使用 `innerHTML` 或 `eval()` 渲染用户数据**
- **向客户端暴露堆栈跟踪或内部错误细节**
- **API 端点返回无分页的全量数据**
- **将 Token 存储在 localStorage 中**

## Success Criteria

- [ ] `tech-blazing-core-scaffold/` 目录结构完整，三个子项目均可独立运行
- [ ] `cd api-server && uvicorn app.main:app --reload` 可启动 API 服务，访问 `http://localhost:8000/docs` 看到 Swagger 文档
- [ ] `cd api-server && gunicorn app.main:app -c gunicorn.conf.py` 可多进程启动
- [ ] `application.yml` 可被正确加载，支持 `application-dev.yml` / `application-prod.yml` 环境覆盖
- [ ] API 健康检查端点 `/api/v1/web/health` 和 `/api/v1/admin/health` 均可正常返回
- [ ] 后台认证端点 `/api/v1/admin/auth/login` 可正常登录并返回 JWT Token
- [ ] 后台受保护端点在无 Token 时返回 401，携带有效 Token 时正常返回
- [ ] admin-app 登录页可完成登录流程，登录后可访问 Dashboard
- [ ] admin-app Token 过期后自动刷新，刷新失败跳转登录页
- [ ] `cd web-app && pnpm dev` 可启动前台开发服务器，页面可正常访问
- [ ] `cd admin-app && pnpm dev` 可启动后台开发服务器，页面可正常访问
- [ ] 前端页面可成功调用 API 健康检查端点并展示结果
- [ ] `cd api-server && pytest tests/ -v` 全部通过
- [ ] `cd web-app && pnpm test` 全部通过
- [ ] `cd admin-app && pnpm test` 全部通过
- [ ] `cd api-server && ruff check .` 无错误
- [ ] `cd web-app && pnpm lint` 无错误
- [ ] `cd admin-app && pnpm lint` 无错误
- [ ] API 响应包含安全响应头（X-Content-Type-Options、X-Frame-Options、HSTS 等）
- [ ] CORS 仅允许配置文件中声明的域名
- [ ] API 限流生效（超限返回 429）
- [ ] 前端所有数据展示组件均处理 loading / error / empty 三态（使用 Arco Skeleton/Result/Empty）
- [ ] 前端页面在 320px / 768px / 1024px / 1440px 断点下布局正常（使用 Arco Grid 响应式）
- [ ] API 响应时间 p95 < 200ms（健康检查端点）
- [ ] 前端 JS 初始包体积 < 200KB (gzip)
- [ ] 前端页面使用 Arco Design 组件体系，无自建基础组件
- [ ] Arco Design 主题 Token 可通过 `arco-theme.css` 覆盖
- [ ] `docker-compose up` 可一键启动全部三个子项目
- [ ] admin-app Token 存储在内存中，不使用 localStorage

## Open Questions

（全部已解决）

## Resolved Decisions

| # | 问题 | 决策 | 影响范围 |
|---|------|------|----------|
| 1 | 前台和后台是否需要不同的 API 路径？ | **是** — `/api/v1/web/` vs `/api/v1/admin/` | api-server 路由结构、前端 API client |
| 2 | 是否需要 Docker 配置？ | **是** — docker-compose.yml + 各子项目 Dockerfile | 项目结构、部署方式 |
| 3 | 是否需要 CI/CD 配置？ | **否** | 无 |
| 4 | 后台登录页是否预置认证逻辑？ | **是** — JWT 认证完整流程 | api-server auth 模块、admin-app 登录页 |
| 5 | API 版本管理策略？ | **v1 满足** — 保持当前设计 | 无变更 |
| 6 | 前端是否需要引入状态管理库？ | **否** — 保持自定义 Hook + Axios，后续按需引入 | 状态管理策略表 |
| 7 | API 限流存储方式？ | **内存存储** — 单机模式，后续按需引入 Redis | slowapi 配置 |
| 8 | Arco Design 主题定制方式？ | **CSS 变量覆盖** — 不使用 DesignLab | arco-theme.css |
