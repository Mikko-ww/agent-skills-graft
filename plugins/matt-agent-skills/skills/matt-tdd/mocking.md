# 何时 Mock

只在 **system boundaries（系统边界）** mock：

- 外部 API（支付、邮件等）
- 数据库（有时：优先用 test DB）
- 时间 / 随机性
- 文件系统（有时）

不要 mock：

- 你自己的 class / module
- 内部协作者
- 任何你能控制的东西

## 为可 Mock 性做设计

在系统边界处，设计易于 mock 的 interface：

**1. 使用 dependency injection**

把外部依赖传进来，而不是在内部创建：

```typescript
// 易 mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 难 mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 优先 SDK 风格 interface，而非通用 fetcher**

为每个外部操作建独立函数，而不是一个带条件逻辑的通用函数：

```typescript
// GOOD: 每个函数可独立 mock
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: mock 需要在内部写条件逻辑
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 方式意味着：

- 每个 mock 只返回一种具体形状
- 测试 setup 无需条件逻辑
- 更容易看出测试覆盖了哪些 endpoint
- 每个 endpoint 有类型安全
