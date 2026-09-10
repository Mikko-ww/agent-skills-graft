# AGENTS.md · agent-skills-graft

> 给接手本仓库的 AI agent / 开发者看的交接文档。先读完本文件，再看 `docs/DESIGN.md`。
> 语言约定：本仓库所有面向人的文字（文档、注释、CLI 文案、自有技能）以**简体中文**为主。

## 1. 这个仓库是什么

一个"金库 + 清单 + 薄胶水"：

- **金库（vault）** `skills/`：我自己维护的 agent 资产的唯一事实来源（目前只有 skill；后续加 agents / commands / rules / plugins）。
- **清单（profile）** `profiles/*.yaml`：声明"哪个资产 → 装到哪个平台 → 全局还是某项目"。
- **胶水** `graft` CLI（Python 3.11 + uv）：读清单、对比磁盘、把差异补齐。金库技能直接 **symlink** 到各平台目录；外部技能委托 `npx skills add`（vercel-labs/skills）。

它**不是**新的安装器、不是技能市场、不 vendor 第三方技能。

## 2. 目录结构

```
agent-skills-graft/
├── AGENTS.md                 # 本文件：交接与约束
├── README.md                 # 用户视角的用法
├── docs/DESIGN.md            # 调研结论、架构决策、状态机、路线图（权威设计文档）
├── skills/                   # 金库：每个子目录一个技能，必含 SKILL.md（agentskills.io 格式）
│   ├── searching-github-projects/   # 自有，中文
│   ├── skill-lookup/                # 自有，中文
│   └── sora/                        # 上游原样收编（Apache-2.0），保持英文
├── profiles/
│   ├── global.yaml           # 机器级清单（当前唯一生效的清单）
│   └── projects/<name>.yaml  # 项目级清单（Phase 2，目录尚未创建）
├── src/graft/                # CLI 源码，见 §4
├── pyproject.toml            # uv 项目；入口 graft = graft.cli:app
└── uv.lock
```

## 3. 核心概念与不变量

| 概念 | 定义 | 不变量 |
|---|---|---|
| 金库技能 | `skills/<name>/SKILL.md` 存在 | 名字取 frontmatter `name`，回退目录名；目录名应与 `name` 一致 |
| 外部技能 | 清单里带 `source: owner/repo` | **不入库**，文件由 `npx skills add` 放置；graft 只判断目标路径是否存在 |
| 被 graft 管理 | 目标路径是 symlink，且 `resolve()` 落在 `<repo>/skills/` 内 | 由此无状态判定 ok / orphan，**没有 lock 文件**，也不要加 |
| 备份 | 任何被替换的真实目录移到 `~/.local/share/graft/backup/<时间戳>/` | **永不直接删除用户文件**；symlink 可直接 unlink |
| 平台 id | 与 vercel `skills` CLI 的 `--agent` 名一致 | 新增平台必须沿用其命名，路径以其 `src/agents.ts` 为准 |

### 平台路径（`src/graft/platforms.py`）

| id | 项目级 | 全局 |
|---|---|---|
| `claude-code` | `.claude/skills` | `$CLAUDE_CONFIG_DIR` 或 `~/.claude/skills` |
| `codex` | `.agents/skills` | `$CODEX_HOME` 或 `~/.codex/skills` |
| `cursor` | `.agents/skills` | `~/.cursor/skills` |
| `opencode` | `.agents/skills` | `$XDG_CONFIG_HOME/opencode/skills` |
| `pi` | `.pi/skills` | `~/.pi/agent/skills` |
| `gemini-cli` / `antigravity` / `github-copilot` | `.agents/skills` | `~/.gemini/skills` / `~/.gemini/antigravity/skills` / `~/.copilot/skills` |
| `universal` | `.agents/skills` | `~/.agents/skills`（vercel skills 的规范目录） |

## 4. 代码地图（`src/graft/`）

| 文件 | 职责 | 改动时注意 |
|---|---|---|
| `platforms.py` | 平台注册表、路径展开、按路径反推平台 | 路径模板用 `$HOME/$XDG_CONFIG_HOME/$CLAUDE_HOME/$CODEX_HOME` 占位，运行时展开，便于测试时用假 HOME |
| `vault.py` | 定位仓库根（`$GRAFT_HOME` → 向上找 `profiles/`+`skills/` → 包所在仓库）、枚举技能、解析 frontmatter | `Vault.contains()` 是"被管理"判定的唯一依据 |
| `profile.py` | 加载/校验/回写清单（ruamel.yaml，保留注释） | `to: "*"` 展开为 `targets`；`to` 里的平台必须在 `targets` 内，否则报错 |
| `engine.py` | `plan()` 产出 `Action` 列表；`apply()` 执行 | 状态机见下表；新增状态要同步 `cli._STATE_STYLE` |
| `importer.py` | `graft import` 收编逻辑 | 外部来源判定顺序：`--source` → 清单已有 `source` → `~/.agents/.skill-lock.json` |
| `external.py` | 组装并执行 `npx -y skills@latest add …` | 按 (source, skill) 分组，一次传多个 `--agent` |
| `fsutil.py` | symlink、备份、递归目录等价比较（忽略 `.DS_Store/.git/__pycache__`） | symlink 用绝对路径 |
| `cli.py` | typer 命令：`status / apply / import / platforms / skills` | 文案中文；`status` 有差异时退出码 1 |

### 状态机（`engine.State`）

