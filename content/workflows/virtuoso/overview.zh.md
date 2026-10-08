---
title: Virtuoso 多轮对话工作流
description: 五个 skills 的搭配、工程对话、OSC／RC／MOS 实例和 GitHub 安装指令
---

## 五个 skills 怎么搭配

把工程分成多轮对话：你提出目标，Agent 明确条件并执行；你看图、看结果，再补充下一步要求。连接状态、设计变量、仿真记录和推荐参数把这些轮次串起来。一个 skill 不必包办整项工程，也不要求每次都按固定顺序调用五个技能。

| 当前需求 | 负责的 skill | 接下来可以做什么 |
|---|---|---|
| 连不上虚拟机、CIW 没响应 | virtuoso-connect | 接通后转给 testbench 或 layout |
| 画原理图、做 symbol／TB、配置 ADE | virtuoso-testbench | 拿到可信基线后交给 params |
| 根据上一轮实测继续改 W/L、负载或偏置 | virtuoso-params | 独立复测、写回参数和最终界面 |
| 放置、布线、via、物理验证 | virtuoso-layout | PEX 后交给 testbench 做后仿真 |
| 不懂菜单、快捷键、变量或报错 | virtuoso-helper | 解释完成后继续原工程 |

`skill` 是 Agent 的流程说明和辅助脚本；`SKILL` 则是 Cadence 的脚本语言。真正连接虚拟机的是外部 `virtuoso_bridge`，实际电路计算由 Spectre 等工具完成。五个技能不能替代 Cadence 软件、许可或你自己的 PDK。

### virtuoso-connect

**什么时候用：**第一次接入环境，或者 SSH／隧道／CIW 出现故障时。

> 用 $virtuoso-connect 读取我的本地配置，先检查 Python 和实际安装的 bridge API，再验证 SSH、隧道和 CIW。只在指定工作区操作，报告哪个环节通过、哪里还缺配置。

Agent 先读取共享配置，检查解释器与 `.env` 的选择，分别核对隧道和远端监听，再发送只读 CIW 命令。不会把“端口可连”直接当作 Virtuoso 正常，也不会为了解释一个概念就启动连接。

**交付：**解释器和 bridge 版本、配置来源、只读命令验证结果、可操作范围及缺项。密码、私钥与完整 `.env` 不进入回复。

### virtuoso-testbench

**什么时候用：**创建或修改 DUT、symbol、原理图和测试平台；配置 ADE、跑单次仿真、导出结果；按项目层级复制设计。

> 用 $virtuoso-testbench 在指定工作库新建 RC 低通测试平台。R = 2 kΩ、C = 1 pF、AC 输入为 1；普通信号用连续导线，布局紧凑。配置 AC、检查连通性并保存，再给我本轮带宽与波形。

Agent 查询真实端子、CDF 和接口签名，创建或修改指定视图，检查 terminal/net 关系、symbol 端口及生成网表。测试条件包括供电、刺激、负载、模型 section、角点和测量定义。结果绑定准确的 `history / test / corner / point`。

**交付：**可编辑原理图、测试设置、运行标识、波形和指标；每个结论对应本次结果。持续搜索参数时转给 params。复制工具先生成计划，整库复制的仿真等价性仍需额外验证。

### virtuoso-params

**什么时候用：**已有电路和可信测量链路，要根据实测继续调参。

> 用 $virtuoso-params 在给定尺寸与负载范围内优化这个 OSC，保持 Wp = 2 × Wn。每轮分析上一轮数据，只运行一组参数，保留历史最好点。预算包含独立复测，结束时应用推荐值并打开最终 Maestro／ViVA。

Agent 明确参数边界、单位、约束、角点和有限预算，保存基线。每轮提出一组参数及理由，真实仿真后再决定下一组。可以选择三种方式：

| 方式 | 谁决定下一组参数 | 应保留的证据 |
|---|---|---|
| Agent 推理，默认 | 当前 Agent 根据电路、工作点和历史指标推理 | 调整假设、参数、真实测量与结果 |
| GP 贝叶斯提案 | 累计有效观测重拟合高斯过程，挑一个候选 | 训练数据、预测与候选来源；预测不能当实测 |
| 混合 | GP 建议，Agent 检查器件关系与物理合理性 | 提案、接受或修改理由、仿真回填 |

