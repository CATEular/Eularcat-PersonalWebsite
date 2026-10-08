---
name: virtuoso-params
description: "Tune existing Virtuoso or Spectre circuits in a sequential closed loop: analyze each measured result and choose the next parameter set using the current ChatGPT/Codex agent, constrained Gaussian-process Bayesian optimization, or both. Use for W/L, bias, compensation, sizing, and design-variable optimization with explicit bounds, metrics, history-bound evidence, and independent validation."
---

# Virtuoso Params

负责已有电路的参数修改、灵敏度分析和闭环优化。默认每轮仿真后由当前 ChatGPT/Codex 分析，再决定下一组参数；不默认生成 W1×W2×… 的全组合 sweep。输出“本次范围与预算内已验证的最佳可行参数”，不承诺全局最优。电路拓扑设计与新测试平台创建不在此技能范围内。

## 开始前

1. 阅读 [平台约定](../virtuoso-connect/references/platform.md)，按 [环境配置协议](../virtuoso-connect/references/environment.md) 读取共享本地配置；需要连接时使用 [virtuoso-connect](../virtuoso-connect/SKILL.md)。解释器、工作范围、PDK 和路径均从配置取得。
2. 明确 DUT/TB、测量定义、目标、约束、参数单位/上下界/合法步进、角点和评估预算。能从项目资料推断就先整理；缺少会改变结果的目标或界限时向用户询问，同时读取现有设计。
3. 保存原始参数和一轮基线结果。测试平台不完整时先交给 [virtuoso-testbench](../virtuoso-testbench/SKILL.md)，完成测量闭环后继续优化。

## 参数与评估

- 用 ADE 变量或已有参数化网表优先，避免每个候选都重建电路。直接改 MOS CDF 时读 [parameter-editing.md](references/parameter-editing.md)。
- 用同一配置和角点评估所有候选；每次保存设置再运行，给本次 run 独立目录与标识；读结果显式绑定 history、test、corner/point。
- 用现有 ADE/OCEAN 测量定义，尤其相位裕度应来自适当的环路测量，不把任意输出电压的相位自动当 PM。
- 本机已验证 SKILL/ADE 改变量与运行、独立 OCEAN 子进程读取具体 PSF、JSON 指标回填搜索器；按 [ocean-skill-flow.md](../virtuoso-testbench/references/ocean-skill-flow.md) 使用，保留全部运行标识和日志。
- 模拟失败、缺指标、非有限数或结果历史不匹配都是无效评估，不当作高分或零值。
- 多角点要求按指标约定取最差值，未跑的角点标记未验证。约束可行性优先于性能提升；不能用平均值掩盖违规点。

## 搜索与停止

按 [adaptive-loop.md](references/adaptive-loop.md) 选择策略：

- **默认 Agent 闭环**：读取电路和工作点、当前及历史指标，诊断主要限制，说明下一组参数的假设与理由，再只运行这组。自带 [iterate_params.py](scripts/iterate_params.py) 每次只执行一次评估，并将控制权交回 Agent；当前 Agent 自己推理，不要求另建 Claude/Gemini/OpenAI API 客户端。
- **贝叶斯或混合闭环**：自带 [bayes_suggest.py](scripts/bayes_suggest.py) 用全部已完成的有效观测重拟合高斯过程，优先可行概率/约束期望改进，只建议一个新点。Agent 可检查器件合法性、对称性及电路假设后接受或修订。预测不计作实测，少量初始试验不是全组合扫参。
- **显式扫参/旧搜索**：用户要求曲线、诊断局部灵敏度或穷举极小离散域时才用；[search_params.py](scripts/search_params.py) 保留为兼容入口，属于网格/随机局部探索，不称为 AI 推理或贝叶斯优化。

两种默认闭环共用 [optimization.md](references/optimization.md) 的项目 adapter、真实仿真和日志契约。可以切换策略继续同一历史。BoTorch/TuRBO 等专业后端可在安装并验证后替换提案层；本套件当前没有安装或实测这些后端，不照搬旧 optimizer 的未核验 Maestro 示例。

遵守用户给定的仿真/时间预算；未指定时声明一个适合任务的有限预算。重复配置错误先修正再搜索；不靠无限重试推进。预算耗尽、无可行点或测量无法成立时，交付当前证据与瓶颈。

## 交付

独立重跑候选并核验约束，随后给出原始/最佳参数、基线/重跑指标、测量配置、角点、评估次数和原始证据。不要把 optimizer 的代理预测当实测。用户要求应用参数时按已有授权写入并读回；仅探索时保留基线设计及候选记录。

有可编辑原理图时，将本次独立复测通过的实际推荐尺寸永久标在电路旁边，标题为 `Recommended (verified)`，包括单位、关键条件/指标、日期和最终 history/test；按 [绘图与推荐标注规范](../virtuoso-testbench/references/drawing-style.md) 保存并读回。保留器件参数化表达式，推荐注释不代替 ADE 变量。后续优化更新 Agent 管理的同一标注；条件改变时明确旧记录是历史结果，不能误称已验证当前设置。无可行点不标推荐。

用户本人的工作流默认要求可视化交付：将本次最佳可行参数写回 ADE 并读回，以这些参数独立重跑；打开该轮 OUT 波形和 Maestro 的测量数值、设计变量，保留原理图、Maestro 和 ViVA 窗口供用户继续修改。明确绑定最终 history，不能展示上一轮波形或代理预测。除非用户明确要求只做探索或关闭窗口，不在结束时恢复基线、关闭最终会话。本机 ADE 会在运行时再次读取全局 startup projectDir，不能在打开会话后提前恢复。每轮运行前确认授权的结果目录，运行后查询实际位置；最终保留可编辑会话时保留适用于用户继续运行的目录设置，并记录原值。经核验的会话专属持久设置可优先使用。

测试平台运行与结果导出使用 [simulation-flow.md](../virtuoso-testbench/references/simulation-flow.md) 和 [Maestro API](../virtuoso-testbench/references/maestro-python-api.md)，不另维护一套仿真接口。
