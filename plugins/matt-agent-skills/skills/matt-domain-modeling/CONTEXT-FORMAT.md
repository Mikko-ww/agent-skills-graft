# CONTEXT.md Format

## 结构

```md
# {Context Name}

{一两句话说明这个 context 是什么、为何存在。}

## Language

**Order**:
{一两句话定义该术语}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 规则

- **Be opinionated。** 同一概念有多个词时，选定最优，其余列入 `_Avoid_`。
- **定义要紧。** 最多一两句。写清它**是什么**，而不是它做什么。
- **只收录对本项目 context 特有的术语。** 通用编程概念（timeout、error type、utility pattern）即使项目大量使用也不进 glossary。新增前自问：这是本 context 独有概念，还是通用编程概念？只有前者才属于这里。
- **有自然聚类时用小标题分组。** 若所有术语同属一个内聚领域，扁平列表即可。

## 单 context 与多 context 仓库

**单 context（多数仓库）：** 根目录一份 `CONTEXT.md`。

**多 context：** 根目录 `CONTEXT-MAP.md` 列出各 context、位置及相互关系：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

本技能按下列规则推断结构：

- 若存在 `CONTEXT-MAP.md`，先读它定位各 context
- 若只有根目录 `CONTEXT.md`，则为单 context
- 若两者皆无，在第一个术语敲定时懒创建根目录 `CONTEXT.md`

多 context 时，推断当前话题属于哪一个；不清楚就问用户。
