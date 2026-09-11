---
name: matt-wayfinder
description: 把超出单次 agent 会话容量的大块模糊工作，规划为 issue tracker 上的共享决策 ticket 地图，一次解决一张直到通往 destination 的路清晰。触发词：matt-wayfinder, fog of war, decision ticket, frontier。
invocation: user
disable-model-invocation: true
---

# Wayfinder

一个松散想法到来，大到放不进一次 agent 会话，且裹在雾里：从这里到 **destination** 的路尚看不见。Wayfinding 是找出那条路，而不是冲向 destination。本技能把路画成仓库 issue tracker 上的 **共享地图（map）**，再一次一张地处理其 **decision ticket**（解决物是决策的问题，不是要执行的构建切片），直到路线清晰。

每次努力的 destination 不同；命名它是制图的第一幕：它塑造每张 ticket。可能是待交接迭代的 Spec、规划前要锁定的决策、或就地完成的变更（如数据结构迁移）。地图与领域无关：工程、课程内容，凡形状契合皆可。

## 计划，不要做

Wayfinder **默认是规划**：每张 ticket 解决一个决策；当地图完成、通往 destination 的路已清、再无事可决时结束。想直接动手通常是信号：你已到地图边缘，该交接了。某次努力可在其 **Notes** 中覆盖，把执行带进地图；否则产出决策，不产出交付物。

## 按名称引用

每张地图与 ticket 都是 issue，因而有 **name**：其标题。人类阅读的一切（叙述、地图的 Decisions-so-far）用该名称引用，绝不用裸 id、编号或 slug。一墙 `#42, #43, #44` 不可读；名称一眼可读。id 与 URL 不消失；名称包裹其链接，但它们骑在名称*里面*，绝不代替名称。

## 地图（The Map）

地图是本仓库 issue tracker 上的单条 issue，标签 `matt-wayfinder:map`，是权威产物。其 ticket 是地图的子 issue。

地图是 **index**，不是 store。它列出已做决策并指向持有细节的 ticket；决策只活在一个地方（其 ticket），地图从不重述，只给 gist 并链接。

**地图、子 ticket、blocking 与 frontier 查询的物理落点因 tracker 而异。** issue tracker 配置应由项目提供。若缺失，请用户先运行 `matt-configure-project-docs`。查阅 tracker 文档的 "Wayfinding operations" 节，了解*本*仓库如何表达。若未提供 tracker，默认用本地 markdown tracker。

### 地图正文

整张地图的低分辨率视图，每会话加载一次。**不**列出开放 ticket：它们是开放子 issue，靠查询发现。

```markdown
## Destination

<到达本地图终点的样子：本努力要找到路去往的 Spec、决策或变更。一两行；每会话在选 ticket 前先对齐它。>

## Notes

<领域；每会话应查阅的技能；本次努力的常驻偏好>

## Decisions so far

<!-- 索引：每条已关闭 ticket 一行，足以判断相关性，再点进链接看 ticket 持有的细节 -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- 见 "Fog of war"：尚无法 ticket 化的范围内雾；随 frontier 推进而毕业 -->

## Out of scope

<!-- 见 "Out of scope"：裁定超出 destination 的工作；已关闭，永不毕业 -->
```

### Tickets

每张 ticket 是地图的 **子 issue**；tracker 的 issue id 即其身份。正文是问题，体量适合一次约 100K token 的 agent 会话：

```markdown
## Question

<本 ticket 要解决的决策或调查>
```

每张 ticket 带一个 `matt-wayfinder:<type>` 标签，取自 `matt-research`、`matt-prototype`、`matt-grilling`、`task`（见 Ticket Types）。

会话**认领** ticket 的方式：先把它 assign 给驱动地图的开发者，**在任何工作之前**，以便并发会话跳过。Assignee *即* 认领：开放且未 assign 的 ticket 未认领。

Blocking 使用 tracker 的**原生**依赖关系：关键，因为它在 tracker 自有 UI 中*可视化* frontier，人类无需打开地图即可看到可取项。仅当 tracker 无原生 blocking 时才回退到正文约定。当阻塞它的每张 ticket 都关闭时，该 ticket **unblocked**；**frontier** 是开放、未阻塞、未认领的子 issue，即已知的边缘。

答案不是正文的一部分；在解决时记录（见「推进地图」）。解决过程中创建的资产从 issue 链接，不粘贴进正文。

## Ticket Types

每张 ticket 要么是 **HITL**（human in the loop，与能为自己说话的人类一起做），要么是 **AFK**（agent 独自驱动）。HITL ticket 只通过现场交流解决；agent 绝不代替人类一方（自己回答自己问题的 matt-grilling agent 已破坏此点）。

