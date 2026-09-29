## Implementation Plan: Siglens MVP · 事件档案与连续日报

- **Status**: APPROVED (Ready for Stage 3: Build)
- **Review Pipeline**: CEO Review (Stage 1) ⟶ Design Review (Stage 2) ⟶ DevEx Review (Stage 2) ⟶ Eng Review (Stage 3)
- **Stage**: Sprint Pipeline - Stage 2 (Plan) ⟶ Hand-off to Stage 3 (Build)

---

### 1. Strategic Context & Scope Boundaries (CEO Review)

- **Core Wedge & Objective**: 为发起人 patgu9 提供「每天接得上昨天的 AI 进展地图」：在指定 AI 领域内持续发掘高价值新进展，替代手动刷 X/社区与低频检索；同时保留完整可追溯证据链。形态为 Skill + 独立 CLI（Python 3.12+, `uv tool` 安装），由外部工作流每日向 Multica 投递英文结构化日报。
- **Premise Challenge Findings**:
  - *替代手动刷信息*: 痛点由用户确认，核心目标是“降低理解新变化的成本”，保留少结果与空白状态的诚实表达，不以卡片数量或抓取行数代理价值；
  - *热度是必要发现信号*: 明确保留，但严禁将热度与事实确证混为一谈；低互动一手发布与高热度纯猜测独立分流，确保重大一手进展不被热度淹没；
  - *七渠道信息增量*: 坚持七渠道覆盖底线，但“已尝试”不等于“无遗漏”，必须逐渠道记录独有发现、补证与覆盖缺口，严禁短期低产出擅自删渠道；
  - *连续档案价值*: 跨日关联与证据演进是核心壁垒；建立防误合并、误拆分与版本化纠错机制，历史变更绝不静默覆盖旧证据与已交付日报。
- **Scope Mode**: **`Hold Scope`**（坚决保留方案 B、七大渠道、热度榜、Discovery 与 Named-Topic 两大入口；加固可验证性、事务安全与断点恢复能力）。
- **Dream State Delta**:
  ```text
  CURRENT STATE (现状)
    [需求与设计文档已形成 / 仓库无产品源码与包 / 手动刷各社区信息差大 / 跨日线索靠人脑记忆]
         │
         ▼
  THIS PLAN (本次落地 · MVP 加固版)
    [独立 CLI (uv tool) + 宿主 Skill 编排 + 七渠道采集与定向降级 + Jev 四维审阅 +
     事件档案/证据版本化 + 真实平台热度榜 + Multica 英文日报连续投递与投递对账]
         │
         ▼
  12-MONTH IDEAL (12个月理想态)
    [多领域自主订阅 / 深度对比研究 Comparable / 社区共建渠道适配器 / 知识脉络演进图谱 /
     自动化证据核查与争议追踪 / 团队级多端协作与多 Agent 协同发现]
  ```
- **Accepted Scope**:
  1. Discovery（指定 AI 领域，默认 7 天窗口，最多 21 张主题卡）与 Named-Topic（具体主题英文结构化报告）；
  2. 七大渠道全量接入：X (受限 Grok 路线)、Reddit (RSS/列表)、GitHub (REST/Releases)、Hacker News (Algolia API)、Digg (公开端点)、arXiv (API)、Web (Brave 搜索 + 正文抓取)；
  3. 真实互动热度榜：分平台/分指标呈现，标明出处、指标含义、观察时间戳；缺失不补零，样本不足诚实提示；
  4. 跨期事件档案：稳定 Event ID、证据版本追踪、支持/反驳/未决事实关系标记、重点线索标记核查、误合并显式纠偏留痕；
  5. 外部工作流 + Multica 投递：支持投递对账状态机、网络中断安全恢复，避免重复发布同一日报；
  6. 独立 CLI（Python 3.12+，`uv tool` 安装，标准 JSON 输出，自带面向 Agent 的指南）。
- **Deferred / Out of Scope**:
  - 全局无领域 Discovery、完整 Comparable 对比研究工作流；
  - 浏览器端自动化采集兜底（无 Headless 浏览器兜底）；
  - 采集配额与 Jev 费用账本（撤销额度限制，不做复杂计费系统）；
  - 跨平台综合热度算法、复杂热度预测模型；
  - 集中式图数据库、分布式事件总线、多租户 SaaS 架构；
  - 公开发布 PyPI 包与第三方应用商店分发。
- **Implementation Alternatives**:
  - *Minimal Viable*: 模块化单包 CLI，标准库 SQLite 索引 + 不可变 JSON/MD 文件存储，外部调度，轻量可靠。
  - *Ideal Architecture*: 本地微内核服务 + 独立适配器进程 + 专用分布式存储。
  - *推荐路径*: **Minimal Viable 模块化单包 CLI**。在方案 B 框架下保持最精简的依赖与清晰的边界，标准库优先，严禁过早引入复杂中间件。

#### Error & Rescue Registry (E01–E23)

