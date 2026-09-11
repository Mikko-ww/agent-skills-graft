# Learning Record 格式

Learning records 存放在 `./learning-records/`，使用顺序编号：`0001-slug.md`、`0002-slug.md` 等。目录惰性创建：仅在写入第一条记录时创建。

它们是教学侧的 ADR 等价物：捕捉非显而易见的教训、关键洞察、以及已声明的先验知识，用以驾驭未来会话。用于计算 zone of proximal development。

## Template

```md
# {所学或所确立内容的短标题}

{1–3 句：学到了什么（或确立了什么先验知识），以及为何对未来会话重要。}
```

这就是全部格式。一条 learning record 可以只有一段。价值在于记录「现在已知」以及「为何改变下一步教什么」，而不是填满章节。

## Optional sections

仅在真正增值时加入。多数记录不需要。

- **Status** frontmatter（`active | superseded by LR-NNNN`）：当早期理解被证伪并被替换时有用。
- **Evidence**：用户如何证明理解（答对问题、完成练习、引用先前经验）。当主张可能被重访时有用。
- **Implications**：这对未来会话解锁或排除了什么。非显而易见时值得记录。

## Numbering

扫描 `./learning-records/` 中已有最大编号，再加一。

## When to write a learning record

满足任一条件时写入：

1. **用户对某非琐碎内容表现出真正理解**：不只是接触过，而是有证据能正确使用该概念。这为下一步教学设定新地板。
2. **用户披露先验知识**：「我已经会 X。」记录下来，避免未来重教。同时记录所声称的 **depth**。
3. **纠正了误解**：用户先前信错了某事，现在明白为何错。高价值：可预测相关主题的未来绊脚石。
4. **Mission 因学习而偏移**：用户发现自己真正在意的与原先设想不同。交叉链接到 [[MISSION.md]] 并更新它。

### What does _not_ qualify

- 仅仅「覆盖过」的材料。Coverage 不是 learning。等待证据。
- 已在 [[GLOSSARY.md]] 中作为术语定义简洁捕捉的内容。不要重复。
- 逐会话活动日志。Learning records 不是日记：它们是决策级洞察。

## Supersession

当后来的记录与早期矛盾（理解加深或被纠正）时，将旧记录标为 `Status: superseded by LR-NNNN`，不要删除。理解如何演化的历史本身就是有用信号。
