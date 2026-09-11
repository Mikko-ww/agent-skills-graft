---
name: matt-to-tickets
description: 把计划、Spec 或当前对话拆成一组 tracer-bullet ticket，每张声明 blocking edges，并发布到已配置的 issue tracker。触发词：matt-to-tickets, tracer bullet, vertical slice。
invocation: user
disable-model-invocation: true
---

# To Tickets

把计划、Spec 或对话拆成一组 **ticket**：tracer-bullet 式的 vertical slice，每张声明**阻塞**它的其他 ticket。

issue tracker 与 triage 标签词表应由项目配置提供。若缺失，请用户先运行 `matt-configure-project-docs`。

## 流程

### 1. 收集上下文

以对话中已有内容为准。若用户传入引用（Spec 路径、issue 编号或 URL），先拉取并阅读全文与评论。

### 2. 探索代码库（可选）

若尚未探索，先了解代码现状。Ticket 标题与描述使用项目 domain glossary 词汇，并遵守相关 ADR。

留意可先做的预重构，让实现更容易："Make the change easy, then make the easy change."

### 3. 草拟 vertical slice

把工作拆成 **tracer bullet** ticket。

**Vertical slice 规则：**

- 每一刀切出一条窄但**完整**的路径，穿过每一层（schema、API、UI、tests）：是 vertical，**不是**只切一层的 horizontal slicing
- 完成的 slice 可单独演示或验证
- 每张 ticket 的体量应能放进一个全新的上下文窗口
- 任何预重构应先完成

给每张 ticket 写上 **blocking edges**：必须先完成才能开始的其他 ticket。无阻塞者可立即开始。

**宽幅重构是 vertical slicing 的例外。** **Wide refactor** 指一次机械变更（重命名列、改共享符号类型）的 **blast radius** 扫过整个代码库，一次编辑会同时弄坏成千上万调用点，没有 vertical slice 能单独变绿。不要硬塞进 tracer bullet；按 **expand–contract** 排序。先 expand：新旧形态并存，保证不破。再按 blast radius 分批迁移调用点（按 package、按目录），每批一张 ticket，被 expand 阻塞，因旧形态仍在而保持 CI 批批为绿。最后 contract：无调用者后删除旧形态，该 ticket 被所有 migrate 批次阻塞。若连分批也无法单独变绿，仍保持该序列，但让它们共享一条 integration 分支，并全部阻塞一张最终的 integrate-and-verify ticket；只在那里承诺变绿。

### 4. 向用户确认

以编号列表展示拟议拆分。每张 ticket 展示：

- **Title**：短描述名
- **Blocked by**：必须先完成的其他 ticket（若有）
- **What it delivers**：这张 ticket 端到端交付的行为

询问用户：

- 粒度是否合适？（过粗 / 过细）
- Blocking edges 是否正确：每张是否只依赖真正卡住它的 ticket？
- 是否应合并或再拆？

迭代直到用户批准。

### 5. 发布到已配置的 tracker

发布已批准的 ticket。**如何**发布取决于 `matt-configure-project-docs` 配置的 tracker；ticket 内容相同，仅 blocking edges 形态不同：

- **本地文件** → 在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每张一个文件，从 `01` 起按依赖序编号（阻塞者在前）。每文件的 "Blocked by" 列出所依赖的编号/标题。使用下方 per-ticket 模板：一文件一 ticket，绝不合并成单文件。
- **真实 issue tracker（GitHub、Linear 等）** → 按依赖序（阻塞者在前）每张发一条 issue，以便 blocking edges 可引用真实标识。若平台有原生 blocking / sub-issue，用原生关系；否则在 "Blocked by" 中列出阻塞 issue。除非另有指示，打上 `ready-for-agent` triage 标签；这些 ticket 按构造即可被 agent 领取。

推进 **frontier**：所有阻塞者都已完成的 ticket。纯线性链则自上而下。

**不要**关闭或修改任何 parent issue。

## 本地 ticket 模板

```markdown
# <NN>: <Ticket title>

**What to build:** 这张 ticket 端到端交付的行为，从用户视角描述，不是按层列实现清单。

**Blocked by:** 阻塞本 ticket 的编号/标题，或 "None (can start immediately)"。

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Issue tracker 模板

```markdown
## Parent

指向 tracker 上 parent issue 的引用（若来源是已有 issue；否则省略本节）。

## What to build

这张 ticket 端到端交付的行为，从用户视角描述，不是按层实现。

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- 每张阻塞 ticket 的引用，或 "None (can start immediately)"。
```

无论哪种形态，避免具体文件路径或代码片段（很快过时）。例外：matt-prototype 产出的决策密集片段（state machine、reducer、schema、type shape）可内联，并注明来自 matt-prototype；只保留重要部分。