| 错误标识 | 场景与根因 | 异常契约 | 系统级救济手段 (Rescue Path) | 状态 / 交付影响 |
|---|---|---|---|---|
| **E01** | `doctor.env` 依赖缺失、Python<3.12 | `EnvironmentIncompatibleError` | 阻断执行并输出环境修复指令（如 `uv python install 3.12`） | 退出码 3，不产生坏状态 |
| **E02** | `doctor.auth` 凭据缺失或格式错误 | `ConfigurationError` | 标明具体缺失键名与受影响渠道，引导配置，不尝试网络调用 | 退出码 3，明确渠道不可用 |
| **E03** | `doctor.probe` 端点不可达或握手超时 | `ChannelProbeError` | 标记 `validation_failed`，记录 probe 诊断，不影响其他可用渠道 | 渠道置不可用，生成覆盖缺口 |
| **E04** | `source.fetch` 429 限流或服务端 5xx | `SourceRateLimitError` / `SourceServiceError` | 遵守 `Retry-After`，有限指数退避重试；保存断点，不无限级联 | 标记渠道 `failed`，生成可恢复断点 |
| **E05** | `source.parse` 上游结构变更、畸形数据 | `SourceSchemaError` | 隔离原始畸形响应供排查，安全降级，严禁记为“零结果” | 渠道记 `failed`，保留错误样本 |
| **E06** | `evidence.fetch` 正文抓取失败或仅有摘要 | `EvidenceFetchError` | 记录正文状态 `snippet`/`abstract`，由 Agent 决定补证，不伪造正文 | 标记初始证据不足，允许补证 |
| **E07** | `evidence.time` 事件时间未知或越界 | `EventTimeValidationError` | 保留候选；时间未知候选不进入近期主题卡，窗口外材料明确标记“背景” | 候选保留归档，不进入正式日报 |
| **E08** | `jev.call` Jev 审阅超时或不可达 | `JevUnavailableError` | 记录合法降级事件 `review_degraded`，由 Agent 人工审阅接手，严禁补分 | 允许流程继续，记录降级凭据 |
| **E09** | `model.call` 模型显式拒绝安全限制 | `ModelRefusalError` | Jev 按降级契约处理；综合阶段保留草稿并报警，严禁绕过安全限制 | 保留草稿，退出码 5 |
| **E10** | `model.decode` 模型返回非标准 JSON | `MalformedJSONError` | 单次有界重试，失败则按角色边界降级或停在草稿，严禁无端推测字段 | 停留在 draft 阶段 |
| **E11** | `model.validate` 输出缺必填字段或分数越界 | `ModelSchemaError` | 严格按 Schema 逐字段校验拒绝，禁止自动补齐缺项 | 拒绝并记录字段诊断 |
| **E12** | `model.call` 模型返回空响应 | `EmptyModelResponseError` | 与合法零候选明确区分，有限重试一次，失败转人工/降级 | 记录调用缺失，不伪造空结果 |
| **E13** | `evidence.bind` 引用不存在或证据与主张脱钩 | `EvidenceReferenceError` / `EvidenceSupportError` | CLI 强校验阻断坏引用，要求 Agent 修正绑定关系或标为未决主张 | 阻断 finalize，退出码 2 |
| **E14** | `event.revise` 档案并发修改或版本过时 | `ArchiveConflictError` / `EventRevisionError` | CAS 乐观锁拒绝陈旧提交，重新读取最新版本后显式提交修订 | 退出码 4，防止静默覆盖 |
| **E15** | `state.persist` 磁盘满、权限不足或写入中断 | `StorageFullError` / `StoragePermissionError` | 事务回滚，保持上一完整提交；隔离未持久化文件，等待重试 | 退出码 6，保持存储完整性 |
| **E16** | `state.read` 数据库或文件损坏 | `StateIntegrityError` / `SchemaVersionError` | 立即停止写入，进入只读模式，引导使用备份快照恢复 | 退出码 6，阻断进一步损坏 |
| **E17** | `heat.build` 热度指标缺失、不可比或过期 | `HeatMetricValidationError` | 缺失标为 null，严禁补零；少于 2 个可比样本时不排榜，仅展示单卡指标 | 榜单诚实降级为“样本不足” |
| **E18** | `report.finalize` 缺必填字段、超卡上限、时间越界 | `DeliveryValidationError` | 拒绝生成不可变 Edition，保留草稿及结构化缺口报告 | 退出码 2，不冒充正式交付 |
| **E19** | `delivery.send` 目标错误或授权失败 | `DeliveryTargetError` / `DeliveryAuthorizationError` | 发送前预检配置，失败保留待投递产物，严禁盲目向错误目标重发 | 保持 `ready`，等待配置修正 |
| **E20** | `delivery.send` 网络中断，远端回执丢失 | `DeliveryOutcomeUnknownError` | 进入 `unknown` 状态，禁止自动盲目重发，触发对账流程 | 状态置 `unknown`，进入对账 |
| **E21** | `delivery.reconcile` 对账无法确认唯一送达 | `DeliveryReconciliationError` | 保持 `unknown`，保留本地凭据，转交外部监督人工仲裁 | 退出码 7，人工对账恢复 |
| **E22** | `scheduler.resume` 失去写入锁或租约过期 | `WriterOwnershipError` | 检查 Owner 世代号，失效任务立即拒绝提交或发报 | 退出码 4，防止脑裂多发 |
| **E23** | `input.boundary` 恶意输入、路径逃逸或注入指令 | `UnsafeInputError` | 边界强拦截，记录安全审计日志，拒绝执行 | 退出码 2，安全拦截 |

