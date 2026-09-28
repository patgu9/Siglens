# last30days 工作流程阅读记录

阅读日期：2026-09-28。用途：为 Siglens 的 Skills + CLI MVP 设计提供事实依据；本文件不是已批准的产品规格。

## 参考版本与核查范围

- 仓库：https://github.com/mvanhorn/last30days-skill
- 本次通过 GitHub API 取得的 main 提交：`084662b501fb0dba95bd55eff0c258d35e0dc499`，提交时间 `2026-09-23T05:44:58Z`。
- 入口：[last30days.py](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/last30days.py)。该版本文件共 4304 行。
- 跟踪模块：`lib/pipeline.py`、`lib/planner.py`、`lib/rerank.py`、`lib/schema.py`、`lib/discovery_handoff.py`、`lib/digg.py`，并对照 `SKILL.md` 的研究分支。
- 本次为静态源码核查，没有运行真实渠道采集；不据此声称供应商可用、检索质量或耗时已经验证。
- 历史阅读记录仅用于定位要核查的分支；以下结论依据本次固定版本源码。

## 入口的职责

`last30days.py` 本身已是 CLI：参数解析、配置与来源诊断、模式分派、研究编排、缓存与保存、报告渲染、退出状态都在这里组织。研究算法和渠道实现主要在 `lib/`。

重要入口：

| 函数 / 位置 | 职责 |
| --- | --- |
| `build_parser`，667 | 主题、来源、时间窗口、深度、研究计划、对比与 Discovery 等参数 |
| `_main`，3168 | 加载配置并分派 setup、doctor、library、queue、Discovery、drill、普通研究 |
| `_resolve_discovery_source_boundary`，1978 | 分开保存提名渠道集合与后续研究渠道边界 |
| `_run_discover_protocol_leg`，2331 | 分派 Discovery 三阶段协议，协议错误转为退出码 2 |
| `_render_save_and_print`，2417 | 单主题或对比报告渲染、文件输出与相关状态 |

因此，新工具的区别应落在产品边界、安装分发、稳定命令与数据契约、运行状态和 Agent 指南，而不是是否接受命令行参数。实现语言尚未决定。

## 三条研究路径

### Named-Topic：已知主题 → 搜集和组织证据

1. 宿主 Agent 在 Skill 层理解意图、消歧，并定位账号、社区、GitHub 对象等目标。
2. Agent 可通过 `--plan` 交付结构化查询计划；没有外部计划时，流水线可使用内部规划器或确定性回退。
3. `pipeline.run()` 确定时间窗口、可用来源和预算，按子查询与来源组合并发采集。
4. 原始结果标准化、时间处理、相关性处理、去重和摘要片段提取；继续做实体定向补搜及薄弱来源重试。
5. 使用加权 RRF 合并不同检索列表，再重排、聚类，产生 `Report`。
6. 保存来源状态、错误、警告和证据；由渲染器与宿主 Agent 承担各自的报告输出工作。

主要依据：[pipeline.run](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L2059)，[Skill 预研究流程](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L1294)。

### Comparable / Comparison：多个对象 → 分别研究 → 汇总对比

1. 通过 `A vs B`、显式对象列表或自动发现同类对象确定比较对象。
2. 每个对象需要独立的账号、社区、仓库等定位信息；不能把主对象的定位信息复用于所有对象。
3. 并发运行多次 `pipeline.run()`，保留各对象的独立证据报告。
4. 主对象失败或有效对象不足两个时，不生成看似完整的对比；部分同类对象失败时注明缺失。
5. 输出合并对比与相关的单对象产物。Skill 还负责对比性补充搜索及综合解读。

