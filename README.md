# agent-skills-graft

一个仓库存放我所有的 agent 资产（目前是 skill；接下来是 agent / command / rule / plugin），
通过声明式清单"嫁接"到我使用的各个平台——Claude Code、Codex、Cursor、OpenCode、pi——
而不是手动复制。

```
skills/                  # 金库（vault）：SKILL.md 目录，agentskills.io 格式
profiles/global.yaml     # 机器级清单：什么装到哪个平台
profiles/projects/*.yaml # 项目级清单（Phase 2）
src/graft/               # graft 命令行（Python，uv）
docs/DESIGN.md           # 调研、架构、路线图
```

## 安装

```bash
uv sync                      # 开发方式：之后用 `uv run graft ...`
uv tool install -e .         # 或者把 `graft` 装到 PATH
```

## 使用

```bash
graft status                 # 对比清单与磁盘，不改任何东西
graft apply --dry-run        # 只看计划
graft apply                  # 金库技能建 symlink，外部技能走 `npx skills add`
graft apply --prune          # 同时删除清单里已不存在的金库 symlink
graft import ~/.codex/skills # 把散落的技能收编进金库和清单
graft platforms              # 各平台读取全局技能的目录
graft skills                 # 金库里有什么
```

金库里的技能是直接 **symlink** 到各平台技能目录的，改一处 `skills/` 立即处处生效。
外部技能（`source: owner/repo`）不入库，`graft` 委托 [`npx skills add`](https://github.com/vercel-labs/skills)
安装，由它维护自己的 lock 文件。

任何东西都不会被直接删除：被 `graft` 替换掉的真实目录会移到
`~/.local/share/graft/backup/<时间戳>/`。

## 清单格式

```yaml
targets: [claude-code, codex, cursor, opencode, universal]

skills:
  searching-github-projects: { to: [codex, cursor] }   # 金库技能
  mcp-builder: { to: "*" }                             # 全部 targets
  frontend-design:                                     # 外部技能
    source: anthropics/skills
    to: [cursor, claude-code]
```

完整设计与路线图见 [docs/DESIGN.md](docs/DESIGN.md)。
