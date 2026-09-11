---
name: matt-domain-modeling
description: 构建并打磨项目的 domain model。在讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。
invocation: model
---

# Domain Modeling

在设计过程中主动构建并打磨项目的 domain model。这是**主动**纪律：质疑术语、发明边界场景，并在概念一清晰就立刻写入 glossary 与决策。（仅仅**阅读** `CONTEXT.md` 取词汇不算本技能：那是任何技能都能做的一行习惯。本技能用于**改写**模型，而不是只消费它。）

## 文件结构

多数仓库只有一个 context：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

若根目录存在 `CONTEXT-MAP.md`，则仓库有多个 context。该 map 指出每个 context 的位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context 专属决策
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

懒创建文件：只有真正要写内容时再创建。没有 `CONTEXT.md` 时，在第一个术语敲定后再创建。没有 `docs/adr/` 时，在需要第一份 ADR 时再创建。

## 会话中

### 对照 glossary 质疑

当用户用的词与 `CONTEXT.md` 已有语言冲突时，立刻指出。「你的 glossary 把 cancellation 定义为 X，但你现在说的像是 Y。到底是哪一个？」

### 打磨模糊用语

当用户用语含混或一词多义时，提出精确的规范术语。「你说 account：是指 Customer 还是 User？这是两件不同的事。」

### 讨论具体场景

讨论 domain 关系时，用具体场景做压力测试。发明能探边、迫使边界变清晰的场景。

### 与代码交叉核对

当用户陈述「某事如何运作」时，核对代码是否一致。发现矛盾就摊开：「你的代码会取消整张 Order，但你刚说 partial cancellation 是可行的。哪边对？」

### 当场更新 CONTEXT.md

术语一敲定，立刻更新 `CONTEXT.md`。不要攒着批处理：发生就记。格式见 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)。

`CONTEXT.md` 必须完全不含实现细节。不要把它当成 Spec、草稿本或实现决策仓库。它只是 glossary，别无他用。

### 谨慎提议 ADR

仅当以下三点**同时**成立时，才提议创建 ADR：

1. **Hard to reverse**：日后改主意的成本显著
2. **Surprising without context**：未来读者会疑惑「为什么要这样做？」
3. **The result of a real trade-off**：存在真实备选，且你因具体理由选了其中一个

缺任何一点就跳过 ADR。格式见 [ADR-FORMAT.md](./ADR-FORMAT.md)。
