---
name: matt-improve-codebase-architecture
description: 扫描代码库寻找 deepening 机会，以可视化 HTML 报告呈现，再对用户选中的候选做 matt-grilling。触发词：matt-improve-codebase-architecture, depth, seam, shallow, deep module。
invocation: user
disable-model-invocation: true
---

# Improve Codebase Architecture

暴露架构摩擦，提出 **deepening** 机会：把 shallow module 变成 deep module 的重构。目标是可测试性与 AI 可导航性。

本技能受项目 domain model 指引，并建立在共享设计词汇上：

- 采用 **matt-codebase-design** 纪律获取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（deletion test、「interface 即测试面」、「一个 adapter = 假设 seam，两个 = 真实」）。每条建议必须精确使用这些词，不要漂成 "component"、"service"、"API"、"boundary"。
- `CONTEXT.md` 中的领域语言给好的 seam 命名；`docs/adr/` 中的 ADR 记录本技能不应重新争论的决策。

## 流程

### 1. 探索

**扫描前先定范围：YAGNI。** Deepening 一个 module 的回报是让它未来的变更更容易，因此加重最近变更过的区域。先决定*看哪里*再看：

- 若用户点名方向（某个 module、子系统、痛点），直接采用，跳过下方推断。
- 否则回溯一段 commit 历史（`git log --oneline`）找热点，即反复出现的文件与区域，优先看这些路径。若变更散乱无热点，再扩大网。

先读项目 domain glossary（`CONTEXT.md`）及触及区域的 ADR。

然后启动后台子代理 / 并行 worker 走读代码库。不要死守刚性启发式；有机探索并记录摩擦点：

- 理解一个概念是否需要在许多小 module 间来回跳？
- 哪些 module **shallow**（interface 几乎与 implementation 一样复杂）？
- 哪里仅为可测性抽出了纯函数，而真正的 bug 藏在调用方式里（无 **locality**）？
- 哪里紧耦合的 module 越过 seam 泄漏？
- 哪些部分未测，或难以通过当前 interface 测试？

对怀疑 shallow 的东西做 **deletion test**：删掉它是会集中复杂度，还是只是搬家？"会集中"才是你要的信号。

### 2. 以 HTML 报告呈现候选

把自包含 HTML 写到 OS 临时目录，避免落进仓库。临时目录取 `$TMPDIR`，否则 `/tmp`（Windows 为 `%TEMP%`），路径形如 `<tmpdir>/architecture-review-<timestamp>.html`。为用户打开（Linux `xdg-open`、macOS `open`、Windows `start`），并告知绝对路径。若环境不便打开浏览器，可同时给出 Markdown + Mermaid 摘要。

报告用 **Tailwind via CDN** 布局样式，用 **Mermaid via CDN** 画图/流/序列。Mermaid 与手写 CSS/SVG 混用：关系呈图式时用 Mermaid，编辑性更强（mass diagram、剖面、折叠动画）时用手写。每个候选一张 **before/after** 可视化。要视觉化。

每个候选卡片包含：

- **Files**：涉及哪些文件/module
- **Problem**：当前架构为何造成摩擦
- **Solution**：用白话描述会改什么
- **Benefits**：用 locality 与 leverage 解释，以及测试会如何改善
- **Before / After diagram**：并排自定义图，说明 shallowness 与 deepening
- **Recommendation strength**：`Strong` / `Worth exploring` / `Speculative` 徽章

报告以 **Top recommendation** 收尾：你会先做哪个、为何。

**领域用 CONTEXT.md 词汇，架构用 matt-codebase-design 词汇。** 若 CONTEXT.md 定义了 "Order"，说 "the Order intake module"，不要说 "the FooBarHandler"，也不要说 "the Order service"。

**ADR 冲突**：若候选与现有 ADR 矛盾，仅在摩擦大到值得重开 ADR 时才呈现。在卡片中明确标出（例如警告：_"contradicts ADR-0007, but worth reopening because…"_）。不要列出 ADR 禁止的每一种理论重构。

报告格式要点见下文「HTML 报告（精简）」。完整图案与语气约束也在该节。

**先不要**提出 interface。文件写好后问用户："Which of these would you like to explore?"

### 3. Grilling 循环

用户选定候选后，采用 **matt-grilling** 纪律一起走决策树：约束、依赖、deepened module 的形态、seam 背后是什么、哪些测试能留下。

决策落地时同步副作用；采用 **matt-domain-modeling** 纪律保持领域模型最新：

- **给 deepened module 起的名不在 CONTEXT.md？** 把术语加入 `CONTEXT.md`。文件不存在则惰性创建。
- **对话中锐化了模糊术语？** 当场更新 `CONTEXT.md`。
- **用户以有载荷的理由拒绝候选？** 提议写 ADR：_"要我记成 ADR，免得以后架构评审再提一遍吗？"_ 仅当该理由确实会被未来探索者需要时才提议；跳过短暂理由（"现在不值得"）与自明理由。
- **想探索 deepened module 的备选 interface？** 采用 **matt-codebase-design** 的 design-it-twice 并行 worker 模式。

## HTML 报告（精简）

自包含单文件 HTML，放临时目录。Tailwind 与 Mermaid 均来自 CDN。Mermaid 负责图式关系；手写 div/SVG 负责编辑性视觉。不要事事依赖 Mermaid。

### Scaffold

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header><!-- repo、日期、图例：实线框=module，虚线=seam，红箭头=leakage，厚深色框=deep module。无开场白。 --></header>
      <section id="candidates" class="space-y-10"><!-- 候选卡片 --></section>
      <section id="top-recommendation"><!-- 首选一条 --></section>
    </main>
  </body>
</html>
```

### 候选卡片

图承担重量；散文稀疏。每张 `<article>`：

- **Title**：短，点名 deepening（如 "Collapse the Order intake pipeline"）
- **Badge**：强度（`Strong`=emerald，`Worth exploring`=amber，`Speculative`=slate）+ 依赖类别标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）
- **Files**：等宽列表
- **Before / After**：中心件，两列并排
- **Problem / Solution**：各一句
- **Wins**：子弹，每条 ≤6 词（英文术语可保留），如 "Tests hit one interface"
- **ADR callout**（若适用）：琥珀色一行

### 图示模式（择一混用）

- **Mermaid flowchart / sequence**：依赖、调用流、"before: 6 round-trips; after: 1"
- **手写 boxes-and-arrows**：Mermaid 布局打架时；after 侧厚边框 deep module + 灰化内部
- **Cross-section**：水平条带示层；before 多层薄、after 一条厚责任
- **Mass diagram**：interface 矩形 vs implementation 矩形；shallow 几乎一样高，deep 则 interface 短、implementation 高
- **Call-graph collapse**：before 调用树；after 收进一框，内部调用淡化

### 语气与用词

**必须用：** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality。

**禁止替换成：** component, service, unit（指 module 时）· API, signature（指 interface 时）· boundary（指 seam 时）· layer, wrapper（本意是 module 时）。

Wins 用 glossary：*"locality: bugs concentrate in one module"*、*"leverage: one interface, N call sites"*。不要写 "easier to maintain" / "cleaner code"。

报告除 Tailwind CDN 与 Mermaid ESM 外保持静态。图高约 320px，便于 before/after 并排。
