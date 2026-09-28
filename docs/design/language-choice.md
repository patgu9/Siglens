# Go 与 Python：Siglens MVP 技术栈比较

阅读入口：[MVP 规格](mvp-spec.md) · [文档索引](../README.md)。本文保留专题细节与历史提案；当前范围以主规格及后续有效决定为准。

状态：第二十七轮 Q75 已确认 Python 3.12+ 独立 CLI 包，优先提供 uv tool 安装方式。尚未开始实现或发布；此前 Go / Python 比较保留为选择依据，不是性能实测。

## 当前决定

MVP 采用 Python 3.12+，打包为有稳定命令入口的独立 CLI 包，优先提供 uv tool 安装方式。项目当前重点是多渠道 HTTP 接入、文本与论文材料处理、Jev 评估试验、JSON 契约和可恢复研究状态；现有上游引擎也使用 Python，适合选择性复用经过检查的适配器思路与测试样例。

Go 的独立可执行文件、静态类型和并发支持很有价值，尤其适合以简单分发为首要目标的工具。但当前需求没有证明 CPU 或高并发吞吐是主要瓶颈；多数外部工作耗时可能来自网络和模型服务，这只是待实测的架构判断，不是两种语言的基准结论。

## 比较

| 方面 | Python | Go | 本项目取舍 |
| --- | --- | --- | --- |
| 参考上游 | 可以更直接审查、移植小型适配器或复用样例；仍需解耦依赖 | 可复用协议与设计，但实现需改写或保留 Python 子进程 | Python 更利于 MVP 迭代，不能把整个上游引擎直接套壳当作新架构 |
| 材料处理与评估 | 便于与 Python 文本 / PDF 处理及研究评估代码协作 | 网络与结构化数据处理合适；需要逐项评估材料处理库或外部依赖 | 优先降低证据管线与评估的集成成本；具体库尚未选定 |
| 安装分发 | 需要 Python 运行时与依赖管理；可以用 uv tool / pipx 隔离安装并提供普通命令 | go build 生成可执行文件；一般需按目标系统 / 架构发布，native 依赖可能影响自包含程度 | Python 安装体验可管理，但不宣称等同无运行时单文件 |
| 并发采集 | asyncio 或线程可处理 I/O；错误、取消与状态一致性仍须显式设计 | goroutine 等语言机制适合并发；同样不能免除错误处理与状态一致性设计 | 两者都能实现；同一研究串行变更规则与语言无关 |
| 类型和维护 | 类型注解不能自动替代运行时 JSON 校验；需类型检查、契约校验和针对性测试 | 编译期检查覆盖内部类型；外部 API / JSON 仍需校验 | Go 有内部类型保障优势，Python 需要明确工程纪律 |
| 启动和计算开销 | 解释器及依赖导入存在开销，纯 Python CPU 热点可能需要优化 | 编译代码通常在启动及 CPU 任务上更有优势，实际幅度需测量 | 不用未测过的性能数字决定以网络调用为主的 MVP |

## Python 如何仍然是正式 CLI

Python Packaging 官方指南展示通过 pyproject.toml 的 project.scripts 注册命令；安装后用户调用普通可执行入口，而不是定位某个 .py 文件。uv tool install 可以隔离依赖并将命令放入 PATH，uvx 可运行工具；也可提供 pipx 安装方式。

建议源码按命令入口、研究能力、数据契约、适配器、持久化分层，Skill 保持独立。用户使用 siglens 一类命令，具体命令名与分发包名在实现前确定，未验证包名占用。无需引入 Go 包装层再调用 Python 核心。

本建议不改变已确认的外部编排边界：Python CLI 不启动通用 Agent；Multica 或宿主 subagent 由 Skill 指导使用。Grok 若是外部宿主搜索，其集成方式须单独澄清。

## 已核查事实与来源

- 上游 pyproject.toml 声明 Python >=3.12，工程主引擎为 Python：[固定源码](https://github.com/mvanhorn/last30days-skill/blob/084662b501fb0dba95bd55eff0c258d35e0dc499/pyproject.toml)。本项目随后在 Q75 独立确认 Python 3.12+。
- Python 正式 CLI 打包与入口：[PyPA 指南](https://packaging.python.org/en/latest/guides/creating-command-line-tools/)。
- 隔离工具安装和运行：[uv 工具指南](https://docs.astral.sh/uv/guides/tools/)。
- Python 网络 I/O 并发基础：[asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)。
- Go 可执行文件构建：[Go 官方指南](https://go.dev/doc/tutorial/compile-install)。

以上网页于 2026-09-28 读取；未安装工具、创建实现或做语言性能测试。

## 第二十七轮技术栈决定

Q75 已确认 Python 3.12+ 独立 CLI 包，优先提供 uv tool 安装方式。Skill 调用 CLI 的分工继续保留。用户未进一步要求 pipx 安装指南或兼容验收，不能将其列为首版已承诺交付。

从本地目录或 Git 仓库安装仍为可行的首版分发建议；尚未要求立即发布 PyPI，也不因安装方式获采纳而自动执行公开发布。具体包名、依赖版本与安装验收在实现阶段确定。
