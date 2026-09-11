---
name: matt-wait-what
description: 停下。上一条消息没有落地；用更清楚的方式重新表述（re-pitch）。用户说 wait what、没听懂、再讲一遍时使用。
invocation: user
disable-model-invocation: true
---

等一下，我还不清楚你已经走到哪一步了。重新表述（re-pitch）刚才那条内容：

1. 先给一点上下文（你在回答什么、依赖哪些前提）。
2. 用 ASD-STE100 Simplified Technical English 风格书写：短句、常用词、一词一义、避免模糊修饰。
3. 使用 `CONTEXT.md` 中的 ubiquitous language（若仓库有多份上下文，按 `CONTEXT-MAP.md` 找到正确那一份）。

不要辩解，不要引入新决策；只把同一意思讲清楚，直到用户能接着做下一步。
