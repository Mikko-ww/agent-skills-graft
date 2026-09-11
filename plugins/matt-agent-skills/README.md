# Matt Agent Skills

面向 coding agent 的工程与生产力技能包。技能 id 均以 `matt-` 为前缀。正文多为简体中文，技术领域专有名词保留英文。

主链路：`matt-grill-with-docs` → `matt-to-spec` → `matt-to-tickets` → `matt-implement`（实现时驱动 `matt-tdd`，收尾 `matt-code-review`）。不确定从哪开始时，显式调用 `matt-skill-flows`。

`graft` **尚未管理**本插件。本仓库只存放内容；本机 Cursor 用下面的安全流程接到 `~/.cursor/plugins/local/`。

## 本机启用（Cursor）

目标：`~/.cursor/plugins/local/matt-agent-skills`  
源：本目录（仓库内 `plugins/matt-agent-skills`）

1. `mkdir -p ~/.cursor/plugins/local`
2. 按目标类型处理：
   - 不存在：`ln -s <源> <目标>`（不要 `-f`）
   - 已是 symlink 且 `realpath` 等于源：不操作
   - 已是 symlink 但指向别处或断链：`unlink` 后 `ln -s`
   - 普通文件或真实目录：先 `mkdir -p ~/.local/share/graft/backup/<时间戳>`，再把目标 **mv** 为该目录下的 `matt-agent-skills`，然后 `ln -s`
3. 确认 `test -L` 为真，且 `realpath` 等于源

不要用裸 `ln -sfn`：`-f` 可能删掉普通文件。

## 调用

| 平台 | 写法 |
| --- | --- |
| Cursor | `/技能id` |
| Claude | `/matt-agent-skills:技能id` |
| Codex | `$技能id` |

`invocation: user`：只应显式调用（Cursor / Claude 为 `disable-model-invocation: true`；Codex 为 `policy.allow_implicit_invocation: false`）。  
`invocation: model`：任务匹配时也可由 agent 主动采用。

## Engineering

User：`matt-skill-flows`、`matt-grill-with-docs`、`matt-triage`、`matt-improve-codebase-architecture`、`matt-configure-project-docs`、`matt-to-spec`、`matt-to-tickets`、`matt-implement`、`matt-wayfinder`

Model：`matt-prototype`、`matt-diagnosing-bugs`、`matt-research`、`matt-tdd`、`matt-domain-modeling`、`matt-codebase-design`、`matt-code-review`、`matt-resolving-merge-conflicts`、`matt-wizard`

## Productivity

User：`matt-grill-me`、`matt-agent-skills-help`、`matt-handoff`、`matt-teach`、`matt-to-questionnaire`、`matt-wait-what`

Model：`matt-grilling`、`matt-writing-for-agents`