依据：[对比编排](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/last30days.py#L3908)。这里暂保留用户的 Comparable 用词；正式术语定义待讨论确认。

### Discovery：未知具体主题 → 候选主题 → 验证 → 简报

Discovery 的输入可以是一个领域，也可以不指定领域。它首先扫描可用于发现的来源，而不是把“最近有什么值得关注”当作普通主题检索。

宿主 Agent 路径：

```text
领域或全局范围
  → 采集榜单 / 信息流 / 领域检索结果
  → 标准化、去重、合并与聚类
  → 生成候选主题及完整种子证据
  → Agent 命名主题、排除噪声、判断价值
  → 为选中的主题调用共用研究流水线补充证据
  → 证据门槛检查、同一事件合并、排序
  → Agent 提供可选内容角度
  → 输出简报、保存产物、记录主题队列
```

| 阶段 | 命令标志 | 产物及职责 |
| --- | --- | --- |
| 提名 | `--discover [DOMAIN] --nominate-only` | `discover-nominations.json`；完整候选池及种子证据，Agent 读取后判断 |
| 研究 | `--discover --judgments FILE` | 应用名称、junk、worthiness；研究入选主题，通过质量门槛后写 `discover-pending.json` |
| 完成 | `--discover --finalize [--angles FILE]` | 应用可选内容角度、渲染、保存、记录主题队列；此阶段不采集网络数据 |

协议特征：

- 三阶段保持同一个保存目录；判断文件通过 `bundle_id` 绑定候选集合。
- 状态有效期为一小时；校验版本、时效、结构以及 mock / real 一致性。
- 交接文件名固定，共享保存目录会覆盖上一轮状态；未来支持并发研究时，需要讨论每次运行的独立身份与存放位置。
- 顶层契约错误会失败；单条缺失或畸形判断可以回退到启发式，因此“命令成功”不等于 Agent 已判断每条候选。
- 无足够证据时允许 `nothing-solid`；不能为了填满榜单强行输出。
- one-shot 也是一条实际路径，主题命名和噪声识别使用确定性规则，默认不产生内容角度。宿主 Agent 的 Skill 路径要求三阶段协议。
- `--discover-shallow` 在 one-shot 中跳过逐主题研究；在三阶段协议中对应较轻量的逐主题研究，两者含义有差异。
- 逐主题研究预算耗尽或失败时可保留仅有种子证据的结果；Siglens 可借鉴失败时保留材料，但第二十轮已移除自身的额度控制。

依据：[CLI 协议入口](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/last30days.py#L2077)、[交接契约](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/discovery_handoff.py#L1)、[研究恢复](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L1682)。

## 对七个目标渠道的启示

这是上游代码中的能力划分，不是 Siglens 已选定的接入方式。

| 渠道 | 上游 Discovery 初始提名 | 上游后续主题研究 |
| --- | --- | --- |
| Reddit | 社区 listings；全局默认 r/all，领域模式定位社区并过滤 | 检索、帖子与评论等 |
| Hacker News | 列表 / 热门故事，领域模式过滤 | 主题检索及讨论 |
| X | 领域模式检索；全局提名显式排除 X | 通过已配置后端研究主题 |
| Digg | 调用 Digg AI 1000 的搜索适配器 | 主题簇和相关 X 帖子 |
| GitHub | 不在 `DISCOVERY_SOURCES` 集合中 | 可参与后续研究；有项目与个人定向能力 |
| arXiv | 不在初始提名集合中 | 可参与后续研究 |
| Web / Brave | 不在初始提名集合中 | `grounding` 来源可使用 Brave 等后端 |

`DISCOVERY_SOURCES` 定义见 [pipeline.py:87](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L87)，全局和领域规划见 [planner.py:23](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/planner.py#L23)。

### 不宜直接照搬的语义

1. **热度不是增长测量。** `engagement_velocity_score` 以累计互动量乘内容年龄权重；`discovery_velocity_score` 再奖励来源种类数量。没有利用两次观测的互动差分测量增长。`momentum` 也只是按内容年龄分类。我们应先定义想发现的是热议主题、早期信号还是已验证的上升趋势。
2. **渠道数量不是独立证据数量。** 代码按不同 `source` 计数；Digg AI 1000 又聚合 X 帖子。同一原始消息经过多个渠道传播，不一定代表独立佐证。
3. **来源存在不代表具备 Discovery 能力。** GitHub / arXiv / Brave 是否独立发现主题，需要单独设计入口，不能只复用主题搜索适配器就声称完成。
4. **Digg 的身份需要明确。** 上游 `lib/digg.py` 接入的是 `digg-pp-cli` 提供的 Digg AI 1000，链接形态为 `https://di.gg/ai/...`；不能未经确认将用户的 Digg 理解成其他同名产品。
5. **全局 Digg 路径存在静态代码不一致。** planner 的注释将 Digg 描述为全局信息流；实际传入空领域，`digg.search_digg` 遇到空主题会直接返回空结果。此为静态路径观察，没有进行真实供应商调用。
6. **内容创作目标不应自动继承。** 上游 worthiness 面向播客 / X 文章价值，最终还有内容角度。Siglens 如果用于技术情报或研究，价值判断标准应重新定义。

依据：[热度评分和门槛](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/rerank.py#L42)、[Digg 接入说明](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/digg.py#L1)、[空查询返回](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/digg.py#L198)。

## 已明确的用户约束

- 产品采用 Skills + CLI，并在 CLI 中提供帮助 Agent 操作的指南。
- MVP 核心投入在 Discovery。
- 当前产品范围要求指定领域；不支持未指定领域的全局发现（用户第三轮决定）。上文对全局模式的分析仅描述参考工程行为。
- 预留 Named-Topic、Comparable 研究能力；用户在第一轮回答中确定首版实现 Discovery 所需的最小主题研究核心。
- 渠道范围为 X、Reddit、GitHub、Hacker News、Digg、arXiv、Web search（Brave）。每个渠道在首版承担哪些角色尚未确定。

## 第一轮设计决策树（历史问题）

以下是第一轮提出的问题。用户已回答，当前决定与下一轮开放问题见 [Discovery MVP 设计讨论](../design/discovery-mvp.md)。

1. **Discovery 的目标产物与首个使用场景**
   - 热议主题、早期信号、历史增长测量、内容选题，还是其他目标？
   - 下游决策：质量门槛、排序、时间窗口、是否必须持续采集历史、结果结构。
2. **宿主 Agent 与 CLI 的推理职责**
   - Agent 负责语义判断与综合，或 CLI 自身配置模型并完成自主研究？
   - 下游决策：指南、交接文件、状态恢复、模型接口、成本控制。
3. **Named-Topic / Comparable 的预留程度**
   - 首版仅预留架构与契约，或同时交付最简可用的公开命令？
   - 下游决策：共享研究核心、命令承诺、验收范围。
4. **Digg 的具体所指**
   - 上游同款 Digg AI 1000，或其他 Digg 产品？
   - 下游决策：适配器、证据溯源、是否与 X 去重。

尚未定案的后续分支包括渠道角色与接入、时延、局部失败与空结果、状态及持久化、命令与 Agent 指南、安装分发、实现语言与验收案例。依赖前述选择的分支在下一轮展开。

第一轮回答已整理为词汇表、设计讨论和分工 ADR。另据本轮当前官网核查，digg.com 明确将 di.gg 列为保留别名，旧 /ai 跳转 /tech；二者不能简单当作独立来源。上面的 Digg 描述记录的是参考版本适配器的行为，当前接入事实见设计讨论中的官方来源。