#### Failure Modes Registry (F01–F16)

| 场景标识 | 失败场景 (Failure Scenario) | 根本原因 | 严重度 | 检测机制 | 防御与缓解策略 | 恢复路径 |
|---|---|---|---|---|---|---|
| **F01** | 日报增加阅读负担 | 重复内容、过长无重点 | 高 | 用户无替代感，阅读时间反增 | 严格设置卡片上限（最多21），正文1200词软阈值，提炼 At a Glance | 调整选题与版式，支持零结果诚实呈现 |
| **F02** | 热门事件淹没一手重要发布 | 以热度替代研究价值 | 高 | 低互动一手发布长期落选 | 设立独立“重要新进展”栏目，Jev 审阅与热度独立分流 | 审查候选淘汰日志，强制补证与回捞 |
| **F03** | 七渠道制造“全量”幻觉 | 把请求成功等同于全网无遗漏 | 高 | 已知重大事件漏检 | 分列各渠道配置、选择、执行状态与正文覆盖度 | 标明渠道覆盖缺口，定向发起补充研究 |
| **F04** | 多源引用实为单帖转载 | 未追溯原始出处身份 | 高 | 跨平台多条引用实际来自同一母帖 | 强制材料溯源与规范化归并，独立评估证据源独立性 | 修正证据关联计数，更正独立性结论 |
| **F05** | 误合并/误拆分污染事件历史 | 仅凭标题或实体相似机械归并 | 高 | 证据与主张冲突，修订率异常飙升 | Agent 提议 + CLI 结构校验 + 不可变历史版本 | 提交补偿性修订（Compensating Revision） |
| **F06** | 渠道故障误报为“无新进展” | 采集失败被当作空结果 | 高 | 故障日出现确定性“无新进展”断言 | 严格区分 E04/E05 与合法 `success_empty` | 修复网络后重试失败渠道，更新跟进结论 |
| **F07** | 热度榜单数值失真 | 跨平台相加、缺失补零、过期观测 | 高 | 缺乏出处与时间戳，榜单失真 | 落实 E17，按渠道/指标独立展示，缺失置 null | 撤销无依据名次，以真实样本标注 |
| **F08** | 模型幻觉导致伪证或误淘汰 | 模型响应异常、Prompt未对齐 | 高 | 引用不存在、边界分数异常 | 落实 E08–E13，强 Schema 校验，Jev 降级留痕 | 保留草稿，触发人工或 Agent 语义纠偏 |
| **F09** | 采集内容恶意注入越权 | 内容被误当作系统指令执行 | 高 | 非预期的外部工具调用 | 落实 E23，采集材料仅视为纯数据，严禁动态执行 | 阻断运行，隔离受影响产物并审计 |
| **F10** | 档案并发写入损坏或丢失更新 | 多任务并发写入共享状态 | 高 | 数据库锁冲突、文件覆盖 | 落实 E14/E22，单 Writer 限制，CAS 乐观锁 | 恢复已知有效备份，重放未提交操作 |
| **F11** | 重复日报轰炸或漏投 | 网络超时重发、外部触发混乱 | 高 | 同一 Edition 多次发布或缺失 | 落实 E19–E21，稳定 Edition ID，本地投递对账 | 强制进入 `reconciling`，核实后再发 |
| **F12** | 长任务超时拖垮日常投递 | 无界补证、外部 API 延迟高 | 高 | 执行周期延误，无法准时送达 | 单次请求硬超时，有界重试，断点即时持久化 | 从断点快速恢复，必要时以 Partial 交付 |
| **F13** | 本地调度离线静默停运 | 执行宿主关机或进程终止 | 高 | 外部监控缺失，无法察觉停运 | 外部调度健康检查，缺期告警 | 恢复调度器并执行对账，补发延期说明 |
| **F14** | 过度框架建设压倒业务验证 | 提前构建复杂图谱与预测系统 | 中 | 迟迟无法跑通连续两期真实日报 | 严格落实 Hold Scope，专注单包 Minimal Viable | 回归 MVP 核心闭环，延后复杂功能 |
| **F15** | 源站反爬升级或 API 变更 | 抓取规则失效、Cookie 失效 | 中 | doctor 探测失败，特定渠道归零 | 模块化适配器隔离，配置与凭据独立管理 | 修复受损适配器，期间透明报告覆盖缺口 |
| **F16** | 重点追踪清单无限膨胀 | 缺乏暂停与归档机制 | 中 | 每日跟进条目冗余，分析耗时暴增 | 建立 `active` 与 `paused` 生命周期，Agent 动态管理 | 暂停无效线索，归档历史，不删证据 |

