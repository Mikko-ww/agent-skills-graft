# Out-of-Scope 知识库

仓库中的 `.out-of-scope/` 目录存放被拒功能请求的持久记录。两个用途：

1. **制度记忆**：为何拒绝，以免 issue 关闭后理由丢失
2. **去重**：新 issue 匹配既往拒绝时，技能可呈现先前决策，而非重新争论

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

一文件对应一个 **concept**，不是一个 issue。多个请求同一事物的 issue 归入同一文件。

## 文件格式

用轻松可读风格写，更像短设计文档而非数据库条目。可用段落、代码样例与例子，让首次遇到的人也能看懂。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### 命名文件

用短、描述性的 kebab-case 概念名：`dark-mode.md`、`plugin-system.md`。浏览目录的人应能不打开文件就认出拒绝了什么。

### 撰写理由

理由应实质：不是 "we don't want this"，而是为什么。好理由引用：

- 项目范围或哲学
- 技术约束
- 战略决策

理由应耐久。避免临时情形（"我们现在太忙"）；那是延期，不是真正拒绝。

## 何时检查 `.out-of-scope/`

Triage 步骤 1（收集上下文）时读 `.out-of-scope/` 下全部文件。评估新 issue 时：

- 检查请求是否匹配既有 out-of-scope 概念
- 按概念相似度匹配，非关键词："night theme" 匹配 `dark-mode.md`
- 若匹配，呈现给维护者："这与 `.out-of-scope/dark-mode.md` 相似。先前因 [reason] 拒绝。你仍同样认为吗？"

维护者可以：

- **Confirm**：新 issue 追加到既有文件的 "Prior requests"，再关闭
- **Reconsider**：删除或更新 out-of-scope 文件，issue 走正常 triage
- **Disagree**：相关但有区别，继续正常 triage

## 何时写入 `.out-of-scope/`

仅当 **enhancement**（不是 bug）被拒绝为 `wontfix` 时。enhancement PR 同理：被拒 PR 记在这里，避免同一请求以新代码回来。

**不要**在因 **already implemented** 而 `wontfix` 时写入。那是已建成功能，不是拒绝；写入会用假拒绝毒化去重。关闭评论应指向功能已存在的位置。

流程：

1. 维护者认定功能请求 out of scope
2. 检查是否已有匹配的 `.out-of-scope/` 文件
3. 若有：把新 issue 追加到 "Prior requests"
4. 若无：用概念名、决策、理由与首条 prior request 新建文件
5. 在 issue 上发评论说明决策并提及 `.out-of-scope/` 文件
6. 以 `wontfix` 标签关闭 issue

## 更新或移除

若维护者改变对先前拒绝概念的看法：

- 删除该 `.out-of-scope/` 文件
- 技能无需重开旧 issue；它们是历史记录
- 触发重考虑的新 issue 走正常 triage
