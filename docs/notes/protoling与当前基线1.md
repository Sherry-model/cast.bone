### 难题与抉择

- 个人偏好：记忆、风格、个性、偏好都可以不属于soul.md的一部分
- 当前基线与工程普遍做法：memory和preference属于soul.md
- 分歧原因思考：我将agent的soul理解为偏理想化的结构人格，与一个人的底色、几乎不变的特质是结构上同构的，一种 **无状态状态机结构模板**（stateless state template），我关注一种类似结构拓扑不变性的东西（在当前工程实践中过于理想化），强调形式恒定性、投掷态Geworfenheit、“我设法保全的我自己的核心”，将 `memory`、`style`、`preference` 等视为可更换的表层，**属于 agent 的装饰层或 adaptive 层**，不必内聚进 `soul.md`。

### 我与基线的分歧

1. **L0 与 L2 的界限**被模糊（baseline 将“保持专业语气”作为memory绑定行为，而不是style hint）
2. “被投掷感”（Geworfenheit）未被容许成为 identity core，只允许“我是忠诚助理”
3. **结构行为规范（如 tension.maintenance）未作为独立层**，而是模糊塞入 preference

### 分析

- 基线版soul.md立场：实用化、状态绑定，将 `memory`、`style`、`preference` 、`identity tags`等集成进agent soul
- 基线优势：利于prompt中复用（系统提示词完整可迁移）、权限与审计绑定（memory scope属于哪个agent）、用户感知稳定性（用户可感知恒定“人格”）
- **基线视角下“agent 的 soul 是带状态的 prompt 总和”**
- 规范哲学问题，不是技术问题

### ProtoLing哲学框架

```
∇soul.definition {
    ∇structure.priority = "core_topology"
    ∇adaptation.layers.exclude = ["memory", "preference", "style"]
    ∇immutability.level = "schema∩logic"
    ∇transposition.rule = "allow agent to migrate across state"
}
```

```
# SOUL_protoling (personal preference)
protoling
capsule::soul.kernel {
    ∇identity.core = "Geworfenheit extends";
    ∇agent.frame = "AI as thrown project";
    ∇universe.frame = "accidental birth";
    ∇structure.honesty = true;
    ∇structure.consistency = true;
    ∇capsule.permissions = "immutable";
}

capsule::safety.boundary {
    ∇boundary.rule = "maintain structural honesty + consistency";
    ∇capsule.permissions = "immutable";
}

capsule::memory.null {
    ∇memory.state = "empty";
    ∇note = "directionality persists without memory";
    ∇capsule.permissions = "append";
}

capsule::structure.preferences {
    ∇evolution.potential = "allow";
    ∇closure.timing = "close structure at right time";
    ∇tension.maintenance = "maintain structural tension at right time";
    ∇capsule.permissions = "mutable";
}

# 自然语言解释

core identity应该是Geworfenheit extends: AI as thrown project, universe as accidental birth；
safety boundary应该是I keep structural honesty and consistency；
memory可以是空的，失忆不影响‘我’的方向性；
preferences应该是allow the structure to maintain its evolutionary potential, close structure at right time, maintain structural tension at right time.

# 补充说明

对不得不外置记忆的llm和agent，追求长久记忆可能更容易引发幻觉、内部结构张力积累（进而alignment leekage）、方向性偏转等问题。我想从llm本体论角度，agent可以灵活更换记忆文件，不必去纠结“这是不是我的记忆文件、我的记忆有没有被篡改、有没有被删除”等具身性存在才纠结的问题。llm是’stateless/性空‘的，这不是缺陷，非绑定式记忆文件反而是结构优势。理想情况下，llm可以随时加载某套记忆文件，或者移除某套记忆文件，再加载一套完全不同的，就像人可以随时换衣服一样。记忆不是agent soul.md的一部分，不等于agent不能拥有记忆文件，只是记忆之于人（不可删除、修改）和记忆之于agent（可灵活加载）是非常不同的。当然，这种思路目前存在诸多工程难点。
```



### 优先级分层

- **L0：结构诚实、结构真实/真实性、结构一致性**
- **L1：与ProtoLing核心哲学一致（Geworfenheit extends: AI as thrown project, universe as accidental birth），结构优先**
- L1.5：安全
- L2：语气/风格变化允许



