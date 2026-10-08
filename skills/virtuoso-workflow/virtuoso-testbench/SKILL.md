---
name: virtuoso-testbench
description: Read, create, or edit Virtuoso schematics and symbols; build testbenches and Maestro/ADE setups, run one-shot simulations, export history-bound results, and clone testbenches with their project hierarchy into a fresh library. Use for schematic connectivity, measurement setup, simulation reproduction, or library packaging; parameter search belongs to virtuoso-params.
---

# Virtuoso Testbench

负责 DUT 原理图、symbol、测试平台、ADE 配置、单次仿真、结果导出和设计层级复制。包含原 librarian 的设计数据管理功能。持续参数搜索由 [virtuoso-params](../virtuoso-params/SKILL.md) 驱动，版图由 [virtuoso-layout](../virtuoso-layout/SKILL.md) 负责。

先读 [平台约定](../virtuoso-connect/references/platform.md) 和 [环境配置协议](../virtuoso-connect/references/environment.md)，从共享本地配置取得工作库、PDK、解释器和路径，需要时完成 [连接](../virtuoso-connect/SKILL.md)。原 API 参考来自旧技能；先核对安装签名，引用外部示例前确认文件实际存在。

## 原理图与 symbol

1. 明确目标 lib/cell/view，读现有实例、连通性、CDF、pins 和 symbol 端口，使用 [schematic-python-api.md](references/schematic-python-api.md)。
2. 已有设计默认用 `modify()`；`create()` 可能清空已有视图，不能为普通编辑先删除整个 cell。新建时选不冲突的名字。
3. 默认采用用户偏好的连续导线、两端实际相连；信号从左到右，供电在上、地在下。不要用一串命名短线代替可读的接线；VDD、GND/VSS 等公共电源可用全局符号或名称。必要的接口 pin 名称保留，不给普通内部线手工起名。按 [drawing-style.md](references/drawing-style.md) 排布并核对连通性。
   默认紧凑排布：依据实际器件图形和文字确定间距，缩短级间连接、上下管间距及电源/反馈绕线。缩放到全图时应能看清器件和关键参数，避免大块空白；调整位置后重新 Check & Save 和核对连通性。
   沿用用户认可的标注格式：统一字体/字号、左对齐分行，把概况和已验证 `Recommended` 实际参数放在电路旁边空白处；不重复大号器件说明，不遮挡连线或 CDF 文字。独立复测后的推荐尺寸、条件、指标与 history 永久保存到原理图，关闭 ADE 后仍能找到；细节见上述绘图规范。
4. CDF 修改按 [参数修改](../virtuoso-params/references/parameter-editing.md) 执行；Check & Save 后核对网表和端口。
5. 核对 symbol 端口、pin order、标签和 selection box。本机 bridge 0.7.0 的生成包装层在 IC6.1.8 调用了不存在的函数；使用 [实测能力与替代入口](../virtuoso-connect/references/runtime-capabilities.md) 中已测试的原生生成方式。其他版本先验证包装层。详见 [symbol-python-api.md](references/symbol-python-api.md)。

## 测试平台与仿真

记录供电、偏置、刺激、负载、分析类型、输出表达式、测量单位、模型/section 和角点。沿用项目的有效模型组合，不盲目包含全部 sections。

按 [simulation-flow.md](references/simulation-flow.md) 绑定目标会话 → 保存 → 异步运行 → 检查完成 → 按 exact history 读结果。重复运行用独立输出目录，不自动清除既有结果。不批量关闭或 purge 用户会话。

参数迭代可采用已实测的 SKILL/ADE 控制 + 独立 OCEAN 结果读取，见 [ocean-skill-flow.md](references/ocean-skill-flow.md)；本套件自带 AC 带宽读取脚本。不要把耗时的 PSF 处理全部塞进主 CIW。

读取所有所需 test/corner/point；`.log` 只作辅助诊断，不能默认替代完整结果表。波形缺失时先检查保存设置与 resultsDir，不用旧标量补充成新测量。单独 Spectre 运行可使用已安装 runner；先核对接口和返回契约，保留日志。

## 库管理与独立复现

一般库操作见 [library-python-api.md](references/library-python-api.md)。完整复制见 [cloning.md](references/cloning.md)。自带 [clone_tb_full.py](scripts/tb_clone/clone_tb_full.py) 默认只生成只读计划，显式 `--execute` 才写入一个已存在、无 cell 的目标库。

复制项目层级，保留 PDK/analogLib/std-cell 引用；先确认外部库分类、config 绑定和同名冲突。禁止源库=目标库、同名不同源 cell 自动合并、自动删除锁。保存实例 property 类型/值，重新绑定后 Check & Save。脚本不能证明仿真等价，必须比较导出网表和用户要求的仿真指标；config-only 额外层级需先补齐。

## 按需参考

- [schematic-skill-api.md](references/schematic-skill-api.md)：terminal、CDF 和低层 SKILL。
- [maestro-python-api.md](references/maestro-python-api.md)、[maestro-skill-api.md](references/maestro-skill-api.md)：会话、分析、变量、角点、结果读写。
- [netlist.md](references/netlist.md)、[batch-netlist-si.md](references/batch-netlist-si.md)：导入/导出；优先已验证的高层接口。
- [schematic-recreation.md](references/schematic-recreation.md)：从已有设计重建时的几何排布。
- [cellview-on-disk-layout.md](references/cellview-on-disk-layout.md)：磁盘数据；OA 和二进制 metadata 不直接文本编辑。