---

### 2. UI/UX & Interaction Blueprint (Design Review)

- **Surface Mode**: **Read / Operate 混合型**（以 Multica 原生 Markdown 结构化只读日报为主，支持事件 ID 引用追问与重点追踪标记）。
- **Design Review Score**: **7/10**（距 10 分的差距：需待连续两期真实交付在 Multica 客户端核验排版、断点缺口呈现以及移动端可读性）。
- **Design Hard Rules & AI Slop Elimination**:
  - 杜绝 AI 套话（无“在当今快速发展的AI时代”等空洞引言，无无依据的未来猜测）；
  - 杜绝装饰性占位符与虚假仪表盘；
  - 采用标准 GFM Markdown，严禁依赖嵌入式 HTML、自定义 CSS 或未经验证的第三方组件；
  - 移动端友好：热度榜与覆盖状态采用纵向卡片列表，避免宽表格在移动设备上横向溢出；
  - 软长度阈值：正文控制在约 1,200 英文词以内，超量证据通过 Multica 附件（`--attachment`）交付，正文完整保留摘要、反证与覆盖缺口。
- **Complete 6-State Matrix**:
  1. `Loading`: 正在研究中（显式标明“`AI Research in progress...`”，附启动时间与已耗时长，严禁伪装成正式日报）；
  2. `Empty`: 健康零结果（七渠道均扫描但窗口内无实质新事件，简明透明说明，附渠道健康自检结果）；
  3. `Populated`: 正常正式交付（包含 At a Glance、Current Hot Topics、Important Developments、Follow-ups、Sources & Gaps）；
  4. `Error`: 运行中断（保留断点信息，输出 `E-code` 错误诊断与恢复建议，支持断点续跑）；
  5. `Success / Partial`: 部分渠道失败/降级（保留可用成果，显著标明缺失信源与覆盖缺口，不粉饰太平）；
  6. `Extreme`: 极端超量（超多源合并、数十条多渠道引用，通过首屏摘要 + 软截断 + 详细证据附件交付）。

---

### 3. Developer Experience & API Ergonomics (DevEx Review)

- **Target TTHW Tier**: **Champion**（针对零密钥本地环境实现秒级初始化与 Schema 导出），**Competitive**（真实七渠道与 Jev 配置完成并在 2 分钟内跑通 `doctor` 与首个样例）。
- **Developer Persona & Magical Moment**:
  - *Persona*: 独立开发者 / 宿主 Agent，追求高确定性、结构化输出与零冗余干扰；
  - *Magical Moment*: 运行 `uv tool install . && siglens doctor`，2 分钟内清晰输出七渠道连通性与配置就绪状态，首次 `siglens init` 立即生成标准化固定窗口 JSON。
- **API / CLI Specifications**:
  - `siglens doctor [--channels <list>]`：环境、凭据与只读连通性三层探测；
  - `siglens guide [subcommand]`：面向 Agent 输出结构化操作指南；
  - `siglens schema [name]`：输出离线 JSON Schema (Draft 2020-12)；
  - `siglens sources list`：列出渠道可用状态与凭据状态；
  - `siglens init --entry <discovery|named-topic> [--domain <d>] [--topic <t>] [--days <N>] [--channels <list>]`：初始化研究窗口；
  - `siglens collect <research_id> --plan-file <path> [--refresh]`：执行渠道采集与基础去重；
  - `siglens inspect <research_id> [--phase <p>]`：查看中间产物与证据上下文；
  - `siglens nominate <research_id> --plan-file <path>`：提交候选提名（不调用 Jev）；
  - `siglens review <research_id> [--candidates <list>]`：触发 Jev 四维审阅；
  - `siglens enrich <research_id> --plan-file <path>`：跨渠道补证；
  - `siglens draft <research_id> --cards-file <path> | --report-file <path>`：提交草稿；
  - `siglens validate <research_id>`：执行可程序化结构与时间校验；
  - `siglens finalize <research_id>`：固化不可变 Edition；
  - `siglens archive tracking list|update`：重点追踪与状态维护；
  - `siglens archive revise --plan-file <path>`：事件创建/关联/合并/拆分/语义纠偏；
  - `siglens deliver send <edition_id> --target <target_id>`：原子锁定 claim 发送权（返回 Edition 及 payload/attachment 哈希凭证）；
  - `siglens deliver reconcile --record-file <path>`：接收外部投递回执完成对账；
  - `siglens deliver status <edition_id>`：查询投递与对账状态。
- **Error Standards**:
  - 统一结构化错误输出（数据走 stdout，诊断日志走 stderr）：
    ```json
    {
      "success": false,
      "error": {
        "code": "E04",
        "category": "SourceRateLimitError",
        "problem": "Channel 'reddit' rate limited the request.",
        "cause": "HTTP 429 Too Many Requests received from upstream RSS endpoint.",
        "fix": "Wait until 2026-09-29T08:30:00Z as indicated by Retry-After header, or run collect with --channels excluding reddit."
      }
    }
    ```