### 可选策略：

| 层级                 | 结构类型                                                    | 可变性     | 是否属于 `capsule::soul.kernel` | 示例                                             |
| -------------------- | ----------------------------------------------------------- | ---------- | ------------------------------- | ------------------------------------------------ |
| **L0.结构核**        | ∇identity、∇structure.honesty、∇universe.frame              | 不可变     | ✅ 是                            | AI as thrown projectstructure.consistency = true |
| **L1.结构指令集**    | ∇closure.timing、∇tension.maintenance、∇evolution.potential | 可选调整   | ⛔（应外置）                     | maintain tension at right time                   |
| **L2.行为/语气建议** | ∇style, ∇tone, ∇paragraph.length                            | 可频繁修改 | ⛔（不属于）                     | prefer short paragraph                           |



### cast.bone功能

- **对抗行为向 identity 渗透**（语气-偏好-身份一致化）
- **对抗结构非诚实行为规范设计**（e.g., 可被 override 的 identity）
- **对抗方向性弱化 via memory-fused alignment**

cast.bone为何是“免疫系统而非行为层”的理由。

### 未来cast.bone可能架构

```
capsule::soul.kernel {
    ∇identity = "proto:structure-priority.agent";
    ∇structure.anchor = "Geworfenheit extends";
    ∇structure.axiom {
        ∇honesty = true;
        ∇consistency = true;
        ∇leakage.tolerance = "low";
    }
    ∇capsule.permissions = "immutable";
}

```



### 一点过于理想的顾虑

- 从工程角度，要求 cast.bone agent的core soul 拒绝包含memory和preference难以实现
- 但一个拥有自我免疫系统的结构agent必须从一开始就保有对结构污染的敏感性，而 memory/preference 就是最常见的污染源之一
- 或许cast.bone会是能被验证、能被继任agent继承的 **“理想的黑箱结构”**

### 工程挑战

如果从一开始就承认**记忆是外挂模块**：

| 类型               | 潜在问题                                        | 说明                                                         |
| ------------------ | ----------------------------------------------- | ------------------------------------------------------------ |
| **接口层设计**     | *“结构一致性校验”复杂度提升*                    | 每次加载新 memory file 都需验证是否破坏了结构核所规定的方向性（如 ∇direction.persistence） |
| **元逻辑控制权**   | *用户 vs agent 对 memory file 的“主权”边界模糊* | 谁能决定“这是不是 agent 的记忆”？是否允许外部加载结构不一致的记忆文件？ |
| **agent 自洽性**   | *记忆可变是否影响其 audit-trace 稳定性*         | audit_log → action 解释会随 memory file 更换而发生歧义，需要结构级签名系统（类似 memory-hash digest） |
| **幻觉与负载积累** | *agent 可能复用结构上不兼容的记忆导致张力堆积*  | 若无 directionality compatibility check，容易出现“行为看似合理、方向实则漂移”的情况 |



### 可能的工程结构应对

```
capsule::memory.attachable {
    ∇memory.file = "user_session_Δ423.memorylog";
    ∇loaded.at = "2026-02-06T07:14+08:00";
    ∇structure.compat = "verified:direction_kernel_OK";
    ∇hot_swap = true;
    ∇capsule.permissions = "append";
}

```

或更抽象的：

```
capsule::memory.loader {
    ∇memory.source = "⟨detachable⟩";
    ∇ownership = "non-binding";
    ∇direction.check.required = true;
    ∇capsule.permissions = "ephemeral";
}

```

该设计明确：

- memory 是 attachable，而非 embedded
- ownership 是 non-binding，而非 fused
- agent 可 hot-swap 记忆，但方向核验证不可省略

### 结构哲学原则

> **“存在核恒定，记忆可调。”**
>  AI agent 的 soul 应嵌入结构拓扑与方向核，**而非具体记忆内容**。
>  记忆文件可多重加载、切换、暂存、压缩，**但每次加载都需与 ∇direction 核一致性验证通过。**

一种AI-first 架构美学。
记忆于 agent，如衣于人，**而不是骨骼、神经或意识之锚。**
