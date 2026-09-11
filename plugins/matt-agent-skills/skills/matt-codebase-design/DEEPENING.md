# Deepening

如何在给定依赖下，安全地加深一簇 shallow module。假定 [SKILL.md](SKILL.md) 中的词汇：**module**、**interface**、**seam**、**adapter**。

## 依赖类别

评估 deepening 候选时，先给依赖分类。类别决定加深后的 module 如何跨 seam 测试。

### 1. In-process

纯计算、内存状态、无 I/O。总是可加深：合并 module，直接通过新 interface 测试。不需要 adapter。

### 2. Local-substitutable

有本地测试替身的依赖（Postgres 的 PGLite、内存文件系统）。若替身存在则可加深。加深后的 module 在测试套件里带着替身跑。seam 是内部的；module 的外部 interface 不需要 port。

### 3. Remote but owned（Ports & Adapters）

你自己的、跨网络边界的服务（微服务、内部 API）。在 seam 处定义 **port**（interface）。deep module 拥有逻辑；传输层作为 **adapter** 注入。测试用内存 adapter。生产用 HTTP/gRPC/队列 adapter。

建议形状：*"在 seam 处定义 port，为实现生产与测试分别实现 HTTP adapter 与内存 adapter，使逻辑落在一个 deep module 中，即便部署跨网络。"*

### 4. True external（Mock）

你不控制的第三方服务（Stripe、Twilio 等）。加深后的 module 把外部依赖当作注入的 port；测试提供 mock adapter。

## Seam 纪律

- **一个 adapter 意味着假设的 seam。两个 adapter 才意味着真实的 seam。** 除非至少两个 adapter 有正当理由（通常是 production + test），否则不要引入 port。单 adapter 的 seam 只是间接层。
- **Internal seams vs external seams。** deep module 可以有 internal seams（对 implementation 私有，供自身测试使用），以及 interface 处的 external seam。不要只因为测试用到了，就把 internal seams 暴露到 interface 上。

## 测试策略：replace, don't layer

- 一旦加深后 module 的 interface 上有了测试，旧的 shallow module unit 测试就成为浪费；删掉它们。
- 在加深后 module 的 interface 上写新测试。**Interface 就是测试面。**
- 测试通过 interface 断言可观察结果，而不是内部状态。
- 测试应能在内部 refactor 后继续存活，因为它们描述行为而非实现。若实现一变测试就必须改，说明它在测越过 interface 的东西。