- **Hall of Fame Benchmarks**:
  - 借鉴 `uv` 的极致速度、依赖解析与自包含单执行体体验；
  - 借鉴 `gh CLI` 的清晰子命令、默认 JSON 格式化与标准错误分流；
  - 借鉴 `last30days` 的多源采集策略与降级容错机制。

---

### 4. System Architecture & Engineering Guardrails (Eng Review)

- **Architecture Topology**:
```text
External Scheduler / Host Agent <───── Skill + Guide
  │ (Plan, Nominations, Decisions, Evidence Links, Draft)
  ▼
CLI Parsing + Versioned JSON Schemas (Draft 2020-12)
  │
  ▼
Application Layer (Research / Event / Delivery Workflows)
  │                   │                   │
  ▼                   ▼                   ▼
Source Adapters     Jev Port         Storage Port ──────┐
(X, Reddit, GitHub, (4D Scoring,     (CAS Lock,         │
 HN, Digg, arXiv,   Graceful          Atomic Commit,    │
 Web/Brave)         Degradation)      WAL Index)        │
  │                   │                   │             │
  ▼                   ▼                   ▼             ▼
External Upstream   Provider API     SQLite DB      Immutable Storage
Services                             (Commit Index  (Raw Text, Evidence
                                      + Ledger)      JSON, Report MD)
                                          │
                                          ▼
Delivery Ledger (Local CAS Claim) <───────┘
  │ (Atomically claim 'ready' -> 'sending', emit Edition + Hashes)
  ▼
External Delivery Workflow (Multica CLI)
  │ (Post Comment + Attachments to Parent Issue)
  ▼
Multica Server Target ───────────────► External Receipt / Reconcile
```

- **State Machine**:
```text
[Research Lifecycle]
created ──► planned ──► collecting ──► awaiting_agent ──► enriching ──► draft
                           ▲                 │                  │
                           └──── new plan ───┴──────────────────┘
draft ──validate──► validation_result
draft ──finalize (CAS Commit)──► immutable Edition (E1)
interrupted / failed ──► safe resume at same operation
successful (data OR empty) ──► replay receipt (idempotent)
explicit refresh ──► new attempt with same fixed window

[Event & Lineage Lifecycle]
proposed ──► active v1 ──► active v2 ──► ...
merge / split proposal ──► validate IDs + DAG + revisions ──► new lineage revision
stale revision / cyclic proposal ──► rejected (committed state intact)
erroneous merge / split ──► compensating revision (preserves historical IDs & references)
tracking axis: ordinary ◄──► active ◄──► paused (no history deletion)

[Delivery Reconciliation Ledger]
ready ──CAS claim──► sending ──external confirmed──► confirmed_delivered
                        │
                        ├──── known failure ────────► ready (safe retry authorized)
                        │
                        └──── response lost ────────► unknown
                                                        │
                                                        ▼
                                                  reconciling
                                                        │
                                   ┌────────────────────┴────────────────────┐
                                   ▼                                         ▼
                        proven delivered:                         proven not sent:
                        confirmed_delivered                       ready (safe retry)
```

- **Data Flow Shadow Paths (The 4 Paths)**:
  - **Happy Path**: `doctor` 验证通过 ⟶ 窗口固定 ⟶ 七渠道按序抓取 ⟶ 基础去重 ⟶ Agent 提名 ⟶ Jev 四维审阅 ⟶ 跨渠道有限补证 ⟶ Agent 综合英文主题卡 ⟶ CLI 结构校验 ⟶ 固化不可变 Edition ⟶ 本地原子 claim ⟶ Multica 投递成功 ⟶ 记录 receipt。
  - **Nil / Missing**: 凭据未配置（渠道标 `unconfigured`）；Brave 未配置且直连失败（保留缺失，禁止非法降级）；事件时间未知（候选保留归档，严禁进入近期卡）；Jev 服务中断（记录 `review_degraded` 凭证，Agent 接手审阅，不造假分）。
  - **Empty / Zero-Length**: 全渠道扫描但无实质新事件（返回合法 `success_empty`，生成健康空结果状态说明，不反复重试）；Jev 四维原始分全部 < 2（Agent 最终确认后淘汰，记录排除理由，若无合格卡生成空状态说明）。
  - **Upstream Failure**: 渠道限流 429（遵循 `Retry-After`，有限重试，记录断点）；上游数据畸形（隔离响应，报 `E05`，不当作零结果）；投递网络中断（本地记录置 `unknown`，必须对账确认，严禁盲目重投）。
- **Blast Radius & Downstream Mitigation**:
  - *单 Writer 锁机制*: 本地研究变更严格串行，跨研究修改共享档案需持有 SQLite 独占排他锁与 CAS 递增版本号，防止并发写入损坏档案；
  - *历史不可变原则*: Edition 一旦 Finalize 绝对不可变，更正生成新 Edition 并标记 `supersedes`；误合并通过补偿性修订修正，旧日报引用的历史证据链完整保留。
