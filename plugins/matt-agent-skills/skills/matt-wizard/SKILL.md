---
name: matt-wizard
description: 为人只能亲自完成的步骤生成分阶段引导（人类清单 + 可选脚本）。用于开通基础设施、配置凭证或 CI secrets、走陌生第三方控制台、或一次性迁移/切换。agent 自己能做的步骤不要调用本技能。触发词：matt-wizard, human checklist, secrets, cutover。
invocation: model
---

# Wizard

**Wizard** 引导人类一步步完成只能由人执行的手工流程：冗长到不愿手记、又冗长到不愿每次向 AI 重讲。它打开每个 URL，精确说明点哪里、复制什么，捕获值并写到该去的地方（`.env`、CI secrets），每阶段确认，并显示还剩多少阶段。可能配置第三方服务、跑一次性迁移，或把项目从一状态搬到另一状态。

## 交付形态（agent 无关）

优先产出 **人类可执行的分阶段清单**（Markdown），必要时再附 **可选可执行脚本**。不要默认假设只有 bash + Claude 终端。

1. **主交付：人类清单（必做）**
   - 有序列 stage：每阶段名称、要打开的 URL、点击/复制路径、捕获的变量名、写入位置（`.env` / CI secret / 变量 / 仅动作）、是否 secret、不可逆动作前的确认门。
   - 进度可见（Stage N/M）、可中断重跑（已写入的值可跳过或回车保留）。
   - 用对话内确认门（或等价 UI）代替「只能在 bash `read` 里按回车」。

2. **可选交付：脚本（用户要求或流程会反复跑时）**
   - 可基于同目录 `template.sh`（bash 库：清屏、open_url、ask/ask_secret、write_env、set_secret/set_var、confirm、finish）生成；或按用户环境改成他们偏好的语言。
   - `template.sh` 中 **STAGES 标记以上的库不要手改**；只在标记以下编写各 stage。
   - 脚本是增强，不是唯一形态。无 shell / 无 `gh` 时，清单本身必须仍可独立跑完。

Wizard 默认短暂：为一次运行而建，落到 scratch 或 `scripts/`，事毕可删。仅当用户要可重复的 setup 路径时才提交进仓库。

## 流程

### 1. 界定流程范围

弄清人类必须采取的每一步，以及沿途捕获的每个值。先读仓库，不要冷问：

- Setup：`.env`、`.env.example`、`.env.*`、`README`、`docker-compose*`、框架配置、以及 CI workflow（每个 `secrets.*` / `vars.*` 引用都是 matt-wizard 必须产出的值）。
- 迁移或切换：当前状态、目标状态、其间的不可逆动作。

然后向用户展示有序 stage 列表及各 stage 产出的值，并确认：他们可增、删、重排。

**完成标准：** 每个 stage 已按序命名；对每个捕获值你知道 (a) 人类从哪取得，(b) 写到哪（`.env`、CI secret、两者、或无处；有些 stage 是纯动作），(c) 是否 secret（隐藏输入）或公开。

### 2. 映射每阶段旅程

为每阶段写出人类精确路径：打开哪个 URL、在那做什么、值显示在哪、填入哪个变量。例如 "Dashboard → Developers → API keys → Reveal test key → copy"。若你不确定当前 UI 或精确命令，如实说明并问用户或查文档：绝不发明可能不存在的步骤。

**完成标准：** 每个 stage 都能追溯到陌生人可跟随的具体说明。

### 3. 撰写交付物

**清单（始终）：** 写成 Markdown，结构建议：

```markdown
# <Wizard title>

总计 N 个 stage。可随时停下；已写入的值在重跑时保留。

## Stage 1/<N>: <Name>
- 打开: <URL>
- 操作:
  1. ...
  2. ...
- 捕获: `VAR_NAME`（secret: yes/no）
- 写入: `.env` / CI secret `NAME` / 仅确认动作
- 确认门: <不可逆时必问>

## Stage 2/<N>: ...
...

## 收尾核对
- [ ] 所有必填值已落盘
- [ ] CI secret 名称与 workflow 中 `secrets.*` 一致
- [ ] 跳过项已列出手工补做说明
```

**可选脚本：** 若用户要脚本，复制 `template.sh` 到目标路径；用 `stage`、`say`/`step`、`open_url`、`ask`/`ask_secret`、`write_env`、`set_secret`/`set_var`、`pause`/`confirm` 按依赖序写各 stage；设 `TOTAL_STAGES`。保持模板标准：先开 URL 再要值；secret 用隐藏输入；持久值用 `write_env`；CI 真正需要的才 `set_secret`；不可逆前 `confirm`。每 `stage` 清屏只留当前步。不要改标记以上的库。

### 4. 校验与交接

- 静态核对：步骤 1 的每个值都被捕获并落到步骤 1 所说之处；每个 CI secret 名与 workflow 中引用完全一致。
- 若有脚本：`bash -n <script>`；有则跑 `shellcheck`；`chmod +x`。不要自己端到端跑（会开浏览器并阻塞人类输入）。
- 告诉用户如何按清单执行（以及若有脚本如何运行）。若是可重复 setup，按用户要求提交并在 README 链接，让下一个人跑清单/脚本而不是再问 AI。

## 反模式

- Agent 自己能完成的步骤却做成 matt-wizard（本技能明确不用于此）。
- 只交 bash、人类无 shell 时无法执行。
- 发明第三方控制台步骤。
- 在不可逆动作前无确认门。
- 把 secret 回显到日志或聊天明文。
