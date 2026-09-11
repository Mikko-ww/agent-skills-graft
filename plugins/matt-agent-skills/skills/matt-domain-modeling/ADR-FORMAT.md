# ADR Format

ADR 放在 `docs/adr/`，按序编号：`0001-slug.md`、`0002-slug.md` 等。

懒创建 `docs/adr/`：仅在需要第一份 ADR 时创建。

## 模板

```md
# {决策的短标题}

{1–3 句：背景是什么、我们决定了什么、以及为什么。}
```

就这样。一份 ADR 可以只有一段。价值在于记下**做了决定**以及**为何**，而不在于填满章节。

## 可选章节

仅在真正增值时加入。多数 ADR 不需要。

- **Status** frontmatter（`proposed | accepted | deprecated | superseded by ADR-NNNN`）：决策会被重访时有用
- **Considered Options**：仅当被否决的备选值得记住时
- **Consequences**：仅当需要点出非显而易见的下游影响时

## 编号

扫描 `docs/adr/` 中已有最大编号，再加一。

## 何时提议 ADR

以下三点必须**同时**成立：

1. **Hard to reverse**：日后改主意的成本显著
2. **Surprising without context**：未来读者看代码会疑惑「到底为什么要这样做？」
3. **The result of a real trade-off**：存在真实备选，且你因具体理由选了其中一个

若决策易于反转，跳过：反正以后会改。若不令人意外，没人会问为什么。若没有真实备选，除了「我们做了显而易见的事」之外没什么可记。

### 什么算合格

- **Architectural shape。** 「我们用 monorepo。」「write model 用 event-sourced，read model 投影到 Postgres。」
- **Context 之间的集成模式。** 「Ordering 与 Billing 通过 domain events 通信，而不是同步 HTTP。」
- **带锁入成本的技术选型。** 数据库、message bus、auth provider、部署目标。不是每一个库：只是那些替换要花一个季度的。
- **边界与范围决策。** 「Customer 数据由 Customer context 拥有；其他 context 仅按 ID 引用。」明确的 no 与 yes 同样有价值。
- **对显而易见路径的刻意偏离。** 「我们用手写 SQL 而不用 ORM，因为 X。」任何合理读者会默认相反做法的地方。这些能阻止下一位工程师「修好」本是刻意的设计。
- **代码里看不见的约束。** 「合规要求不能用 AWS。」「因合作方 API 合同，响应必须低于 200ms。」
- **否决理由非显而易见的备选。** 若考虑过 GraphQL 却因微妙理由选了 REST，记下来；否则六个月后又有人会再提议 GraphQL。