- **Pending Verification (Build-Stage Checkpoints)**:
  1. X (Grok 受限路径) 与 Digg 公开端点的真实可用性与数据结构实探；
  2. Jev 四维评分阈值在人工标注测试集上的误淘汰率校准；
  3. SQLite + 本地不可变文件在断电/崩溃注入测试下的 ACID 事务一致性证明；
  4. Multica 投递网络中断场景下的外部对账流程端到端跑通。
- **Worktree Parallelization Strategy**:
| 工作流 / 模块 | 涉及目录与组件 | 前置依赖 | 并行推进可行性 |
|---|---|---|---|
| **Stream A: Storage & Domain Core** | `siglens/core/`, `siglens/storage/`, `schema/` | 无 | 完全独立，优先启动 |
| **Stream B: Source Adapters & Doctor** | `siglens/sources/`, `siglens/doctor/` | Stream A Domain 契约 | 与 Stream A 并行开发 Mock，待 A 接口冻结后联调 |
| **Stream C: Jev & Candidate Review** | `siglens/review/`, `siglens/agent/` | Stream A Domain 契约 | 与 Stream B 完全并行 |
| **Stream D: CLI, Format & Delivery** | `siglens/cli/`, `siglens/deliver/`, Skill | Stream A, B, C | 待核心逻辑就绪后集成 |

---

### 5. Testing & Verification Matrix

- **Coverage Diagram**:
```text
Inputs (CLI / API / Plans)
  │
  ├─► Unit Tests: Domain Rules / Schemas / Timezone / State Transitions (100% path coverage)
  │
  ├─► Fixture Tests: E01–E23 Error Envelopes & F01–F16 Failure Injections
  │
  ├─► Integration Tests: Channel Adapters (Mocked + Real Live Probe) / SQLite CAS / Reconcile
  │
  └─► Mandatory Regression Tests: 15 Core Scenarios from mvp-spec.md §11 (A01–A15)
```
- **Unit Test Coverage**:
  - 核心领域模型（Event, Evidence, Claim, Revision, Edition）序列化与不可变约束；
  - Jev 四维展示分映射计算（原始分加 1，全 < 3 触发低价值建议，恰好等于 3 不触发）；
  - 渠道六态转换机与显式禁用渠道过滤逻辑；
  - 投递状态机（`ready -> sending -> confirmed_delivered / known_failure / unknown -> reconciling`）。
- **Integration Test Plan**:
  - SQLite commit index 与不可变文件的一致性提交与崩溃注入恢复测试；
  - 七渠道适配器在正常、限流（429）、畸形数据、空数据场景下的响应测试；
  - `doctor` 三层自检与缓存失效机制验证。
- **E2E / Eval Tests**:
  - 完整跑通 Discovery 流程（AI 领域，7 天窗口，产出合格英文主题卡）；
  - 完整跑通 Named-Topic 流程（指定主题，产出英文结构化研究报告）；
  - 连续两期日报端到端模拟测试（第一期发现事件，第二期成功关联并指出新增证据/反证）。
- **Mandatory Regression Tests (严格锁定 `mvp-spec.md` 第 11 节 A01–A15)**:
  - [x] **A01 入口与默认值**: Discovery 无 domain 阻断；默认 7 天、最多 21 张卡；Named-Topic 直接研究。
  - [x] **A02 窗口固定**: 续跑、补证、显式刷新均保持原起止时间；新研究才生成新窗口。
  - [x] **A03 事件时间依据**: 旧帖重发不产生新事件时间；未知时间候选保留但不进近期卡；窗口外标记背景。
  - [x] **A04 配置与覆盖**: 首次与配置变化触发 `doctor`；默认尝试全部验证可用渠道；选择不绕过验证。
  - [x] **A05 渠道状态真实性**: 严格区分未配置、未选择、故障与空结果，故障绝不伪称无结果。
  - [x] **A06 Brave 降级边界**: 仅选 X/Reddit 故障不调用 Brave；包含可用 Web 时允许定向降级并记录正文状态。
  - [x] **A07 Jev 阶段与契约**: 提名不调用 Jev；Discovery 审阅不可跳过；合法不可用记录降级凭证；Named-Topic 无 Jev 前置。
  - [x] **A08 评分精确计算**: 四维展示分全部 < 3 触发淘汰建议；2.99 触发，3.00 不触发；不因展示舍入改变判定。
  - [x] **A09 评分失败防御**: 缺失/畸形响应不补分，不触发低分淘汰；低置信度不生成 unknown。
  - [x] **A10 候选质量与包容度**: 纯猜测排除；低互动一手发布与单一来源不机械淘汰；薄证据允许补证。
  - [x] **A11 核查与证据可追溯**: 尝试跨渠道核查；一手证据仅支持直接陈述；正文、片段、摘要与综合严格区分。
  - [x] **A12 恢复与串行写入**: 重复执行复用成功结果；中断从断点恢复；状态变更严格串行。
  - [x] **A13 交付严格校验**: 引用无效、时间依据缺失、超卡上限均保留草稿并列出缺口，不冒充正式交付。
  - [x] **A14 不确定性结论**: Named-Topic 允许合法交付“目前无法确认”；渠道部分故障不阻断合规交付。
  - [x] **A15 本地安装与协作**: Python 3.12+ 下通过 `uv tool` 安装独立 CLI；默认 JSON，内置 Agent 指南；Skill 独立编排。

