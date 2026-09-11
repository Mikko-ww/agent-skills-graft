---
name: matt-writing-for-agents
description: 为 agent 撰写文档（skills、AGENTS.md、由 pointer 指向的文档）。创建或编辑 skill、修改 agent 说明文档时采用。
invocation: model
---

为 agent 消费的任何文档提供写作参考：一份 skill、一份 `AGENTS.md`（或项目约定的 agent 说明文件）、一份由 pointer 到达的文档。包装不同，写法相同：同一组杠杆让每次运行采取相同的**过程**，而不是产出相同的输出。

当所写文档是 skill 时，阅读 [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md)，了解 frontmatter、invocation 选择，以及 router skills。

## Context pointers

**Context pointer** 是 agent 上下文中持有的引用：它命名某段「上下文之外」的材料，并编码何时去取它。Skill 的 `description` 是一种；`AGENTS.md` 中点名某文档的一行是同一种对象。决定 agent 何时、以何可靠度取到材料的，是 pointer 的**措辞**，不是目标本身。必须抵达的目标若挂在弱措辞 pointer 后面，就是 variance bug：先锐化措辞；只有锐化失败才考虑内联材料。

Pointer 做两件事：说明材料是什么，并列出应触发取用的 **branches**（branch 是文档处理的不同情形，因此不同运行会走不同路径）。始终加载的 pointer 每个词都在每一轮花钱，因此比正文更需要修剪：

- **把 leading word 前置**：pointer 在这里完成触发工作。
- **每个 branch 一个触发。** 只是同一 branch 换名的同义词，是写了两遍的一个 branch；合并它们，只保留真正不同的 branches。
- **删掉正文已携带的身份信息。**

## The two loads

你加入的每个文档与 pointer 都花费两种预算之一：

- **Context load**：始终加载材料对 agent 窗口的成本：`AGENTS.md` 的一行、skill `description`、任何每轮都在上下文中的内容，无论是否触发都消耗 tokens 与注意力。
- **Cognitive load**：对人的成本：存在哪些文档、何时取用哪一份。人是索引。这不是要最小化的成本：它是人类 agency 的代价；在人类判断重要处花费它，在不重要处移除它。

仅通过 pointer 到达的材料逃脱 context load，代价是 pointer 自身那一行；完全没有 pointer 的材料则全部压在 cognitive load 上。

## Information hierarchy

文档由两类内容建成：**steps**（agent 按序执行的动作）与 **reference**（按需查阅的定义、规则、事实）。二者可自由混合：全是 steps（菜谱）、全是 reference（某次 review 的规则、本技能本身），或两者兼有。核心决策是每块内容落在 **information hierarchy** 的哪一层：按 agent「多快需要」排序的梯子：

1. **In-file step** 是主层：agent 做什么，按顺序。
2. **In-file reference** 按需查阅。常常是合法的扁平 peer-set（一次 review 的每条规则同层），这是好的安排，不是坏味道。
3. **Disclosed reference** 被推到单独文件，由 context pointer 到达，仅在 pointer 触发时加载。范围从同文件夹的兄弟文件，到任何文档都可指向的完全外部 reference。

往下推得太少，顶层膨胀；推得太多，藏起 agent 真正需要的材料。这张力就是整个决策。

**Progressive disclosure** 是沿梯子下移（离开主文件、藏到 pointer 后），使顶层保持可读。首要不是省 tokens：它是如何保护 hierarchy。Branching 是最干净的 disclosure 测试：每个 branch 都需要的内联；只有部分 branch 才到达的推到 pointer 后。当文档有 steps 时，本应被 disclose 却仍留在文件内的 reference 会埋葬 steps，使是否注意到它们变成抛硬币：这是 variance 杠杆，不只是可读性杠杆。

**Co-location** 是文件内的伴侣：梯子决定一块内容「往下多远」，co-location 决定到位后「旁边放什么」。把一个概念的定义、规则与 caveat 放在同一标题下，而不是打散，这样读一部分会带上邻居。检验：文档应读起来像写给 agent 的 documentation。成组材料是那样；打散材料不是。（与 duplication 不同：duplication 在两处重复一个意思；scattering 把一个意思撕成许多碎片。）

**Sprawl** 是这里的失败模式：文档就是太长，即使每一行都还活着且唯一。注意力在过量中变薄，多出的每一行都是又一条要保持相关的负担。药方是梯子：把 reference disclose 到 pointer 后，并按 branch 或 sequence 拆分，使每条路径只携带所需。

## Steps and completion criteria

每个 step 以 **completion criterion** 结束：告诉 agent 工作已完成的条件。两个属性使它成为杠杆：

