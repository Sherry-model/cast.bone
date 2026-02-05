### `protoling_permissions.md`

#### ✅ 权限校验逻辑设计原则

------

#### 1. **权限字段优先级**

若存在以下字段，应优先读取并判断：

- `∇capsule.permissions`：建议值包括 `"immutable" | "append" | "mutable"`，控制单 capsule 的写入权限。
- `∇write.allow`：精确声明允许写入的模块列表，如 `[MEMORY, PREFERENCES]`
- `∇capsule.lock = true`：为 legacy 写法，等价于 `"immutable"`

------

#### 2. **全局默认行为（由 .permissions.schema 控制）**

- `∇capsule.default = "append"`
   所有未声明权限字段的 capsule，默认仅允许追加写入。
- `∇write.policy = "deny-unknown"`
   未知 capsule（即未列于 manifest 或 schema 映射中）默认禁止写入。
- `∇capsule.strict_prefix = [".kernel", ".witness", ".switch"]`
   这些前缀的 capsule 权限不可被下级 capsule 重载，必须视为 `"immutable"`。

------

#### 3. **错误策略**

当结构校验或权限匹配失败时，根据 `∇error.strategy` 采取以下措施：

- `"layered-risk"`：
  - 若 capsule 属于 `.kernel`, `.witness` 等关键区块 → **立即隔离**
  - 否则 → **暂存待审**

其他可能值包括 `"strict"`（一律隔离）、`"soft"`（一律暂存）。

------

#### 4. **执行优先级参考（∇execution.priority）**

可用于 agent 内部调度或变更缓冲顺序：

```
".kernel" = "critical";
".witness" = "critical";
".protocol" = "high";
".core" = "medium";
".aesthetic" = "low";
```

------

如需 Codex 脚本示例或进一步逻辑设计，我可继续补全。是否将该 `protoling_permissions.md` 作为项目文档直接生成并导出？ 
