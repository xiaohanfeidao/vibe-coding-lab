# Trae 实战示例：搭建 FastAPI 脚手架

> 日期：2026-05-03
> 定位：通过一个完整的脚手架搭建案例，展示 Trae + agent-skills 体系的端到端实战流程
> 适用环境：Trae IDE + agent-skills 仓库已 clone 到本地

---

## 目录

1. [场景描述](#场景描述)
2. [模式选择](#模式选择)
3. [阶段 1：DEFINE — 用 spec-driven-development 明确边界](#阶段-1define--用-spec-driven-development-明确边界)
4. [阶段 2：PLAN — 用 planning-and-task-breakdown 拆任务](#阶段-2plan--用-planning-and-task-breakdown-拆任务)
5. [阶段 3：BUILD — 用 SOLO Coder 自动化实现](#阶段-3build--用-solo-coder-自动化实现)
6. [阶段 4：REVIEW — 多智能体并行审查](#阶段-4review--多智能体并行审查)
7. [脚手架产出物设计参考](#脚手架产出物设计参考)
8. [关键技能映射表](#关键技能映射表)
9. [完整操作清单（复制执行）](#完整操作清单复制执行)
10. [总结](#总结)

---

## 场景描述

```
需求：搭建一套 Python 后端 API 开发脚手架，后续所有新项目基于此模板快速启动

技术栈：    Python 3.11+ / FastAPI / SQLAlchemy 2.0（async） / MySQL 8.0
核心要求：
  ① 配置用 application.yml（不是 .env），支持多环境（dev/prod）
  ② 后台 worker 支持多进程处理（gunicorn + uvicorn workers）
  ③ MySQL 连接池管理（SQLAlchemy pool_size / max_overflow / pool_recycle）
  ④ 产出一个开箱即用的 scaffold 模板，可直接复制到新项目使用
```

---

## 模式选择

| 维度 | 判断 |
|------|------|
| 场景定性 | 一次性工程，多文件产出，从零到完整交付 |
| 决策 | **用 SOLO Coder 模式为主，Chat 模式为辅** |
| 原因 | 自动规划 + 多任务并行 + 一站式交付，效率最高 |

> **完整需求用 SOLO Coder，讨论/审查用 Chat 模式**（详见 [trae.md](../trae.md) 第 3 章）

---

## 阶段 1：DEFINE — 用 spec-driven-development 明确边界

### 操作

```
你对 Trae 说：

"读 skills/spec-driven-development/SKILL.md，为 FastAPI 脚手架项目写 SPEC.md。

核心要求：
1. 配置用 application.yml（不是 .env），支持多环境
2. 后台 worker 支持多进程处理（gunicorn/uvicorn workers）
3. MySQL 连接池管理（SQLAlchemy 连接池配置 + 可能用 asyncmy）
4. 产出一个开箱即用的 scaffold 模板

技术栈：Python 3.11+ / FastAPI / SQLAlchemy 2.0（async） / MySQL 8.0 / PyYAML"
```

### 为什么这一步不能跳过

- 脚手架"不做什么"比"做什么"更重要——scope creep 是脚手架最常见的失败模式
- AI 默认会按自己的理解自由发挥，产出的结构可能和你的习惯不一致
- SPEC.md 是后续所有阶段的契约文档，没有它就没有验证标准

### Agent 会自动做的事

1. 列出假设并请你确认（如："项目名是什么？""需要 Docker 吗？""需要 Alembic migrations 吗？"）
2. 你确认假设后，Agent 撰写 SPEC.md
3. SPEC.md 包含：目标、命令、项目结构、代码风格、测试策略、边界规则 6 大部分
4. 你 review SPEC.md 并确认

### 产出物

```
SPEC.md — 脚手架开发的契约文档，涵盖所有 6 大部分
```

---

## 阶段 2：PLAN — 用 planning-and-task-breakdown 拆任务

### 操作

```
你对 Trae 说：

"读 skills/planning-and-task-breakdown/SKILL.md，按 SPEC.md 拆可执行任务"
```

### Agent 会自动做的事

1. 分析 SPEC.md 中的功能模块
2. 将每个模块拆成原子化的可执行任务
3. 标注任务间依赖关系
4. 输出 `tasks/plan.md`（任务规划）和 `tasks/todo.md`（执行跟踪）

### 任务拆分示例

```
tasks/
├── 01_project_structure      项目目录结构 + pyproject.toml
├── 02_config_loader          application.yml 加载器（支持多环境）
├── 03_database               SQLAlchemy async engine + 连接池配置
├── 04_base_crud              通用 CRUD 基类
├── 05_middleware             异常处理 + 请求日志 + CORS 中间件
├── 06_worker                 多进程 worker 启动脚本
├── 07_health_check           健康检查 + readyz/livez 端点
├── 08_example_module         示例用户模块（CRUD + API）
├── 09_docker_compose         Docker Compose（MySQL + App）
└── 10_tests                  测试基础设施 + 示例测试
```

### 产出物

```
tasks/
├── plan.md     ← 任务规划（含依赖关系）
└── todo.md     ← 执行跟踪（状态管理）
```

---

## 阶段 3：BUILD — 用 SOLO Coder 自动化实现

### 前提

- AGENTS.md 已配置好核心规则（spec first、TDD、review before merge）
- 3 个自定义智能体已创建（code-reviewer、security-auditor、test-engineer）

### 操作

**切换到 SOLO 模式，一句话交付：**

```
你："按 tasks/ 任务列表实现全部模块，遵守以下规则：
     → 所有函数用 async def
     → 数据库操作用 SQLAlchemy 2.0 async session
     → 连接池 pool_size=20, max_overflow=40, pool_recycle=3600
     → application.yml 分 default/profile/dev/prod
     → 多进程通过 gunicorn + uvicorn workers 启动
     → 所有配置项从 application.yml 读取，不留任何硬编码"
```

### SOLO Coder 自动做的事

```
┌── 创建完整项目目录结构
├── config/application.yml 加载逻辑（PyYAML + Pydantic settings）
├── db/ 连接池配置（SQLAlchemy async engine factory）
├── worker 启动脚本（gunicorn.conf.py）
├── 健康检查端点
├── 示例 CRUD 模块
├── Docker Compose 配置
├── 单元测试
└── Diff 展示 → 你审查
```

### 你的角色

| 你做的事 | 不需要做的事 |
|----------|-------------|
| 审查 Diff 视图 | 不用手写代码 |
| 接受满意的文件 | 不用手动拆分任务 |
| 要求修改不满意的文件 | 不用逐个指挥每一步 |
| 全部审查完毕后确认 | |

---

## 阶段 4：REVIEW — 多智能体并行审查

### 操作（回到 Chat 模式，三条消息可并行发送）

```
你对 Trae 说：

(消息 1) "@code-reviewer 审查全部 scaffold 代码，重点检查架构维度"

(消息 2) "@security-auditor 检查配置管理和数据库连接安全"

(消息 3) "@test-engineer 评估测试覆盖是否达到金字塔标准"
```

### 三个智能体并行工作

```
@code-reviewer         @security-auditor       @test-engineer
─────────────────     ──────────────────      ───────────────
五维度审查：          安全审计：              测试评估：
├── 正确性            ├── 配置安全             ├── 单元测试覆盖
├── 可读性            ├── 连接池安全           ├── 集成测试覆盖
├── 架构              ├── 密钥管理             ├── 边界条件
├── 安全性            ├── SQL 注入防护         └── 测试质量
└── 性能              └── 依赖审计

     ↓                     ↓                       ↓
     └─────────────────────┼───────────────────────┘
                           ↓
                    汇总三份报告
                           ↓
                    你决定是否需要修正
```

### 收到审查报告后的处理

```
你对 Trae 说：

"根据三份审查报告的 Critical 和 Important 问题逐一修复"
```

修复完成后可再次发送审查请求验证。

---

## 脚手架产出物设计参考

以下是你验收时的核心检查点，可在 SOLO Coder 执行完成后逐项核对。

### 1. 项目结构

```
fastapi-scaffold/
├── app/
│   ├── main.py                 # FastAPI 应用工厂
│   ├── config/
│   │   ├── __init__.py
│   │   ├── loader.py           # application.yml 加载器
│   │   └── settings.py         # Pydantic settings 模型
│   ├── db/
│   │   ├── __init__.py
│   │   ├── engine.py           # async engine factory + 连接池
│   │   ├── session.py          # async session 依赖注入
│   │   └── base.py             # declarative base
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py       # 全局异常定义
│   │   ├── middleware.py       # 中间件（CORS/日志/限流）
│   │   └── response.py         # 统一响应格式
│   ├── modules/
│   │   ├── __init__.py
│   │   └── user/               # 示例模块
│   │       ├── __init__.py
│   │       ├── model.py        # SQLAlchemy ORM 模型
│   │       ├── schema.py       # Pydantic 请求/响应模型
│   │       ├── repository.py   # 数据访问层
│   │       └── router.py       # API 路由
│   └── utils/
│       ├── __init__.py
│       └── pagination.py       # 通用分页
├── config/
│   ├── application.yml         # 默认配置
│   ├── application-dev.yml     # 开发环境
│   └── application-prod.yml    # 生产环境
├── migrations/                 # Alembic 数据库迁移
├── tests/
│   ├── conftest.py             # pytest fixtures（测试 DB、client）
│   └── test_user.py            # 示例测试
├── scripts/
│   └── start.sh                # 多进程启动脚本
├── gunicorn.conf.py            # Gunicorn 配置
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env                         # 仅存放敏感信息，不是核心配置
```

### 2. application.yml 设计（核心里程碑）

```yaml
# config/application.yml — 默认配置
app:
  name: fastapi-scaffold
  version: "1.0.0"
  debug: false

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4                       # ★ 多进程 worker 数
  worker_class: "uvicorn.workers.UvicornWorker"

database:
  driver: "mysql+asyncmy"
  host: "${DB_HOST:localhost}"     # 支持环境变量占位
  port: 3306
  user: "${DB_USER:root}"
  password: "${DB_PASSWORD:}"
  name: "${DB_NAME:scaffold}"
  pool:                            # ★ 连接池配置
    size: 20                       # 常驻连接数
    max_overflow: 40               # 额外可创建连接数
    recycle: 3600                  # 连接回收时间（秒）
    timeout: 30                    # 获取连接超时（秒）
    pre_ping: true                 # 连接前 ping 检测

logging:
  level: INFO
  format: json                     # 结构化日志，便于采集
```

### 3. 连接池管理（关键代码）

```python
# app/db/engine.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.config.settings import get_settings

def create_engine() -> AsyncEngine:
    settings = get_settings()
    url = (
        f"{settings.db.driver}://"
        f"{settings.db.user}:{settings.db.password}"
        f"@{settings.db.host}:{settings.db.port}/{settings.db.name}"
    )
    return create_async_engine(
        url,
        pool_size=settings.db.pool.size,
        max_overflow=settings.db.pool.max_overflow,
        pool_recycle=settings.db.pool.recycle,
        pool_timeout=settings.db.pool.timeout,
        pool_pre_ping=settings.db.pool.pre_ping,
        echo=settings.app.debug,
    )
```

### 4. 多进程启动

```python
# gunicorn.conf.py
import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", "4"))      # ★ 多进程
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
```

---

## 关键技能映射表

| 你要的东西 | 对应技能 | 为什么 |
|-----------|----------|--------|
| 明确需求边界 | `spec-driven-development` | 确定 scaffold 不做什么比做什么更重要 |
| 项目结构设计 | `api-and-interface-design` | 模块分层、接口契约、分层架构 |
| 编码实现 | `test-driven-development` | scaffold 必须自带测试，否则不可信 |
| 增量开发 | `incremental-implementation` | 按薄切片逐步交付，步步可验证 |
| 多进程 + 连接池 | `performance-optimization` | 先理解负载再定 workers 数和 pool_size |
| 安全检查 | `security-and-hardening` | 密码不入配置、SQL 参数化、密钥管理 |
| 最终审查 | `@code-reviewer` | 五维度质量门（正确性/可读性/架构/安全/性能） |

> 注意：架构设计（如模块如何分层、接口如何建模）需要你作为专家介入决策。详见 [trae.md](../trae.md) 第 5 章"什么是 Command（命令层）？"中关于架构设计需要人为干预的讨论。

---

## 完整操作清单（复制执行）

以下每条消息都可以直接复制到 Trae 对话中使用：

### 步骤 1（Chat 模式）

```
"读 skills/spec-driven-development/SKILL.md，
 为 FastAPI 脚手架项目写 SPEC.md。

 核心要求：
 1. 配置用 application.yml（不是 .env），支持多环境
 2. 后台 worker 支持多进程处理（gunicorn/uvicorn workers）
 3. MySQL 连接池管理（SQLAlchemy 连接池配置 + 异步驱动）
 4. 产出一个开箱即用的 scaffold 模板

 技术栈：Python 3.11+ / FastAPI / SQLAlchemy 2.0（async） / MySQL 8.0 / PyYAML"
```

→ Agent 列假设 → 你确认 → SPEC.md 产出 → 你 review

### 步骤 2（Chat 模式）

```
"读 skills/planning-and-task-breakdown/SKILL.md，按 SPEC.md 拆可执行任务"
```

→ tasks/ 产出 → 你确认任务列表

### 步骤 3（切换到 SOLO 模式）

```
"按 tasks/ 任务列表实现全部模块，遵守以下规则：
 → 所有函数用 async def
 → 数据库操作用 SQLAlchemy 2.0 async session
 → 连接池 pool_size=20, max_overflow=40, pool_recycle=3600
 → application.yml 分 default/profile/dev/prod，支持 ${ENV:default} 占位
 → 多进程通过 gunicorn + uvicorn.workers.UvicornWorker 启动
 → 所有配置项从 application.yml 读取，不留任何硬编码
 → 健康检查包含 /health、/readyz、/livez 端点"
```

→ SOLO Coder 自动编码、自动测试、自动提交
→ Diff 展示 → 你逐文件审查 → 接受/拒绝

### 步骤 4（回到 Chat 模式，三条消息可并行发送）

```
"@code-reviewer 审查全部 scaffold 代码，重点检查架构维度"
```

```
"@security-auditor 检查配置管理和数据库连接安全"
```

```
"@test-engineer 评估测试覆盖是否达到金字塔标准"
```

→ 等待并行审查报告 → 根据 Critical/Important 问题修正

### 步骤 5（Chat 模式，修正问题后）

```
"根据审查报告的 Critical 和 Important 问题逐一修复，修复完成后重新跑测试验证"
```

→ 脚手架最终交付

---

## 总结

```
┌─────────────────────────────────────────────────────────┐
│  本示例展示了 Trae + agent-skills 体系的核心价值：       │
│                                                         │
│  ✅ Spec First — 先定义边界，再用代码填充                │
│  ✅ Plan Then Build — 先拆任务，再 SOLO Coder 自动化     │
│  ✅ Multi-Agent Review — 三智能体并行审查，质量有保障    │
│  ✅ 全流程可复制 — 以上流程适用于任何"从零搭建"的场景     │
│                                                         │
│  你只管定义和审查，代码交给人机协作体系完成。            │
└─────────────────────────────────────────────────────────┘
```

---

> **相关文件**：
> - [trae.md](../trae.md) — Trae IDE 中的 agent-skills 完整操作手册
> - [PROJECT_DOCS.md](../PROJECT_DOCS.md) — agent-skills 项目全部文件说明
> - [docs/trae-skill-concept.md](./trae-skill-concept.md) — agent-skills 的 Skill 与 Trae 的 Skill 概念对齐
