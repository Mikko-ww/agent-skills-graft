# GitHub 项目检索策略

在需要构造查询或核验 GitHub 数据时读取本文件。

## 工具优先级

1. `gh search repos`：发现候选、获取当前 Star、更新时间、语言和链接。
2. `gh api repos/{owner}/{repo}`：核验仓库详情、许可证、是否归档/Fork、创建和推送时间。
3. GitHub 仓库 README、文档和 Releases：确认产品形态与能力。
4. Web 搜索：消歧产品、寻找官方站点或弥补 `gh` 不可用。
5. Star History、OSS Insight 等：仅在能看到明确时间序列时用于 Star 趋势。

`gh` 未安装、未认证或 API 限流时，改用 Web 搜索和 GitHub 页面。不要因工具不可用而编造指标。

## 查询矩阵

为同一需求构造 3–6 组互补查询：

| 查询类型 | 目的 | 示例 |
|---|---|---|
| 精确实体 | 找官方与生态 | `"LibTV"`、`org:libtv-labs` |
| 产品类别 | 找直接竞品 | `"AI video workspace"` |
| 交互形态 | 找相似体验 | `"infinite canvas" video AI` |
| 核心工作流 | 找业务链路 | `"script to storyboard" video` |
| 技术能力 | 找关键模块 | `"GitHub App" "code review agent"` |
| 自部署/许可证 | 满足落地约束 | `self-hosted language:TypeScript` |
| Topics | 扩展社区词汇 | `topic:ai-video topic:storyboard` |

优先使用英文检索，再补中文行业词。GitHub 上大量中文项目的描述同时含英文，但不能假定全部如此。

## 常用命令

发现候选：

```bash
gh search repos "AI video workspace" \
  --sort=stars \
  --archived=false \
  --limit=30 \
  --json fullName,description,stargazersCount,forksCount,language,updatedAt,url
```

按形态和 Topic 检索：

```bash
gh search repos '"infinite canvas" video' --archived=false --sort=stars --limit=30
gh search repos --topic=ai-video --topic=storyboard --archived=false --sort=stars
```

核验仓库：

```bash
gh api repos/OWNER/REPO --jq '{
  name: .full_name,
  description: .description,
  stars: .stargazers_count,
  forks: .forks_count,
  archived: .archived,
  fork: .fork,
  language: .language,
  license: .license.spdx_id,
  created_at: .created_at,
  pushed_at: .pushed_at,
  topics: .topics,
  homepage: .homepage
}'
```

读取 README：

```bash
gh api repos/OWNER/REPO/readme --jq '.content' | base64 --decode
```

若命令不可用，使用等价的 GitHub 页面或 Web 工具。不要把命令失败解释为“没有相关项目”。

## 从宽到窄

1. 先搜索参考产品和类别，收集仓库描述中的行业词。
2. 用产品形态与工作流词再次搜索。
3. 加入用户硬约束：`self-hosted`、语言、许可证、桌面/Web 等。
4. 从各查询保留候选并去重。
5. 先粗筛 15–30 个，再深入核验 5–10 个。

搜索结果过窄时，去掉一个限定词或改用同义词；过宽时增加产品形态、工作流或 `--match name,description,readme`。

## 产品消歧查询

遇到陌生产品名，至少尝试：

```text
"产品名" official
"产品名" GitHub
"产品名" docs
"产品名" [用户描述的领域]
site:github.com "产品名"
```

优先确认官方域名、组织名和产品定位。注意：

- 同名仓库可能属于完全不同领域。
- 官方 GitHub 可能只有 SDK/Skill，产品本身并不开源。
- 第三方仓库可能在描述中自称“替代品”，但功能尚未实现。

## Star 趋势

当前 Star 与趋势是两个指标：

- 当前 Star：GitHub REST/Search API 的 `stargazers_count`。
- Star 趋势：带时间戳的累计或新增 Star 序列。

可接受的报告：

```text
当前 12,438 Stars（GitHub，2026-08-27）
近 30 天 +1,204 Stars（Star History，查询于 2026-08-27）
```

不可接受的替代指标：

- “最近提交很多，所以 Star 增长快”
- “项目刚创建就有 10k Star，所以趋势很好”
- 用 `updatedAt` 或 `pushedAt` 推断 Star 增量

只能取到最近若干 Stargazer 时，清楚写成下限或样本，不要冒充完整 30/90 天趋势。

## 搜索停止条件

满足以下条件即可停止扩展查询：

- 至少有 3 个经过 README 核验的强候选，或确认该领域没有这么多。
- 核心产品形态、工作流和技术能力查询均已覆盖。
- 新查询主要返回重复候选。
- 首选、模块参考和明显误匹配已能区分。