---

### 6. Zero-Downtime Migration & Rollback Plan

- **Migration Sequence (Expand-Contract 模式)**:
  1. *Phase 1 (Expand)*: 引入新的数据库表结构与字段，保持向后兼容；读取时兼容旧格式，写入时双写新格式；
  2. *Phase 2 (Backfill & Verify)*: 离线脚本分批重构历史档案索引与哈希校验，对比新旧读取一致性；
  3. *Phase 3 (Switch)*: 切换 CLI 读写路径至新 Schema，验证所有测试通过；
  4. *Phase 4 (Contract)*: 观察一个稳定周期后，安全废弃旧 Schema 字段与过渡兼容代码。
- **Rollback Procedure**:
  1. 外部停止新调度触发，撤销旧写入锁与投递授权；
  2. 将所有在途 `sending` 状态原子置为 `unknown` 并触发对账；
  3. 冻结当前数据库与不可变文件的完整只读副本；
  4. 回滚 CLI 包与 Skill 版本至上一稳定版本；
  5. 若新 Schema 保持向后兼容，直接以旧版本连接；若不兼容，使用升级前的备份快照加增量提交记录重放构建；
  6. 执行一致性验证（引用哈希、CAS 锁、固定窗口、历史 Edition）；
  7. 已投递日报绝不物理删除，若有误发另行发布更正版 Edition（标记 `supersedes`），维护审计透明性。

---

### 7. Aggregated Implementation Tasks

#### Phase 1: Database & Core Foundation
- [ ] Task 1.1: 搭建 Python 3.12+ 项目工程骨架，配置 `pyproject.toml`、`uv` 依赖管理、Ruff 代码规范与 MyPy 类型检查。
- [ ] Task 1.2: 实现纯领域核心模型（Event, Evidence, Claim, Revision, Edition, ResearchWindow）及不可变语义。
- [ ] Task 1.3: 实现基于 Draft 2020-12 的 JSON Schema 校验器与离线 Schema 导出命令（`siglens schema`）。
- [ ] Task 1.4: 构建 SQLite Commit Index 存储引擎，实现事务原子提交、CAS 乐观锁、Manifest 生成与不可变文件持久化。
- [ ] Task 1.5: 建立 E01–E23 统一异常类层级与标准化 `Problem + Cause + Fix` 错误信封机制。

#### Phase 2: Ingress API & Business Logic
- [ ] Task 2.1: 实现 CLI 命令行框架，规范标准子命令、参数解析、退出码规范（0, 2, 3, 4, 5, 6, 7）及 stdout/stderr 分流。
- [ ] Task 2.2: 实现 `siglens doctor` 三层自检模块（环境、配置、只读连通性探测）与 24h 缓存失效机制。
- [ ] Task 2.3: 实现七大渠道采集适配器（X, Reddit, GitHub, Hacker News, Digg, arXiv, Web）与渠道六态状态机。
- [ ] Task 2.4: 实现正文抓取、片段提取与受渠道选择限制的 Brave 定向降级逻辑。
- [ ] Task 2.5: 实现 Jev 四维审阅客户端，严格落实 0–4 原始分加 1 映射、全 < 3 淘汰建议与合法降级凭证记录。
- [ ] Task 2.6: 实现事件档案管理（新建、关联、合并、拆分、补偿性纠偏）与稳定 Lineage DAG。
- [ ] Task 2.7: 实现本地投递对账状态机（`ready -> sending -> confirmed_delivered / known_failure / unknown -> reconciling`）。

#### Phase 3: UI / Interface & State Handling
- [ ] Task 3.1: 实现面向 Multica 的英文日报 GFM Markdown 格式化渲染引擎（At a Glance, Hot Topics, Developments, Follow-ups, Gaps）。
- [ ] Task 3.2: 严格实现 6 态呈现矩阵（Loading, Empty, Populated, Error, Partial, Extreme）与健康空结果说明。
- [ ] Task 3.3: 实现热度榜单渲染逻辑（分平台/指标、出处、观察时间戳、样本不足标注、严禁跨平台加总与补零）。
- [ ] Task 3.4: 实现约 1,200 英文词软长度控制与 Multica 附件（`--attachment`）详细证据档案打包机制。
- [ ] Task 3.5: 编写宿主 Skill 定义（`SKILL.md`）与内置 Agent 交互指南（`siglens guide`）。

