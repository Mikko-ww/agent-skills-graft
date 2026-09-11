---
name: matt-handoff
description: 将当前对话压缩成 handoff 文档，供另一个 agent 接手继续工作。用户显式调用；可附带「下一会话用途」说明。
invocation: user
disable-model-invocation: true
---

撰写一份 handoff 文档，概括当前对话，使全新 agent 能继续工作。保存到用户操作系统的临时目录（例如 Linux/macOS 的 `/tmp`），**不要**写进当前工作区。

文档中须包含 **suggested skills（建议技能）** 一节，点名下一 agent 应采用哪些同名技能（按技能 id 列出，并说明为何需要）。

不要重复已经落在其他产物中的内容（specs、plans、ADR、issues、commits、diffs）。用路径或 URL 引用它们。

脱敏任何敏感信息，例如 API keys、密码、个人身份信息（PII）。可用 `<REDACTED>` 占位。

若用户传入了参数，将其视为对「下一会话将聚焦什么」的描述，并据此裁剪文档内容与 suggested skills。

## 建议结构

```md
# Handoff: <简短标题>

## Goal
下一会话要完成什么。

## State
已完成 / 进行中 / 阻塞点（各用短列表）。

## Artifacts
路径或 URL 列表（specs、ADR、CONTEXT.md、PR、diff 等）。勿粘贴全文。

## Decisions already made
只写尚未写入 ADR/spec 的、下一 agent 必须知道的决策。

## Open questions
仍未落定、会影响下一步的问题。

## Suggested skills
- `<skill-id>`: 为何调用
- …

## Do not
明确禁止的动作（例如不要重开已关闭的讨论、不要提交密钥）。
```

写完后向用户报告文件的绝对路径，便于粘贴到下一会话或交给另一 agent。
