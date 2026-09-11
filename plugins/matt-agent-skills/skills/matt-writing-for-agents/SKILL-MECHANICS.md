# Skill mechanics（通用 Agent）

[`matt-writing-for-agents`](SKILL.md) 的 skill 专用分支：当文档是 skill 时，frontmatter、invocation 选择与 router skills 有何不同。其余写法见 `SKILL.md` 的通用参考。

本仓库约定的 frontmatter：

```yaml
---
name: <id>
description: <一句中文「何时使用」+ 保留关键英文触发词>
invocation: user | model
---
```

不要使用产品专属字段（例如 `disable-model-invocation`、`agents/openai.yaml`、`policy.allow_implicit_invocation`、Claude plugin 安装说明）。用 `invocation` 表达同一意图。

## Invocation

两种选择，交换两种 load：

- **Model-invoked**（`invocation: model`）：保留面向模型的 `description`，agent 可自主触发，其他技能也可「调用同名技能」到达它。用户仍可显式点名：model-invocation **始终包含**用户可达；`description` 只增加 agent 发现，从不剥夺人类。`description` 是 skill 的顶层 context pointer，被迫始终加载：用永久 context load 换可发现性。内容全是 reference 的 model-invoked skill，也可作为共享 reference 的家：其他 skill 可调用它，使多份 skill 共用的 reference 只活在一处。写法：`invocation: model`，并写带 trigger branches 的模型向 `description`（`SKILL.md` 的 pointer 写作规则全部适用）。

- **User-invoked**（`invocation: user`）：从 agent 自主触发中剥离：只有人类点名该 id 才能调用，其他 skill 也不能靠 description 发现它。零 context load，但花费 cognitive load：你是必须记得它存在的索引。写法：`invocation: user`；`description` 改为面向人类的一行摘要，去掉「Use when…」式触发列表（仍可保留中文「何时由用户显式调用」的简短说明）。

仅当 agent 必须自行到达该 skill，或另一 skill 必须到达它时，才选 model-invocation。若永远只靠人手触发，做成 user-invoked，不付 context load。

两个 user-invoked skill 都需要的共享 reference，不能放在其中任一个里：没有可被发现的 description，彼此无法触发对方。把它推到技能系统外的普通文件：任何 skill 都可指向的 external reference。

## Splitting by invocation

拆分的 invocation 切口（sequence 切口在 `SKILL.md`）：当你有一个应独立触发的、清晰的 leading word（你在 prompts 中真实使用的触发词），或另一 skill 必须到达它时，拆出一个 model-invoked skill。你为新的始终加载 `description` 付 context load，因此独立可达必须值得。

## Router skills

当 user-invoked skills 多到记不住时，堆积的 cognitive load 用 **router skill** 治愈：一个 user-invoked skill，点名其他技能及各自何时取用，使人只需记住一个入口。它只能提示，不能代替人类触发那些 user-invoked skills：它们没有面向模型的触发 description，除人类外无人能到达。

Router 正文应写「调用同名技能 `<id>` / 采用下列纪律」，而不是绑定某一产品的 Skill tool、slash command 或 plugin API。

## 组合不变量

- User-invoked skill 可以编排（调用）model-invoked skills，**不要**要求再调用另一个 user-invoked skill。
- 跨技能引用用技能 id 与「调用同名技能」表述，保持 agent-agnostic。