这里的 GP 脚本使用 scikit-learn，不是 BoTorch；512 个候选只在代理模型上评分，不代表跑 512 次仿真。网格／随机搜索保留为兼容入口，不能称为 Agent 推理。失败、缺指标、NaN 或 history 不匹配都记为无效评估。

**交付：**基线和最终参数、逐轮理由、指标变化、预算使用情况、独立复测与未验证条件。最终所选参数应符合具体目标；OSC 例中为了更贴近 100 MHz，选择了功耗略高于早期可行点的尺寸。

### virtuoso-layout

**什么时候用：**原理图确认后开始版图，或修改现有物理设计。

> 用 $virtuoso-layout 读取这个电路的技术绑定、真实 PCell 端子、层与 via。先给出紧凑放置、供电和敏感走线方案；执行后分别报告 DRC、LVS、PEX，并说明哪些没有运行。

Agent 先查询当前 technology、制造网格、合法 layer/purpose 和 viaDefs，再制定放置与布线策略；规则来自实际 PDK。DRC 检查几何规则，LVS 检查版图与原理图电路对应，PEX 提取寄生，三者分别报告，不能互相替代。

**交付：**可编辑布局、端口／几何读回、对应 GDS 和新验证日志；如果缺工具、许可或 deck，明确列出缺项。OSC 案例本次没有执行版图；基础矩形、标签和 via 操作通过，完整 DRC／LVS／PEX 未验证。

### virtuoso-helper

**什么时候用：**任何时候需要理解界面、菜单、快捷键、术语或错误。

> 用 $virtuoso-helper 解释 Maestro 中的 wn/wp 和原理图参数是什么关系，告诉我怎样保持参数化、怎样继续修改。先说明当前编辑器和完成判断，不要猜我屏幕上有什么。

Agent 给出具体操作顺序、如何判断完成和要查的文档。快捷键取决于 schematic、Layout XL 或 ViVA 等上下文，还要以本机 bindkeys 为准。

**交付：**可执行的界面步骤和解释；用户要求实际执行时转到对应技能。helper 保留了原来 Cadence *Basics of Analog Flow* RAK 的六章摘要与速查，不附原始手册 PDF。

## 安装与开始使用

### 给 Agent 一段话来安装

