# last30days 交付内容核查

核查日期：2026-09-28。固定版本 `084662b501fb0dba95bd55eff0c258d35e0dc499`，从本地源码快照只读检查 Skill、入口、渲染及数据结构；未运行真实采集或模型，以下不代表端到端质量验证。

## 综合报告与证据资料是不同产物

| 层次 | 实际交付 |
| --- | --- |
| 普通 Named-Topic 的 Skill 输出 | 聊天综合简报：What I learned、KEY PATTERNS、来源统计与原始材料路径 footer、后续邀请。普通默认不是固定研究问题与确认状态的长篇报告 |
| Skill Agent 模式 | Research Report 标题、日期与来源、3–5 条 Key Findings、What I learned、Stats；直接交付后结束，不要求后续互动 |
| CLI compact / md stdout | 供宿主综合的证据块；Skill 要求不要把 ranked evidence clusters 原样当最终正文 |
| CLI --save-dir | 普通单主题 Markdown 保存完整 render_full 的证据材料，与 compact stdout 不同；包括全部聚类与按来源列出的条目 |
| CLI --output | 保存当前渲染文本，不能与 --save-dir 的完整证据保存策略混为一谈 |
| CLI JSON | agent 为版本化精简契约，包含来源状态、聚类、结果、URL 等；raw 为内部完整 Report。精简 agent JSON 不等于全部原文归档 |
| CLI brief / HTML | brief 面向内容生产的故事线、角度、张力、受众问题、来源聚类；显式 HTML 交付可嵌入 Agent 生成的综合文本，不是普通运行默认产物 |

来源：[普通简报](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L2079-L2168), [Agent 模式](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L1149-L1180), [输出分派](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/last30days.py#L488-L523), [保存策略](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/last30days.py#L2467-L2529), [JSON 数据契约](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/schema.py#L863-L945), [brief 渲染](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/render.py#L2130-L2275), [HTML 交付](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/references/save-html-brief.md#L5-L73)。

完整证据 Markdown 包含研究窗口、警告、聚类、来源条目的 ID、分数、作者、日期、互动数、标题、原始 URL 和片段；数据存在时还包含评论、洞察或字幕，末尾列来源覆盖与错误。因此上游已有“Agent 综合 + CLI 证据材料”的分层，值得沿用。

[完整证据渲染](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/render.py#L1801-L2008)。

## 引用、未确认信息与背景

- 上游综合关注故事线、跨主题模式、来源矛盾与社区声音。single-source / thin-evidence 是证据簇标签，不是每项陈述的事实确认状态。
- 引擎证据条目保存原始 URL，但用户正文的引用展示因宿主而异。尤其 Skill 对补充 WebSearch 附录规定 publisher + domain + 摘要，禁止加入完整 URL；Siglens 不应继承这个限制，应保留具体证据链接。
- 来源失败与健康零结果区分，证据不足可以交付 Nothing solid this window。失败不代表平台没有讨论，这个原则值得保留。
- 未找到普通报告统一的“窗口外背景材料”结构；采集层存在 arXiv 窗口、带字幕老视频等例外，不等于报告已经具有“7 天新进展 + 明示背景”的契约。

来源：[综合指导](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L1756-L1800), [补充 WebSearch 附录](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L1722-L1753), [引用展示](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L209-L218), [来源覆盖与缺失](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/render.py#L2587-L2632), [空结果](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/render.py#L394-L421), [日期归一化例外](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/normalize.py#L87-L118)。

## 对 Siglens 的设计建议

继承综合结果与证据材料分层、按研究问题组织证据、承认空结果与覆盖缺口。新增或强化逐项发现状态、具体原始链接、窗口内外区分、研究问题及下一步；报告是否已交付与研究对象是否可确认是不同状态。

Discovery 上游原样交付引擎主题简报、Comparison 使用单独比较模板，均不代表 Named-Topic 应照搬其版式。Siglens 的结构化报告草案见 [报告设计](../design/research-report.md)，并不要求复制上游的聊天话术、社交优先引用顺序或内容创作角度。
