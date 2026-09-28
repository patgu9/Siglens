# last30days 的 junk 与评分核查

日期：2026-09-28。固定提交：`084662b501fb0dba95bd55eff0c258d35e0dc499`。核查本地固定源码及调用链，并执行了 `topic_shape.is_junk_shape` 的纯函数样例；没有真实渠道或模型质量测试。后半部分为 Siglens 设计草案，不是上游已有契约。

## Junk：Skill 政策与代码规则分开看

| 类型 | 上游实际行为 | 位置 |
| --- | --- | --- |
| 求助、求推荐、入门问题 | 标题匹配 help/advice/beginner/noob/recommend 等形式 | `topic_shape.py:112–120,198` |
| 问句形式 | 特定 wh/助动词开头组合，或无实体且以问号结束；含实体不一定能豁免前者 | `topic_shape.py:104–111,196–203` |
| 个人感想、空泛观点 | I think/feel/believe、hot take、rant、change my mind 等开头 | `topic_shape.py:121–125,198` |
| 空内容 | 标题和片段都空则标 junk | `topic_shape.py:187–191` |
| 纯推广 | Skill 要求宿主判断；启发式函数没有对应专用规则 | `SKILL.md:333–335` |
| Show HN / Launch HN | 启发式直接豁免，早于其他判断；宿主仍可否决 | `topic_shape.py:194–195` |
| 预测、旧闻 | 此 junk 函数没有专门排除规则；时间处理在其他流程 | `topic_shape.py:179–209` |

代码不是完整的垃圾信息语义分类器。例如 `How do I deploy Gemma 4?` 返回 junk，而 `Ask HN: How do I deploy Gemma 4?` 在此函数中并未先清除前缀，返回非 junk；`New course: Buy my guide today` 也未被启发式排除。这些例子不能转成 Siglens 的产品规则。

宿主显式 `junk=true` 会在强化调研前排除；显式 false 可覆盖启发式。判断缺失或不是 JSON boolean 时，才使用启发式；启发式 junk 在拥有足够不同 seed 渠道时仍可能继续，不是绝对黑名单。

