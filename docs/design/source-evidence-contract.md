# 渠道降级与证据产物契约

阅读入口：[MVP 规格](mvp-spec.md) · [文档索引](../README.md)。本文保留专题细节与历史提案；当前范围以主规格及后续有效决定为准。

状态：已记录至第二十八轮，已确认默认启用全部支持渠道、doctor 验证和 CLI 参数选择，以及材料默认保留不自动过期。具体数据结构及接口尚未实现。

## 已确认前提

七渠道都能贡献候选。Q73 明确全部支持渠道默认启用，经 doctor 验证配置，仅允许已完成配置的渠道；Discovery 与 Named-Topic 默认尝试这些渠道（Q37 / Q64），用户可通过 CLI 参数选择所需渠道。渠道不可用时可降级并明确缺失；Jev 与 Agent 需要原文片段及上下文，保留原始证据链接。研究 CLI 负责采集与校验，Skill 负责宿主编排和产物传递。

## Web 搜索作为渠道降级

第十四轮 Q48 确认在渠道专用采集不可用时允许通过 Brave 定向检索，并明确记录内容所在渠道、实际检索方式和原文是否取得。执行此降级需要 Brave 已配置可用，且本次渠道选择允许使用 Web / Brave；Q77 明确指定渠道列表未包含 Web 时不调用 Brave 兜底。Brave 官方 Web Search 文档支持 site 运算符，并可返回附加片段；这证明存在实现入口，不保证特定平台的覆盖、时效、完整正文或互动指标。

