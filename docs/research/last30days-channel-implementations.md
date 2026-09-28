# last30days 六渠道实际采集实现

日期：2026-09-28。固定快照 `084662b501fb0dba95bd55eff0c258d35e0dc499`，只读静态调用链核查，未联网采集、安装依赖或使用凭据。此文替代“官方 API 优先”作为本轮接入讨论依据，不代表用户已经选定照搬这些实现。X 另见 [Grok 认证与采集](grok-auth-path.md)。

| 渠道 | 实际路径 | 凭据 / 依赖 | 不宜直接照搬的点 |
| --- | --- | --- | --- |
| Reddit | 常规检索：免费 keyless 优先，包括 RSS、shreddit 页面与 Arctic Shift 补充；默认空结果且有 key 才使用 ScrapeCreators。Discovery 提名另走 subreddit rising / top(week) 列表及 Arctic 补充 | 免费路径不读 OAuth；ScrapeCreators 需 key；Arctic Shift 是第三方归档 | 顶部 public JSON 注释落后；页面解析 / 归档不是官方稳定 API，归档近期取样不等于实时榜单 |
| GitHub | REST 主要搜 Issues + PRs，再补评论；person / project 模式另取 releases、stars 等 | 显式 token → GITHUB_TOKEN → gh auth token → 匿名 | 不是简单仓库 Trending；issue 活跃不等于项目发布新进展 |
| Hacker News | Algolia 搜索与 Discovery 榜单查询 | 无 key，Python HTTP | 不是 Firebase 默认路径；评论补抓函数虽存在，却未接入当前普通 pipeline |
| Digg | 子进程 digg-pp-cli search，去重后存活项再 posts 补原帖 | 额外安装 CLI 且在 PATH | 命令硬编码 since 30d，from/to 仅 advisory，不能保证满足我们七天事件窗口 |
| arXiv | 子进程 arxiv-pp-cli query；精确短语干净零结果后拆词 AND 重试 | 额外安装 CLI 且在 PATH，无 key | 内部近期窗口为 365 天，不等于本次研究窗口；失败不应冒充零结果扩词 |
| Web | 按配置选择 Brave → Exa → Serper → Parallel → keyless | 各服务 key；Brave 直接 HTTP | auto 是配置选择优先级，不是运行失败逐级重试；Brave 返回的 description 不是正文 |

## Reddit 细节与证据

reddit_public.search_reddit_public 现转发到 reddit_keyless.search_and_enrich；旧 search.json 函数保留但没有接入免费主路径，不能根据文件开头注释误写为默认先试 JSON。指定专属 subreddit 时会取 top / hot / new，并使用 RSS 搜索；没有专属 subreddit 时，RSS 推导出的社区列表用于补互动数据，不将全部热门条目混入查询。

Arctic Shift 为第三方归档，主要提供近期取样与缺失字段补充。shreddit 提供页面列表与重点帖评论。默认免费优先、空结果再付费，也支持显式反转为 ScrapeCreators 优先；是否启用“薄结果也补充”由配置决定。Gemini 是可选推理 provider，不是 Reddit 采集服务。

来源：[实际兼容入口](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/reddit_public.py#L238-L274)、[keyless 主流程](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/reddit_keyless.py#L75-L223)、[Arctic 补充](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/reddit_arctic.py#L161-L208)、[付费补充选择](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L4745-L4880)、[Discovery 提名](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L560-L573)。

## 其他渠道证据

- GitHub：[认证](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/github.py#L49-L77)、[Issues / PRs 主查询](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/github.py#L289-L345)。
- HN：[搜索与榜单](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/hackernews.py#L73-L188)、[实际 pipeline](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L5166-L5171)。
- Digg：[命令](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/digg.py#L110-L133)、[时间参数](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/digg.py#L179-L205)。
- arXiv：[365 天范围与 query / 重试](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/arxiv.py#L43-L209)。
- Digg / arXiv 安装：[setup_wizard](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/setup_wizard.py#L204-L354)。通过 printing-press-library 安装额外可执行程序，不随 Python 标准库自动具备。
- Brave：[HTTP 与字段](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/grounding.py#L49-L80)、[Web 提供者选择](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/grounding.py#L226-L289)。

## Siglens 可复用的设计与待决定事项

适合复用：渠道与后端分开、查询与原文补抓分开、缺失与零结果分开、先去重后限量补抓、精确查询零结果时有控制地扩展、外部工具依赖可诊断。具体适配器须接受统一证据与执行状态契约，不能整包搬入多阶段旧引擎。

建议 GitHub / HN / Brave 直接复用协议思路；Reddit 的 RSS / 社区列表作为候选路径但须验证当前可用性，页面与归档不自动成为必需依赖。Digg / arXiv 可选择包裹现有 CLI，或由 Python 直接访问相应公开数据；后者减少安装项并有利于观察请求，但不保证立即覆盖旧 CLI 的所有功能。第十七轮 Q57 已选定 Digg / arXiv 由 Python 直接接入公开数据；其余具体组合仍待确认。

Grok 与其他外部 CLI 的内部请求数不能仅凭进程启动次数精确还原，不得伪造精确次数；MVP 已不控制额度，详见 Grok 核查文档。旧代码硬编码时间范围必须改为显式记录检索覆盖与事件时间验证，不能包装成已满足本产品研究窗口。
