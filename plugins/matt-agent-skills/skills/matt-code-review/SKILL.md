---
name: matt-code-review
description: 相对固定点（commit / branch / tag / merge-base）做两轴 review：Standards（是否遵循仓库编码标准）与 Spec（是否忠实实现 originating issue/spec）。并行 worker 两侧审查后并排汇报。在用户要 review 分支、PR、进行中改动、或说 review since X 时使用。
invocation: model
---

相对用户给出的固定点，对 `HEAD` 与该点之间的 diff 做两轴 review：

- **Standards**：代码是否符合本仓库已文档化的 coding standards？
- **Spec**：代码是否忠实实现 originating issue / Spec？

两轴作为 **并行 worker / 后台子代理** 运行，以免污染彼此上下文；然后由本技能汇总发现。

Issue tracker 应已提供给你。若缺少 `docs/agents/issue-tracker.md`，告诉用户运行 `matt-configure-project-docs`（或项目内等价的 tracker / 文档配置步骤）。

## 流程

### 1. 钉住固定点

用户所说的固定点（commit SHA、分支名、tag、`main`、`HEAD~5` 等）。若未指定，向用户询问。

一次性固定 diff 命令：`git diff <fixed-point>...HEAD`（三点，相对 merge-base 比较）。并用 `git log <fixed-point>..HEAD --oneline` 记下 commit 列表。

继续之前，确认固定点可解析（`git rev-parse <fixed-point>`）且 diff 非空。坏 ref 或空 diff 应在此失败，而不是进到两个并行 worker 里。

### 2. 识别 Spec 来源

按此顺序寻找 originating Spec：

1. Commit message 中的 issue 引用（`#123`、`Closes #45`、GitLab `!67` 等），按 `docs/agents/issue-tracker.md` 中的工作流拉取。
2. 用户作为参数传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与分支名或功能匹配的 Spec 文件。
4. 若一无所获，问用户 Spec 在哪。若他们说没有，**Spec** worker 将跳过并报告 "no spec available"。

### 3. 识别 Standards 来源

仓库中任何文档化「代码应如何写」的材料，例如 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md`。

在仓库已文档化的内容之上，Standards 轴始终携带下方的 **smell baseline**：一套固定的 Fowler code smells（《Refactoring》第 3 章），即便仓库什么都没写也适用。两条约束：

- **仓库优先。** 已文档化的仓库标准永远赢；若它认可 baseline 会标出的做法，压制该 smell。
- **始终是判断调用。** 每个 smell 是带标签的启发式（「可能的 Feature Envy」），从不是硬性违规。与此处任何标准一样，跳过工具链已强制执行的项。

每个 smell 读作 *它是什么* → *如何修*；对着 diff 匹配：

- **Mysterious Name**：函数、变量或类型名未揭示它做什么或装什么。→ 重命名；若想不出诚实的名字，设计本身浑浊。
- **Duplicated Code**：同一逻辑形状出现在变更的多个 hunk 或文件。→ 抽出共享形状，两边调用。
- **Feature Envy**：方法伸进另一对象的数据多于自己的。→ 把方法移到它所 envy 的数据上。
- **Data Clumps**：同样几个字段或参数总一起旅行（一个想诞生的类型）。→ 捆成一个类型再传递。
- **Primitive Obsession**：用原始类型或字符串顶替值得独立类型的领域概念。→ 给概念一个小类型。
- **Repeated Switches**：同一类型上的同一 `switch` / `if` 瀑布在变更中反复出现。→ 用多态替换，或两边共享一张 map。
- **Shotgun Surgery**：一次逻辑变更迫使 diff 里许多文件零散编辑。→ 把一起变的东西收进一个 module。
- **Divergent Change**：一个文件或 module 因几个无关理由被编辑。→ 拆分，使每个 module 只因一个理由而变。
- **Speculative Generality**：为 Spec 没有的需求加上的抽象、参数或钩子。→ 删掉；内联回去直到真实需求出现。
- **Message Chains**：长 `a.b().c().d()` 导航，调用方本不该依赖。→ 把行走藏到第一个对象的一个方法后面。
- **Middle Man**：class 或函数大多只是转发。→ 砍掉，直接调真正目标。
- **Refused Bequest**：子类或实现者忽略或覆盖大部分继承。→ 丢掉继承，改用组合。

### 4. 并行启动两个 worker

**Standards worker 的 prompt** 应包含：

- 完整 diff 命令与 commit 列表。
- 你在 step 3 找到的 standards 源文件列表，**外加 step 3 的 smell baseline 全文粘贴**（该 worker 没有其他途径拿到它）。
- Brief：「按相关 file/hunk 报告：(a) diff 违反已文档化标准的每一处：引用标准（文件 + 规则）；(b) 你发现的任何 baseline smell：命名并引用 hunk。区分硬性违规与判断调用：已文档化标准的违背可以是硬性的，但 baseline smells 始终是判断调用，且已文档化的仓库标准覆盖 baseline。跳过工具链已强制执行的项。400 词以内。」

**Spec worker 的 prompt** 应包含：

- Diff 命令与 commit 列表。
- Spec 的路径或已拉取内容。
- Brief：「报告：(a) Spec 要求但缺失或部分实现的需求；(b) diff 中未被要求的行为（scope creep）；(c) 看起来已实现但实现似乎错误的需求。每条发现引用 Spec 行。400 词以内。」

若 Spec 缺失，跳过 Spec worker，并在最终报告中注明。

### 5. 汇总

在 `## Standards` 与 `## Spec` 标题下呈现两份报告，原文或轻微清理。**不要**合并或重排发现，因为两轴故意分开（见下方「为何两轴」）。

以一行摘要结束：每轴发现总数，以及*每轴内*最严重的问题（若有）。不要跨轴挑单一赢家：那正是分离要防止的重排。

## 为何两轴

一次变更可以过一轴而挂另一轴：

- 遵循一切标准却实现了错误的东西 → **Standards 过，Spec 挂。**
- 精确做了 issue 要求的事却打破项目约定 → **Spec 过，Standards 挂。**

分开汇报，防止一轴掩盖另一轴。