来源：[Brave Web Search](https://api-dashboard.search.brave.com/app/documentation/web-search)。2026-09-28 只读文档核查，未调用付费 API 验证结果质量。

内容所在渠道与实际检索方式分别记录。例如搜索到 Reddit 页面时，内容渠道为 Reddit，检索方式为 Brave site 搜索；保留“未成功直连 Reddit”的状态。相同页面被直连与 Web 检索发现不构成两个独立来源；只有搜索片段时不能声称已取得完整原文。

这是 Siglens 已确认的降级方向，不表示上游所有渠道都实现了相同降级。被用户明确禁用的渠道是否允许间接检索，及禁用原因的表达仍需定义，不能将主动禁用视为故障自动替代。

## 上游降级核查

固定快照 `084662b501fb0dba95bd55eff0c258d35e0dc499` 中不存在七渠道统一转 Web site 搜索的机制：X 主要在专用后端间切换，无可用后端时报告错误；GitHub 可匿名调用但减少返回量；HN 使用无认证 Algolia；Web 有自身后端选择与 keyless 降级。这些是源码事实，不代表当前服务可用性实测。

上游 SourceOutcome 区分 attempted、state、items_returned 和 detail，适合参考。其普通 Web 补充还排除了 Reddit / X 域名，不能把上述 site 降级提案说成照搬上游。另有 Web 命中 Reddit 后补抓正文的操作，成功后记录 enriched_via，说明发现材料与取得正文可以是两条路径。

来源：[来源状态](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/schema.py#L181-L201)、[X 后端路径](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L4893-L4926)、[Web 后端选择与 Reddit 补抓](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/grounding.py#L230-L337)、[Web 补充要求](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L1703-L1706)。

## 证据保存范围

第十四轮 Q49 确认默认保存取得的正文文本，单独标记实际引用的片段与上下文，附原始链接、取得时间和材料类型。只有摘要时如实标记；网页 HTML、完整 API 响应作为可选调试资料。

正文文本是实际取得的材料，不承诺每个来源都能取得完整正文。原文与 Agent 摘要须区分，搜索摘要、论文摘要、完整或截断正文应明确其类型和取得程度；未取得部分不得自动补全为原文。来源及检索方式按 Q48 保留。

默认保存正文不等于把全部正文无差别发送给 Jev；实际判断仍使用相关片段及其上下文。建议保存判断与引用所用的材料版本，避免后续刷新覆盖后使已有引用失去依据。Q74 已确认默认保留、不自动过期清理；片段定位、版本和体积处理仍待设计。

## 交付文件

第十四轮 Q50 确认 JSON 保存结构化研究数据与状态，Markdown 保存主题卡和研究报告。建议两者共享证据引用，JSON 保留来源缺失和处理状态，Markdown 由 Agent 综合后交给 CLI 校验保存。

这些是普通研究文件，不引入跨机器运输或专用研究包。具体 schema、CLI 输出协议、文件组织与兼容策略在能力契约确认后设计。

## 早期接入方向（历史，后续已选定）

第十六轮用户要求 X 优先 Grok 认证，其余渠道参考上游后再讨论。当前依据为 [上游实际实现](../research/last30days-channel-implementations.md) 与 [Grok 路径](../research/grok-auth-path.md)；此前 [官方接入候选表](../research/source-access-mvp.md) 仅作事实参考，未被选定。以上均非已运行或已获批准的服务配置。

## 第十七轮接入决定

Q57 已确认 Digg 与 arXiv 使用 Python 直接接入公开数据接口，不依赖上游 digg-pp-cli / arxiv-pp-cli。这确定实现路径，不表示已验证所有接口、历史窗口覆盖或领域范围；第十八轮已进一步确认 Reddit RSS / 社区列表、GitHub REST、HN Algolia 与 Brave 搜索 / 正文抓取。X 保持 Grok 登录方向。

Q56 的免费外部 CLI 计数例外属于早期额度设计。第二十轮已移除 MVP 额度控制，不再为收费或免费采集分别设计额度门槛，详见 [执行约束](research-limits.md)。

## 第十八轮默认接入组合

| 渠道 | 已确认方向 |
| --- | --- |
| X | Grok 登录认证方向，适配器调用与能力验收待实现 |
| Reddit | RSS 搜索 + 社区列表；失败且本次选择包含可用 Web / Brave 时允许定向检索 |
| GitHub | REST Issues / PRs 检索与相关项目 Release 补证 |
| Hacker News | Algolia 搜索和榜单查询 |
| Digg | Python 直接访问公开数据 |
| arXiv | Python 直接访问公开 API |
| Web | Brave 搜索，另行取得结果页面正文 |

第十九轮 Q60 已确认 MVP 不实现浏览器兜底，仅使用 Brave 兜底。普通 HTTP 正文获取仍保留；Brave 无结果或原文仍无法取得时，保存已有片段并明确缺失，不自动启动浏览器。Jev + 浏览器的 [设计研究](browser-fallback.md) 仅作后续参考。

## 第二十七轮配置与保留决定

Q73 已确认全部支持渠道默认启用，需要通过 doctor 验证，仅允许已完成配置的渠道参与；用户通过 CLI 参数定义需要的渠道。无需凭据不代表免除适配器配置 / 能力检查；参数选择不能让缺失依赖或凭据的适配器直接执行。

建议 doctor 分别记录配置完整性、必要依赖及认证 / 最小读取检查的结果与时间，不将“配置存在”伪装为成功联网；暂时网络故障与缺失配置也应分开。Q76 已确定首次研究或相关配置变化时自动执行 doctor；具体检查项目与验证记录格式待设计。仅通过一次检查不能保证未来每次请求成功，运行失败仍保留降级记录。

Q77 明确仅选 X / Reddit、未选择 Web 时不使用 Brave 兜底，即使 Brave 已配置。参数选择因此同时约束可调用的渠道与 Web 兜底，不自动扩展到未选择渠道。指定与缺失记录仍需保留，未调用 Brave 不能记录为 Brave 请求失败。

Q74 已确认默认保留、不自动过期清理，适用于研究状态、取得正文、引用、审阅及交付产物。普通日志和可选 HTML / API 调试资料不因此变为必存证据，不新增跨机器归档或传输功能。

## 第二十八轮确认

- Q76：首次研究或相关配置变化时自动执行 doctor。显式 doctor 命令仍可用于检查；不新增用户未要求的定时刷新或后台监控。
- Q77：指定列表未包含 Web / Brave 时，无需 Brave 兜底。若用户选择包含 Web / Brave 且它通过配置验证，沿用既有定向降级规则；未配置渠道不能因参数被选择就绕过配置检查。

示例：仅选择 X / Reddit 时，Reddit 失败就保留缺失并继续其他操作；选择 X / Reddit / Web 时，允许使用可用的 Brave 定向兜底，保留实际检索方式。不指定渠道参数时，仍沿用默认尝试全部配置完成渠道的原则；不能把本轮回答解释为取消该默认覆盖。
