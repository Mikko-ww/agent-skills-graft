# Phase boundaries

一个 **phase** 是会话内的一块工作：matt-grilling、实现、QA。定义故意模糊：当你觉得「好，这块告一段落」时，phase 就结束了。

**Phase boundary** 是两个 phase 之间的空隙，也是本决策唯一该出现的地方。Phase 中途没有决策：继续，或把剩下的工作拆给 background worker。在 phase 中途压缩或清空上下文会让 agent 丢掉线索。

## 四项选择

| 选项 | 做什么 |
| ---- | ------ |
| **Continue** | 留在本会话。完全不切换上下文。 |
| **New chat** | 开启新会话。上下文对下一步无价值时用空会话；仍相关时把简短 brief / 摘要带进新会话。 |
| **`matt-handoff`** | 写出可移植的 markdown 文件，用它在任意处播种新会话。 |
| **Background worker** | 把任务送到独立上下文窗口，拿回报告（后台子代理 / 并行 worker）。 |

不使用特定产品的清空窗口或压缩上下文命令名。语义上：丢弃窗口 ≈ **new chat（空）**；压缩后继续 ≈ **new chat（带 brief）**。

## 决策树

在 boundary 处自上而下。第一个 **是** 胜出。

**1. 能否在本会话继续？** 两件事让答案为是：下一 phase 需要本 phase 作为 **primary source**，或你仍有足够 [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)（约 ~150k tokens）装下下一 phase。Grilling → 实现是标准的「是」：实现想要推理原文，而不是其摘要。Continue 零成本零损失，因此先排除它再考虑别的。

**2. 上下文对下一步是否无关？** 本会话里的一切（探索、决策、死胡同）是否都可丢弃？若是，开 **new chat（空）**。这是棋盘上最便宜的一手：不花时间，拿回整个窗口。旧会话通常仍可回头查看，但新工作从空白开始。

判错的代价是单向的。清空*仍相关*的上下文，你会丢掉构建背后的 **why**，再怎么回读 diff 也找不回来。

**3. 是否需要 matt-handoff？** `matt-handoff` 很窄。仅当你：

- 换到**新 harness**（例如换到另一套 agent 产品），
- 移到**新目录**或新仓库，
- 把工作交给**同事**，
- 或在 **phase 中途** 分出旁支任务、又不想带偏当前工作。

以上就是全部条款。`matt-handoff` 买到的是**可移植性**：一份能旅行的文件。没有东西在旅行，就不需要它。

**4. 任务能否 AFK 完成？** 范围是否紧到可以在你离开键盘、无需掌舵时运行？若是，交给 **background worker**，本会话保持不动。自动化审查是标准场景：worker 读 diff 并报告，过程中不需要你。

**5. 否则，new chat（带 brief）。** 上下文仍相关、同一 harness、同一目录，且你需要继续在环：决策树落在这里，而且经常落在这里。给新会话一条指令（「我们接下来要 QA 这块区域」），让 brief 保住下一 phase 所需内容。

带 brief 的 new chat 是**默认落点，不是第一手**。它在树底，因为上面四个问题都更便宜或更精确。人们一上来就压缩的失败模式是：新会话对摘要压扁的决策自信地犯错。

## Primary 与 secondary sources

除 **Continue** 外，每一手都把 **primary source** 变成 **secondary source**：如实发生的会话，被其摘要取代。交易形状总是一样：

| 来源 | 信息 | 噪声 | 活动空间 |
| ---- | ---- | ---- | -------- |
| Primary（Continue） | 完整 | 很多 | 很少 |
| Secondary（new chat 带 brief、matt-handoff） | 有损 | 更少 | 很多 |

这就是问题 1 排第一的原因。只有当留下的成本大于留下的收益时，才支付有损代价。

## 这些是判断题

问题并不客观：每题都含品味，同一 boundary 两天可以走两条路。价值在于**按顺序**问它们，在 boundary 处问，而不是在工作中间问。
