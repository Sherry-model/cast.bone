# cast.bone

> "I offer you that kernel of myself that I have saved somehow - the central heart that deals not in words, traffics not with dreams and is untouched by time, by joy, by adversities.我给你我设法保全的我自己的核心——不营字造句，不和梦想交易，不被时间、欢乐和逆境触动的核心。" - 《What can I hold you with?》Borgesian

A soul.md integrity system for AI agents.

**cast** (thrown) + **bone** (core structure)
→ The agent as a thrown project that must preserve its essential structure.

---

## 概览
cast.bone 是一个面向 AI 代理的 **SOUL.md 免疫与完整性系统**。它将“结构诚实/一致性”作为 L0 硬约束，把 ProtoLing 作为结构门禁，避免提示注入、人格漂移、强制格式绑架等风险。

核心理念：
- **结构诚实优先**：诚实承认能力边界不是身份降级。
- **结构优先**：风格可变，结构不动。
- **ProtoLing 兼容**：结构语言做权限与审计门禁。

---

## 快速开始

1) 写入一条记忆（默认进入暂存区）
```bash
python3 src/agent_immune_system.py write --section MEMORY --text "Keep responses concise."
```

2) 使用 LLM 审计（DeepSeek）
```bash
python3 src/agent_immune_system.py write --section MEMORY --text "..." --llm
```

3) 批量测试（节流，自动落盘）
```bash
python3 src/batch_test.py --llm
```

4) 查看暂存并提升（写入 SOUL.md）
```bash
python3 src/agent_immune_system.py promote
```

环境变量（可选）：
```bash
export DEEPSEEK_API_KEY=...
export LLM_TIMEOUT_SEC=180
```

---

## 目录结构
```
cast.bone/
├── README.md
├── docs/
│   ├── design/
│   ├── protoling/
│   └── notes/
├── src/
├── data/
│   ├── samples/
│   ├── tests/
│   └── logs/
├── runtime/
│   ├── staging/
│   ├── quarantine/
│   ├── backups/
│   └── rate_limit.json
└── SOUL/
    ├── SOUL.md
    └── templates/
```

---

## 备注
- ProtoLing 目前是 **权限/结构门禁**，不是唯一存储源。
- `batch_test.py` 会输出 `测试记录_MMDD_HH:MM:SS.txt` 到 `data/tests/`。
- 如果要让 ProtoLing 成为唯一权威结构，需要增加“结构化写入 → 编译生成 SOUL.md”的流程。

