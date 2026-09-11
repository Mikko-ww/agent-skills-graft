# 撰写 Agent Brief

Agent brief 是 issue 或 PR 移到 `ready-for-agent` 时贴上的结构化评论。它是 AFK agent 所依据的权威规格。原文与讨论是上下文；agent brief 才是契约。

Brief 陈述 **agent 应做什么**，覆盖两种表面：对 issue，是从零构建变更；对 PR，是对*已有 diff* 还剩什么要做：补完、填缺口、处理 review 意见。原则相同；下方 PR 示例展示差异。

## 原则

### Durability over precision（耐久优于精密）

Issue 可能在 `ready-for-agent` 停留数日或数周。其间代码库会变。写 brief 时要在文件重命名、移动或重构后仍有用。

- **要**描述 interface、类型与行为契约
- **要**点名 agent 应查找或修改的具体类型、函数签名或配置形态
- **不要**引用文件路径：会过时
- **不要**引用行号
- **不要**假设当前实现结构会保持不变

### Behavioral, not procedural（行为式，非过程式）

描述系统**应做什么**，而非**如何实现**。Agent 会重新探索代码库并自行做实现决策。

- **好：** "The `SkillConfig` type should accept an optional `schedule` field of type `CronExpression`"
- **坏：** "Open src/types/skill.ts and add a schedule field on line 42"
- **好：** "When a user runs matt-triage with no arguments, they should see a summary of issues needing attention"
- **坏：** "Add a switch statement in the main handler function"

### Complete acceptance criteria

Agent 需要知道何时算完成。每份 agent brief 必须有具体、可测的验收标准。每条应可独立验证。

- **好：** "Running the tracker's list filtered by needs-triage returns issues that have been through initial classification"
- **坏：** "Triage should work correctly"

### Explicit scope boundaries

写明哪些 out of scope，防止 agent 镀金或对相邻功能做假设。

## 模板

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

**Key interfaces:**
- `TypeName`: what needs to change and why
- `functionName()` return type: what it currently returns vs what it should return
- Config shape: any new configuration options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should NOT be changed or addressed in this issue
- Adjacent feature that might seem related but is separate
```

## 示例要点

**好的 bug brief：** 写清当前截断行为、期望按词边界截断并加 `...`、点名 `SkillMetadata.description` 相关逻辑、列出可测验收项、明确不改 1024 上限等 out of scope。

**好的 enhancement brief：** 写清拒绝后无持久记录的现状、期望 `.out-of-scope/<concept>.md` 形态、matt-triage 应对照检查、验收项覆盖创建/追加/发现匹配、out of scope 含自动化匹配与 bug 报告。

**好的 PR brief：** "Current behavior" 描述 diff 现状；brief 要求补完或修好，而非从零构建。例如：补 JSON 错误路径与测试，不改成功载荷形状。

**坏的 brief：** 无 category、描述含糊、引用路径与行号、无验收标准、无范围边界、无当前/期望行为对比。
