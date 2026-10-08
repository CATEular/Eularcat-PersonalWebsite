# 仿真 adapter 与历史兼容搜索器

默认调参入口已改为 [adaptive-loop.md](adaptive-loop.md) 的逐轮 Agent / 贝叶斯闭环。本文件定义三种入口共享的参数配置与真实仿真 adapter。

保留的 `scripts/search_params.py` 使用 Python 标准库，无 EDA 内置调用。它执行基线 → 小离散网格或固定种子随机探索/局部候选 → 对最佳可行点独立重跑。属于旧兼容策略，不是 Agent 推理或贝叶斯优化，不再默认使用。

## 输入

项目的 JSON 配置：

```json
{
  "parameters": {
    "width_um": {"min": 1, "max": 20, "step": 1},
    "fingers": {"values": [1, 2, 4, 8]}
  },
  "baseline": {"width_um": 5, "fingers": 2},
  "objective": {"metric": "power_mw", "goal": "min"},
  "constraints": [
    {"metric": "gain_db", "min": 60, "scale": 10},
    {"metric": "pm_deg", "min": 60, "scale": 10}
  ],
  "max_evals": 20,
  "seed": 7
}
```

数值统一使用项目定义的单位，不解析 `u`/`m` 后缀。连续变量不写 step；离散变量用 values 或 min/max/step。基线必须在合法域内。约束 scale 是违规度归一化单位，必须为正；默认 scale 为 1，不对不同单位自动猜权重。`max_evals` 包含基线和最后一次复核。

## 项目 adapter 协议

提供一个 Python 文件，导出 `evaluate(parameters: dict, run_dir: Path) -> dict`。这是本套件自己定义的函数，不是假想 bridge API。adapter 的责任是：

- 显式绑定目标设计、写候选参数、保存设置、运行仿真并验证完成状态。
- 为每次调用使用给定的独立 run_dir，绑定 exact history/test/corner/point。
- 对多点结果返回配置要求的最差值，并保存完整原始结果与测量定义。
- 返回 `{"ok": true, "metrics": {"power_mw": 1.2, "gain_db": 62, "pm_deg": 65}, "evidence": {...}}`；`evidence` 写 history、结果目录等 JSON 可序列化信息。
- 错误返回 `{"ok": false, "error": "..."}` 或抛异常。缺失/NaN/Infinity 指标按无效评估记录。
- 不擅自修改测试标准、扩大参数域或关闭无关会话；记录基线恢复方案。adapter 超时需要由实际仿真工具控制，搜索器不会强制终止远端作业。

```text
python scripts/search_params.py config.json --adapter project_adapter.py --output project_runs
```

输出目录必须尚不存在，避免覆盖。生成 config.json、evaluations.jsonl、每次 run 目录及 summary.json。`validated` 只表示最佳可行点在独立复核中满足配置约束；不是 PVT sign-off，除非 adapter 实际覆盖要求的所有角点。复核失败时状态是 `validation_failed`，不能把历史最佳点交付为已验证结果。

可行性优先排序：有效且满足全部约束的候选优先；无可行点时只报告最小归一化违规度的候选，不宣称成功。重复候选不重复仿真，最后复核例外。预算耗尽或有限离散域已探索完时停止。
