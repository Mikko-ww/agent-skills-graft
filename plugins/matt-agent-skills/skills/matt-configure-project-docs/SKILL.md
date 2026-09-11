---
name: matt-configure-project-docs
description: 为本仓库配置工程技能所需的文档布局：issue tracker、triage 标签词汇、domain 文档结构。在首次使用其他工程技能之前运行一次。
invocation: user
disable-model-invocation: true
---

# Configure Project Docs

为工程技能脚手架好仓库级配置，它们依赖这些约定：

- **Issue tracker**：议题存放位置（默认 GitHub；本地 markdown 开箱可用）
- **Triage labels**：五个规范 triage 角色所用的字符串
- **Domain docs**：`CONTEXT.md` 与 ADR 的位置，以及读取它们的消费规则

这是提示驱动的技能，不是确定性脚本。先探索、展示发现、与用户确认，再写入。

## 流程

### 1. 探索

查看当前仓库的起始状态。读已有文件，不要假设：

- `git remote -v` 与 `.git/config`：是否 GitHub / GitLab 仓库？是哪一个？
- 根目录的 `AGENTS.md`：是否存在？其中是否已有 `## Agent skills` 小节？
- 根目录的 `CONTEXT.md` 与 `CONTEXT-MAP.md`
- `docs/adr/` 以及任意 `src/*/docs/adr/`
- `docs/agents/`：本技能先前的产出是否已存在？
- `.scratch/`：是否已在用本地 markdown issue tracker 约定？
- 是否已安装 `matt-triage` 技能？（同目录旁有 `matt-triage` 文件夹，或可用技能列表中有 `matt-triage`。）这决定 Section B 是否执行。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 的 `workspaces` 字段，或已有自带 `src/` 的 `packages/*`。这些只在真正大型多包仓库出现；没有则视为单 context（几乎所有仓库都是）。

### 2. 展示发现并提问

总结已有与缺失。按节顺序推进：一节一个答案，再下一节。

每节先给出推荐答案，方便用户一词确认。仅当选择真正分叉时给一行说明；探索已裁定则整节跳过（未安装 `matt-triage` 则跳过 Section B；非 monorepo 则跳过 Section C 的提问）。

**Section A: Issue tracker。**

> 说明：issue tracker 是本仓库议题的存放处。`matt-to-tickets`、`matt-triage`、`matt-to-spec` 等技能会读写它。它们需要知道是调用 `gh issue create`、在 `.scratch/` 下写 markdown，还是按你描述的其他工作流。选你**实际**用来跟踪本仓库工作的地方。

默认姿态：这些技能为 GitHub 设计。若 `git remote` 指向 GitHub，提议 GitHub。若指向 GitLab（`gitlab.com` 或自托管），提议 GitLab。否则（或用户另有偏好）提供：

- **GitHub**：议题在仓库的 GitHub Issues（用 `gh` CLI）
- **GitLab**：议题在仓库的 GitLab Issues（用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **Local markdown**：议题为仓库内 `.scratch/<feature>/` 下的文件（适合 solo 项目或无 remote 的仓库）
- **Other**（Jira、Linear 等）：请用户用一段话描述工作流；技能以自由散文记录

选择写入 `docs/agents/issue-tracker.md`。GitHub / GitLab 模板带有「PRs / MRs as a request surface」开关，默认**关闭**。保持关闭且不要主动提起：若用户希望外部 PR/MR 进入 matt-triage 队列，可稍后在文件里打开。

**Section B: Triage label vocabulary。** 若未安装 `matt-triage`（探索已知），整节跳过，因为未安装的技能不需要标签。

若已安装，只问一题：

> 是否保留默认 triage 标签？（推荐：**是**）

默认即五个规范角色，标签字符串与角色名相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。答「是」则原样写入。仅当用户说不（通常因 tracker 已有其他命名，例如用 `bug:matt-triage` 表示 `needs-triage`）时，收集覆盖项，让 `matt-triage` 复用已有标签而不是制造重复。

**Section C: Domain docs。** 默认 **single-context**（根目录一份 `CONTEXT.md` + `docs/adr/`）。这适合几乎所有仓库；直接写入，不必提问。

仅当探索发现 monorepo 信号时，才提供 **multi-context**（根目录 `CONTEXT-MAP.md` 指向各 context 的 `CONTEXT.md`），并确认用户想要的布局。

### 3. 确认并编辑

向用户展示草稿：

- 将写入 `AGENTS.md` 的 `## Agent skills` 块（选文件规则见步骤 4）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md`、以及（仅当安装了 `matt-triage`）`docs/agents/matt-triage-labels.md` 的内容

写入前允许用户修改。

### 4. 写入

**选择要编辑的文件（优先 AGENTS.md）：**

- 若存在 `AGENTS.md`，编辑它。
- 否则若存在 `AGENTS.md`，编辑它。
- 若两者都不存在，优先创建 `AGENTS.md`；不要静默创建两者。

始终编辑 `AGENTS.md`；不要另建 Claude 专用说明文件。

若所选文件已有 `## Agent skills` 块，就地更新内容，不要追加重复块。不要覆盖周围小节的用户编辑。

块内容：

```markdown
## Agent skills

### Issue tracker

[一行总结议题存放位置]。见 `docs/agents/issue-tracker.md`。

### Triage labels

[一行总结标签词汇]。见 `docs/agents/matt-triage-labels.md`。

### Domain docs

[一行总结布局："single-context" 或 "multi-context"]。见 `docs/agents/domain.md`。
```

仅当安装了 `matt-triage` 且跑过 Section B 时，才包含 `### Triage labels` 子块并写入 `docs/agents/matt-triage-labels.md`；否则两者都省略。

然后用本技能目录中的种子模板写入 docs 文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 markdown issue tracker
- [triage-labels.md](./triage-labels.md)：标签映射（仅当安装了 `matt-triage`）
- [domain.md](./domain.md)：domain 文档消费规则与布局

对于「other」issue tracker，根据用户描述从零撰写 `docs/agents/issue-tracker.md`。

### 5. 完成

告知用户配置已完成，以及哪些工程技能会读取这些文件。说明之后可直接编辑 `docs/agents/*.md`；仅在想切换 issue tracker 或从头重配时才需要再跑本技能。
