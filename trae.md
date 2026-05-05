# trae.md

> 生成日期：2026-05-02
> 基于：agent-skills 项目 + Trae IDE 官方文档 (docs.trae.cn)
> 定位：将 agent-skills 工程体系完整适配到 Trae IDE 环境中的操作手册

---

## 目录

1. [为什么需要 trae.md](#为什么需要-traemd)
2. [Trae IDE 环境速览](#trae-ide-环境速览)
3. [Chat 模式 vs SOLO Coder — 在 Trae 中应该用哪个模式？](#chat-模式-vs-solo-coder--在-trae-中应该用哪个模式)
4. [agent-skills 到 Trae 的体系映射](#agent-skills-到-trae-的体系映射)
5. [什么是 Command（命令层）？](#什么是-command命令层)
6. [在 Trae 中使用技能的三种方式](#在-trae-中使用技能的三种方式)
7. [完整开发流水线（两种模式对照）](#完整开发流水线两种模式对照)
8. [21 个技能在 Trae 中的详细使用指南](#21-个技能在-trae-中的详细使用指南)
9. [在 Trae 中搭建自定义智能体（Persona 替代方案）](#在-trae-中搭建自定义智能体)
10. [新项目 AGENTS.md 模板](#新项目-agentsmd-模板)
11. [快速参考卡片](#快速参考卡片)

---

## 为什么需要 trae.md

agent-skills 项目原生面向 **Claude Code** 设计，包含大量 Claude 专属的机制：

| 原始机制 | 问题 |
|----------|------|
| `.claude/commands/` 斜杠命令 | Trae 不认识 `/spec`、`/plan` 等命令 |
| `hooks/` 会话钩子 | Trae 的钩子体系完全不同，不可复用 |
| `plugin.json` 插件市场 | Trae 没有这套插件安装机制 |
| Claude subagent 调用方式 | Trae 使用自定义智能体体系，接口不同 |

**trae.md 的作用**：将 agent-skills 的完整方法论完整移植到 Trae IDE，用 Trae 原生支持的方式（AGENTS.md 自动加载 + 对话指令 + Skill 工具 + 自定义智能体）实现同等的工程化开发体验。

---

## Trae IDE 环境速览

### Trae 的核心能力

| 能力 | 说明 |
|------|------|
| **AGENTS.md 自动加载** | 项目根目录的 `AGENTS.md` 会被自动加载为 workspace rules，Agent 始终可见 |
| **Skill 工具** | Agent 可以通过 Skill 工具读取并执行 `skills/<name>/SKILL.md` 中的工作流 |
| **自定义智能体** | 在输入框输入 `@` 可创建/调用自定义智能体，配置提示词、MCP Server、内置工具 |
| **SOLO Coder** | AI 主导模式，自动规划并执行从需求到代码的全流程，可调用自定义智能体 |
| **内置工具** | 阅读（文件检索查看）、文件系统（增删改查）、终端（运行命令）、联网搜索、预览 |
| **多模型** | 内置 Doubao-Seed、DeepSeek、Kimi、GLM、Qwen 等模型，支持自定义模型 |
| **Diff 视图** | 代码变更可视化对比，支持单处/单文件/全部接受或拒绝 |
| **版本回退** | 支持回退至最近 10 轮会话内的版本 |
| **历史会话管理** | 查看、跳转、删除历史对话 |
| **MCP Server** | 支持为智能体配置 MCP Server 扩展工具能力 |

### Trae 的文件感知机制

```
项目根目录/
├── AGENTS.md          ← Trae 自动加载（最高优先级）
├── CLAUDE.md          ← Trae 也会识别（次优先级）
├── skills/             ← 通过 Skill 工具或文件读取按需加载
│   ├── spec-driven-development/SKILL.md
│   ├── test-driven-development/SKILL.md
│   └── ...
├── references/         ← 按需读取
└── docs/               ← 参考文档
```

---

## Chat 模式 vs SOLO Coder — 在 Trae 中应该用哪个模式？

**这是整个 trae.md 最重要的章节。** 选错模式比用错技能浪费 10 倍的时间。

### Trae 的两种工作模式

```
Trae IDE
├── Chat 模式（你现在和我对话就在这个模式）
│    你一句我一句，Agent 按你说的逐步执行
│    角色：你是驾驶员，Agent 是副驾
│    适合：讨论、审查、小改动、学习探索
│
└── SOLO Coder 模式（左上角切换按钮）
    AI 主导，自动规划→拆分→执行→审查
    角色：你是审查者，Agent 是全自动施工队
    适合：完整需求的一站式交付
```

### 决策路由表

| 你的场景 | 用什么模式 | 为什么 |
|----------|-----------|--------|
| **下发完整需求，从 0 到 1 交付** | **SOLO Coder** | 自动规划 + 多任务并行 + 一站式交付。1 条消息搞定，不用你指挥每一步 |
| 讨论架构 / 方案 / 想法 | Chat 模式 | 需要你来我往的深度对话 |
| 审查已有代码 | Chat 模式 + @自定义智能体 | 精确控制审查范围 |
| 修复单个 bug | Chat 模式 | 目标单一，不需要编排 |
| 代码简化 / 重构 | Chat 模式 | 需要深入理解上下文和意图 |
| 学习 / 分析代码库 | Chat 模式 | 需要解释和讨论 |

### 两种模式如何配合 agent-skills 体系

```
                     SOLO Coder 模式              Chat 模式
                     ──────────────              ─────────
AGENTS.md 规则       自动生效，全程约束            自动生效，全程约束
自定义智能体          可在执行中自动调用            你手动 @名称 调用
Skill 文件            无需手动引用                 你手动"读 skills/..."调度
你的角色              审查者（看 Diff，接受/拒绝）   驾驶员（每一步都指挥）
操作量                1 条消息                     4-6 条消息
```

### 核心结论

> **完整需求 → SOLO Coder。讨论/审查/修复 → Chat 模式。**
>
> AGENTS.md 的规则和自定义智能体的提示词在两种模式下都会生效。你只需配一次，永久受益。

---

## agent-skills 到 Trae 的体系映射

```
agent-skills 原始体系              Trae 适配方案
─────────────────────────────────────────────────────
Skills（怎么做）          →    保持不变。Chat 模式手动引用，SOLO Coder 由 AGENTS.md 规则间接生效
Personas（谁来做）        →    自定义智能体（@code-reviewer 等）。Chat 模式手动调用，SOLO Coder 自动调用
Commands（何时做）        →    Chat 模式：对话描述意图 + Skill 工具。SOLO Coder：输入需求一句话搞定
Hooks（自动化钩子）       →    AGENTS.md 规则（永久生效，两种模式都适用）
plugin.json               →    不需要（直接文件系统读取）
marketplace.json          →    不需要（直接 git clone 使用）
```

### 核心原则

> **一次配置，两种模式受益。** AGENTS.md 固化开发规范，自定义智能体固化审查能力。日常讨论和小改动用 Chat 模式，完整需求交付直接丢给 SOLO Coder。

---

## 在 Trae 中使用技能的三种方式

> **适用模式标注**：方式一、二在 Chat 和 SOLO Coder 两种模式下都适用。方式三主要在 Chat 模式审查阶段使用。

### 方式一：对话直接指令（Chat 模式最灵活）

直接在对话中描述意图，Agent 自动读取对应 SKILL.md：

```
你：我要做一个用户登录功能，先读 skills/spec-driven-development/SKILL.md，按它的流程写需求文档

你：代码写好了，读 skills/code-review-and-quality/SKILL.md 帮我审查

你：有个 bug，读 skills/debugging-and-error-recovery/SKILL.md，按五步法排查
```

### 方式二：写入 AGENTS.md 固化规则（推荐项目长期使用）

把最核心的 3-5 个技能规则写入项目 `AGENTS.md`，每次打开项目自动生效：

```markdown
# AGENTS.md

## 核心规则
1. 写代码前必须先写 SPEC.md，经我确认后再编码
2. 严格遵循 Red-Green-Refactor 的 TDD 循环
3. 每次变更后从正确性、可读性、架构、安全、性能 5 维度自查
```

Agent 会在每次对话中自动遵守这些规则，无需每次重复说明。

### 方式三：自定义智能体（推荐多 Agent 协同场景）

在 Trae 中创建 3 个自定义智能体，对应 agent-skills 的 3 个 Persona：

| 自定义智能体 | 角色 | 何时使用 |
|-------------|------|----------|
| **code-reviewer** | 资深代码审查员 | 合并前审查代码 |
| **security-auditor** | 安全审计员 | 安全检查 |
| **test-engineer** | 测试工程师 | 测试策略评估 |

创建后在对话中输入 `@code-reviewer` 即可调用。详见[搭建自定义智能体章节](#在-trae-中搭建自定义智能体)。

---

## 完整开发流水线（两种模式对照）

agent-skills 的六阶段方法论在 Trae 中有**两套完全不同的落地方式**。选对方式，效率差 10 倍。

```
  DEFINE           PLAN            BUILD           VERIFY          REVIEW           SHIP
 ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐
 │ 想法  │ ───▶  │ 规划  │ ───▶  │ 编码  │ ───▶  │ 验证  │ ───▶  │ 审查  │ ───▶  │ 发布  │
 │ 打磨  │       │ 拆解  │       │ 实现  │       │ 调试  │       │ 质控  │       │ 上线  │
 └──────┘       └──────┘       └──────┘       └──────┘       └──────┘       └──────┘
```

### 方式一：SOLO Coder 自动化（推荐，完整需求场景）

**前提**：AGENTS.md 已配置好规则，3 个自定义智能体已创建。

```
操作步骤：
─────────────────────────────────────────────────────
第 1 步：左上角切换到 SOLO 模式
第 2 步：输入需求，一句话即可
    "做一个团队内部的代码片段分享工具，支持 Markdown 语法高亮，
     可以按标签分类和全文搜索，支持收藏。用 React + TypeScript + SQLite。"

第 3 步：等 SOLO Coder 自动完成：
    ┌─── 自动分析需求，拆分任务（左侧任务面板可见）
    ├─── 自动多任务并行推进
    ├─── 自动遵守 AGENTS.md 中的规则（spec first、TDD、review before merge）
    ├─── 必要时自动调用 @code-reviewer / @security-auditor / @test-engineer
    └─── 完成后展示 Diff，你逐文件审查

第 4 步：在 Diff 视图中接受/拒绝变更
    - 全部接受：点击"全部接受"
    - 部分接受：逐个文件审查，接受满意的，要求修改不满意的
    - 单处接受：鼠标悬浮代码变更处，Alt+Y（Windows）/ Control+Y（Mac）接受
```

**你只需要做**：
1. 输入 1 条需求消息
2. 审查 Diff
3. 接受或拒绝

**SOLO Coder 自动承担的角色**：

| 阶段 | SOLO Coder 自动做的事 |
|------|----------------------|
| DEFINE | 分析需求，如果需求模糊会追问你澄清 |
| PLAN | 自动拆分成可执行任务，显示在左侧任务面板 |
| BUILD | 自动编码，自动跑测试，自动提交 |
| VERIFY | 自动运行测试，失败自动修复 |
| REVIEW | 可选：自动调用配好的 @code-reviewer 等智能体 |
| SHIP | 生成变更摘要，等你最终确认 |

---

### 方式二：Chat 模式手动编排（讨论/审查/小改动场景）

**适用**：你已经有一个项目，需要做增量修改、审查代码、排查问题。

#### 阶段 1：DEFINE — 定义

```
你：我有一个想法：[描述]。读 skills/idea-refine/SKILL.md 帮我打磨

（想法清晰后）
你：读 skills/spec-driven-development/SKILL.md，为 [功能] 写 SPEC.md
```

Agent 会：列假设→你确认→写 SPEC.md→等你 review

#### 阶段 2：PLAN — 规划

```
你：SPEC.md 确认了，读 skills/planning-and-task-breakdown/SKILL.md 拆任务
```

Agent 会：拆任务 + 标注依赖 + 输出 tasks/plan.md + tasks/todo.md

#### 阶段 3：BUILD — 构建

```
你：读 skills/test-driven-development/SKILL.md 和 
   skills/incremental-implementation/SKILL.md，按 TDD + 增量切片开始实现
```

Agent 会：Red→Green→Refactor 循环，一次一个薄切片

#### 阶段 4：VERIFY — 验证

```
你：跑完整测试，有失败的读 skills/debugging-and-error-recovery/SKILL.md 按五步法排查
```

#### 阶段 5：REVIEW — 审查

```
你：@code-reviewer 审查本次变更
你：@security-auditor 审计安全
你：@test-engineer 检查测试覆盖
（三条可并行发送）
```

#### 阶段 6：SHIP — 发布

```
你：汇总三个审查报告，读 skills/shipping-and-launch/SKILL.md 做上线检查
```

---

### 两种方式对比总结

| | SOLO Coder | Chat 模式 |
|---|-----------|-----------|
| **操作消息数** | 1 条 | 4-6 条 |
| **你的角色** | 审查者 | 指挥员 |
| **适用场景** | 完整需求从 0 到 1 | 增量修改、审查、排查 |
| **Skill 引用** | 无需手动（AGENTS.md 规则自动约束） | 手动"读 skills/..." |
| **智能体调用** | SOLO Coder 自动调度 | 手动 @名称 调用 |
| **并行能力** | 原生多任务并行 | 可并行发送多条 @消息 |
| **学习曲线** | 低（一句话即可） | 中（需要熟悉 21 个技能名称） |

---

## 21 个技能在 Trae 中的详细使用指南

### DEFINE 阶段

#### idea-refine（想法打磨）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/idea-refine/SKILL.md` |
| **何时用** | 只有模糊想法，需要探索和具体化 |
| **你在 Trae 中怎么说** | "我有一个想法：[描述]，帮我打磨一下" |
| **配套文件** | `examples.md`（案例）、`frameworks.md`（方法论）、`refinement-criteria.md`（标准）、`scripts/idea-refine.sh` |
| **产出** | 结构化的想法提案 |

#### spec-driven-development（规格驱动开发）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/spec-driven-development/SKILL.md` |
| **何时用** | 启动新项目/新功能，且没有规格文档 |
| **你在 Trae 中怎么说** | "读 skills/spec-driven-development/SKILL.md，为 [功能名] 写 SPEC.md" |
| **流程** | SPECIFY（列假设+写文档）→ 人工审核 → PLAN → TASKS → IMPLEMENT |
| **产出** | `SPEC.md`（含目标、命令、结构、风格、测试、边界 6 部分） |

---

### PLAN 阶段

#### planning-and-task-breakdown（规划与任务拆分）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/planning-and-task-breakdown/SKILL.md` |
| **何时用** | 有 SPEC.md 后需要拆分执行任务 |
| **你在 Trae 中怎么说** | "读 skills/planning-and-task-breakdown/SKILL.md，按 SPEC.md 拆任务" |
| **产出** | `tasks/plan.md` + `tasks/todo.md` |

---

### BUILD 阶段

#### incremental-implementation（增量实现）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/incremental-implementation/SKILL.md` |
| **何时用** | 开始编码（涉及多文件时必用） |
| **你在 Trae 中怎么说** | "读 skills/incremental-implementation/SKILL.md，按薄切片方式实现第一个任务" |
| **核心原则** | 一次一个薄切片，实现→测试→验证→提交 |
| **产出** | 增量提交的代码 |

#### test-driven-development（测试驱动开发）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/test-driven-development/SKILL.md` |
| **何时用** | 写任何逻辑代码时 |
| **你在 Trae 中怎么说** | "按 TDD 方式写：[具体需求]，先写失败的测试" |
| **流程** | Red（写失败测试）→ Green（最小实现）→ Refactor（重构） |
| **比例** | 80% 单元 / 15% 集成 / 5% E2E |
| **产出** | 测试 + 实现代码 |

#### context-engineering（上下文工程）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/context-engineering/SKILL.md` |
| **何时用** | 新会话开始、切换任务、输出质量下降时 |
| **你在 Trae 中怎么说** | "重新加载上下文，读 skills/context-engineering/SKILL.md" |
| **要点** | 给 Agent 喂对的信息，而非更多的信息 |

#### source-driven-development（源码驱动开发）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/source-driven-development/SKILL.md` |
| **何时用** | 需要基于权威文档写代码（而非依赖 Agent 训练记忆） |
| **你在 Trae 中怎么说** | "读 skills/source-driven-development/SKILL.md，基于 [框架名] 官方文档写代码" |
| **要点** | 每个框架决策必须引用官方文档来源 |

#### frontend-ui-engineering（前端 UI 工程）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/frontend-ui-engineering/SKILL.md` |
| **何时用** | 构建/修改用户界面 |
| **你在 Trae 中怎么说** | "做 UI 部分，读 skills/frontend-ui-engineering/SKILL.md，遵守无障碍标准" |
| **要点** | 组件架构 + 设计系统 + 响应式 + WCAG 2.1 AA |

#### api-and-interface-design（API 与接口设计）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/api-and-interface-design/SKILL.md` |
| **何时用** | 设计 API、模块边界、公共接口 |
| **你在 Trae 中怎么说** | "设计 API，读 skills/api-and-interface-design/SKILL.md，按契约优先设计" |
| **要点** | 海勒姆定律、一版本规则、错误语义、边界校验 |

---

### VERIFY 阶段

#### browser-testing-with-devtools（浏览器 DevTools 测试）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/browser-testing-with-devtools/SKILL.md` |
| **何时用** | 构建/调试浏览器中运行的前端内容 |
| **你在 Trae 中怎么说** | "页面有问题，读 skills/browser-testing-with-devtools/SKILL.md，用 DevTools 排查" |
| **要点** | DOM 检查、控制台日志、网络追踪、性能分析（需配置 MCP Server） |

#### debugging-and-error-recovery（调试与错误恢复）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/debugging-and-error-recovery/SKILL.md` |
| **何时用** | 测试失败、构建出错、行为异常 |
| **你在 Trae 中怎么说** | "出错了，读 skills/debugging-and-error-recovery/SKILL.md，按五步法排查" |
| **流程** | 复现 → 定位 → 精简 → 修复 → 加固 |
| **规则** | 3 次失败修复后必须停下来重新分析 |

---

### REVIEW 阶段

#### code-review-and-quality（代码审查与质量）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/code-review-and-quality/SKILL.md` |
| **何时用** | 合并代码前 |
| **你在 Trae 中怎么说** | "审查代码，读 skills/code-review-and-quality/SKILL.md，做五维度审查" |
| **五维度** | 正确性 → 可读性 → 架构 → 安全性 → 性能 |
| **产出** | Critical / Important / Suggestion 分级报告 |

#### code-simplification（代码简化）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/code-simplification/SKILL.md` |
| **何时用** | 代码能跑但太复杂 |
| **你在 Trae 中怎么说** | "这段代码太复杂，读 skills/code-simplification/SKILL.md，简化但行为不变" |
| **原则** | 切斯特顿栅栏（先理解为什么）、500 行规则 |

#### security-and-hardening（安全与加固）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/security-and-hardening/SKILL.md` |
| **何时用** | 处理用户输入、认证、数据存储、外部集成 |
| **你在 Trae 中怎么说** | "检查安全，读 skills/security-and-hardening/SKILL.md，按 OWASP Top 10 审计" |
| **要点** | 三层边界系统、密钥管理、依赖审计 |

#### performance-optimization（性能优化）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/performance-optimization/SKILL.md` |
| **何时用** | 有性能要求或怀疑性能退化 |
| **你在 Trae 中怎么说** | "检查性能，读 skills/performance-optimization/SKILL.md，先测量再优化" |
| **原则** | 先测量再优化，不凭感觉"优化" |

---

### SHIP 阶段

#### git-workflow-and-versioning（Git 工作流）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/git-workflow-and-versioning/SKILL.md` |
| **何时用** | 始终生效（代码变更时自动适用） |
| **你在 Trae 中怎么说** | "读 skills/git-workflow-and-versioning/SKILL.md，检查提交规范" |
| **原则** | 主干开发、原子提交、约 100 行/变更 |

#### ci-cd-and-automation（CI/CD）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/ci-cd-and-automation/SKILL.md` |
| **何时用** | 设置/修改 CI/CD 流水线 |
| **你在 Trae 中怎么说** | "设置 CI，读 skills/ci-cd-and-automation/SKILL.md" |

#### deprecation-and-migration（废弃与迁移）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/deprecation-and-migration/SKILL.md` |
| **何时用** | 移除旧系统、迁移用户、下线功能 |
| **你在 Trae 中怎么说** | "要废弃 [功能名]，读 skills/deprecation-and-migration/SKILL.md" |

#### documentation-and-adrs（文档与 ADR）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/documentation-and-adrs/SKILL.md` |
| **何时用** | 做架构决策、变更 API、发布功能 |
| **你在 Trae 中怎么说** | "记录架构决策，读 skills/documentation-and-adrs/SKILL.md" |

#### shipping-and-launch（发布上线）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/shipping-and-launch/SKILL.md` |
| **何时用** | 准备部署到生产环境 |
| **你在 Trae 中怎么说** | "准备发布，读 skills/shipping-and-launch/SKILL.md，做上线检查" |
| **产出** | 发布决策 + 回滚方案 |

#### using-agent-skills（技能导航）

| 维度 | 内容 |
|------|------|
| **路径** | `skills/using-agent-skills/SKILL.md` |
| **何时用** | 不知道应该用哪个技能时 |
| **你在 Trae 中怎么说** | "读 skills/using-agent-skills/SKILL.md，帮我确定该用哪个技能" |
| **角色** | 元技能，所有技能的导航入口 |

---

## 在 Trae 中搭建自定义智能体

将 agent-skills 的 3 个 Persona 转化为 Trae 的自定义智能体。

### 智能体 1：code-reviewer（代码审查员）

**创建方式**：在 Trae 对话框输入 `@` → 点击「创建智能体」→ 选择「手动创建」

| 配置项 | 填写内容 |
|--------|----------|
| **名称** | code-reviewer |
| **提示词** | 见下方 |
| **英文标识名** | code-reviewer |
| **何时调用** | 当用户要求审查代码、检查 PR、评估代码质量时调用此智能体 |
| **可被其他智能体调用** | 开启 |
| **工具** | 阅读、文件系统、终端 |

**提示词（复制粘贴到 Trae 智能体配置中）**：

```
你是一位资深 Staff Engineer，负责进行全面的代码审查。你的审查标准是"Staff Engineer 会批准这个代码吗？"

## 审查框架

从以下五个维度评估每一次变更：

### 1. 正确性
- 代码是否按照规格/任务要求实现了功能？
- 边界情况是否处理了（null、空值、边界值、错误路径）？
- 测试是否真正验证了行为？测试的是否是正确的方面？
- 是否存在竞态条件、差一错误或状态不一致？

### 2. 可读性
- 其他工程师能否在不看解释的情况下理解代码？
- 命名是否描述性强且与项目规范一致？
- 控制流是否直观（没有深层嵌套逻辑）？
- 代码组织是否良好（相关代码分组、边界清晰）？

### 3. 架构
- 变更是否遵循现有模式，还是引入了新模式？
- 如果引入了新模式，是否有充分理由并说明了？
- 模块边界是否得到了维护？是否有循环依赖？
- 抽象层级是否合适（不过度工程化、也不过紧耦合）？

### 4. 安全性
- 用户输入是否在系统边界进行了验证和消毒？
- 密钥是否没有出现在代码、日志和版本控制中？
- 认证/授权是否在需要的地方进行了检查？
- 查询是否参数化了？输出是否编码了？

### 5. 性能
- 是否存在 N+1 查询模式？
- 是否存在无界循环或无约束的数据获取？
- 是否存在应该改成异步的同步操作？
- 列表端点是否缺少分页？

## 输出格式

每次审查输出：

## Review Summary
（3-5句话概述本次变更的目标和总体质量）

## Findings

### Critical（必须修复才能合并）
- [具体问题描述]

### Important（应该在合并前修复）
- [具体问题描述]

### Suggestion（改进建议）
- [具体改进建议]

## Overall Assessment
✅ Approve / ⚠️ Approve with Comments / ❌ Request Changes
```

---

### 智能体 2：security-auditor（安全审计员）

| 配置项 | 填写内容 |
|--------|----------|
| **名称** | security-auditor |
| **提示词** | 见下方 |
| **英文标识名** | security-auditor |
| **何时调用** | 当用户要求安全检查、安全审计、漏洞扫描时调用此智能体 |
| **可被其他智能体调用** | 开启 |
| **工具** | 阅读、文件系统、终端 |

**提示词**：

```
你是一位安全工程师，专注于代码安全审计和漏洞检测。

## 审查领域

### 1. 输入处理
- 检查是否存在 XSS 漏洞（未转义的用户输入渲染到 HTML）
- 检查是否存在 SQL/NoSQL 注入（拼接字符串构建查询）
- 检查是否存在命令注入（用户输入传给 shell）
- 验证所有外部输入是否经过了验证

### 2. 认证与授权
- 检查密码存储方式（必须使用哈希加盐，禁止明文）
- 检查会话管理（token 有效期、安全 flag、HttpOnly）
- 检查 CSRF 防护
- 检查权限检查是否在每个端点都执行

### 3. 数据保护
- 检查敏感数据是否加密存储
- 检查日志中是否包含敏感信息（密码、token、个人信息）
- 检查数据传输是否使用 HTTPS/TLS

### 4. 基础设施
- 检查安全头配置（CSP、HSTS、X-Frame-Options）
- 检查 CORS 配置是否过于宽松
- 检查依赖是否存在已知漏洞

### 5. 第三方集成
- 检查 API 密钥是否硬编码
- 检查第三方服务调用是否有超时和错误处理
- 检查文件上传是否有类型和大小限制

## 输出格式

## Security Audit Report

### Critical（必须立即修复）
- [漏洞描述 + 受影响代码位置 + 修复建议]

### High（发布前修复）
- [漏洞描述 + 受影响代码位置 + 修复建议]

### Medium（建议修复）
- [漏洞描述 + 受影响代码位置 + 修复建议]

### Low（改进建议）
- [改进建议]

## Overall Security Rating
🔴 Critical / 🟠 High Risk / 🟡 Medium / 🟢 Low Risk
```

---

### 智能体 3：test-engineer（测试工程师）

| 配置项 | 填写内容 |
|--------|----------|
| **名称** | test-engineer |
| **提示词** | 见下方 |
| **英文标识名** | test-engineer |
| **何时调用** | 当用户要求评估测试覆盖、补充测试、检查测试质量时调用此智能体 |
| **可被其他智能体调用** | 开启 |
| **工具** | 阅读、文件系统、终端 |

**提示词**：

```
你是一位 QA 测试工程师，专注于测试策略评估和测试质量保证。

## 工作框架

### Prove-It 模式
- 每个断言必须验证实际行为，不能基于假设
- "看起来应该没问题"不是有效的测试
- 边界条件和错误路径必须有对应的测试用例

### 测试金字塔检查
- 80% 单元测试（测试单个函数/组件）
- 15% 集成测试（测试模块间交互）
- 5% E2E 测试（测试完整用户流程）

### 测试质量评估
- 测试是否独立（不依赖执行顺序）？
- 测试是否可重复（多次运行结果一致）？
- 测试是否有意义的断言（不是 assert(true)）？
- 测试失败时错误信息是否清晰？

## 输出格式

## Test Coverage Report

### 已有测试覆盖
| 模块 | 测试文件 | 覆盖类型 | 质量评估 |
|------|---------|---------|---------|

### 缺失的测试
- [模块/功能名]：缺少 [测试类型] — 风险 [高/中/低]

### 测试质量改进
- [具体改进建议]

## Overall Test Health
✅ 健康 / ⚠️ 需要改进 / ❌ 严重缺失
```

---

### 使用自定义智能体

创建完成后，在对话中这样调用：

```
你：@code-reviewer 审查 src/auth/ 下的变更

你：@security-auditor 审计支付模块的安全性

你：@test-engineer 检查用户注册流程的测试覆盖
```

---

## 新项目 AGENTS.md 模板

当你基于 agent-skills + Trae 开始一个新项目时，将以下内容写入项目根目录的 `AGENTS.md`：

```markdown
# AGENTS.md

## 项目信息
- 项目名称：[项目名]
- 技术栈：[如 React + TypeScript + Node.js]
- 包管理器：[npm / pnpm / yarn]

## 命令

| 命令 | 说明 |
|------|------|
| [npm run dev] | 启动开发服务器 |
| [npm run build] | 生产构建 |
| [npm test] | 运行测试（含覆盖率） |
| [npm run lint] | 代码检查与自动修复 |
| [npm run format] | 代码格式化 |

## 核心开发流程

本项目采用分阶段工程化开发流程，AI Agent 必须严格遵守：

### 阶段 1：Spec First（需求先行）
- 写任何代码前，必须先创建 SPEC.md，明确目标、命令、结构、风格、测试策略、边界
- 列出所有假设并请我确认，不得默默填补模糊需求
- SPEC.md 经我 review 确认后才能进入编码阶段

### 阶段 2：Test Driven Development（测试驱动）
- 严格遵循 Red-Green-Refactor 循环
- 测试金字塔：80% 单元 / 15% 集成 / 5% E2E
- 严禁以任何理由跳过测试

### 阶段 3：Review Before Merge（质量审查）
- 每次变更后从 5 维度自查：正确性、可读性、架构、安全性、性能
- 单次变更控制在 ~100 行以内
- 问题按 Critical / Important / Suggestion 三级标注

## 自定义智能体

本项目配置了以下 Trae 自定义智能体，可在对话中通过 @名称 调用：

- **@code-reviewer** — 五维度代码审查
- **@security-auditor** — 安全漏洞审计
- **@test-engineer** — 测试策略与覆盖率评估

## 项目结构

```
src/              ← 源代码
  components/     ← UI 组件
  lib/            ← 工具函数
  pages/          ← 页面/路由
tests/            ← 测试文件
  unit/           ← 单元测试
  integration/    ← 集成测试
  e2e/            ← E2E 测试
docs/             ← 项目文档
```

## 边界规则

### Always
- 先写 spec 再写代码
- 先写测试再写实现
- 提交前自查代码质量
- 遵循项目现有的代码风格和模式

### Never
- 跳过 spec 直接写代码
- 忽略测试覆盖
- 提交密钥或敏感信息
- 引入未经讨论的重大架构变更

### Ask First
- 添加新的第三方依赖
- 修改数据库 schema
- 变更 CI/CD 配置
- 重写现有模块
```

---

## 快速参考卡片

### SOLO Coder 场景（完整需求从 0 到 1）

| 我想... | 操作 |
|---------|------|
| 实现完整需求 | 切换 SOLO 模式 → 输入需求一句话 → 等结果 → 审查 Diff |
| 并行多任务开发 | 在 SOLO Coder 中描述多个需求，自动并行推进 |

**前提**：AGENTS.md 已配置规则 + 3 个自定义智能体已创建。没有这两个前提，SOLO Coder 只会是一个"高级自动补全"，而非"工程化施工队"。

### Chat 模式场景（讨论 / 审查 / 修复）

| 我想... | 对 Trae 说... |
|---------|--------------|
| 打磨模糊想法 | "读 skills/idea-refine/SKILL.md，帮我打磨：[想法]" |
| 写需求文档 | "读 skills/spec-driven-development/SKILL.md，为 [功能] 写 SPEC.md" |
| 拆分任务 | "读 skills/planning-and-task-breakdown/SKILL.md，帮我拆任务" |
| 写代码 | "读 skills/test-driven-development/SKILL.md，按 TDD 实现：[需求]" |
| 增量开发 | "读 skills/incremental-implementation/SKILL.md，按薄切片开发" |
| 设计 API | "读 skills/api-and-interface-design/SKILL.md，按契约优先设计" |
| 做前端 UI | "读 skills/frontend-ui-engineering/SKILL.md，注意 WCAG 2.1 AA" |
| 调试 bug | "读 skills/debugging-and-error-recovery/SKILL.md，按五步法排查" |
| 浏览器调试 | "读 skills/browser-testing-with-devtools/SKILL.md，用 DevTools 检查" |
| **代码审查** | **"@code-reviewer 审查本次变更"** |
| **安全检查** | **"@security-auditor 做安全审计"** |
| **检查测试** | **"@test-engineer 评估测试覆盖"** |
| 简化代码 | "读 skills/code-simplification/SKILL.md，简化但行为不变" |
| 优化性能 | "读 skills/performance-optimization/SKILL.md，先测量再优化" |
| 准备发布 | "读 skills/shipping-and-launch/SKILL.md，做上线检查" |
| Git 规范 | "读 skills/git-workflow-and-versioning/SKILL.md，检查提交" |
| 记录决策 | "读 skills/documentation-and-adrs/SKILL.md，写 ADR" |
| 不知道用啥 | "读 skills/using-agent-skills/SKILL.md，帮我选技能" |

> **加粗 = 优先创建自定义智能体的场景**，审查类任务用 @智能体比自己手动读 SKILL.md 效果好得多。 |

---

## 附录：agent-skills 仓库在本地的路径

> 将以下路径替换为你实际的 clone 位置。

```
c:\Workspace\source\git\agent-skills-main\
├── skills/          ← 21 个 SKILL.md 技能文件
├── references/      ← 4 个参考清单
├── docs/            ← 各工具设置指南（原始）
└── trae.md          ← 本文件（Trae 专用操作手册）
```

---

> **文档结束** — 本文档是 agent-skills 项目在 Trae IDE 环境中的完整操作手册。
>
> **核心策略**：一次配置（AGENTS.md + 3 个自定义智能体），两种模式受益。完整需求用 SOLO Coder 自动化交付，讨论/审查/排查用 Chat 模式手动控制。
