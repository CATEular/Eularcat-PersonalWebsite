# 每轮结果决定下一轮参数

## 默认：当前 Agent 推理

当前 ChatGPT/Codex 就是决策者。脚本负责一次仿真、状态持久化和合法性检查，不在脚本中调用另一个 LLM。无需用户每轮批准常规参数调整，沿用已授权范围、规格、角点与预算。

先读原理图/网表、参数物理意义、偏置和测量定义，尽量选择有作用机理的独立变量；匹配对、共用偏置、宽度比等关系用项目 adapter 派生，避免把所有晶体管宽度都独立优化。实际修改参数前仍检查 CDF 与网表一致性。

每次测量后查看完整指标、工作点/器件区域、相较基线和前轮的变化，以及当前最优可行点。区分：测量错误、偏置/区域不正确、规格尚未满足、已可行而需要提升性能。前轮可能变差；保留历史最佳，不默认把前轮当最佳。

为下一轮记录主要瓶颈、调整假设、拟修改变量及幅度、预期权衡。先用少数有诊断价值的改动建立方向，得到足够证据后允许联合修改。没有工作点或拓扑证据时将解释标为假设，不从 Gain/PM 两个数编造器件工作状态。可以做小幅局部探测来检验假设，不扩成全域 sweep。

每轮只交一组合法候选给仿真；读回结果后再决定下一组。模型/角点/测量规则改变时另立可比较的基线，不能靠改评分标准制造改善。

## 可执行的逐轮入口

配置与 adapter 协议沿用 [optimization.md](optimization.md)。`iterate_params.py` 不循环选点，一次 step 只调用一次 `evaluate(parameters, run_dir)`。

```text
python scripts/iterate_params.py init config.json --output tuning_session
python scripts/iterate_params.py step tuning_session --proposal candidate_01.json --adapter project_adapter.py
```

第一次 proposal 必须是配置中的 baseline。之后 Agent 根据实际结果编写下一轮 proposal：

```json
{
  "based_on_evaluations": 1,
  "strategy": "agent_reasoning",
  "parameters": {"W1_um": 12, "W2_um": 18},
  "rationale": "此处写基于本轮电路/指标证据的调整理由，不预先假定增益与 PM 一定改善。",
  "hypothesis": "此处记录待下一轮仿真检验的机制假设。"
}
```

参数名必须完整匹配 config；单位、上下界、步进和离散值由 config 定义。rationale 必填，based_on_evaluations 必须等于当前已完成次数，拒绝旧结果生成的过期提案。无效指标仍消耗一次预算，不能把失败当好结果。

每轮目录保留 attempt.json、record.json、adapter 原始日志与结果。inspect 从已完成记录恢复历史，提供最新/最佳点、逐指标变化和剩余预算；改变策略不清空历史。

```text
python scripts/iterate_params.py inspect tuning_session
python scripts/iterate_params.py validate tuning_session --adapter project_adapter.py
```

最后一次预算保留给当前最佳可行点的独立复测。可提前 validate，但随后此 session 结束；无可行点不能标为成功。程序中断留下未完成 run 时先确认远端作业和已保存结果再恢复，不盲重跑；`.iteration.lock` 属于本工作流，不是可随意清除的 Cadence 设计锁。

## 可选：数据驱动的贝叶斯提案

`bayes_suggest.py` 使用 NumPy/SciPy/scikit-learn，每次读取全部已完成有效记录，分别为目标和约束指标拟合 Matérn 高斯过程，计算预测均值和不确定度。在已经存在可行点时按期望改进×可行概率选点；尚无可行点时先找可能满足约束的点。参见 [BoTorch 官方闭环约束优化示例](https://botorch.org/docs/tutorials/closed_loop_botorch_only/)。本脚本独立使用 sklearn，不声称运行了 BoTorch。

```text
python scripts/bayes_suggest.py tuning_session --output candidate_02.json
python scripts/iterate_params.py step tuning_session --proposal candidate_02.json --adapter project_adapter.py
```

实际执行时科学计算解释器与 bridge 解释器可以分开。从共享配置取 `local.scientific_python` 和 `local.bridge_python`，分别核对 numpy/scipy/sklearn 与 bridge 依赖。前者出候选 JSON，后者执行一次真实仿真。

默认先获得 min(8, max(3, 2×参数数+1)) 个有效初始观测，缺数据时提出一个与已测点分开的合法试验，明确标为 initial_maximin，而非已拟合的 GP。预算不足以训练并复测时选 Agent 模式，不宣称贝叶斯模型已建立。

候选池默认512个，仅在便宜的代理模型上评分，**不会对512个点跑仿真**；只选择其中一个交给 step。每轮新结果回填后重训，下一点随测量数据改变。Agent 可以拒绝不符合电路机理/相关尺寸关系的建议，修改后仍保存理由和该轮观测索引。

限制：采用独立指标模型及单点 EI、候选池近似优化，归一化输出空间默认 noise_variance=1e-6。强噪声、指标强相关、很多变量或稀有可行域，需要适当噪声估计、降维或经过验证的 BoTorch/TuRBO/SCBO 后端；本脚本不保证全局最优。仿真失败不作为有限高分塞进 GP。预测改善不能代替实测可行性。

## 混合方式与验证边界

Agent 负责物理假设、变量关系、工作区和失败诊断；贝叶斯模型负责从累计测量中挑选下一个有价值的点。接受候选→仿真→更新历史→Agent 分析→再次建议，直到预算、目标或有证据的停滞条件触发；随后独立复测。没有改善时缩步长、回到历史最好点附近或更换假设，不无限重复同一候选。

逐轮状态、合法性/预算保护、数据改变导致 BO 建议改变，均有本地合成函数测试。配置所记录的真实验证 PDK 上的五级 CMOS 环振（10 MOS）也已跑通：三组基线/Agent 反馈实测后，显式 initial_points=3 拟合 GP 并执行两次约束 EI 候选，模型在第4组测量回填后重训，下一组参数随之改变。两次 BO 探索分别得到92.727MHz和125.897MHz，没有胜过此前100.907MHz的点；违规候选被排除，历史最佳保留。随后 Agent 拟合局部周期模型精调并独立验证最佳。该示例验证决策→真实仿真→结果回填的闭环，不证明少量数据下 BO 比物理推理更高效，也不证明全局最优。
