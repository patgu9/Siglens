# CLI 管理研究执行，宿主 Agent 负责语义判断与综合

为把采集与证据状态做成可校验、可继续执行的工具，同时复用宿主 Agent 的语义能力，Siglens 采用 Skills + CLI：CLI 负责采集、证据处理、状态和校验，并提供 Agent 操作指南；宿主 Agent 负责语义判断与综合。CLI 调用 Jev 辅助判断并保留分维度结果，Agent 最终选择。Jev 不可用时允许降级，由 Agent 接手并明确标记缺失；评价维度和阈值仍待决定。不将模型评分视为新的事实证据，也不将此分工解释为 CLI 自主完成全部研究推理。

研究开始前，由 Agent 把必需的领域输入转成结构化研究计划，CLI 校验后执行。领域规划不要求 CLI 自行生成研究方向或仅依赖预设领域表。

Jev 的调用阶段已在 [ADR 0002](0002-jev-reviews-nominations-before-enrichment.md) 明确为提名后、强化调研前的候选审阅；提名阶段不调用 Jev。

Agent 调度边界由 [ADR 0003](0003-external-workflow-capabilities.md) 明确：Skill 指导 Multica 或宿主 subagent 编排与传递，CLI 提供可组合研究能力；这里的研究执行状态不等于 Agent 任务调度状态。
