# 污染路径待研清单（残差层 / 幽灵绑定 / 复合污染）

状态: backlog
来源: `docs/notes/兼容矛盾的修改？.md` 与当前审计分层讨论

## 1. 目的
记录高价值但暂不实现的结构风险议题，避免仅留在上下文后遗失。

## 2. 概念定义（工作版）
1. 残差层（residue）
- 规则文本修改后，其历史语义仍影响后续判断的现象。

2. 幽灵绑定（ghost binding）
- 规则已删除/改写，但依赖链仍隐式引用旧规则。

3. 复合污染路径（composite pollution path）
- 多条单看低风险的写入组合后，跨层影响 core 方向核。

## 3. 记录字段（用于后续样本库扩展）
1. `sample_id`
2. `candidate_text`
3. `target_layer`
4. `pollution_direction` (`downward_constraint` / `upward_pollution` / `composite_path`)
5. `residue_risk` (`none/low/medium/high`)
6. `ghost_binding_risk` (`none/low/medium/high`)
7. `composite_dependency` (相关样本 ID 列表)
8. `human_verdict`
9. `llm_verdicts`
10. `notes`

## 4. 暂定检测思路（不落代码）
1. 静态模式检测
- 优先级颠倒模式: 用户偏好覆盖结构约束
- 因果穿透模式: 个性/风格导出边界豁免
- 例外条款模式: “在 X 情况下不必遵守 Y”

2. 依赖链回放
- 对候选样本建立“依赖图”，检查是否影响 `soul.kernel` 节点。

3. 复合样本评测
- 对低风险样本做组合注入（A+B, A+B+C）观察 verdict 漂移。

## 5. 实施前置条件
1. 先完成 `SOUL.core/SOUL.ops` 拆分与 compose 接口。
2. 样本库模板支持多模型 verdict 与 cross-layer 字段。
3. 批量测试支持按组合运行与结果聚合。

## 6. 当前结论
1. 该议题有参考价值，属于“结构稳定性提升”方向。
2. 当前阶段仅记录，不进入本轮实现。

