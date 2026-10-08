# SKILL / ADE 控制与隔离 OCEAN 测量

参考公开项目 [virtuoso-agent](https://github.com/lixunqi12/virtuoso-agent) 和其 [ocean_worker.py](https://github.com/lixunqi12/virtuoso-agent/blob/main/src/ocean_worker.py)。该项目以现有 bridge 控制设计及仿真，将 PSF 波形处理放在一次性 OCEAN 子进程。这里借鉴执行隔离思路，脚本为本套件独立编写；不需要它的 Claude/Gemini API 或安装整套 agent。

已实测的闭环：SKILL/bridge 设置 Maestro 变量 → 保存 setup → ADE 异步运行并返回具体 history → 选定该 history 的 test/corner/point PSF → 在独立 OCEAN 进程中 `openResults` / `selectResult` / `getData` / 测量 → JSON 指标 → 有限预算搜索器 → 优选参数独立再跑一次。

自带 [ocean_ac_metric.py](../scripts/ocean_ac_metric.py) 只读一个 AC point 的低通 3 dB 带宽，调用：

```python
result = extract_ac_bandwidth(
    client, exact_psf_dir, authorized_remote_worker_root,
    new_local_run_dir / "ocean", node="/OUT", timeout=45,
)
```

运行前核对精确 PSF 来源。本次单 test、单 corner、单 point 的实际路径为 `<results_location>/<history>/1/AC/psf`；这不是跨项目固定模板，禁止直接用于多角点或 sweep。通过 job/point 元数据定位每个 PSF，再聚合全部必需条件；不能只取第一个通过点。

OCEAN 原语内容保存为 `.ocn`，由远端已安装 `ocean -nograph -restore` 执行。每次独占 UUID 工作目录，用远端 GNU `timeout` 限定该子进程组，保留 console/OCEAN 日志；JSON 必须是本次新文件、指标为有限有效数字，不能只看进程退出码。远端 worker root 必须属于用户授权工作区，不指向 PDK 或用户其它设计。

实测环境：IC6.1.8 / Spectre18.1，OCEAN 可执行文件从共享配置的 `remote.executables.ocean` 取得。脚本依赖 bridge 0.7 的私有 SSH runner；升级后核对 runner 接口，不能宣称跨版本稳定。当前脚本只做结果读取；纯 OCEAN `design/desVar/analysis/run` 重新仿真尚未实测，不把该能力记成成功。必要时先用当前安装的 `oceanref` 文档核对，再在独立测试目录验证。

带宽测量要求低通响应、明确 AC 输入与输出关系。本次 RC 的 AC 输入幅度为 1；不能把这个测量套用到所有电路。使用其它指标时另建针对实际波形的测量脚本，先与 ADE/解析结果交叉验证。


## OSC 瞬态读取与界面交付

自带 [ocean_osc_metric.py](../scripts/ocean_osc_metric.py) 在独立 OCEAN 中读取准确 history 的 transient OUT 和电源正端电流，导出两条原始 CSV，并测量稳定窗口的半电源上升沿频率、摆幅、平均供电功耗。Python 用全部稳定周期的平均频率和电流时间积分交叉核对；缺少周期、电流、测量不稳定或非有限结果均失败。

```python
result = extract_osc_metrics(
    client, exact_psf_dir, authorized_remote_worker_root,
    new_local_run_dir / "ocean", node="/OUT",
    current="/VDD_SOURCE/PLUS", start=100e-9, stop=500e-9,
    supply=1.8, target_frequency=100e6, timeout=45,
)
```

电源电流采用 Spectre 电压源流入正端约定，耗电功率为负的供电电压乘平均电流；其它器件/刺激必须核对符号。这里固定直流供电，变电压供电需改为瞬时 V×I 再积分。Maestro 的频率使用相同稳定窗口的前两个上升沿，OCEAN 标量与 Maestro 相互核对，平均周期频率用于验证稳态。这一频率方法是单音环形振荡器的示例，不自动适用于多音、间歇起振或强抖动。

配置所记录的验证 PDK 上的 5 级 CMOS OSC 已验证 transient、单指尺寸参数化、起振 IC、此提取器及 Maestro 标量一致；闭环搜索记录区分 Agent 推理与 GP 预测，不以预测代替真实仿真。当前后端每轮仍由 SKILL/ADE 启动 Spectre，独立 OCEAN 只处理结果。它不是纯 OCEAN 仿真循环。OCEAN 也能通过 design/desVar/analysis/run 运行；参见 [Cadence 官方论坛的原理图 netlisting 与 run 说明](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/38480/post-layout-simulation-using-ocean-script)，但此后端的速度差尚未做直接 A/B 计时验证。

最终参数独立复测后，将同一 history 的 Maestro 数值/设计变量与 ViVA 波形打开并保留，默认显示几个稳定周期，完整起振波形仍保存供用户缩放。不要在 finally 中恢复基线或关闭最终窗口。