| state | 含义 | `apply` 动作 |
|---|---|---|
| `ok` | 已链接 / 外部技能已存在 | 无 |
| `link` | 目标不存在 | 建 symlink |
| `relink` | 是 symlink 但指向别处或断链 | 重建 |
| `adopt` | 真实目录且内容与金库一致 | 备份 → symlink |
| `conflict` | 真实目录且内容不同 | 报错退出 1；`--force` 时备份 → symlink |
| `external-missing` | 外部技能不存在 | 调 `npx skills add`（`--no-external` 跳过） |
| `orphan` | 指向金库但清单未声明 | 仅 `--prune` 时 unlink |
| `not-in-vault` | 清单声明了金库里没有的技能 | 报错退出 1 |
| `error` | 文件系统操作失败 | 记录并继续，最终退出 1 |

## 5. 日常工作流

```bash
uv sync                          # 首次
uv run graft status              # 看差异（退出码 1 = 有事要做）
uv run graft apply -n            # 预演
uv run graft apply               # 执行
uv run graft apply --prune       # 顺带清孤儿链接
uv run graft import <path> [-n] [--source owner/repo] [--to a,b] [--rename x]
```

**新增一个自有技能**：`skills/<name>/SKILL.md`（frontmatter `name` 与目录同名）→ 在 `profiles/global.yaml` 的 `skills:` 加一行 → `graft apply`。

**新增一个外部技能**：在清单加 `source` + `to` → `graft apply`（会联网调 npx）。**不要**把第三方技能拷进 `skills/`。

**更新外部技能**：`npx skills update`，不归 graft 管。

## 6. 验证要求

- 改 `src/graft/` 后必须通过：`uvx ruff format src/ && uvx ruff check src/`。
- 手工验证用**隔离环境**，不要直接对真实 HOME 试错：
  ```bash
  export HOME=/tmp/x/home GRAFT_HOME=/tmp/x/vault XDG_CONFIG_HOME=$HOME/.config XDG_DATA_HOME=$HOME/.local/share
  ```
  流程覆盖：import（moved / linked / external / conflict）→ apply（link / adopt / conflict → `--force`）→ 删清单条目 → orphan → `--prune` → 再跑 `status` 应为全 ok。
- 对真实机器执行前先 `-n` 预演；完成后 `graft status` 退出码必须为 0。
- 验证脚本放在仓库外（`/tmp`），不要提交。仓库目前**没有** `tests/`，若要加请用 pytest + `tmp_path`，并复用上面的隔离环境思路。

## 7. 硬性约束

1. **不删除用户文件**：只 unlink symlink；真实目录一律走 `fsutil.backup()`。
2. **不引入 lock/状态文件**：管理状态从文件系统推导。
3. **外部技能不入库**；如需本地修改上游技能，先 fork 或放到 `skills/` 并去掉 `source`，二者不可并存。
4. **平台 id 与路径跟随 vercel-labs/skills**，不自造命名。
5. **不碰 `~/.codex/skills/.system/`**（Codex 内置技能）。
6. 清单回写只通过 `Profile.add_skill()/save()`，保留注释；不要用 `yaml.safe_dump` 重写。
7. 中文优先（见 `docs/DESIGN.md` §6）；机器值（状态名、平台 id、标识符）保持英文。
8. 提交信息用中文，一次提交一个主题。

## 8. 路线图与接手点

详细见 `docs/DESIGN.md` §5。摘要：

- **Phase 1 · plugins**：`plugins/<name>/plugin.yaml` 生成三家 manifest（`.cursor-plugin/plugin.json`、`.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`）；本仓库注册为三家 marketplace（Claude `claude plugin marketplace add <path>`；Codex `~/.agents/plugins/marketplace.json`；Cursor symlink 到 `~/.cursor/plugins/local/<name>`）；清单加 `plugins:` 段。
- **Phase 2 · 项目级**：`profiles/projects/<name>.yaml`（含 `path:`），`graft apply <name>`；`graft link` 在项目目录内生成清单；`graft doctor`。引擎已按 `profile.project` 抽象，主要是 CLI 与清单发现的工作。
- **Phase 3 · rules / MCP / hooks / pi**：接 rulesync 生成 AGENTS.md / CLAUDE.md / `.cursor/rules` / MCP；根 `package.json` 加 `pi` 字段；CI 跑 `graft plugin build --check`。

接手任一阶段前：先 `uv run graft status` 确认当前机器状态干净；再读 `docs/DESIGN.md` 对应小节；新增功能沿用"plan 产出 Action → apply 执行"的模式，不要绕过 `engine`。

## 9. 已知坑

- vercel `skills` 的 symlink 模式会把技能**复制**到 `~/.agents/skills/<name>` 再链过去，不是链到源仓库；所以自有技能必须由 graft 自己建链，否则改动不实时。
- 技能目录名与 frontmatter `name` 不一致时，`import` 以 `name` 为准，并在原目录**规范名**位置留 symlink（历史上 `skills-lookup/` → `skill-lookup`）。
- `universal` 平台对应 `~/.agents/skills`；vercel 新版把 universal agent 的全局目录改成 `~/.config/agents/skills`，但规范拷贝仍在 `~/.agents/skills`，存在性判断不受影响。
- 沙箱环境可能禁止写 `~/.cursor`，本地验证时若报 `Operation not permitted`，是沙箱而非代码问题。
- 清单被 `import` 改写的条目会丢失该条目自身的行内注释（ruamel 局限）。
- Windows 未考虑（symlink 权限）。
