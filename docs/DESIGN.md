# agent-skills-graft · 设计文档

> 2026-09-10 · 状态：Phase 0 已落地（skills 全局分发）

## 1. 问题

我会持续积累大量 agent 资产（skill、subagent、command、rule、plugin），并同时使用多个平台
（Claude Code、Codex、Cursor、OpenCode、pi……）。每个平台读取资产的目录不同、格式略有差异，
而且资产要按需分发：有的全局可用，有的只给某个项目，有的只给某个平台。手动复制不可持续：

- 同一技能出现多份分叉副本（曾经的 `~/.codex/skills/gh-search-projects` vs `~/.agents/skills/searching-github-projects`）。
- 技能散落在 5 个目录，部分平台（Claude/Cursor/OpenCode 的全局目录）根本没吃到。
- 平台插件各自缓存，版本漂移。

## 2. 结论：不造安装器，造"仓库 + 清单 + 薄胶水"

调研结论（Star 数为 2026-09-10 实时核验）：

| 项目 | Stars | 对本方案的角色 |
|---|---|---|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 30.8k | 事实标准的 skill 安装器（79 个 agent）。**外部技能**直接委托给它。 |
| [eljulians/skillfile](https://github.com/eljulians/skillfile) | 145 | 声明式 `Skillfile` + lock + patch 的思路，是 profile 格式的参考。 |
| [dyoshikawa/rulesync](https://github.com/dyoshikawa/rulesync) | 1.4k | rules/commands/mcp/subagents/hooks 的多平台生成器，Phase 3 接入。 |
| [intellectronica/ruler](https://github.com/intellectronica/ruler) | 2.9k | rules + MCP 分发，与 rulesync 二选一。 |

关键源码发现（`vercel-labs/skills/src/installer.ts`）：其 symlink 模式并不是链到你的源目录，而是先
**copy** 到规范目录 `~/.agents/skills/<name>`，再从各平台目录 symlink 过去。因此仓库里改了
SKILL.md 不会实时生效。这决定了本仓库自有技能由 `graft` **直接 symlink 到仓库**，只有外部技能才交给它。

## 3. 架构

```
agent-skills-graft/
├── skills/                   # vault：自有技能，SKILL.md 目录（agentskills.io 格式）
├── profiles/
│   ├── global.yaml           # 机器级：什么 → 哪个平台的全局目录
│   └── projects/<name>.yaml  # 项目级（Phase 2）
├── src/graft/                # CLI（Python 3.11+，uv）
│   ├── platforms.py          #   平台注册表：各平台 project/global skills 目录
│   ├── vault.py              #   仓库根定位、技能发现、frontmatter 解析
│   ├── profile.py            #   YAML 清单加载/校验/回写（ruamel，保留注释）
│   ├── engine.py             #   plan / apply：对比清单与磁盘，幂等修正
│   ├── importer.py           #   graft import：收编散落技能
│   ├── external.py           #   委托 `npx skills add`
│   └── fsutil.py             #   symlink、备份、目录等价比较
├── docs/DESIGN.md
└── README.md
```

### 3.1 三类资产、三条通道

| 资产 | 通道 | 说明 |
|---|---|---|
| vault 内 skill | `graft` 直接 symlink：`<平台目录>/<name> → <repo>/skills/<name>` | 编辑即生效；绝对路径；仓库移动后重新 `apply` 即可 |
| 外部 skill（`source: owner/repo`） | `npx -y skills@latest add <source> --skill <name> -a <平台…> -g -y` | 不 vendor；由其 `~/.agents/.skill-lock.json` 记录 hash；更新用 `npx skills update` |
| plugin / rules / MCP / pi extension | Phase 1–3 | 见路线图 |

### 3.2 平台路径（与 vercel skills 一致）

| id | 项目级 | 全局 |
|---|---|---|
| `claude-code` | `.claude/skills` | `$CLAUDE_CONFIG_DIR|~/.claude/skills` |
| `codex` | `.agents/skills` | `$CODEX_HOME|~/.codex/skills` |
| `cursor` | `.agents/skills` | `~/.cursor/skills` |
| `opencode` | `.agents/skills` | `$XDG_CONFIG_HOME/opencode/skills` |
| `pi` | `.pi/skills` | `~/.pi/agent/skills` |
| `gemini-cli` / `antigravity` / `github-copilot` | `.agents/skills` | `~/.gemini/skills` / `~/.gemini/antigravity/skills` / `~/.copilot/skills` |
| `universal` | `.agents/skills` | `~/.agents/skills`（vercel skills 的规范目录，amp/cline/zed 读取） |

项目级里 Codex / Cursor / OpenCode 共用 `.agents/skills`，一个 symlink 三家共享。

### 3.3 清单格式

```yaml
targets: [claude-code, codex, cursor, opencode, universal]

skills:
  searching-github-projects: { to: [codex, cursor] }   # vault 技能
  mcp-builder: { to: "*" }                             # "*" = 全部 targets
  frontend-design:                                     # 外部技能
    source: anthropics/skills
    to: [cursor, claude-code]
  pdf: [codex]                                         # 简写
```

### 3.4 无状态的 drift 检测

不维护 lock。"被 graft 管理"的定义是：**该路径是 symlink，且解析后落在 `<repo>/skills/` 内**。
据此可以纯靠文件系统判定：

| state | 含义 | `apply` 动作 |
|---|---|---|
| `ok` | 已链接 / 外部技能已存在 | 无 |
| `link` | 目标不存在 | 建链 |
| `relink` | 是 symlink 但指向别处 / 断链 | 重建 |
| `adopt` | 真实目录且与 vault 内容一致 | 备份后换成 symlink |
| `conflict` | 真实目录且内容不同 | 报错；`--force` 备份后换链 |
| `external-missing` | 外部技能缺失 | 分组调用 `npx skills add` |
| `orphan` | 指向 vault 但清单未声明 | `--prune` 删除 |
| `not-in-vault` | 清单写了 vault 里没有的技能 | 报错 |

任何被替换的真实目录都移动到 `~/.local/share/graft/backup/<时间戳>/`，永不直接删除。

### 3.5 `graft import` 的收编规则

对每个含 `SKILL.md` 的目录（名字取 frontmatter `name`，回退目录名；平台按路径前缀推断）：

1. 已是指向 vault 的 symlink → 只补清单。
2. 外部技能（`--source` 指定、清单已有 `source`、或出现在 vercel lock 里）→ 文件原地不动，只记 `source` + `to`。
3. vault 中已有同名且内容一致 → 原目录备份，换成 symlink。
4. vault 中已有同名但内容不同 → 报 conflict，跳过（`--rename` 另存）。
5. 新技能 → 移入 `skills/<name>`，在原目录的**规范名**位置留 symlink，写入清单。

## 4. Phase 0 执行记录（2026-09-10）

- `.agents/skills/searching-github-projects` → `skills/`（顶层 vault）。
- 收编：`sora`、`skill-lookup`（原目录名 `skills-lookup`）进入 vault；`figma-use/pdf/playwright` 记为 `openai/skills` 外部；
  `find-skills/mcp-builder/skill-creator/frontend-design` 记为外部（vercel-labs/skills、anthropics/skills）。
- 旧分叉副本 `~/.codex/skills/gh-search-projects` 归档到 `~/.local/share/graft/backup/manual/`。
- 删除 `~/.agents/skills/.git`（GitKraken 残留，非真实仓库）和各处 `.DS_Store`。
- `graft apply` 后 `searching-github-projects` 在 Claude Code / Codex / Cursor / OpenCode / universal 五处全局可用；`graft status` = 14 ok。

## 5. 路线图

**Phase 1 · plugins**
- `plugins/<name>/plugin.yaml` → 生成 `.cursor-plugin/plugin.json`、`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`（三者同构：`name/version/description` + `skills/`、`hooks/`、`.mcp.json`；Cursor 多 `rules/agents/commands`，Codex 多 `apps/interface`）。
- 本仓库注册为三家 marketplace：Claude `claude plugin marketplace add <path>`；Codex `~/.agents/plugins/marketplace.json`；Cursor symlink 到 `~/.cursor/plugins/local/<name>`。
- 清单增加 `plugins:` 段；外部插件（如 superpowers）只记来源，调各平台原生命令安装。

**Phase 2 · 项目级 + 体检**
- `profiles/projects/<name>.yaml`（含 `path:`），`graft apply <name>`；`graft link` 在任意项目目录内生成并应用。
- `graft doctor`：各平台 marketplace 注册状态、CLI 是否在 PATH、断链、`.DS_Store`。
- 引擎已按 `project` 参数抽象，主要是 CLI 与清单发现的工作。

**Phase 3 · rules / MCP / hooks / pi**
- 接 rulesync（生成模式）分发 AGENTS.md / CLAUDE.md / `.cursor/rules` / MCP / hooks。
- 仓库根 `package.json` 增加 `pi` 字段，使 `pi install git:<repo>` 能装 TS extension。
- GitHub Action：`graft plugin build --check` 防止 manifest 漂移。

## 6. 已知取舍

- 清单回写用 ruamel.yaml 保留注释，但被 `import` 改写的条目会丢失该条目自己的行内注释。
- 外部技能的"是否已安装"仅看目标路径是否存在，不校验 hash；版本更新交给 `npx skills update`。
- Windows 未考虑（symlink 权限）。
- `universal` 平台对应 `~/.agents/skills`；vercel skills 新版把 universal agent 的全局目录改成了 `~/.config/agents/skills`，但规范拷贝仍在 `~/.agents/skills`，所以存在性判断不受影响。
