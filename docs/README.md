# Siglens 文档索引

整理日期：2026-09-29。当前处于 MVP 需求与设计阶段，尚无产品实现或端到端验收结果。

**从 [MVP 规格](design/mvp-spec.md) 开始阅读。** 它汇总截至第二十九轮 Q78 的有效决定、首版边界、待定接口和验收清单。下表覆盖现有文档，区分当前需求、专题草案、历史决定与研究参考。

## 阅读与维护规则

1. 当前范围、默认行为和交付要求以 MVP 规格的已确认部分为入口；术语查阅 [CONTEXT.md](../CONTEXT.md)。
2. 专题文档继续保存设计理由、例子和接口建议。“建议”“草案”“待定”不等于已确认要求，示意命令不等于可用工具。
3. 设计访谈与 ADR 用于追溯决定。发生冲突时回查后续有效回答，再同步主规格和相关专题；不以文件位置或旧段落覆盖后续决定。
4. 研究资料说明当时核查的事实、快照和限制，不自动成为 Siglens 的需求，也不证明当前服务可用。
5. 本次保留所有原有文档路径和历史记录，仅收拢当前范围入口。后续范围变化先更新主规格，再更新相关专题，避免多份“当前范围”独立演变。

## 当前规格与领域语言

| 文档 | 用途 | 状态 |
| --- | --- | --- |
| [实施方案 (Implementation Plan)](design/implementation-plan.md) | Stage 2 方案评审终审实施方案、架构拓扑、状态机、错误表与测试矩阵 | 已批准 (APPROVED)，移交 Stage 3 Build |
| [事件档案与连续日报](design/event-archive-and-daily-brief.md) | Stage 1 Think 产出方案 B 设计文档：事件档案、连续日报与热度榜 | 已批准 (APPROVED) |
| [MVP 规格](design/mvp-spec.md) | 产品范围、流程、渠道、评分、证据、恢复、待定项、验收与决定追溯 | 当前汇总基线；实现和验收未开始 |
| [领域语言](../CONTEXT.md) | Domain、Topic、Nomination、Evidence、Topic Card 等术语 | 当前术语表，不承担实现规格 |

## 专题设计

以下文档混合已确认行为与待定设计，应结合各文档状态说明及主规格阅读。

| 文档 | 负责的问题 | 仍需细化的重点 |
| --- | --- | --- |
| [研究能力](design/research-capabilities.md) | 提名、候选审阅、主题研究和交付的组合 | 能力前置条件、产物契约 |
| [CLI 交互](design/cli-interaction.md) | 操作面、指南、输入输出、提交与交付校验 | 命令名、schema、退出码及冲突处理 |
| [执行、复用与恢复](design/research-limits.md) | 串行写入、复用、续跑与固定窗口 | 操作身份、版本和异常恢复；额度控制已撤回 |
| [渠道与证据契约](design/source-evidence-contract.md) | 七渠道、doctor、Brave 降级、正文和文件保存 | 验证细节、引用结构、禁用渠道的间接检索边界 |
| [Jev 辅助判断](design/jev-assistance.md) | 调用阶段、四维五档 Score、模型判断边界 | 具体量表与调用契约；早期 unknown 段落为历史 |
| [候选淘汰](design/candidate-elimination.md) | 资格、薄证据、低分建议和最终选择 | 状态及审计记录、阈值评测 |
| [结构化研究报告](design/research-report.md) | Named-Topic 报告、背景材料、不确定结论 | 章节为建议，数据格式与模板待定 |
| [Skill 与 Agent 分工](design/agent-routing.md) | 外部编排、Agent 分配和产物交接 | 具体工作流与交接方式 |
| [Go / Python 比较](design/language-choice.md) | 技术栈取舍和安装方向 | Python 3.12+ / uv tool 已确认；包名和依赖待定 |

## 决定与历史记录

| 文档 | 内容 | 当前用法 |
| --- | --- | --- |
| [设计访谈](design/discovery-mvp.md) | 第一至第二十九轮回答和少量当时事实核查 | 保留决定演进；当前范围统一跳转主规格 |
| [ADR 0001](adr/0001-agent-cli-responsibilities.md) | CLI 与宿主 Agent 的职责 | 有效架构边界；其中评分待定措辞反映记录当时状态，现行评分查主规格 |
| [ADR 0002](adr/0002-jev-reviews-nominations-before-enrichment.md) | Jev 在提名后、强化调研前审阅 | 有效；Named-Topic 不要求候选审阅 |
| [ADR 0003](adr/0003-external-workflow-capabilities.md) | Skill 指导外部编排，CLI 提供研究能力 | 有效；研究 CLI 不承担运输 |
| [unknown 与 Jev Score](design/jev-unknown.md) | Q69 前的评分 unknown / Choice 分析 | 已撤回，不属于实现待办 |
| [浏览器兜底探索](design/browser-fallback.md) | Jev + browser_use 可行性研究 | Q60 排除出 MVP，仅作后续参考 |

## 研究参考

这些文件主要记录 2026-09-28 的核查。last30days 源码分析采用固定提交，不能据此宣称实时渠道或本项目已通过验证。

| 文档 | 内容与限制 |
| --- | --- |
| [last30days 工作流程](research/last30days-workflow.md) | 上游 Skill / CLI 调用链及可借鉴边界，不是 Siglens 规格 |
| [last30days 交付](research/last30days-deliverables.md) | 综合报告与证据资料的分层，辅助设计研究报告 |
| [last30days junk 与评分](research/last30days-junk-scoring.md) | 固定源码规则、局部纯函数样例和 Siglens 量表草案；非模型质量验证 |
| [last30days 六渠道实现](research/last30days-channel-implementations.md) | 接入调用链及依赖，不代表本项目照搬全部后端 |
| [Grok 认证与 X 采集](research/grok-auth-path.md) | 登录 CLI、宿主搜索和 API Key 路径的区分；适配器仍待实现 |
| [早期七渠道接入候选](research/source-access-mvp.md) | 早期官方 API 优先候选表，未采纳为默认组合；当前组合查主规格 |

## 当前整理结论

MVP 的两条入口、职责分工、七渠道方向、候选审阅规则、证据要求及恢复原则已明确。下一步需要细化可执行接口并进行实现与实测，详见主规格的“尚待细化与验证”和“验收清单”。浏览器、额度控制、评分 unknown、CLI 内调度与运输均不应因旧资料仍存在而重新进入首版范围。
