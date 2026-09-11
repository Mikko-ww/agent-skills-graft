---
name: matt-resolving-merge-conflicts
description: 解决进行中的 git merge / rebase conflict。在需要处理冲突 hunk、且不要 abort 时使用。
invocation: model
---

1. **看清当前状态**：merge / rebase 走到哪了。检查 git history 与冲突文件。

2. **为每个冲突找到 primary sources。** 深入理解每处改动为何做出、原始意图是什么。读 commit message，查 PR，查原始 issue / ticket。

3. **逐 hunk 解决。** 尽可能同时保留双方意图。若互不相容，选与本次 merge 既定目标一致的一方，并记下 trade-off。**不要**发明新行为。永远解决；从不 `--abort`。

4. 发现项目的 **automated checks** 并运行，通常是 typecheck，然后 tests，然后 format。修好 merge 弄坏的任何东西。

5. **完成 merge / rebase。** Stage 一切并 commit。若在 rebase，继续 rebase 直到所有 commit 完成。
