---
name: matt-implement
description: 按 Spec 或一组 ticket 实现工作：在约定 seam 上采用 matt-tdd，收尾做 matt-code-review。仅在用户明确要求时才 commit。触发词：matt-implement, Spec, ticket。
invocation: user
disable-model-invocation: true
---

# Implement

实现用户在 Spec 或 ticket 中描述的工作。

## 流程

1. 确认实现范围（哪份 Spec / 哪些 ticket）与已约定的 **seam**。若 seam 未确认，先与用户确认再动笔。

2. 尽可能采用 **matt-tdd** 纪律（同名技能 `matt-tdd`）：在预约定的 seam 上按 red → green 做 vertical slice。不要在未确认的 seam 上写测试。

3. 定期跑类型检查与单测文件；全量测试套件在结束时跑一次。

4. 完成后采用 **matt-code-review** 纪律（同名技能 `matt-code-review`）：按 Standards 与 Spec 两轴审查本次变更。

5. **Commit 策略（覆盖 Matt 原版的自动 commit）：**
   - **仅当用户明确要求 commit / 提交时**才创建 commit。
   - 用户未要求时：把变更留在工作区，汇报做了什么、测试与 review 结果，等待指示。
   - 不要擅自 `git push`，除非用户明确要求。

## 约束

- 本技能是编排层：驱动 `matt-tdd` 与 `matt-code-review` 等**模型纪律**技能，不要再调用其他 user-invoked 编排技能。
- 多文件大改动可用后台子代理 / 并行 worker，但 seam、验收标准与 commit 决策仍由本会话掌握。