- **Clarity**：agent 能否区分 done 与 not-done？模糊边界（「理解已达成」）会诱发 **premature completion**：在真正完成前结束该 step，注意力滑向「已经做完」。后面仍可见的 steps（**post-completion steps**）提供拉力；criterion 的清晰度是阻力。按序防守：**先锐化边界**（局部且便宜）；仅当边界不可约地模糊**且**你观察到抢跑时，才通过拆分序列把后续 steps 藏起来。隐藏只在真正的上下文边界上有效（matt-handoff 或子代理派发；同上下文内联调用仍把后续 steps 留在上下文中，清不掉）。
- **Demand**：它要求多少。「每个被修改的 model 都已交代」强制彻底工作，「产出变更列表」则否。Demand 驱动 **legwork**（agent 在工作内做的挖掘，潜伏在措辞中，而非写成单独 step），且不限于 step：「每条规则都已应用」绑定扁平 reference，正如「每个 step 都完成」绑定序列；这就是全 reference 文档仍能携带穷尽性门槛的方式。

最强的 criteria 既可检查，又穷尽。

## When to split

把一份文档拆成两份，会花费两种 load 之一，因此仅在切割赚回代价时拆：

- **By sequence**：在 post-completion steps 会诱使 agent 抢跑当前 step 的地方拆开一步序列。把后续挡在视野外，会驱动对当前任务更多 legwork。当心反向：合并序列会把每个 step 的后续暴露给后面的内容，诱发 premature completion。
- **By invocation**（skill 专用）：见 [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md)。

## Leading words

**Leading word** 是已活在模型预训练中的紧凑概念，agent 在运行文档时用它思考（_lesson_、_fog of war_、_tracer bullets_）。作为 token 重复，而不是作为句子；它累积分布式定义，并用最少 tokens 锚定整片行为，因为征用了模型已有的 priors。自造词若定义清楚也能用，但自造词征用不到 priors：你用定义 tokens 支付预训练词免费给的东西；优先使用已有词。

它锚定两次。在正文中是 **execution**：词每次出现，agent 都伸向同一行为；在扁平 reference 内，它把注意力聚焦到要寻找的一类事物。在 pointer 中是 **invocation**：当同一词活在你的 prompts、docs 与 codebase 中，agent 把共享语言链到材料，并更可靠地取到它。

寻找用 leading words 重构的机会。三元组在三处写开、pointer 用一整句指向一个想法：每一处都乞求坍缩成单个 token：

- "fast, deterministic, low-overhead" → _tight_（一个 _tight_ loop）
- "a loop you believe in" → _red_，把模糊门禁变成可观察的二元状态（loop 在 bug 上变 _red_，或没有）

你赢两次：更少 tokens，以及更锋利的钩子供 agent 挂住思考。假定每份文档都带着可被 leading words 退休的复述。去找它们。

**Negation** 是这杠杆旁的失败模式：用禁止来转向，会把被禁行为拖进上下文，使其**更**可用，而非更少。_Don't think of an elephant_，于是只剩大象；否定是弱修饰语，被强激活的概念碾过，于是禁令半读成「去做那件事」的指令。提示 **positive**：陈述目标行为（「写一行注释」），使被禁行为从未被说出。禁止仅在你无法用正面表述的硬护栏时才挣得位置；即便如此，也要配上正面目标，使注意力落在该做什么上。

## Pruning

- 每个意思保持在 **single source of truth**：一处权威，使改变行为是一处编辑。**Duplication**（同一意思多处出现）花费维护与 tokens，并把该意思在梯子上的显眼度抬到超过真实等级。（这是 leading word 的意外反面：leading word 有意重复 token，从不重复意思。）
- **Environment** 也是真相来源（`package.json` scripts、配置文件、目录布局、`--help` 输出）；复述它的文档是 **cache**：lookup 的副本，仅当 lookup 昂贵时才挣得加载。缓存 agent 无法靠查看找到的东西：未写下的约定、选择背后的原因、配置不会坦白的 gotcha。把「一个文件、一条命令」的 lookup 留给 environment，它们不会在那里过期。
- 检查每一行的 **relevance**：它是否仍作用于文档所做之事？一行失去 relevance，或因从未作用于任务（纯说明，或本应 disclose 的 branch），或因所描述的行为/世界变了而过期。更短的文档更容易保持相关。没有修剪纪律，默认命运是 **sediment**：陈旧层沉淀，因为添加感觉安全、删除感觉危险，直到你必须向下挖核才能找到仍活着的部分。
- 逐句猎杀 **no-ops**：模型默认已服从的指令，花钱说了等于没说。检验（相对默认是否改变行为？）是相对模型的，不是相对读者的：两人对 no-op 意见不合，是对默认意见不合，用运行文档解决，不是辩论。句子失败时，删掉整句，而不是削词。该检验也给 leading words 打分：弱到打不过默认的词（agent 已经偏 thorough 时说 _be thorough_）是 no-op；修复是更强的词（_relentless_），不是另一种技法。