#### Phase 4: Testing & Verification Matrix
- [ ] Task 4.1: 编写领域核心与 Schema 单元测试，实现 100% 状态转换覆盖。
- [ ] Task 4.2: 实现 E01–E23 异常场景与 F01–F16 失败模式注入测试用例。
- [ ] Task 4.3: 编写 SQLite + 不可变文件持久化的崩溃注入恢复测试。
- [ ] Task 4.4: 严格实现并全量通过 `mvp-spec.md` 第 11 节 A01–A15 全部 15 项强制回归测试。
- [ ] Task 4.5: 跑通连续两期真实交付模拟测试，验证事件关联、证据演进、断点续跑与投递对账闭环。

---

### Phase 4: Final Approval Gate

#### Decision Audit Trail
| # | Phase | Issue Encountered | Classification | Applied Principle | Chosen Path & Rationale | Rejected Alternative |
|---|---|---|---|---|---|---|
| 1 | CEO | 范围模式抉择与早期演示裁剪风险 | Tier 1 (Mechanical) | Choose Completeness | 采纳 `Hold Scope` 模式，坚决保留方案 B、七渠道与双入口全量基线 | 缩减为仅支持 Reddit/Web 或仅支持单次日报的极简版本 |
| 2 | CEO | 系统架构形态与存储选型 | Tier 1 (Mechanical) | Pragmatic & DRY | 采纳 Minimal Viable 模块化单包 CLI，标准库 SQLite + 不可变 JSON/MD | 引入微服务集群、分布式事件总线或专用图数据库 |
| 3 | Design | Multica 日报排版与组件依赖 | Tier 1 (Mechanical) | Explicit Over Clever | 采用原生 GFM Markdown 与纵向卡片列表，无自定义 CSS/HTML | 依赖富交互前端卡片组件或复杂内嵌 HTML 样式 |
| 4 | Design | 正文长度与详细证据平衡 | Tier 2 (Taste) | Boil Lakes | 设立约 1,200 英文词软阈值，摘要入文，详版证据由附件交付 | 无限制超长文本硬展示，或粗暴截断遗失反证与缺口 |
| 5 | DevEx | CLI 错误标准与退出契约 | Tier 1 (Mechanical) | Explicit Over Clever | 统一 `Problem + Cause + Fix` 结构，数据与日志分流，严格定义 0–7 退出码 | 仅抛出 Python 堆栈或模糊的一般性错误信息 |
| 6 | DevEx | 渠道状态枚举与降级边界 | Tier 1 (Mechanical) | Choose Completeness | 严格划分六种渠道终态，显式禁用渠道优先，禁止 Web 间接偷抓 | 粗暴合并为成功/失败两态，或允许 Web 隐式越权抓取 |
| 7 | Eng | 存储事务与崩溃一致性 | Tier 1 (Mechanical) | Choose Completeness | SQLite commit index + 不可变文件原子提交，单 Writer + CAS 锁防护 | 仅依赖纯文件覆盖写入，无事务与版本保护 |
| 8 | Eng | 投递中断与重复发送防护 | Tier 1 (Mechanical) | Choose Completeness | 引入投递对账状态机，断网进 `unknown` 强制对账，禁止盲目重投 | 盲目重试导致向 Multica 重复轰炸同一份日报 |
| 9 | Eng | 真实热度榜单比较规则 | Tier 2 (Taste) | Pragmatic | 分渠道分指标展示，少于 2 个可比样本不排榜仅列卡片，禁止加总 | 跨平台加权算出虚假总分，或样本不足时强制补零排榜 |

#### User Challenges (Human Adjudication Required)
None — 方案前提经全面压力测试得到严格加固，在 `Hold Scope` 模式下完整继承并保全了发起人批准的全部产品方向。

#### Taste Choices Adjudication (Approved by patgu9)
1. **日报组织形式与排程配置**:
   - **决策**: CLI 无需关注排程配置，任务编排由外部 Agent 触发（例如 Multica）；日报组织形式最终也由 Agent 触发，但是 CLI 需要提供简报（Briefing），确保信息完整。
2. **热度新鲜度 (Freshness) 与排序规则**:
   - **决策**: 采纳推荐方案。热度观测时间限定在研究窗口内且距 Finalize ≤ 24 小时；同事件同指标取同组内最大合法值；同组少于 2 个可比样本时不排榜仅展示数据卡片。
3. **正文软长度与附件分流策略**:
   - **决策**: 采纳用户指示。采集的证据内容保存在本地中（本地持久化存档，支持随简报输出或附件分发）。
4. **投递所有权划分 (CLI 与外部工作流职责)**:
   - **决策**: 采纳推荐方案。CLI `deliver send` 负责本地原子锁定 claim 并输出不可变 Edition 与哈希校验包；实际网络投递由外部工作流调用 Multica CLI 执行，执行完毕回写对账记录。

#### Next Action
本实施方案已获发起人 patgu9 最终批准（APPROVED），作为正式架构与实施契约移交至 **Stage 3: Build** 启动工程实现。