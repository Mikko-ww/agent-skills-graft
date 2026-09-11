---
name: matt-agent-skills-help
description: 输出 matt-agent-skills 全部技能的 Markdown 总览（面向不熟悉本项目的人）。仅当用户显式调用本技能、或明确要「技能列表 / 说明书 / help / 有哪些 matt 技能」时使用；禁止因对话中顺带提到 matt-* 而自动触发。
invocation: user
disable-model-invocation: true
---

# matt-agent-skills-help

**仅用户显式调用。** 不要因为用户提到某个 `matt-*` 技能、或正在工程讨论，就自行运行本技能。

本技能产出一份**面向新人的 Markdown 说明书**：列出本项目有哪些技能、各自干什么、怎么调用。不替代各技能正文；也不替代 `matt-skill-flows`（那条回答「该走哪条路」）。

## 本发布版本的静态分类索引

分类以本列表为准，不要解析 README 标题，也不要按目录发明分类。

### Engineering

- user：`matt-skill-flows`、`matt-grill-with-docs`、`matt-triage`、`matt-improve-codebase-architecture`、`matt-configure-project-docs`、`matt-to-spec`、`matt-to-tickets`、`matt-implement`、`matt-wayfinder`
- model：`matt-prototype`、`matt-diagnosing-bugs`、`matt-research`、`matt-tdd`、`matt-domain-modeling`、`matt-codebase-design`、`matt-code-review`、`matt-resolving-merge-conflicts`、`matt-wizard`

### Productivity

- user：`matt-grill-me`、`matt-agent-skills-help`、`matt-handoff`、`matt-teach`、`matt-to-questionnaire`、`matt-wait-what`
- model：`matt-grilling`、`matt-writing-for-agents`

## 输出要求

向用户发送**一份完整 Markdown**（可直接复制），结构如下：

### 1. 项目是什么（短）

用 2–4 句说明：

- 这是面向任意 coding Agent 的工程技能库（`matt-agent-skills`）
- 正文多为简体中文，技术领域专有名词保留英文
- 技能 id 均以 `matt-` 为前缀；按下方「怎么用」分平台显式调用

### 2. 主链路（示意）

给出：

`matt-grill-with-docs` → `matt-to-spec` → `matt-to-tickets` → `matt-implement`

（`matt-implement` 驱动 `matt-tdd`，收尾 `matt-code-review`。）

并写一句：不确定从哪开始时，可再显式调用 `matt-skill-flows`。

### 3. 技能一览（主体）

**分类用上方静态索引；扫描只补 `description` / `invocation`，不用于发明分类或技能名单。**

扫描顺序（有则用，缺则跳过）：

1. 从本 `SKILL.md` 向上找到含 `plugin.yaml` 或 `.cursor-plugin/plugin.json` 的插件根，扫描 `skills/*/SKILL.md`
2. 若插件根不可解析，再试 `~/.cursor/plugins/local/matt-agent-skills/skills/*/SKILL.md`
3. 仍没有 frontmatter：表格仍列出静态 id，简介写「未找到 SKILL.md」，禁止编造技能

对每个找到的 `SKILL.md` 解析 YAML frontmatter：

- `name`（技能 id）
- `description`（一句「何时用」）
- `invocation`：`user` = 仅显式调用；`model` = 用户或模型均可按描述触发

按桶输出两个小节（桶内按静态索引顺序），扫描到但不在静态列表中的 id 另开「未分类」：

#### Engineering

#### Productivity

每桶用 Markdown 表格，列：

| 技能 id | 调用 | 简介 |
| ------- | ---- | ---- |

- **调用**列写 `user` 或 `model`（缺省则写 `未知`）
- **简介**列用 frontmatter `description` 原文（可去掉开头的「在以下场景使用：」前缀以更易读）；找不到文件时写「未找到 SKILL.md」
- 本技能 `matt-agent-skills-help` 一并列入，简介可标注「本说明书」

表格前加一句：`user` = 只应显式调用；`model` = 任务匹配时也可由 agent 主动采用其纪律。

### 4. 怎么用（短）

三条即可：

1. 显式调用某个 `matt-*`（或本 help）：Cursor `/技能id`；Claude `/matt-agent-skills:技能id`；Codex `$技能id`
2. 复杂改动：先计划再动手（与用户偏好一致时注明）
3. 某条技能的细节：再显式打开该技能正文，而不是依赖本总览

### 5. 收尾

一句：以上为总览；具体流程、门禁与模板以各 `matt-*/SKILL.md` 为准。

## 反模式

- 把全部技能全文粘进回复
- 未对照磁盘却凭记忆编造静态索引以外的技能
- 解析 README 标题做分桶
- 模型隐式触发本技能
- 用本技能代替 `matt-skill-flows` 做路径决策
