---
name: matt-skill-flows
description: 询问当前情境该用哪条技能或 flow。本仓库技能的路由器。在不确定从哪条技能起步、或需要 phase boundary 决策时使用。
invocation: user
disable-model-invocation: true
---

# Skill Flows

你不必记住每一条技能，直接问。

一条 **flow** 是穿过技能的路径。多数路径走一条 **main flow**，另有两条 **on-ramp** 并入它。其余是 standalone，或在下方运行的词汇层。

## Main flow：idea → ship

多数工作走的路线。你有一个想法，想把它做成。

1. **`matt-grill-with-docs`** 用面试打磨想法。只要你在**工作目录**里工作，就从这里开始：它有状态，把学到的内容留在 `CONTEXT.md` 与 ADR 中。（没有工作目录？改用 `matt-grill-me`，见 Standalone。两者共用同一 `matt-grilling` 原语；`matt-grill-with-docs` 会留下纸面痕迹，因此只要有仓库可写，它就是更好的那个。）
2. **分支：能否在对话里解决每个问题？** 若某个问题需要可运行的答案（状态、业务逻辑、必须亲眼看到的 UI），经 **`matt-handoff`** 双向桥接，绕道原型（原型住在自己的目录，正是 `matt-handoff` 的用途；见 Phase boundaries）：
   - **`matt-handoff`** 出去，再以该文件开启新会话，
   - **`matt-prototype`** 用可丢弃代码回答问题，
   - **`matt-handoff`** 带回所学，并在原想法线程中引用它。
3. **分支：这是多会话构建吗？**
   - **是** → **`matt-to-spec`**（把线程收成 Spec），再 **`matt-to-tickets`** 拆成 tracer-bullet tickets，每张声明 **blocking edges**。本地 tracker 下是 `.scratch/<feature>/issues/` 每票一文件，按 blocker 优先手工推进；真实 tracker 上 edges 变成原生 blocking links，任何 blocker 已完成的票都可领取：对每张票启动 **`matt-implement`**，票与票之间用 **new chat** 清空上下文。每张票自洽，上一张的上下文可丢弃。
   - **否** → 就在同一上下文窗口里直接 **`matt-implement`**。

   无论哪种，**`matt-implement`** 通过内部驱动 **`matt-tdd`** 构建每个议题（一次一个 red-green 切片），收尾前跑 **`matt-code-review`**（Standards + Spec 双轴审查 diff），再提交。单独需要 test-first 构建某个具体行为、又不想上完整 Spec 时，直接用 **`matt-tdd`**；想对照固定点审查分支或 PR 时，单独用 **`matt-code-review`**。

### 上下文卫生

步骤 1–3 保持在**同一个不间断的上下文窗口**（在 `matt-to-tickets` 完成前不要开 new chat 丢掉推理链），让 matt-grilling、Spec 与 tickets 建立在同一思考上。之后每次 `matt-implement` 从票出发重新开始。

上限是 **smart zone**：模型仍能锐利推理的窗口（前沿模型大约 ~150k tokens）。若会话在到达 `matt-to-tickets` 前逼近该区，不要在降级状态下硬推；在最近的 phase boundary 做决策（见 Phase boundaries），通常是把必要摘要带进 **new chat** 再继续。

## On-ramps

产生工作、再并入 main flow 的起始情境。

- **Bug 与请求堆积** → **`matt-triage`**。它把议题推过 triage 角色，产出 agent-ready 议题，之后由 **`matt-implement`** 领取。

  Triage 只用于**不是你创建的**议题：bug 报告、外来 feature request、任何原始到达的东西。`matt-to-tickets` 产出的票已经是 agent-ready，**不要再 triage**。

- **东西坏了** → **`matt-diagnosing-bugs`**。用于硬问题：一眼看不穿的 bug、间歇 flake、两个已知良好状态之间潜入的回归。在拿到 **tight feedback loop**（一条命令已经在*这个* bug 上变红）之前拒绝空想，再用回归测试修复。事后复盘若发现真正问题是没有好 seam 锁住 bug，则交接给 **`matt-improve-codebase-architecture`**。

- **巨大、雾气重的努力：greenfield 或大到单会话装不下的功能** → **`matt-wayfinder`**，这里认知负担最重的 flow。当从这里到终点的路尚不可见时，它在 issue tracker 上绘制由 **decision tickets** 组成的 **shared map**，一次解决一张，产出的是**决策而非交付物**，直到雾被推开、路变清晰。`matt-grill-with-docs` 打磨你能在单会话中握住的想法；matt-wayfinder 用于你握不住的那种，更慢更密，只留给那种情况，绝不要用在已界定清楚的功能上。

  map 清晰后，**它交接，不构建**：在 **`matt-to-spec`** 并入 main flow，把 map 上链锁的决策收成可构建计划，再照常 `matt-to-tickets` 与 `matt-implement`。把 map 直接塞进 `matt-implement` 会跳过那次收束并丢掉链锁细节，因此仅当努力结果其实很小才直接 `matt-implement`。

## 代码库健康

不是功能工作，只是维护。

- **`matt-improve-codebase-architecture`** 在你有空闲想让代码库更利于 agent 操作时运行。它浮现 **deepening opportunities**；选中一个会**生成一个想法**，可带到 main flow 的 `matt-grill-with-docs`。它是找到候选的勘测；**`matt-codebase-design`**（下方）是你在其上设计所选方案的工作台。

