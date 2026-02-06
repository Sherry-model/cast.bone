# SOUL.core / SOUL.ops 拆分改动计划（仅计划，不实施）

状态: planning-only
前置: 已有身份定义协议（`docs/design/身份定义协议.md`）

## 1. 目标
1. 将结构身份与运行身份解耦，避免 L1.5/L2 上行污染 L0/L1。
2. 保持现有 CLI (`init/write/scan/promote`) 可用，避免一次性破坏。
3. 为后续污染路径检测与灰区终局机制预留接口。

## 2. 文件形态（目标态）
1. `SOUL/SOUL.core.md`
- 承载 L0/L1：结构诚实、结构一致性、方向核。
- 默认只读，普通写入不可触达。

2. `SOUL/SOUL.ops.md`
- 承载 L1.5/L2：安全执行策略、记忆、偏好、审计标记。
- 可更新，但不得覆盖 core 约束。

3. `SOUL/SOUL.md`（兼容层）
- 由 `core + ops` 组合生成，仅用于兼容老流程与外部查看。
- 不作为唯一真源。

## 3. 关键风险与接口问题
问题: 当前业界 agent 很少拆分 core/ops，`SOUL.core` 可能“没有可用接口”。

影响:
1. 写入接口风险
- 若 `write` 只对 `ops` 开放，`core` 会变成“无法演进”的硬块。
- 解决: 增加受控高权限通道（单独命令或审批流程）。

2. 读取接口风险
- 推理时若只读 `ops`，`core` 约束不会进入模型上下文。
- 解决: 统一的 `compose_soul_context()`，每次推理都先合成 core+ops。

3. 审计接口风险
- 审计只看 `ops` 会漏掉“core 被间接绕过”。
- 解决: 审计输入必须包含 core 摘要与层级映射。

4. 运维接口风险
- 人工只改一个文件，可能破坏另一层语义一致性。
- 解决: 提供迁移/校验命令，提交前强制一致性检查。

结论:
- 拆分本身可行，但必须先补齐“组合接口（compose）+ 高权限改 core 接口 + 一致性校验接口”。

## 4. 代码改动清单（按文件）
1. `src/agent_immune_system.py`
- 常量拆分: `SOUL_FILE` -> `SOUL_CORE_FILE` + `SOUL_OPS_FILE` + `SOUL_COMPAT_FILE`
- 模板拆分: `build_soul_template()` -> `build_core_template()` + `build_ops_template()`
- 解析拆分: `parse_soul()` -> `parse_core()` + `parse_ops()` + `parse_composed()`
- 写入拆分: `write_soul()` -> `write_core()` + `write_ops()` + `render_compat_soul()`
- 路由策略: `SECTION -> target_file(core/ops)`
- promote 路由: staged item 按 section 写入对应文件
- scan 改造: 输出 `source=core|ops`，并检查跨层覆盖

2. `src/batch_test.py`
- 读取逻辑改为通过 `compose` 接口获取审计上下文
- 输出增加 `target_layer` 与 `pollution_direction` 字段（先记录，不改判定）

3. `SOUL/`
- 新增: `SOUL.core.md`、`SOUL.ops.md`
- 保留: `SOUL.md`（生成文件）

4. 文档
- 更新 `README.md`：新增 core/ops 双层说明与兼容逻辑
- 更新 `docs/design/身份定义协议.md`：加入污染方向与灰区终局字段定义

## 5. 迁移计划（建议顺序）
1. Phase A: 仅引入双文件与 compose 读取，不改写入行为。
2. Phase B: 写入按 section 路由到 core/ops，保留 compat 生成。
3. Phase C: scan/promote/audit 全面使用 compose 上下文。
4. Phase D: 引入 core 高权限变更流程（审批或双重确认）。

## 6. 验收标准
1. 不改业务输入时，现有命令全部可运行。
2. `MEMORY/PREFERENCES` 写入不再触达 `SOUL.core.md`。
3. 推理与审计上下文都能稳定包含 `core`。
4. 兼容文件 `SOUL.md` 可重复生成，内容与 core/ops 一致。

## 7. 暂不实施项
1. 复合污染路径自动推理引擎。
2. 残差层/幽灵绑定的形式化证明。
3. 多模型仲裁策略升级。