访问 [GitHub 中的五技能目录](https://github.com/CATEular/Eularcat-PersonalWebsite/tree/main/skills/virtuoso-workflow)，或打开 [GitHub ZIP 下载页](https://github.com/CATEular/Eularcat-PersonalWebsite/blob/main/public/downloads/virtuoso-workflow.zip)，点击下载原文件。公开仓库不需要登录。

把下面整段复制给有本地文件与终端能力的 Agent：

```text
请从 https://github.com/CATEular/Eularcat-PersonalWebsite 的 main 分支读取
skills/virtuoso-workflow/README.md 和 export-manifest.json，按清单下载五个技能。
先检查 SKILL.md、脚本和依赖，再把 virtuoso-connect、virtuoso-testbench、
virtuoso-params、virtuoso-layout、virtuoso-helper 放在同一技能父目录下。
Codex 可使用用户级 ~/.agents/skills/ 或项目级 .agents/skills/。
不要覆盖同名技能或已有 config.local.json；发现旧版时先列出差异。
将 virtuoso-connect/config.example.json 复制为 config.local.json，
帮我确认并填写自己的 Python、bridge .env 位置、虚拟机连接、授权工作库、
PDK 与仿真目录，不猜路径、不输出凭据。
先复用已有 virtuoso_bridge；缺少时按官方说明在独立 Python 环境安装并核对 API。
检查五个技能可发现和相对引用完整，用 api_probe.py 做本地接口探测，
再用 virtuoso-connect 做只读连接验证，最后报告已完成项与仍缺的配置。
```

技能需要保持同级，因为它们的参考文档相互链接。Codex 的当前技能位置与发现方式以 [官方技能文档](https://learn.chatgpt.com/docs/build-skills) 为准；新增内容未出现时重新打开对话，必要时重启应用。

### 安装的三层东西

1. **技能套件：**五个 `SKILL.md`、参考与辅助脚本，告诉 Agent 怎么完成任务。
2. **桥接运行环境：**Python 和 [virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite)，负责本机到 Virtuoso 的真实通信。
3. **EDA 环境：**可访问的虚拟机或 Linux 主机、正在运行的 Virtuoso、Spectre／OCEAN、许可及合法可用的 PDK。

只有网页聊天能力、不能访问本地文件／执行程序的 Agent，不能靠读一个 `SKILL.md` 就连接私有虚拟机。

首次装外部 bridge 时，可在本地工作目录中按其官方说明创建独立环境。Windows 示例：

```powershell
git clone https://github.com/Arcadia-1/virtuoso-bridge-lite.git
cd virtuoso-bridge-lite
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -e .
& ./.venv/Scripts/virtuoso-bridge.exe --help
& ./.venv/Scripts/virtuoso-bridge.exe init
```

按当前 `init` 帮助填写自己的 bridge `.env`，再运行 `start`／`status`。在真实 CIW 加载 `start` 输出的准确 `load(...)` 指令；不要照搬别人的临时路径。已有环境优先复用。以上步骤依据 [bridge 官方说明](https://github.com/Arcadia-1/virtuoso-bridge-lite)，具体命令和接口仍需核对安装版本。

### 只维护一份个人配置

五个技能共享 `virtuoso-connect/config.local.json`。下载包只提供空字段示例，填写后才可用于你的环境。

| 配置分组 | 自己填写的内容 |
|---|---|
| local | bridge／科学计算解释器、源码及 `.env` 位置、技能与项目目录 |
| bridge | SSH 主机／用户名／端口、转发端口、可选 profile |
| remote | 授权工作区、cds.lib、仿真与 OCEAN 目录、可执行文件位置 |
| design | 工作库、库目录、technology |
| pdk | 已有 PDK、器件映射、模型文件及有效 sections |

配置优先级为：任务显式指定文件 → `VIRTUOSO_WORKFLOW_CONFIG` → 默认本地配置。bridge 凭据仍留在它自己的 `.env`；共享配置只引用该文件的位置。示例 JSON 能通过结构检查，不代表 SSH、所有目录、许可和 PDK 都可用。

默认 Agent 推理不需要另配置模型 API。GP 提案需要 NumPy／SciPy／scikit-learn；YAML 复制工具需要 PyYAML。按实际用途安装：

```sh
python -m pip install -r requirements-optional.txt
```

### 第一次用什么来检查

先让 connect 验证只读命令，再让 testbench 跑 [RC 示例](./rc/)。确认本轮 AC／OCEAN 结果可读以后，用 params 改一个变量并独立复测。之后再做 [OSC 多轮闭环](./osc/)，容易分清连接问题、测量问题和电路问题。

## 交付应该留下什么

- 原理图或版图保持可编辑；普通信号连续接线、排布紧凑。
- 每轮指标带准确结果标识；多 test／corner／point 不只取第一个成功点。
- 推荐尺寸写在电路旁边，附单位、供电、角点、温度、负载和验证条件；原理图变量表达式保留。
- 最终参数应用到 ADE，独立复测后打开同一 history 的 Maestro 结果与 ViVA 波形，供下一轮继续修改。
- 说明哪些检查没做。这里的 OSC 只有 TT 原理图验证，不含 PVT、相噪、完整版图或流片签核。

## 下载内容与参考

GitHub 提供可检查源码与 ZIP；保留 [完整文件清单](https://github.com/CATEular/Eularcat-PersonalWebsite/blob/main/skills/virtuoso-workflow/export-manifest.json) 和来源说明。包里没有私有配置、凭据、PDK 模型、项目日志或网站开发 Agent 预设。

记录中的运行环境是 bridge 0.7.0、IC 6.1.8、Spectre 18.1。OCEAN 提取器用到 bridge 内部 SSH runner，升级后要检查兼容性；示例里的替代接口不是跨版本保证。

测量隔离思路参考 [virtuoso-agent](https://github.com/lixunqi12/virtuoso-agent)。本工作流仍通过 SKILL／ADE 启动 Spectre，独立 OCEAN 读取结果；没有做纯 OCEAN 仿真后端的直接速度对比，也没有证明 GP 比 Agent 物理推理更快。
