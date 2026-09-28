# last30days 的 Grok 认证与 X 采集路径

日期：2026-09-28。固定快照 `084662b501fb0dba95bd55eff0c258d35e0dc499`，核查源码及当前官方文档；未读取用户凭据、未运行 Grok、未调用付费模型。

## 三条路径

| 路径 | 实际执行 | 认证责任 |
| --- | --- | --- |
| grok 后端 | 程序启动本地 grok -p 并要求 JSON 输出，使用其原生 X 搜索能力 | 用户预先通过 Grok CLI 登录；上游不自动发起登录 |
| xai 后端 | 程序使用 xAI Responses API 的 x_search | XAI_API_KEY，独立于 Grok 登录路径 |
| --x-posts | 宿主 Agent 通过自己的 X connector 检索后交付材料 | 宿主负责；上游仅校验摄取并跳过 X 后端 |

Grok 后端需要显式选择，并非发现用户登录就自动启用。上游确实使用 subprocess.run 调用 Grok；不能把它误写为只支持外部宿主导入。

来源：[grok 适配器声明](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/grok_x.py#L1-L9)、[进程调用](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/grok_x.py#L782-L833)、[显式启用](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/env.py#L1320-L1328)、[xAI API](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/xai_x.py#L97-L125)、[宿主导入](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/skills/last30days/scripts/lib/pipeline.py#L4873-L4881)。

## 官方能力与未验证部分

官方 CLI Reference 提供 grok login（包括设备认证）；Headless 文档支持 -p 和 JSON / streaming-json 输出。这支持复用已登录 CLI 的集成方向，但未验证用户的账号、安装版本或原生 X 工具可用性，不能把源码实现当作当前账户成功验收。

来源：[认证与命令](https://docs.x.ai/build/cli/reference)、[程序化调用](https://docs.x.ai/build/cli/headless-scripting)、[xAI API X Search](https://docs.x.ai/developers/tools/x-search)。Grok 登录所用额度与 API-key 路径费用不能混为一谈。

上游会把 Grok 认证文件复制到临时子进程 HOME，且调用使用了绕过权限的参数。这些是需重新设计的实现细节，不能当作稳定认证 API 原样搬入 Siglens；应由 Grok 管理认证，并核验可支持的最小工具范围与隔离方式。当前没有为用户复制或修改任何认证资料。

## 对 Siglens 职责的影响

建议把 Grok 限定为 X 采集适配器：输入检索计划，输出可校验帖子与链接；它不负责研究计划、候选选择或 Agent 分派。若采用该路径，需要把“研究 CLI 不调度通用 Agent”与“可以调用受限的 Grok 检索后端”分清楚；该适配器细节待用户确认。

## 计数限制

Siglens 可以观测启动 Grok 查询的次数，但其内部可能调用多个 X 工具或发生重试。上游 _invoke 仅返回 stdout 文本，没有提供独立核实的底层请求计量；不能把一次 grok 进程等同一次 X HTTP 请求。

第二十轮已移除 MVP 额度控制，第十七轮 Q56 的免费外部 CLI 计数例外不再需要单独实现。可保留调用诊断，不将未知内部次数伪造为精确数据；宿主 --x-posts 中的 calls 属宿主报告值，不是 CLI 独立观测值。登录认证不代表服务免费，此事实不构成 Siglens 的额度门槛。