## 下方的词汇层

两条可由模型触发的参考，在其他技能*之下*运行，各自是其词汇的单一真相来源。当问题在**用词**而非流程时直接取用；或让上方技能自行拉入。

- **`matt-domain-modeling`**：打磨项目的 *domain* 语言：质疑模糊术语、拆开一词多用（「account」干三份活）、把难反转决策记为 ADR。这是 `matt-grill-with-docs` 用来保持 `CONTEXT.md` 为干净 glossary 的主动纪律。
- **`matt-codebase-design`** 是 deep-module 词汇（module、interface、depth、seam、adapter、leverage、locality），用于设计模块的 *shape*：在干净 seam 上以小 interface 承载大量行为。`matt-tdd` 与 `matt-improve-codebase-architecture` 都说这套话。

## Phase boundaries

一个 **phase** 是会话内的一块工作：matt-grilling、实现、QA。在两个 phase 之间的 **boundary**，你有四项选择，挑选是整张地图里最模糊的决策：

- **Continue**：留在原地。零成本，零损失。
- **New chat**：开启新的空会话（可附带简短 brief），当旧上下文对下一步无价值或窗口已逼近 smart zone。
- **`matt-handoff`** 写出可移植的 markdown 文件。用途很窄：仅用于**新 harness**、**新目录**、**同事**，或在 **phase 中途** 分出旁支任务。它买到的是可移植性。
- **Background worker**：把收紧范围的任务交给后台子代理 / 并行 worker，拿回报告。

完整有序决策树、各分支理由，以及为何 primary-source 成本让 **Continue** 必须最先排除，见 [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md)。在 boundary **处**做决定；phase 中途则继续，或把剩余拆给 background worker。

## Standalone

完全离开 main flow。

- **`matt-agent-skills-help`**：不熟悉本技能库时先调这个。它扫描并输出全部 `matt-*` 技能的 Markdown 总览（仅显式调用；不替你选路径）。

- **`matt-grill-me`**：与 `matt-grill-with-docs` 相同的 relentless interview，但是**无状态**：不落盘，不建 `CONTEXT.md`。在**没有工作目录**时用（打磨计划、设计、文稿等，下面没有仓库）。若在工作目录里，改用 `matt-grill-with-docs`：同一访谈且留下纸面痕迹，因此严格更好。
- **`matt-grilling`** 是访谈原语本身：轮次、frontier、事实归 agent、决策归你。`matt-grill-me` 与 `matt-grill-with-docs` 是两种具名入口；`matt-triage`、`matt-wayfinder`、`matt-improve-codebase-architecture` 也会在内部运行它。仅当你想要没有包装的访谈时直接取用。
- **`matt-resolving-merge-conflicts`** 处理进行中的 merge 或 rebase 冲突，逐 hunk 按**意图**解决（追溯到各方 primary source），而不是挑行，然后完成操作。它从不执行 `--abort`。Standalone，不在任何 flow 上：当你已在冲突中时取用。
- **`matt-prototype`** 是回答一个设计问题的小型可丢弃程序：这个状态模型感觉对吗，或 UI 该长什么样。可丢弃约束的是代码写法，不是销毁承诺：答案会折进正式代码，原型本身作为 **primary source** 留在 `matt-prototype/<name>` 分支（离开 main），并由实现议题指向。它是 main flow 步骤 2 的绕道，但任何难在纸上敲定的设计问题都可取用。
- **`matt-research`**：把阅读杂活交给 **background worker**：对照 **primary sources** 调查问题，在仓库留下带引用的 Markdown 文件。它读的时候你可以继续工作。产出的文件应带进 main flow 的 `matt-grill-with-docs`，因为研究喂养思考而非取代思考。
- **`matt-to-questionnaire`**：当卡住你的东西不在你脑子里也不在代码库、而在**别人**脑子里时，为对方写一份问卷。它是 `matt-grill-me` 的逆：不是就主题面试你，而是就**发送**（寄给谁、你需要拿回什么）面试你，把问题对准缺口。收回的材料供 `matt-grill-with-docs` 或 `matt-to-spec` 使用。
- **`matt-wizard`** 用于只有**人类**能完成的步骤：配置基础设施、设置凭证或 CI secrets、点开不熟悉的第三方控制台、跑一次性迁移或切换。它生成交互式 bash 脚本，打开每个 URL、捕获每个值，写入 `.env` 与密钥库，让流程不再每次向 agent 重讲。可由模型触发，因此 agent 一撞上只有你能过的墙就会取用。若 agent 自己就能做，就该自己做；这是给人类真正在环的地方。
- **`matt-wait-what`** 是消息没落地时的纠正。在任何其他技能中途使用，agent 用你缺的上下文、用平实语言、用 `CONTEXT.md` 词汇重新表述刚说的话。它事后生效；`matt-grill-with-docs` 是事前预防，因为早期约定的共享语言才能阻止行话冒出来。
- **`matt-teach`**：跨多会话学习一个概念，以当前目录为有状态工作区。
- **`matt-writing-for-agents`** 是撰写 agent 消费文档的参考：技能、AGENTS.md、被指针指向的文档。

## 前置条件

**`matt-configure-project-docs`**：在第一次工程 flow 之前运行，配置其他技能所假设的 issue tracker、triage 标签与文档布局。自定义 issue tracker 也可以。
