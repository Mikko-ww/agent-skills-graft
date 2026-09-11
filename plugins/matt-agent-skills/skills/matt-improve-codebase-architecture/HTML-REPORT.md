# HTML 报告格式（精简）

架构评审渲染为 OS 临时目录中的单个自包含 HTML。Tailwind 与 Mermaid 均来自 CDN。Mermaid 负责图式；手写 div/SVG 负责编辑性视觉。混用二者，不要事事靠 Mermaid。

完整 scaffold、卡片字段、图示模式与用词约束已并入 `SKILL.md` 的「HTML 报告（精简）」节。本文件保留为速查要点：

1. 临时路径：`$TMPDIR` / `/tmp` / `%TEMP%` → `architecture-review-<timestamp>.html`
2. Header：repo、日期、图例（实线框=module，虚线=seam，红箭头=leak，厚深色=deep）。无开场白。
3. 每候选：Title、强度徽章、Files、Before/After、Problem、Solution、Wins（≤6 词）、可选 ADR 警告。
4. 图模式：Mermaid graph/sequence、手写 boxes-and-arrows、cross-section、mass diagram、call-graph collapse。混用，避免千篇一律。
5. 用词硬约束：只用 module / interface / depth / seam / adapter / leverage / locality；禁止 component / service / boundary 等漂移。
6. Top recommendation：一张大卡，候选名 + 一句理由 + 锚点链接。
7. 除 CDN 脚本外报告静态；图高约 320px。
