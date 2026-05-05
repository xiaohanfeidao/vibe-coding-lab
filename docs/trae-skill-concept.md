## 重要：agent-skills 的 "Skill" 和 Trae 的 "Skill" 是两回事

> **应该在 trae.md 的第 3 章（模式选择）和第 5 章（体系映射）之间插入此章节。**

**你的直觉完全正确——它们不是同一个概念。如果不理解这个差异，你会以为自己在用 Trae 原生能力，实际上只是在让 Agent 读一份外部文档。**

### 两个 "Skill" 的本质区别

agent-skills 的 SKILL.md = 一份 Markdown 工作流文档（操作手册，告诉 Agent "怎么做"）。

Trae 的内置 Skill = 框架内部的能力/知识模块（告诉 Agent "这个项目是怎么组织的"）。

```
agent-skills SKILL.md                    Trae 内置知识文档（~/.trae-cn/）
─────────────────────────              ─────────────────────────────
YAML: name + description               YAML: name + description（特定字段）
Overview（技能做什么）                   Module Structure（目录布局）
When to Use（触发条件）                   Gotchas（踩坑记录）
Process（步骤流程）                       Architecture（架构知识）
Rationalizations（防偷懒反驳）             Patterns（代码模式）
Verification（验证清单）                  Conventions（命名规范）
存放：skills/<名称>/SKILL.md             存放：~/.trae-cn/builtin_skills/
```

### 当前做法的局限性

当前 trae.md 的"读 skills/.../SKILL.md"方式本质是 **Agent 读取外部文档并理解执行**，不是 Trae 框架级的技能调度。这意味着：

| 问题 | 影响 |
|------|------|
| 每次对话都要重新读文件 | 浪费 Token，长文件尤其明显 |
| Agent 可能在长对话中"忘记"规则 | 对话后期行为不再受 SKILL.md 约束 |
| SOLO Coder 不直接引用 SKILL.md | SOLO Coder 只能调度自定义智能体 |

### 正确关系：SKILL.md 是原材料，AGENTS.md + 智能体才是成品

```
agent-skills SKILL.md（详尽知识源）
         │
         ├── 提炼核心规则 → AGENTS.md（自动生效，无需每次引用）
         │
         ├── 转化审查框架 → @code-reviewer 智能体提示词（独立上下文）
         ├── 转化安全检查 → @security-auditor 智能体提示词
         └── 转化测试策略 → @test-engineer 智能体提示词
```

> **核心公式**：SKILL.md → 提炼进 AGENTS.md（规则自动约束）+ 提炼进智能体提示词（审查能力固化）。日常干活不再手动引用 SKILL.md，因为它已经"内化"成了 Trae 的原生行为。

### 什么时候该直接读 SKILL.md，什么时候不该

| 场景 | 做法 |
|------|------|
| 第一次配置项目 | 读 SKILL.md → 提炼核心规则写进 AGENTS.md |
| 创建自定义智能体 | 读 SKILL.md → 提炼审查框架写进智能体提示词 |
| 不确定该用什么流程 | 读 using-agent-skills/SKILL.md 帮你导航 |
| **每次日常编码** | ❌ 不要读 TDD/增量实现的 SKILL.md（规则已在 AGENTS.md 中） |
| **每次代码审查** | ❌ 不要读 code-review 的 SKILL.md（审查能力已在 @code-reviewer 中） |
| 想学习一个技能的完整方法论 | ✅ 读对应 SKILL.md 作为学习材料 |

### Trae 内置知识文档 vs agent-skills SKILL.md 的协同

Trae 的内置知识文档体系（`~/.trae-cn/builtin_skills/`）定义的是"这个代码库有什么"（Gotchas、Architecture、Patterns），而 agent-skills 的 SKILL.md 定义的是"开发流程应该怎么做"（Spec First、TDD、Review）。两者互补：

```
Trae 内置知识文档（项目是什么）  +  agent-skills 方法论（流程怎么做）
         │                                    │
         └──────────── 融合在 AGENTS.md ──────┘
                           │
                    完整的 Agent 行为约束
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          SOLO Coder    Chat 模式    自定义智能体
         （自动遵守）  （自动遵守）   （专注执行）
```
