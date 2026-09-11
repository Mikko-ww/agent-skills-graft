---
name: matt-grill-with-docs
description: 对 plan 或设计做 relentless interview（grill），同时边问边产出文档（ADR 与 glossary）。在有工作目录、需要留下 CONTEXT.md / ADR 纸面痕迹时使用。
invocation: user
disable-model-invocation: true
---

# Grill with Docs

同时采用下列两套纪律（不要只做访谈、也不要只写文档）：

1. **matt-grilling**：对 plan、决策或想法做 relentless interview，直到 design tree 的每个分支都被解决。
2. **matt-domain-modeling**：主动打磨 domain 语言，当场更新 `CONTEXT.md`，并在符合门槛时记录 ADR。

先加载（或按同名技能纪律执行）`matt-grilling` 与 `matt-domain-modeling`，再在同一会话中交织推进：每一轮面试既推进 frontier，也把敲定的术语与决策写入文档。

## 与 matt-grill-me 的边界

- 在**有工作目录 / 仓库**时用本技能：有状态，把学到的内容留在 `CONTEXT.md` 与 ADR 中。
- 若**没有**工作目录，改用 `matt-grill-me`（同样基于 `matt-grilling` 原语，但不落盘）。
