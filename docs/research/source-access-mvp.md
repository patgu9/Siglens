# MVP 七渠道接入核查

日期：2026-09-28。只读公开官方文档，未使用凭据、未调用付费 API、未验证用户账号或七渠道端到端质量。以下是第十五轮提出的候选默认后端，尚未获用户确认；第十六轮用户要求 X 改为优先研究 Grok 认证路径，其余渠道重新以 last30days 实现为参考，不应将本表当作已选定方案。

| 渠道 | 文档事实与候选默认接入 | 研究范围上的限制 |
| --- | --- | --- |
| X | 官方 Search API，App / Bearer Token，按量付费 | Recent Search 为最近 7 天，更长窗口需要 Full-Archive 能力；领域查询由 Agent 计划提供，不能把搜索当完整平台趋势 |
| Reddit | 官方 OAuth Data API，API 访问需获批准 | 不保证匿名 .json 开箱即用；可用社区榜单与搜索，缺少可用接入时可按既定规则降级到 Brave |
| GitHub | 官方 REST Search，公开资源可匿名，认证提高请求额度 | 项目 stars / updated 只是线索，需要核查 release、commit 或 issue 才能确定具体新事项 |
| Hacker News | 官方 Firebase API 可取榜单和内容；全文搜索可选 Algolia | Firebase 没有同等全文搜索端点，若用 Algolia 须记录实际提供者；榜单不保证覆盖七天全部主题 |
| Digg | 已核实官方机器可读 JSON / YAML feeds 公开免认证 | 当前文档中的 ranked / rising feeds 面向 tech / AI 和今日 / 滚动 24h，不能保证完整七天历史；文档与首页分类曾有差异，不据此断言平台只有这些领域 |
| arXiv | 官方查询 API，Atom 元数据、摘要和原文链接 | 摘要不是全文；新版本时间与首次发表时间分开记录，HTML / PDF 正文需另取 |
| Web | Brave Web Search，订阅 Token；支持语言、日期、site 与 snippets | 检索日期过滤不等于事件发生时间，片段不等于完整原文 |

来源：

- X：[搜索范围](https://docs.x.com/x-api/posts/search/introduction)、[认证](https://docs.x.com/x-api/posts/search/quickstart/recent-search)、[计费](https://docs.x.com/x-api/getting-started/pricing)。
- Reddit：[API 端点](https://www.reddit.com/dev/api/)、[接入政策](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)、[Data API Terms](https://redditinc.com/policies/data-api-terms)。官方文档另有商业使用审批要求，未核查用户接入资格。
- GitHub：[搜索](https://docs.github.com/en/rest/search/search#search-repositories)、[内容](https://docs.github.com/en/rest/repos/contents)。
- HN：[官方 API](https://github.com/HackerNews/API)、[Algolia 搜索 API](https://hn.algolia.com/api)、[维护项目](https://github.com/algolia/hn-search)。
- Digg：[llms.txt](https://digg.com/llms.txt)。当前 doc 不能作为所有分类及端点历史覆盖的实测证明。
- arXiv：[API 手册](https://info.arxiv.org/help/api/user-manual.html)、[访问约束](https://info.arxiv.org/help/api/tou.html)。
- Brave：[Web Search 指南](https://api-dashboard.search.brave.com/app/documentation/web-search/get-started)。

## 第十五轮候选接入策略（未采纳）

建议 MVP 每个渠道先采用一个默认路径：X 官方 API、Reddit 官方 OAuth、GitHub REST、HN Firebase + 标明提供者的 Algolia 查询、Digg 公开 feeds、arXiv 官方 API、Brave。缺少可用专用接入时，按用户已确认规则使用 Brave 定向检索并明确降级。首版不同时建设多个付费聚合商后端；该范围建议尚未确认。

“适配器代码存在”与“用户已有可用访问资格”分别记录。覆盖局限、接口失败和未配置不能伪装成健康零结果；尤其 Digg 当前榜单不能声称完整覆盖用户要求的七天。

## 与预算决定的关系

X 文档按返回资源等单位计费，因此实际数据请求次数不等于渠道货币费用封顶。第二十轮已移除 Siglens MVP 的额度控制；此处计费事实仅说明服务可能收费，不要求 CLI 实现预算门槛。

## 与证据来源的关系

检索提供者、内容渠道与原始出处应能分别追溯。Digg 聚合的某条 X 帖与直接取得的同一 X 帖不构成两个独立来源；Brave 发现的 Reddit 链接也不代表 Reddit 专用接口可用。具体数据契约见 [渠道与证据](../design/source-evidence-contract.md)。
