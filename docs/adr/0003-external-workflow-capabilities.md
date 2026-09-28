# Skill 组织外部工作流，CLI 提供可组合研究能力

为了允许用户按任务选择不同模型、推理档位和 Agent 程序，工作流与产物传递由 Skill 指导外部工具完成：当前可用 Multica CLI，也允许宿主 subagent 协作，Multica 不是研究 CLI 的必需依赖。Siglens CLI 提供研究能力、本地证据产物、状态和校验，继续直接调用 Jev 辅助判断；它不实现 Agent 调度或跨机器产物运输，Discovery 与 Named-Topic 流程保留为可组合能力的参考用法。

第九轮澄清并收紧此前“Multica 编排 + CLI 研究包导入导出”的提案：运输及其工具选择属于 Skill，研究 CLI 保留普通产物读写与校验。
