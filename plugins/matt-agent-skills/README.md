# Matt Agent Skills

面向 coding agent 的工程与生产力技能包。技能 id 均以 `matt-` 为前缀。正文多为简体中文，技术领域专有名词保留英文。

主链路：`matt-grill-with-docs` → `matt-to-spec` → `matt-to-tickets` → `matt-implement`（实现时驱动 `matt-tdd`，收尾 `matt-code-review`）。不确定从哪开始时，显式调用 `matt-skill-flows`。

## 本机启用（Cursor）

由 `graft` 管理。清单 `profiles/global.yaml` 里已声明：

```yaml
plugins:
  matt-agent-skills: { to: [cursor] }
```

```bash
uv run graft status        # 插件行显示 copy / sync / ok
uv run graft apply         # 拷贝到 ~/.cursor/plugins/local/matt-agent-skills
```

这是**拷贝**不是 symlink：Cursor 的本地插件加载器对 `~/.cursor/plugins/local/` 下的每个条目做
`realpath` 校验，指向目录外的软链会被 `rejected: symlink target … is outside` 拒绝（可在
`Cursor Plugins.log` 里看到）。因此改了本目录任何文件后，需要再跑一次 `graft apply`；`status` 会把过期的
拷贝标为 `sync`，重新拷贝前旧副本会移到 `~/.local/share/graft/backup/<时间戳>/cursor-plugins/`。
Cursor 会在几秒内自动重新扫描本地插件目录，不需要重启。

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
