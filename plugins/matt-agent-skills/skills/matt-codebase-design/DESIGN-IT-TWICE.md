# Design It Twice

当用户想为选定的 deepening 候选探索备选 interface 时，使用此并行 worker / 后台子代理模式。基于 "Design It Twice"（Ousterhout）：你的第一个想法多半不是最好的。

使用 [SKILL.md](SKILL.md) 中的词汇：**module**、**interface**、**seam**、**adapter**、**leverage**。

## 流程

### 1. 框定问题空间

在启动子代理之前，为选定候选写一段面向用户的问题空间说明：

- 任何新 interface 必须满足的约束
- 它会依赖什么，以及它们落入哪一类（见 [DEEPENING.md](DEEPENING.md)）
- 一段粗略的示意代码草图，用来把约束落地，而不是提案本身

展示给用户，然后立刻进入 Step 2。用户阅读思考的同时，子代理并行工作。

### 2. 启动并行 worker

并行启动 3 个以上 worker / 后台子代理。每个必须为加深后的 module 产出**截然不同**的 interface。

给每个子代理一份独立的技术 brief（文件路径、耦合细节、来自 [DEEPENING.md](DEEPENING.md) 的依赖类别、seam 背后是什么）。brief 独立于 Step 1 面向用户的问题空间说明。给每个 agent 不同的设计约束：

- Agent 1：「最小化 interface：最多 1–3 个入口。最大化每个入口的 leverage。」
- Agent 2：「最大化灵活性：支持多种用例与扩展。」
- Agent 3：「为最常见调用方优化：让默认情况变得trivial。」
- Agent 4（若适用）：「围绕 ports & adapters 设计跨 seam 依赖。」

把 [SKILL.md](SKILL.md) 词汇与 CONTEXT.md 词汇都放进 brief，使每个子代理用架构语言与项目领域语言一致地命名。

每个子代理输出：

1. Interface（类型、方法、参数，以及不变式、顺序、错误模式）
2. 调用方如何使用的 usage example
3. Implementation 在 seam 背后藏了什么
4. 依赖策略与 adapters（见 [DEEPENING.md](DEEPENING.md)）
5. Trade-offs：哪里 leverage 高，哪里薄

### 3. 呈现与比较

依次呈现各设计，让用户消化每一个，再用散文比较它们。按 **depth**（interface 处的 leverage）、**locality**（变更集中在何处）、**seam placement** 对比。

比较后给出你自己的推荐：你认为哪个设计最强、为什么。若不同设计的元素可以很好组合，提出 hybrid。要有主见：用户要的是有力解读，而不是菜单。
