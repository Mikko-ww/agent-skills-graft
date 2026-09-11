---
name: matt-codebase-design
description: 设计 deep module 的共享词汇。在用户要设计或改进 module 的 interface、寻找 deepening 机会、决定 seam 落点、提高可测性或 AI 可导航性、或其他技能需要 deep-module 词汇时使用。
invocation: model
---

# Codebase Design

设计 **deep modules**：小 interface 背后大量行为，落在干净的 seam 上，并能通过该 interface 测试。凡是在设计或重构代码的地方，都使用这套语言与原则。目标是：给调用方 leverage，给维护者 locality，给所有人 testability。

## Glossary

精确使用这些术语：不要用 "component"、"service"、"API"、"boundary" 替换。一致的语言正是全部意义所在。

**Module**：任何具有 interface 与 implementation 的东西。刻意与规模无关：函数、class、package、或跨层的 slice。_避免_：unit、component、service。

**Interface**：调用方要正确使用该 module 必须知道的一切：类型签名，以及不变式、顺序约束、错误模式、必需配置、性能特征。_避免_：API、signature（太窄，它们只指类型层表面）。

**Implementation**：module 内部的代码体。有别于 **Adapter**：一个东西可以是小 adapter 配大 implementation（Postgres repo），或大 adapter 配小 implementation（内存 fake）。当话题是 seam 时用 "adapter"；其余时候用 "implementation"。

**Depth**：interface 处的 leverage。调用方（或测试）每学习一单位 interface 所能行使的行为量。当小 interface 背后坐着大量行为时，module 是 **deep**；当 interface 几乎与 implementation 一样复杂时，是 **shallow**。

**Seam** _(Michael Feathers)_：你可以在不编辑该处的前提下改变行为的位置；即 module 的 interface *所在位置*。seam 放哪里是独立的设计决策，有别于它背后放什么。_避免_：boundary（与 DDD 的 bounded context 过载）。

**Adapter**：在 seam 处满足某 interface 的具体物。描述*角色*（填哪个槽），而非实质（里面是什么）。

**Leverage**：调用方从 depth 得到的东西。每学习一单位 interface 获得更多能力。一次 implementation 在 N 个调用点与 M 个测试上得到回报。

**Locality**：维护者从 depth 得到的东西。变更、bug、知识与验证集中在一处，而不是散落到调用方。修一次，处处修好。

## Deep vs shallow

**Deep module** = 小 interface + 大量 implementation：

```
┌─────────────────────┐
│   Small Interface   │  ← 少量方法，简单参数
├─────────────────────┤
│                     │
│  Deep Implementation│  ← 复杂逻辑藏在里面
│                     │
└─────────────────────┘
```

**Shallow module** = 大 interface + 很少 implementation（避免）：

```
┌─────────────────────────────────┐
│       Large Interface           │  ← 许多方法，复杂参数
├─────────────────────────────────┤
│  Thin Implementation            │  ← 只是透传
└─────────────────────────────────┘
```

设计 interface 时自问：

- 能否减少方法数？
- 能否简化参数？
- 能否把更多复杂度藏进内部？

## 原则

- **Depth 是 interface 的属性，不是 implementation 的。** 一个 deep module 内部可由小的、可 mock、可替换的部件组成；它们只是不属于 interface。module 可以有 **internal seams**（对 implementation 私有，供自身测试使用），以及 interface 处的 **external seam**。
- **删除测试（The deletion test）。** 想象删掉该 module。若复杂度随之消失，它是透传。若复杂度在 N 个调用方重新出现，它在赚回自己的存在。
- **Interface 就是测试面。** 调用方与测试穿过同一个 seam。若你想测*越过* interface，module 形状多半不对。
- **一个 adapter 意味着假设的 seam。两个 adapter 才意味着真实的 seam。** 除非有东西真正在其上变化，否则不要引入 seam。

## 为可测性设计

好的 interface 使测试自然：

1. **接受依赖，不要创建依赖。**

   ```typescript
   // 可测
   function processOrder(order, paymentGateway) {}

   // 难测
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不要制造副作用。**

   ```typescript
   // 可测
   function calculateDiscount(cart): Discount {}

   // 难测
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **小表面。** 更少方法 = 更少需要的测试。更少参数 = 更简单的测试 setup。

## 关系

- 一个 **Module** 恰好有一个 **Interface**（呈现给调用方与测试的表面）。
- **Depth** 是 **Module** 的属性，相对其 **Interface** 度量。
- **Seam** 是 **Module** 的 **Interface** 所在之处。
- **Adapter** 坐在 **Seam** 上并满足 **Interface**。
- **Depth** 为调用方产生 **Leverage**，为维护者产生 **Locality**。

## 被拒绝的框架

- **把 Depth 当作 implementation 行数与 interface 行数之比**（Ousterhout）：奖励给 implementation 注水。我们改用 depth-as-leverage。
- **把 "Interface" 当作 TypeScript 的 `interface` 关键字或 class 的 public 方法**：太窄；此处的 interface 包括调用方必须知道的每一个事实。
- **"Boundary"**：与 DDD 的 bounded context 过载。说 **seam** 或 **interface**。

## 进一步

- **在给定依赖下加深一簇 module**，见 [DEEPENING.md](DEEPENING.md)：依赖类别、seam 纪律、以及 replace-don't-layer 测试。
- **探索备选 interface**，见 [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)：并行启动多个 worker / 后台子代理，用几种截然不同的方式设计 interface，再按 depth、locality 与 seam 落点比较。
