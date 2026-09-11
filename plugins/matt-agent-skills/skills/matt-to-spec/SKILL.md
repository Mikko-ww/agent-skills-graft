---
name: matt-to-spec
description: 把当前对话综合成 Spec 并发布到项目 issue tracker。不做访谈，只综合已讨论内容。触发词：matt-to-spec, Spec, ready-for-agent。
invocation: user
disable-model-invocation: true
---

# To Spec

把当前对话上下文与代码库理解综合成一份 Spec。**不要**再访谈用户；只综合你已经知道的内容。

issue tracker 与 triage 标签词表应由项目配置提供。若缺失，请用户先运行 `matt-configure-project-docs`。

## 流程

1. 若尚未探索仓库，先探索以理解代码库现状。Spec 全文使用项目 domain glossary 词汇，并遵守相关区域的 ADR。

2. 草拟将用来测试该功能的 **seam**。优先复用已有 seam；尽量选最高层的 seam。若必须新增，也提到你能达到的最高点。整个代码库里 seam 越少越好，理想数量是一个。

   与用户确认这些 seam 符合其预期。

3. 按下方模板撰写 Spec，然后发布到项目 issue tracker。打上 `ready-for-agent` triage 标签，无需额外 triage。

## Spec 模板

```markdown
## Problem Statement

用户视角下，用户面临的问题。

## Solution

用户视角下的解决方案。

## User Stories

一份**很长**的、编号的用户故事列表。每条格式：

1. As an <actor>, I want a <feature>, so that <benefit>

示例：

1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending

该列表应极为详尽，覆盖功能的各个方面。

## Implementation Decisions

已做出的实现决策列表，可包括：

- 将构建/修改的 module
- 将修改的那些 module 的 interface
- 开发者给出的技术澄清
- 架构决策
- Schema 变更
- API 契约
- 具体交互

**不要**写入具体文件路径或代码片段（很快会过时）。

例外：若 matt-prototype 产出的片段比散文更能精确编码决策（state machine、reducer、schema、type shape），可内联在相关决策中，并简短注明来自 matt-prototype。只保留决策密集部分，不是可运行 demo。

## Testing Decisions

已做出的测试决策列表，包括：

- 何为好测试的描述（只测外部行为，不测实现细节）
- 将测试哪些 module
- 测试的 prior art（代码库中同类测试）

## Out of Scope

本 Spec 明确不做的事情。

## Further Notes

关于该功能的其他说明。
```
