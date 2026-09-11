# Issue tracker: GitLab

本仓库的议题与 Spec 存放在 GitLab Issues。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建议题**：`glab issue create --title "..." --description "..."`。多行 description 用 heredoc。传 `--description -` 可打开编辑器。
- **读取议题**：`glab issue view <number> --comments`。机器可读输出用 `-F json`。
- **列出议题**：`glab issue list -F json`，配合适当的 `--label`。
- **评论议题**：`glab issue note <number> --message "..."`。GitLab 称评论为 notes。
- **添加 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可用逗号分隔或重复该 flag。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，因此先用 `glab issue note <number> --message "..."` 说明，再关闭。
- **Merge requests**：GitLab 称 PR 为 merge requests。用 `glab mr create`、`glab mr view`、`glab mr note` 等，形态与 `gh pr ...` 相同，把 `pr` 换成 `mr`，把 `comment`/`--body` 换成 `note`/`--message`。

从 `git remote -v` 推断仓库；在 clone 内运行时 `glab` 会自动推断。

## Merge requests 作为 triage 表面

**MRs as a request surface: no。** _（若本仓库把外部 merge request 当作 feature request，设为 `yes`；`matt-triage` 会读此开关。）_

设为 `yes` 时，MR 走与议题相同的标签与状态，使用 `glab mr` 等价命令：

- **读取 MR**：`glab mr view <number> --comments`，以及 `glab mr diff <number>` 看 diff。
- **列出待 triage 的外部 MR**：`glab mr list -F json`，只保留作者不是项目成员/owner 的 MR（贡献者的 MR，而非维护者进行中的工作）。
- **评论 / 标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 的 issue 与 MR 编号空间分离，因此一旦知道是哪条表面，`#42` 无歧义。

## 当技能说「发布到 issue tracker」

创建一条 GitLab issue。

## 当技能说「拉取相关 ticket」

运行 `glab issue view <number> --comments`。

## Wayfinding 操作

供 `matt-wayfinder` 使用。**map** 是一条议题，**child** 议题是 tickets。

- **Map**：带 `matt-wayfinder:map` 标签的单条议题，正文含 Notes / Decisions-so-far / Fog。`glab issue create --label matt-wayfinder:map`。（在支持原生 epic 的 GitLab 层级上，也可用 epic 承载 map；带标签的议题处处可用。）
- **Child ticket**：描述顶部带 `Part of #<map>`，标签 `matt-wayfinder:<type>`（`matt-research` / `matt-prototype` / `matt-grilling` / `task`）。认领后指派给驱动开发者。
- **Blocking**：GitLab **原生 blocking link**，规范且 UI 可见。用 `/blocked_by #<n>` quick action 添加，作为 note 发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生 blocking links 是 Premium/Ultimate 功能；免费层（或不可用时）回退为描述顶部的 `Blocked by: #<n>, #<n>` 行。当每个 blocker 都关闭时，ticket 才 unblocked。
- **Frontier 查询**：`glab issue list -F json` 限定到 map 的 children，丢掉仍有开放 blocker 的项：指向开放议题的原生 `blocked_by` 链接（`glab api projects/:id/issues/:iid/links`），或 `Blocked by` 行中仍开放的议题，或已有 assignee；按 map 顺序取第一个。
- **Claim**：`glab issue update <n> --assignee @me`，会话的首次写入。
- **Resolve**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再把 context 指针（摘要 + 链接）追加到 map 的 Decisions-so-far。
