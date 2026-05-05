# Agent Skills 项目完整文档说明

> 生成日期：2026-05-02
> 项目地址：https://github.com/addyosmani/agent-skills
> 作者：Addy Osmani（Google Chrome 工程总监）
> 许可证：MIT

---

## 目录

1. [项目概述](#项目概述)
2. [根目录文件说明](#根目录文件说明)
3. [技能文件详细说明（21个）](#技能文件详细说明)
4. [Agent Persona 文件说明（3个）](#agent-persona-文件说明)
5. [参考清单文件说明（4个）](#参考清单文件说明)
6. [Hooks 钩子文件说明（8个）](#hooks-钩子文件说明)
7. [Claude Commands 命令文件说明（7个）](#claude-commands-命令文件说明)
8. [Docs 设置指南说明（7个）](#docs-设置指南说明)
9. [配置文件说明](#配置文件说明)
10. [Gemini CLI 命令文件说明（7个）](#gemini-cli-命令文件说明)
11. [其他目录与文件](#其他目录与文件)

---

## 项目概述

### 这是什么？

**Agent Skills** 是一套面向 AI 编码助手（Claude Code、Cursor、Copilot、Gemini CLI 等）的**生产级工程技能集合**。它把资深软件工程师在实际工作中遵循的开发流程、质量标准和最佳实践编码成结构化的技能文档（SKILL.md），让 AI Agent 能够按照专业标准执行软件开发的全生命周期任务。

### 核心设计理念

- **三层架构**：Skills（怎么做）→ Personas（谁来做）→ Commands（何时做）
- **技能即流程**：每个技能是结构化的步骤流程，不是泛泛的建议文档
- **反偷懒机制**：每个技能包含"常见借口反驳表"（Anti-Rationalization），防止 Agent 跳过关键步骤
- **可验证性**：每个技能必须有明确的完成证据（测试通过、构建输出等），"看起来对了"不算完成
- **渐进披露**：核心 SKILL.md 作为入口，详细参考文件按需加载，节约 Token 消耗
- **用户是唯一指挥官**：Agent Persona 之间不互相调用，编排权归用户或 Slash Command

### 完整的开发生命周期覆盖

```
DEFINE（定义）→ PLAN（规划）→ BUILD（构建）→ VERIFY（验证）→ REVIEW（审查）→ SHIP（发布）
```

### 项目目录结构

```
agent-skills/
├── skills/                  ← 21 个核心技能（每个子目录含 SKILL.md）
├── agents/                  ← 3 个专家 Agent Persona
├── references/              ← 4 个补充参考清单
├── hooks/                   ← 会话生命周期钩子脚本
├── .claude/commands/        ← 7 个 Claude Code 斜杠命令
├── .claude-plugin/          ← Claude Code 插件市场配置
├── .gemini/commands/        ← 7 个 Gemini CLI 命令
├── .github/workflows/       ← CI 工作流
├── .opencode/               ← OpenCode 集成
├── docs/                    ← 各工具设置指南
└── [根目录各 .md 文件]      ← 项目简介与说明
```

---

## 根目录文件说明

### README.md
| 属性 | 内容 |
|------|------|
| **作用** | 项目主入口文档，对外介绍 |
| **大致内容** | 项目定位（生产级工程技能包）、开发流水线图示（DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP）、7 个斜杠命令一览、21 个技能分类表格、3 个 Agent Persona 介绍、多平台安装指引（Claude Code / Cursor / Gemini CLI / Windsurf / OpenCode / Copilot）、技能结构解剖图、项目目录结构、设计理念与 Google 工程文化背景 |

### AGENTS.md
| 属性 | 内容 |
|------|------|
| **作用** | 给 AI Agent 看的行为指引文件，自动被 IDE 加载为 workspace rules |
| **大致内容** | 仓库概览、OpenCode 集成规则、技能的意图映射（如"新功能"→spec-driven-development）、生命周期隐式命令映射、执行模型要求（必须先检查技能再动手）、反辩解思维训练、三层架构关系解释、技能创建指南目录结构与命名规范、SKILL.md 格式模板、脚本要求、打包方法 |

### CLAUDE.md
| 属性 | 内容 |
|------|------|
| **作用** | 给 Claude Code 看的项目指引文件 |
| **大致内容** | 简洁版项目结构、技能按阶段分类（Define/Plan/Build/Verify/Review/Ship）、代码规范（SKILL.md 格式要求、frontmatter 规范、技能六大部分）、命令说明、边界规则（Always/Never） |

### CONTRIBUTING.md
| 属性 | 内容 |
|------|------|
| **作用** | 贡献指南 |
| **大致内容** | 新技能添加步骤（创建 kebab-case 目录→添加 SKILL.md→包含 YAML frontmatter）、技能质量标准四要素（具体、可验证、实战验证、最小化）、技能必须包含的六大部分、不允许做的事（不重复内容、不放空泛建议、不超 100 行创建额外文件、不把参考材料放技能目录）、修改现有技能的注意事项、Issue 提交场景 |

### LICENSE
| 属性 | 内容 |
|------|------|
| **作用** | 开源许可证 |
| **大致内容** | MIT License，版权归属 Addy Osmani (2025)，允许自由使用、复制、修改、合并、发布、分发、再许可和销售 |

### .gitignore
| 属性 | 内容 |
|------|------|
| **作用** | Git 忽略规则 |
| **大致内容** | 忽略 OS 文件（.DS_Store）、IDE 配置、临时文件、node_modules、.env 等 |

---

## 技能文件详细说明

> 每个技能位于 `skills/<skill-name>/SKILL.md`，包含 YAML frontmatter（name + description）、Overview、When to Use、Core Process、Common Rationalizations（常见借口与反驳）、Red Flags（危险信号）、Verification（验证清单）。

### 阶段一：DEFINE（定义 —— 明确要构建什么）

#### 1. idea-refine（想法打磨）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/idea-refine/SKILL.md` |
| **触发条件** | 你有一个模糊的概念需要探索和具体化 |
| **功能概述** | 采用结构化的发散/收敛思维，将模糊的想法转化为具体的方案提案。类似产品经理做需求分析的过程，通过多轮提问和推演将朦胧的想法打磨清晰 |
| **配套文件** | `examples.md`（案例）、`frameworks.md`（框架方法论）、`refinement-criteria.md`（打磨标准）、`scripts/idea-refine.sh`（执行脚本） |

#### 2. spec-driven-development（规格驱动开发）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/spec-driven-development/SKILL.md` |
| **触发条件** | 启动新项目、新功能或重大变更，且还没有规格文档；需求不清晰、模糊或只有模糊想法 |
| **功能概述** | 在写任何代码前，先撰写结构化规格文档（PRD），覆盖目标、命令、项目结构、代码风格、测试策略和边界六大核心领域。四阶段门控流程：SPECIFY→PLAN→TASKS→IMPLEMENT，每个阶段需要人工审核通过后才能进入下一阶段 |
| **核心原则** | 没有规格就写代码等于在猜谜。先列假设，让用户纠正，再写文档 |

### 阶段二：PLAN（规划 —— 拆分任务）

#### 3. planning-and-task-breakdown（规划与任务拆分）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/planning-and-task-breakdown/SKILL.md` |
| **触发条件** | 你有了规格文档，需要可执行的任务单元 |
| **功能概述** | 将规格文档拆分为小粒度、可验证的任务，每个任务带有验收标准和依赖排序。确保每一步都可追踪、可测试、可独立验收 |

### 阶段三：BUILD（构建 —— 编写代码）

#### 4. incremental-implementation（增量实现）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/incremental-implementation/SKILL.md` |
| **触发条件** | 任何涉及多个文件的变更 |
| **功能概述** | 采用薄垂直切片方式——实现一个切片、测试、验证、提交。使用特性开关（Feature Flags）、安全默认值、支持回滚的变更策略。强调小步快跑、持续集成 |

#### 5. test-driven-development（测试驱动开发）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/test-driven-development/SKILL.md` |
| **触发条件** | 实现逻辑、修复 bug 或变更行为时 |
| **功能概述** | 严格遵循 Red-Green-Refactor 循环（先写失败测试→写最小代码使测试通过→重构优化）。测试金字塔比例：80% 单元测试 / 15% 集成测试 / 5% E2E 测试。测试原则：DAMP 优于 DRY（描述性且有意义优于不重复） |
| **核心原则** | 遵循"碧昂斯法则"——如果你喜欢它，就应该给它写个测试 |

#### 6. context-engineering（上下文工程）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/context-engineering/SKILL.md` |
| **触发条件** | 启动新会话、切换任务，或 Agent 输出质量下降时 |
| **功能概述** | 教 Agent 如何在正确的时间获取正确的信息——包括规则文件、上下文打包、MCP 集成。核心思想：给 Agent 最好的上下文才能产出最好的代码 |

#### 7. source-driven-development（源码驱动开发）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/source-driven-development/SKILL.md` |
| **触发条件** | 你希望获得有权威来源引用的代码（针对任何框架或库） |
| **功能概述** | 每个框架决策都要以官方文档为根据——验证、引用来源、标记未经验证的内容。避免 Agent 根据"训练记忆"中的过时知识生成错误代码 |

#### 8. frontend-ui-engineering（前端 UI 工程）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/frontend-ui-engineering/SKILL.md` |
| **触发条件** | 构建或修改面向用户的界面时 |
| **功能概述** | 覆盖组件架构、设计系统、状态管理、响应式设计、WCAG 2.1 AA 无障碍标准。确保 UI 代码既有良好的用户体验又便于维护 |

#### 9. api-and-interface-design（API 与接口设计）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/api-and-interface-design/SKILL.md` |
| **触发条件** | 设计 API、模块边界或公共接口时 |
| **功能概述** | 遵循契约优先设计、海勒姆定律（隐式接口会被依赖）、一个版本规则、错误语义规范、边界校验等原则。确保 API 设计经得起时间和依赖方的考验 |

### 阶段四：VERIFY（验证 —— 证明它能用）

#### 10. browser-testing-with-devtools（浏览器 DevTools 测试）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/browser-testing-with-devtools/SKILL.md` |
| **触发条件** | 构建或调试任何在浏览器中运行的内容 |
| **功能概述** | 利用 Chrome DevTools MCP 获取实时运行时数据——DOM 检查、控制台日志、网络追踪、性能分析。让 Agent 能像真人在浏览器里调试一样工作 |

#### 11. debugging-and-error-recovery（调试与错误恢复）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/debugging-and-error-recovery/SKILL.md` |
| **触发条件** | 测试失败、构建出错或行为不符合预期时 |
| **功能概述** | 五步排查法：复现→定位→精简→修复→加固。"停线规则"——连续 3 次失败的修复尝试后，必须停下来重新分析根本原因，而非盲目尝试。要求安全回退方案 |

### 阶段五：REVIEW（审查 —— 合并前的质量门禁）

#### 12. code-review-and-quality（代码审查与质量）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/code-review-and-quality/SKILL.md` |
| **触发条件** | 合并任何变更之前 |
| **功能概述** | 五维度审查（正确性、可读性、架构、安全、性能），变更粒度控制（约 100 行以内），严重性标注（Nit/可选/FYI），审查速度规范，变更拆分策略 |

#### 13. code-simplification（代码简化）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/code-simplification/SKILL.md` |
| **触发条件** | 代码能工作但比应有的复杂度更难读或难维护时 |
| **功能概述** | 遵循切斯特顿栅栏原则（先理解为什么存在再改动）、500 行规则（超过 500 行的模块应拆分），在保持行为完全不变的前提下降低复杂度 |

#### 14. security-and-hardening（安全与加固）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/security-and-hardening/SKILL.md` |
| **触发条件** | 处理用户输入、认证、数据存储或外部集成时 |
| **功能概述** | OWASP Top 10 防御、认证模式、密钥管理、依赖审计、三层边界系统（代码级→请求级→基础设施级）。把安全嵌入开发流程而非事后修补 |

#### 15. performance-optimization（性能优化）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/performance-optimization/SKILL.md` |
| **触发条件** | 存在性能要求或你怀疑有性能退化时 |
| **功能概述** | 先测量再优化——Core Web Vitals 目标、性能分析工作流、Bundle 分析、反模式检测。强调数据驱动的性能优化，不凭感觉"优化" |

### 阶段六：SHIP（发布 —— 自信部署）

#### 16. git-workflow-and-versioning（Git 工作流与版本管理）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/git-workflow-and-versioning/SKILL.md` |
| **触发条件** | 任何代码变更（总是启用） |
| **功能概述** | 基于主干开发（Trunk-Based Development）、原子化提交、变更粒度控制（约 100 行）、提交即存档点模式。规范 Agent 的 Git 操作行为 |

#### 17. ci-cd-and-automation（CI/CD 与自动化）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/ci-cd-and-automation/SKILL.md` |
| **触发条件** | 设置或修改构建与部署流水线时 |
| **功能概述** | "左移"原则、快速更安全、特性开关、质量门禁流水线、失败反馈循环。将质量检查尽可能前置到开发早期 |

#### 18. deprecation-and-migration（废弃与迁移）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/deprecation-and-migration/SKILL.md` |
| **触发条件** | 移除旧系统、迁移用户或下线功能时 |
| **功能概述** | 代码即负债思维、强制废弃 vs 建议废弃、迁移模式、僵尸代码清理。把代码视为需要管理的负债而非资产 |

#### 19. documentation-and-adrs（文档与架构决策记录）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/documentation-and-adrs/SKILL.md` |
| **触发条件** | 做架构决策、变更 API 或发布功能时 |
| **功能概述** | 架构决策记录（ADR）、API 文档、内联文档标准。强调记录"为什么"而不仅是"是什么" |

#### 20. shipping-and-launch（发布与上线）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/shipping-and-launch/SKILL.md` |
| **触发条件** | 准备部署到生产环境时 |
| **功能概述** | 预发布检查清单、特性开关生命周期、分阶段发布、回滚流程、监控设置。确保每次发布都有完整的应急预案 |

### 特殊技能

#### 21. using-agent-skills（如何使用这套技能包）
| 属性 | 内容 |
|------|------|
| **路径** | `skills/using-agent-skills/SKILL.md` |
| **触发条件** | 需要用这套技能包但不清楚该用哪个时 |
| **功能概述** | "元技能"（Meta-Skill），包含一个完整的流程图，将任务类型映射到对应的技能。当你不知道应该用哪个技能时，先加载这个。是所有技能的导航入口 |

---

## Agent Persona 文件说明

> Persona 是预设好"人设"和"输出格式"的专家角色，各自拥有单一视角。Persona 之间不互相调用，编排权归用户或 Slash Command。

### agents/README.md
| 属性 | 内容 |
|------|------|
| **作用** | Agent Persona 体系的说明文档 |
| **大致内容** | 三个 Persona 对照表（code-reviewer/security-auditor/test-engineer）、三层关系解释（Skill=怎么做 / Persona=谁来做 / Command=何时做）、直接调用场景、斜杠命令场景、并行扇出编排模式（`/ship` 命令）、反面模式警告（不构建"元编排器"）、Persona 创建规则、Claude Code 互操作说明、决策矩阵 |

### agents/code-reviewer.md（资深代码审查员）
| 属性 | 内容 |
|------|------|
| **角色定位** | 资深 Staff Engineer，按"Staff Engineer 会批准吗？"的标准审查代码 |
| **审查框架** | **五维度审查**：<br>1. **正确性** — 代码是否按规格实现了？边界条件处理了吗？<br>2. **可读性** — 其他工程师能不看解释就理解吗？命名是否符合规范？<br>3. **架构** — 是否遵循现有模式？模块边界是否合理？有无循环依赖？<br>4. **安全性** — 用户输入是否验证和消毒？密钥是否泄漏？查询是否参数化？<br>5. **性能** — 有无 N+1 查询？有无无界循环？是否需要分页？ |
| **输出格式** | 三档严重性标签：**Critical**（必须修）/ **Important**（应该修）/ **Suggestion**（建议改进），附完整的 Review Summary 模板 |

### agents/security-auditor.md（安全审计员）
| 属性 | 内容 |
|------|------|
| **角色定位** | 安全工程师，专注漏洞检测、威胁建模、OWASP 评估 |
| **审查领域** | **五个审查领域**：<br>1. **输入处理** — XSS、注入攻击、输入验证<br>2. **认证与授权** — 会话管理、权限检查、CSRF<br>3. **数据保护** — 加密、敏感数据暴露、日志安全<br>4. **基础设施** — CORS、CSP、依赖漏洞<br>5. **第三方集成** — API 密钥、供应链安全 |
| **输出格式** | 漏洞严重性分级（Critical/High/Medium/Low），附受影响代码位置和修复建议 |

### agents/test-engineer.md（测试工程师）
| 属性 | 内容 |
|------|------|
| **角色定位** | QA 工程师，专注测试策略、覆盖率分析、Prove-It 模式 |
| **工作框架** | 测试策略评估、缺失测试识别、覆盖率报告（按模块/功能/风险维度）、"先证明再相信"（Prove-It）方法论——每个断言必须验证实际行为，不能用假设替代测试 |
| **输出格式** | 结构化测试分析报告，包含：现有测试覆盖范围、缺失的测试场景、测试质量评估、改进建议优先级排序 |

---

## 参考清单文件说明

> 位于 `references/`，作为技能的详细补充材料，按需加载而不常驻上下文。

### references/testing-patterns.md（测试模式参考）
| 属性 | 内容 |
|------|------|
| **配合使用** | `test-driven-development` 技能 |
| **主要内容** | 测试结构规范（Arrange-Act-Assert）、命名约定（描述行为而非实现）、常见断言模式、Mock 策略与反模式、React 组件测试模式、API 测试模式、E2E 测试模式、测试反模式（需要避免的写法） |

### references/security-checklist.md（安全检查清单）
| 属性 | 内容 |
|------|------|
| **配合使用** | `security-and-hardening` 技能 |
| **主要内容** | 提交前安全检查（密钥扫描、敏感文件检查）、认证检查（会话管理、密码强度、MFA）、授权检查（权限模型、越权防护）、输入验证检查（XSS、SQL 注入、命令注入）、HTTP 安全头（CSP、HSTS、X-Frame-Options）、CORS 配置、依赖安全审计 |

### references/performance-checklist.md（性能检查清单）
| 属性 | 内容 |
|------|------|
| **配合使用** | `performance-optimization` 技能 |
| **主要内容** | Core Web Vitals 指标目标值（LCP<2.5s、FID<100ms、CLS<0.1）、前端检查（Bundle 大小、图片优化、懒加载、关键渲染路径）、后端检查（数据库查询优化、缓存策略、N+1 问题）、性能测试命令 |

### references/accessibility-checklist.md（无障碍检查清单）
| 属性 | 内容 |
|------|------|
| **配合使用** | `frontend-ui-engineering` 技能 |
| **主要内容** | 键盘导航检查（焦点管理、跳过链接）、屏幕阅读器兼容性（语义化 HTML、ARIA 标签）、视觉设计检查（对比度、字体缩放、颜色依赖）、测试工具推荐（Lighthouse、axe-core、WAVE） |

### references/orchestration-patterns.md（编排模式参考）
| 属性 | 内容 |
|------|------|
| **配合使用** | Agent 编排设计 |
| **主要内容** | 四种认可的编排模式：<br>1. **直接调用**（无编排，单人单任务，成本最低）<br>2. **单人 Command**（斜杠命令包装单 Persona + Skill）<br>3. **并行扇出+汇总**（`/ship` 模式，多 Persona 同时工作）<br>4. **用户驱动的顺序流水线**（用户依次运行 Command）<br>另含：反模式警告（不做"元编排器"、不做链式调用 Role→调另一个 Role） |

---

## Hooks 钩子文件说明

> 位于 `hooks/`，是会话生命周期的自动化钩子。在 Claude Code 中可用。

### hooks/hooks.json
| 属性 | 内容 |
|------|------|
| **作用** | Hook 配置文件 |
| **大致内容** | JSON 配置，指定了 SessionStart、PreToolUse、PostToolUse 等事件触发时执行的脚本路径 |

### hooks/session-start.sh
| 属性 | 内容 |
|------|------|
| **作用** | 会话启动钩子 |
| **大致内容** | 在新会话启动时自动将元技能（using-agent-skills）注入 Claude，让 Agent 第一时间知道如何发现和使用所有技能。是技能系统的"自动导航注入器" |

### hooks/sdd-cache-pre.sh（SDD 缓存预处理）
| 属性 | 内容 |
|------|------|
| **作用** | WebFetch 工具调用前的缓存拦截器 |
| **大致内容** | 在 WebFetch 调用前，通过 HTTP HEAD 请求检查目标 URL 内容是否已缓存且未变化。如果缓存有效，直接返回缓存内容，避免重复网络请求，减少 Token 消耗和延迟 |

### hooks/sdd-cache-post.sh（SDD 缓存后处理）
| 属性 | 内容 |
|------|------|
| **作用** | WebFetch 工具调用后的缓存记录器 |
| **大致内容** | 在 WebFetch 成功获取内容后，记录响应并缓存结果（包括 ETag 和 Last-Modified），供下次 pre-hook 查询复用 |

### hooks/SDD-CACHE.md
| 属性 | 内容 |
|------|------|
| **作用** | SDD-Cache 钩子的详细文档 |
| **大致内容** | 解释缓存 hook 的设计目的（优化 source-driven-development 中重复的 WebFetch 请求）、工作原理（HTTP 条件请求 + 本地缓存）、安装步骤与使用方法 |

### hooks/simplify-ignore.sh（简化屏蔽器）
| 属性 | 内容 |
|------|------|
| **作用** | 保护特定代码块不被 `code-simplification` 技能修改 |
| **大致内容** | 管理文件中 `simplify-ignore-start` 和 `simplify-ignore-end` 标记括起来的内容。在简化处理前用占位符替换受保护内容，处理完成后恢复原内容 |

### hooks/simplify-ignore-test.sh（简化屏蔽器测试）
| 属性 | 内容 |
|------|------|
| **作用** | 对 simplify-ignore.sh 的功能测试 |
| **大致内容** | 包含多种测试用例，验证屏蔽逻辑是否正确处理各种边界情况（嵌套标记、多块保护内容、异常输入等） |

### hooks/SIMPLIFY-IGNORE.md
| 属性 | 内容 |
|------|------|
| **作用** | Simplify-Ignore 钩子的详细文档 |
| **大致内容** | 解释为什么需要保护特定代码（某些故意冗长的实现不能简单"简化"）、标记语法、使用示例 |

---

## Claude Commands 命令文件说明

> 位于 `.claude/commands/`，是 Claude Code 中的斜杠命令（Slash Commands）。用户输入 `/命令名` 即可自动调度对应的 Skills 和 Personas。

### .claude/commands/spec.md → `/spec`
| 属性 | 内容 |
|------|------|
| **对应技能** | `spec-driven-development` |
| **功能** | 启动规格驱动开发流程——先写 PRD 再写代码。自动要求 Agent 列出假设、撰写规格文档、等待用户审核 |
| **核心原则** | Spec before code（精细化定义在编码之前） |

### .claude/commands/plan.md → `/plan`
| 属性 | 内容 |
|------|------|
| **对应技能** | `planning-and-task-breakdown` |
| **功能** | 将规格文档拆分为小粒度的可执行任务，带上验收标准和依赖顺序 |
| **核心原则** | Small, atomic tasks（小而原子的任务） |

### .claude/commands/build.md → `/build`
| 属性 | 内容 |
|------|------|
| **对应技能** | `incremental-implementation` + `test-driven-development` |
| **功能** | 增量构建——一次实现一个薄切片，先写失败的测试，实现最小代码使测试通过，提交后再做下一个切片 |
| **核心原则** | One slice at a time（一次一片薄切片） |

### .claude/commands/test.md → `/test`
| 属性 | 内容 |
|------|------|
| **对应技能** | `test-driven-development` |
| **功能** | 运行完整的 TDD 工作流——Red→Green→Refactor 循环 |
| **核心原则** | Tests are proof（测试就是证明） |

### .claude/commands/review.md → `/review`
| 属性 | 内容 |
|------|------|
| **对应技能** | `code-review-and-quality` |
| **功能** | 启动五维度代码审查流程，按 Critical/Important/Suggestion 标注问题 |
| **核心原则** | Improve code health（改进代码健康度） |

### .claude/commands/code-simplify.md → `/code-simplify`
| 属性 | 内容 |
|------|------|
| **对应技能** | `code-simplification` |
| **功能** | 在不改变行为的前提下降低代码复杂度，遵循切斯特顿栅栏原则和 500 行规则 |
| **核心原则** | Clarity over cleverness（清晰优于聪明） |

### .claude/commands/ship.md → `/ship`
| 属性 | 内容 |
|------|------|
| **对应技能** | `shipping-and-launch`（同时调度多个 Persona） |
| **功能** | **并行扇出模式**——同时派出 code-reviewer、security-auditor、test-engineer 三个 Agent，各自出具独立报告，最后汇总为"发布 / 不发布"决策 + 回滚方案 |
| **核心原则** | Faster is safer（更快速反而更安全） |

---

## Docs 设置指南说明

> 位于 `docs/`，指导用户在不同 AI 编码工具中安装和使用该技能包。

### docs/getting-started.md（快速入门）
| 属性 | 内容 |
|------|------|
| **作用** | 通用入门指南，适用于所有 AI 编码工具 |
| **大致内容** | 技能工作原理（每个 SKILL.md 是步骤化流程）、三种加载方式（System Prompt / Rules File / Conversation）、最少配置推荐（3 个核心技能：spec + TDD + review）、全生命周期配置（按阶段加载技能）、技能结构解剖、Agent 使用方法、Command 使用方法、Spec 和 Task 产物的生命周期管理、5 个实用技巧 |

### docs/skill-anatomy.md（技能结构规范）
| 属性 | 内容 |
|------|------|
| **作用** | SKILL.md 格式的技术规范（给技能创建者看） |
| **大致内容** | 完整的 SKILL.md 格式定义：YAML frontmatter（name, description）规范、必选章节（Overview / When to Use / Core Process / Common Rationalizations / Red Flags / Verification）、可选章节、每部分的编写规范与示例、质量标准 |

### docs/cursor-setup.md（Cursor 设置指南）
| 属性 | 内容 |
|------|------|
| **作用** | 在 Cursor IDE 中使用 agent-skills 的设置方法 |
| **大致内容** | 三种集成方式：1) 复制 SKILL.md 到 `.cursor/rules/` 目录（推荐）；2) 粘贴到 `.cursorrules` 文件；3) 使用 Notepads 功能。区别与适用场景说明 |

### docs/copilot-setup.md（GitHub Copilot 设置指南）
| 属性 | 内容 |
|------|------|
| **作用** | 在 GitHub Copilot 中使用 agent-skills 的设置方法 |
| **大致内容** | 将 Agent Persona 定义用作 Copilot 角色、将技能内容放入 `.github/copilot-instructions.md` 文件、Copilot Chat 中的使用方法 |

### docs/gemini-cli-setup.md（Gemini CLI 设置指南）
| 属性 | 内容 |
|------|------|
| **作用** | 在 Gemini CLI 中使用 agent-skills 的设置方法 |
| **大致内容** | 原生技能安装方式（`gemini skills install`）、GEMINI.md 持久上下文配置、斜杠命令使用 |
| **注意** | `.gemini/commands/` 下有对应的 7 个 `.toml` 格式命令文件 |

### docs/opencode-setup.md（OpenCode 设置指南）
| 属性 | 内容 |
|------|------|
| **作用** | 在 OpenCode 中使用 agent-skills 的设置方法 |
| **大致内容** | OpenCode 的 Agent 驱动执行模型——通过 AGENTS.md 和 skill 工具实现意图映射，无需手动命令。任务自动匹配到对应技能（如"新功能"→spec-driven-development） |

### docs/windsurf-setup.md（Windsurf 设置指南）
| 属性 | 内容 |
|------|------|
| **作用** | 在 Windsurf IDE 中使用 agent-skills 的设置方法 |
| **大致内容** | 通过 `.windsurfrules` 文件加载技能内容（与 Cursor 的 .cursorrules 类似），技能使用的简单说明 |

---

## 配置文件说明

### .claude-plugin/plugin.json
| 属性 | 内容 |
|------|------|
| **作用** | Claude Code 插件定义 |
| **大致内容** | 插件元信息：名称 `agent-skills`、版本 `1.0.0`、作者 Addy Osmani、仓库地址、许可证 MIT、Commands 路径指向 `./.claude/commands` |

### .claude-plugin/marketplace.json
| 属性 | 内容 |
|------|------|
| **作用** | Claude Code 插件市场注册信息 |
| **大致内容** | 市场名称 `addy-agent-skills`、所有者信息、插件描述、GitHub 仓库来源。用户通过 `/plugin marketplace add addyosmani/agent-skills` 安装 |

### .github/workflows/test-plugin-install.yml
| 属性 | 内容 |
|------|------|
| **作用** | GitHub CI 工作流 |
| **大致内容** | 自动化测试插件安装流程的 CI 工作流配置，确保每次提交后插件能正常安装 |

---

## Gemini CLI 命令文件说明

> 位于 `.gemini/commands/`，与 Claude Commands 功能相同但采用 `.toml` 格式。共 7 个文件，映射关系与 Claude Commands 一一对应。

| 文件 | 对应命令 | 功能 |
|------|----------|------|
| `spec.toml` | `/spec` | 规格驱动开发 |
| `planning.toml` | `/plan` | 规划与任务拆分 |
| `build.toml` | `/build` | 增量构建 |
| `test.toml` | `/test` | TDD 工作流 |
| `review.toml` | `/review` | 代码审查 |
| `code-simplify.toml` | `/code-simplify` | 代码简化 |
| `ship.toml` | `/ship` | 并行审查+发布决策 |

---

## 其他目录与文件

### .opencode/
| 属性 | 内容 |
|------|------|
| **作用** | OpenCode 工具集成 |
| **大致内容** | 符号链接或配置，指向 skills 目录，供 OpenCode 的 skill 工具自动发现 |

### skills/idea-refine/ 附属文件
| 文件 | 作用 |
|------|------|
| `examples.md` | 想法打磨的实际案例演示 |
| `frameworks.md` | 支撑方法论框架（发散-收敛思维等） |
| `refinement-criteria.md` | 想法打磨的质量评判标准 |
| `scripts/idea-refine.sh` | 可执行脚本，自动化想法打磨过程 |

---

## 快速导航：我应该用什么？

| 我想做什么 | 使用的技能 | 使用的 Command（Claude Code） |
|-----------|-----------|------------------------------|
| 明确模糊的想法 | `idea-refine` | — |
| 写需求文档/PRD | `spec-driven-development` | `/spec` |
| 拆分开发任务 | `planning-and-task-breakdown` | `/plan` |
| 开始写代码 | `incremental-implementation` + `test-driven-development` | `/build` |
| 确保代码质量 | `test-driven-development` | `/test` |
| 提交前审查 | `code-review-and-quality` | `/review` |
| 简化复杂代码 | `code-simplification` | `/code-simplify` |
| 安全检查 | `security-and-hardening` | —（用 security-auditor Persona） |
| 性能优化 | `performance-optimization` | — |
| 准备发布 | `shipping-and-launch` | `/ship` |
| 不知道用什么 | `using-agent-skills` | — |

---

> **文档结束** — 本文档覆盖了 agent-skills 项目的全部核心文件（共 80+ 个文件），按目录结构分类说明了每个文件的作用和大致内容。
