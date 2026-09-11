# UI Prototype

在同一路由上生成**几种截然不同的 UI 变体**，用底部浮动栏切换。用户在浏览器里翻变体，挑一个（或从每个里偷一点），然后扔掉其余。

若问题关乎逻辑/状态而非长什么样，这是错误分支。用 [LOGIC.md](LOGIC.md)。

## 何时是正确形状

- 「这页应该长什么样？」
- 「想在提交前看看这个 dashboard 的几种选项。」
- 「给 settings 屏试一种不同布局。」
- 任何否则会在脑子里花一天在三个模糊 mockup 间挑选的场合。

## 两种子形状：强烈偏好子形状 A

当 UI matt-prototype **紧贴应用其余部分**时，评判容易得多：真实 header、真实 sidebar、真实数据、真实密度。孤立的一次性路由是真空：每个变体单独看都好看。只要有说得通的既有页面可以承载变体，就默认子形状 A。只有 matt-prototype 真的没有附近家园时，才伸手要子形状 B。

### 子形状 A：调整既有页面（首选）

路由已存在。变体**在同一路由上**渲染，由 `?variant=` URL search param 门控。既有的数据拉取、params、auth 都留下。只换渲染。这是默认；除非有具体理由，否则选它。

若 matt-prototype 针对的东西尚无页面，但*自然会活在某个页面里*（dashboard 的新区块、settings 屏的新卡片、既有流程的新步骤），仍是子形状 A。把变体挂进宿主页面。

### 子形状 B：新页面（最后手段）

仅当被原型化的东西真的没有既有页面可栖身时使用（例如全新顶层表面，或无法合理嵌入任何地方的流程）。

按项目已有的路由约定创建**一次性路由**。不要发明新的顶层结构。命名上让人一眼看出是 matt-prototype（例如路径或文件名含 `matt-prototype`）。同样的 `?variant=` 模式。

提交子形状 B 之前做一次 sanity-check：真的没有既有页面可以嵌入吗？空路由会藏起一个充实页面会暴露的设计问题。

两种子形状下，底部浮动栏相同。

## 流程

### 1. 陈述问题并选定 N

默认 **3 个变体**。超过 5 就不再是截然不同，而变成噪声，因此封顶。

在 matt-prototype 所在位置或文件顶注释里用一行写下计划：

> 「settings 页的三个变体，经 `?variant=` 切换，挂在既有 `/settings` 路由上。」

无论用户是否在场反驳，这都管用。

### 2. 生成截然不同的变体

起草每个变体。对每个坚持：

- 页面的目的与它能拿到的数据。
- 项目的组件库 / 样式系统（TailwindCSS、shadcn、MUI、纯 CSS 等）。
- 清晰导出的组件名，例如 `VariantA`、`VariantB`、`VariantC`。

变体必须**结构上不同**：不同布局、不同信息层级、不同主 affordance，而不只是不同颜色。三个微调过的卡片网格不是 UI matt-prototype，是壁纸。若两稿太像，用明确的「不要用卡片网格」指导重做其中一个。

### 3. 接线

在路由上做一个单一 switcher 组件：

```tsx
// 伪代码，按项目框架适配
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

子形状 A（既有页面）：把既有数据拉取留在 switcher 之上；只有渲染子树按变体变化。

子形状 B（新页面）：在 `/matt-prototype/<name>` 下的一次性路由挂上同样的 switcher。

### 4. 构建浮动切换器

屏幕底部中央一个小的固定栏，三块：

- **左箭头**：切到上一变体（环绕）。
- **变体标签**：显示当前变体 key，以及若变体导出了名字则一并显示，例如 `B (Sidebar layout)`。
- **右箭头**：向前切（环绕）。

行为：

- 点箭头更新 URL search param（用框架的 router，例如 Next 的 `router.replace`、React Router 的 `navigate` 等），使变体可分享且刷新稳定。
- 键盘：`←` 与 `→` 也循环。当 `<input>`、`<textarea>` 或 `[contenteditable]` 聚焦时不要拦截方向键。
- 视觉上与页面区分（例如高对比 pill、轻阴影），使它明显不是被评估设计的一部分。
- 生产构建中隐藏：用 `process.env.NODE_ENV !== 'production'` 或等价检查门控，避免误 merge 把栏送到用户手里。

把 switcher 放进单一共享组件，使两种子形状都能复用。放在项目共享 UI 所在之处。

### 5. 交接

把 URL（以及 `?variant=` keys）摊开。用户会在有空时翻。有趣的反馈通常是**「我要 B 的 header 配 C 的 sidebar」**，那才是他们真正想要的设计。

### 6. 捕获答案并清理

一旦某个变体胜出，捕获答案（哪个变体以及为什么），再按 [SKILL](SKILL.md) 描述的方式捕获 matt-prototype。把赢家折进真实代码，其余移到一次性分支，而不是进 main：

- **子形状 A**：把赢家折进既有页面；从 main 去掉落败变体与 switcher。
- **子形状 B**：把胜出变体提升为真实路由；从 main 去掉一次性路由与 switcher。

完整变体集是 primary source，因此落在一次性分支上，而不是垃圾桶：留在 main 里的变体组件与 switcher 会很快腐烂并迷惑下一读者。

## 反模式

- **变体只差颜色或文案。** 那是微调，不是 matt-prototype。真变体在结构上意见不合。
- **变体之间共享太多代码。** 共享 `<Header>` 可以；共享 `<Layout>` 会毁掉意义。每个变体应能自由扔掉布局。
- **把变体接到真实 mutation。** 只读 matt-prototype 没问题。若变体需要 mutation，指到 stub：问题是「这应该长什么样」，不是「后端能不能工作」。
- **把 matt-prototype 直接升为生产。** 变体代码是在 matt-prototype 约束下写的（无测试、最少错误处理）。折进去时要正当重写。