- **Research**（AFK）：阅读文档、第三方 API 或本地知识库等，浮出决策所等的事实。由子代理 / 后台 worker 采用 **matt-research** 纪律解决。当需要当前工作目录之外的知识时使用。
- **Prototype**（HITL）：用廉价、粗糙、具体的产物提高讨论保真度（大纲、粗稿、桩，或 UI/逻辑代码），采用 **matt-prototype** 纪律。把 matt-prototype 作为资产链接。当关键问题是 "how should it look" 或 "how should it behave" 时使用。
- **Grilling**（HITL）：对话。默认情形。始终同时采用 **matt-grilling** 与 **matt-domain-modeling** 纪律。
- **Task**（HITL 或 AFK）：必须在*决策*做出前发生的手工活：无可决策、matt-prototype 或 matt-research，但讨论被卡住直到做完。注册服务以便评判其 API、开通访问、搬数据以见其形状。这是唯一*做*而非决的类型；它靠解锁决策赢得席位，而非交付 destination。agent 能独自驱动则 AFK；否则交给人类精确清单（HITL）。工作完成即解决；答案记录做了什么及后续 ticket 依赖的事实（凭证位置、新 URL、行数等）。

## Fog of war

地图*故意*不完整：看不见的不要画。现有 ticket 之外是 **fog of war**：你能感到将至但尚钉不住的决策与调查，因为它们挂在仍开放的问题上。解决一张 ticket 会清掉其前方的雾，把现已可规格化的东西毕业为新 ticket，一次一张，直到通往 destination 的路清晰且无 ticket 剩余。

地图的 **Not yet specified** 节写下那层暗景：疑似问题、稍后重访的区域。它是朝向 destination 的未发现 frontier：这里全在范围内，只是还不够锐利无法 ticket。按视野允许写得松或满；也给协作者指路。

**Fog 还是 ticket？** 检验是：你*现在*能否精确陈述问题，*不是*你现在能否回答。

- **可 ticket：** 问题已锐利，即使被阻塞、尚不能行动。
- **Not yet specified：** 尚无法那么锐利地措辞。不要把雾预先切成 ticket 大小：它比 ticket 粗，一块雾可能毕业成多张 ticket，或在 frontier 到达时一张都没有。

**Not yet specified** 排除：已决定的（Decisions so far）、已是活 ticket 的、以及 out of scope（下一节）。

## Out of scope

雾只朝 destination 聚集。Destination 固定范围，因此超出它的工作是 **out of scope**：不是雾，也不属于 **Not yet specified**。地图自有 **Out of scope** 节：你有意识裁定不在*本次*努力内的工作。是范围而非锐利度把它放在这里。

Out-of-scope 工作永不毕业（frontier 止于 destination），仅当 destination 重画时才回来，且作为新努力，不是恢复。

裁定 out of scope 是定范围行为，不是路线上的一步。当已有 ticket 被发现坐落在 destination 之外（制图时误纳入，或被某次解决暴露），**关闭它**（关闭的 ticket 明确离开 frontier），并在 **Out of scope** 节留一行：gist + 为何 out of scope，并链接已关闭 ticket。它不进 **Decisions so far**；那记录实际走过的路，范围边界不是路上的一步。

## 调用方式

两种模式。无论哪种，**每会话绝不解决超过一张 ticket**（matt-research ticket 例外）。

### 绘制地图

用户以松散想法调用。

1. **命名 destination。** 同时采用 **matt-grilling** 与 **matt-domain-modeling**，钉住本地图要找到路去往的东西：Spec、决策或变更。Destination 固定范围，故最先落定。
2. **绘制 frontier。** 再 grill，这次 **breadth-first**：在整个空间扇出，而非深挖一线，浮出开放决策与现在可走的第一步。**若未浮出任何雾**（通往 destination 的路已清、整段旅程小到一次会话够用），不需要地图。停下问用户希望如何继续。
3. **创建地图**（标签 `matt-wayfinder:map`）：填好 Destination 与 Notes，Decisions-so-far 为空，雾草绘进 **Not yet specified**。
4. **创建现在能规格化的 ticket** 作为地图子 issue，再**第二遍**接线 blocking edges（issue 需要 id 才能互相引用）。接线把它们分成 frontier 与 blocked；尚不能规格化的留在雾里：**Not yet specified**。
5. **发射 matt-research 子代理。** 对刚创建的每张 `matt-research` ticket，启动后台子代理 / 并行 worker，采用 **matt-research** 纪律并行解决，把发现记在一次性 `matt-research/<name>` 分支上，并从 ticket 放上下文指针。
6. 停下：制图是一次会话的工作；它不手工解决任何 ticket。

### 推进地图

用户以地图（URL 或编号）调用。Ticket **可选**：未指定时由你选下一个决策，不是用户。

1. 加载 **地图**：低分辨率视图，不是每张 ticket 正文。
2. 选择 ticket。若用户点名则用它。否则按序取 frontier 第一张。**认领**：任何工作前先 assign 给自己。
3. 解决它。**按需缩放**：按需拉取相关或已关闭 ticket 全文；采用 `## Notes` 点名的技能纪律。若有疑，同时采用 **matt-grilling** 与 **matt-domain-modeling**。
4. 记录解决：以 **resolution comment** 贴答案，**关闭** issue，并向地图 Decisions-so-far **追加**上下文指针。
5. 添加新浮出的 ticket（先创建再接线）；把答案已使可规格化的雾毕业，并从 **Not yet specified** 清掉已毕业块，使它只作为新 ticket 存在。若答案揭示某 ticket（本张或其他）坐落在 destination 之外，**裁定 out of scope**，而不是在路线上解决它。若决策使地图其他部分失效，更新或删除那些 ticket。

用户可能并行跑未阻塞 ticket，因此预期其他会话在并发编辑 tracker。
