### 步骤 1（Chat 模式）：
   "读 skills/spec-driven-development/SKILL.md，
    为 FastAPI 脚手架项目写 SPEC.md。
    要求：application.yml 配置、多进程、MySQL 连接池管理"
    → Agent 列假设，你确认 → SPEC.md 产出，你 review

### 步骤 2（Chat 模式）：
   "读 skills/planning-and-task-breakdown/SKILL.md，按 SPEC.md 拆任务"
   → tasks/ 产出，你确认任务列表

### 步骤 3（切换到 SOLO 模式）：
   "按 tasks/ 全部实现。
    规则：异步全局、SQLAlchemy 2.0 async、连接池 pool_size=20、
    application.yml 多环境、gunicorn 多进程启动、无硬编码"
   → SOLO Coder 自动编码、测试、提交
   → Diff 展示，你逐文件审查

### 步骤 4（回到 Chat 模式）：
   "@code-reviewer 审查全部 scaffold 代码"
   "@security-auditor 检查配置管理和数据库连接安全"
   等待并行审查报告
   → 根据报告修正后，脚手架交付