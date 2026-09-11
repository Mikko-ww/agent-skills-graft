---
name: matt-tdd
description: 测试驱动开发（TDD）。在用户要以测试先行构建功能或修 bug、提到 red-green-refactor、或要做 integration tests 时使用。
invocation: model
---

# Test-Driven Development

TDD 是 red → green 循环。本技能是让该循环产出「值得保留的测试」的参考：什么是好测试、测试落在哪里、反模式、以及循环规则。每一节在每一轮循环都适用：在循环之前与之中查阅，而不是事后补课。

探索代码库时，若存在 `CONTEXT.md` 则先阅读，使测试名与 interface 用语对齐项目的领域语言，并尊重你所触及区域的 ADR。

## 什么是好测试

测试通过公共 interface 验证行为，而不是实现细节。代码可以整体改写；测试不应随之碎裂。好测试读起来像规格说明：「user can checkout with valid cart」准确说出存在何种能力，且能在 refactor 后继续存活，因为它不依赖内部结构。

示例见 [tests.md](tests.md)；mock 指南见 [mocking.md](mocking.md)。

## Seam：测试落在哪里

**Seam** 是你在其上测试的公共边界：在不深入内部的前提下观察行为的 interface。测试只活在 seam 上，从不对着内部实现写。

**只在预先约定的 seam 上测试。** 写任何测试之前，先写下待测 seam 并与用户确认。未确认的 seam 上不写测试。你不可能测尽一切，因此事先约定 seam，才能把测试精力落在关键路径与复杂逻辑上，而不是每个边角。

先问：「公共 interface 是什么，我们应该在哪些 seam 上测试？」

当 interface 的形状本身存疑（module 该有多深、seam 该落在哪、interface 该暴露什么）时，采用同名技能 `matt-codebase-design` 的词汇。它是 module、interface、depth、seam、adapter、leverage、locality 的共享来源；当作参考查阅，而不是再开一场完整会话。

## 反模式

- **Implementation-coupled（实现耦合）**：mock 内部协作者、测 private 方法、或通过旁路验证（直接查数据库而不是走 interface）。特征：你做 refactor 时测试碎了，但行为没变。
- **Tautological（同义反复）**：断言用与代码相同的方式重算期望值（`expect(add(a, b)).toBe(a + b)`、手工按同样方式推导的 snapshot、常量断言等于自身），因而「构造上必过」，永远无法与代码分歧。期望值必须来自独立真相源：已知正确的字面量、演算过的例子、或 Spec。
- **Horizontal slicing（水平切片）**：先写完全部测试，再写全部实现。批量测试验证的是*想象中的*行为：你测的是事物的*形状*而非面向用户的行为，测试对真实变化变得迟钝，且在理解实现之前就锁定了测试结构。改为以 **vertical slice** 推进：一个测试 → 一次实现 → 重复；每个测试是一发 **tracer bullet**，对上一轮循环学到的东西作出响应。

## 循环规则

- **先 red 再 green。** 先写失败测试，再只写刚好让它通过的代码。不要预判后续测试，也不要加投机功能。
- **一次一个 slice。** 每轮循环：一个 seam、一个测试、一次最小实现。
- **Refactoring 不属于本循环。** 它属于 review 阶段（见 `matt-code-review` 技能），不属于 red → green 实现循环。