源码：[规则函数](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/topic_shape.py#L179)、[宿主政策](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/SKILL.md#L333)、[应用判断](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L1737)。

## Discovery 实际评分链路

1. 将各平台原生互动指标相加；没有把各平台单位校准成同一指标。
2. 单条分数为互动量除以 `sqrt(内容年龄天数 + 1)`，不足 7 天再乘 1.5；这是年龄加权热度，不是历史增长率，也不是独立确定的事件时间。
3. 聚类分数求和，再按不同 source 种类每增加一个加 15%。不同 source 不一定是独立出处。
4. 宿主提供一个 `worthiness`，范围 0–100，含义是能否支撑播客或 X 文章。**上游没有拆开的多维研究价值 rubric。**
5. 选择强化调研对象时，用 `velocity × (0.5 + worthiness / 100)` 排序，缺失 worthiness 视为 50；host junk 先排除。
6. 补证后检查互动门槛，再按新的 velocity 排最终结果，worthiness 不再直接出现在最终排序公式中。

上游普通候选门槛为至少一项材料、互动总数至少 25，同时有两个 source 或互动总数至少 200。不能直接移植到允许低互动一手发布、arXiv 和 Web 材料的 Siglens。

第二十三轮复核补充：提名阶段已过滤 velocity <= 0（pipeline.py:904–918），协议最多 15 个提名、6 个强化调研（1316–1320、975、1769–1771）；worthiness 无独立低分硬门槛。补证失败可回用 seed 证据计算门槛（1066–1116），且没有自动从剩余提名补位的循环。新 [淘汰规则提案](../design/candidate-elimination.md) 区分上述事实与 Siglens 建议。

`rerank.py:151–160` 关于提名阶段由引擎调用 LLM 的注释已落后于实际路径；当前宿主协议由 Agent 提交判断。主题研究中 60% relevance + 20% RRF + 10% freshness + 5% source quality + 5% engagement 的公式属于另一条证据重排路径，不是 Discovery 的最终排名。

源码：[互动、热度、门槛与 blend](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/rerank.py#L42)、[无引擎 LLM 的提名](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L855)、[研究后的合并与排序](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L1443)。

## Siglens junk 分类与边界

第十五轮 Q52 已确认按内容排除下列缺乏具体新事项的内容；具体实现与提示词未定。不能将上游启发式正则视为本项目的判定契约。

| 类别 | 处理原则 | 边界 |
| --- | --- | --- |
| 无依据的发布猜测 / 传闻 | 排除（已确认） | 官方宣布未来发布可形成“宣布计划”事件，不冒充“已经发布” |
| 个人求助、入门问答、购买建议 | 排除缺乏具体新事项的条目 | 求助帖若暴露可证实的新故障，应研究故障事件，而非机械按问句删除 |
| 无新增事实的个人感想、情绪或空泛观点 | 排除 | 有实证的新分析、复现或反例不因第一人称而删除 |
| 无具体变化的纯推广 | 排除 | 有实物、论文、代码或正式公告的发布不自动属于纯推广 |
| 无可识别对象与事项的空泛内容 | 排除 | 抓取失败或文本截断应记录缺失，不当作已判定垃圾 |

领域无关单独标记；过期由事件时间规则处理；重复材料合并。这些不必都挤进一个 junk 布尔值，建议保留具体原因与原始材料。

## Siglens 分维度评分草案

把判定资格、语义价值和观测信号分开。Jev 不负责重新计算时间、互动量或来源数，也不自行生成判断理由和证据；解释由 Agent 给出，调用上下文和证据 ID 由 CLI 关联。

### 独立审阅字段

- 领域相关性。
- 是否纯猜测。
- 初始证据状态：能够支持哪些明确陈述、哪里不足或存在冲突。
- junk 类别与候选处理状态（具体枚举待定）。

### Jev 研究价值维度

四个维度在第十五轮 Q51 获确认，第二十二轮 Q65 进一步确认五档量表，替换此前 0–3 四档草案。下表以 1–5 展示五档的具体描述建议，不是概率，也未成为最终 schema；第二十五轮 Q69 已替换此前 Q66 的 unknown 政策，直接使用 Jev Score；材料不足作为证据状态另行记录，响应失败不补造分数。

第十五轮 Q53 确认：有明确事件线索但只有摘要或搜索片段的候选，可标记“初始证据不足”并进入补证，不自动判作垃圾或已确认事实。

| 维度 | 1：很低 | 2：较低 | 3：中等 | 4：较高 | 5：很高 |
| --- | --- | --- | --- | --- | --- |
| 实质变化 | 重述既有事项，无新增变化 | 局部修正，基本能力或认识不变 | 有具体的新结果或能力，扩展已有工作 | 改变重要能力边界、工作方式或关键认识 | 材料支持对该领域核心方法或能力边界的重大改变 |
| 具体性与信息量 | 只有空泛标签或口号 | 说明对象和动作，缺少关键细节 | 有清晰结果及基本适用条件 | 有可检查的结果、机制及关键条件 | 有足以复核核心陈述的细节，并交代限制 |
| 潜在影响 | 已有材料表明实际后果可忽略 | 影响局限于个别狭窄用途 | 对某类用户或实践有明确后果 | 对广泛使用场景或关键环节有显著后果 | 对领域基础能力、关键依赖或多类实践有重大后果 |
| 后续研究空间 | 材料已回答相关问题，没有实质待查问题 | 仅有宽泛兴趣，缺少具体待查问题 | 存在能明确表述的实质问题 | 有具体实质问题和可行验证路径 | 对关键实质问题可通过明确路径取得有区分力的新证据 |

依据关系：具体性从上游 junk / worthiness 的隐含标准拆出；实质变化补充上游纯日期 freshness；影响和后续研究空间将内容创作价值调整为研究价值。不得把“热议”本身当作高影响的证明。

各维度保留分值和适用的概率分布 / confidence；不臆造 100 分总分或已校准阈值。组合权重和 Agent 选择规则待验证。

### CLI 提供的观测信号

- 事件时间、时间依据与窗口匹配。
- 平台原生互动量及采集时刻；缺失指标保留未知。
- 渠道覆盖、采集成功 / 空结果 / 失败。
- 原始出处与转载关系、已尝试的交叉核查及结果。

这些借鉴上游热度、新鲜度与来源广度，但不照搬互动阈值、按平台计数的独立性假设或热度主导公式。
