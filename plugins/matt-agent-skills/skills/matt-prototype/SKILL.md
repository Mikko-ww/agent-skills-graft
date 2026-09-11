---
name: matt-prototype
description: 用一次性 prototype 回答设计问题。在用户要 sanity-check 某状态模型或逻辑是否对劲、或探索 UI 应长什么样时使用。
invocation: model
---

# Prototype

Prototype 是**回答一个问题的一次性代码**。问题决定形状。

## 选分支

根据用户提示、周围代码、或在用户在场时询问，识别正在回答哪个问题：

- **「这套逻辑 / 状态模型对劲吗？」** → [LOGIC.md](LOGIC.md)。做一个可分享的单文件 HTML（自由试玩按钮 + 分页引导 walkthrough），把状态机推过纸面上难推理的案例，且非开发者也能驱动。
- **「这应该长什么样？」** → [UI.md](UI.md)。在同一路由上生成几种截然不同的 UI 变体，通过 URL search param 与底部浮动栏切换。

两个分支产出截然不同的产物，选错会浪费整个 matt-prototype。若问题真的暧昧且用户够不着，默认选更贴合周围代码的分支（后端 module → logic；页面或组件 → UI），并在 matt-prototype 顶部声明该假设。

## 两边通用的规则

1. **从第一天起就是一次性的，并明确标成这样。** 把 matt-prototype 代码放在靠近它将来真正使用之处（紧挨它所原型化的 module 或页面），使上下文一目了然，但命名上让随便扫一眼的读者看出这是 matt-prototype，不是生产代码。对一次性 UI 路由，遵守项目已有的路由约定；不要发明新的顶层结构。
2. **跑起来要 trivial。** UI matt-prototype 从项目 task runner 的一条命令启动：`pnpm <name>`、`python <path>`、`bun <path>` 等。Logic demo 是用户双击即可打开的单个 HTML 文件。无论哪种，启动都无需思考。
3. **默认无持久化。** 状态活在内存里。持久化是 matt-prototype *在检查* 的东西，不是它该依赖的东西。若问题明确涉及数据库，打 scratch DB 或带清晰「PROTOTYPE, wipe me」名字的本地文件。
4. **跳过 polish。** 无测试、无超出「让它能跑」之外的错误处理、无抽象。目的是快速学到东西。
5. **把状态摊开。** 每次动作之后（logic）或每次切换变体时（UI），打印或渲染完整相关状态，让用户看见变了什么。
6. **完成后捕获。** 把任何已验证的决策折进真实代码，然后把 matt-prototype 本身当作 **primary source** 捕获：提交到一次性分支（离开 main），并在实现 issue 上留一个指向该分支的上下文指针。同时把答案（裁决与它解决的问题）写进 issue 或 commit。main 分支只保留已验证的决策。
