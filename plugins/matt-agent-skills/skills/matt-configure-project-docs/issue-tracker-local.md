# Issue tracker: Local Markdown

本仓库的议题与 Spec 存放为 `.scratch/` 下的 markdown 文件。

## 约定

- 每个功能一个目录：`.scratch/<feature-slug>/`
- Spec 为 `.scratch/<feature-slug>/spec.md`
- 实现议题为每个 ticket 一个文件：`.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 起编号，绝不用单一合并的 tickets 文件
- Triage 状态记在每个议题文件靠近顶部的 `Status:` 行（角色字符串见 `triage-labels.md`）
- 评论与对话历史追加到文件底部的 `## Comments` 标题下

## 当技能说「发布到 issue tracker」

在 `.scratch/<feature-slug>/` 下新建文件（目录不存在则创建）。

## 当技能说「拉取相关 ticket」

读取引用路径处的文件。用户通常会直接给出路径或议题编号。

## Wayfinding 操作

供 `matt-wayfinder` 使用。**map** 是一个文件，每个 ticket 一个 **child** 文件。

- **Map**：`.scratch/<effort>/map.md`（Notes / Decisions-so-far / Fog 正文）。
- **Child ticket**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 起编号，问题写在正文。`Type:` 行记录 ticket 类型（`matt-research` / `matt-prototype` / `matt-grilling` / `task`）；`Status:` 行记录 `claimed` / `resolved`。
- **Blocking**：靠近顶部的 `Blocked by: NN, NN` 行。当所列每个文件都是 `resolved` 时，ticket 才 unblocked。
- **Frontier**：扫描 `.scratch/<effort>/issues/`，找仍开放、未阻塞、未认领的文件；按编号取第一个。
- **Claim**：设 `Status: claimed` 并保存，再开始任何工作。
- **Resolve**：在 `## Answer` 标题下追加答案，设 `Status: resolved`，再把 context 指针（摘要 + 链接）追加到 `map.md` 的 Decisions-so-far。
