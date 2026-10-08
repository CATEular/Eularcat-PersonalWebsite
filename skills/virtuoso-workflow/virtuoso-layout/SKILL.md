---
name: virtuoso-layout
description: Create or edit Virtuoso layouts with verified technology, PCells, pin geometry, layers, vias, matching and routing constraints; export GDS and run or interpret DRC, LVS, and PEX checks. Use for physical design and layout verification; connection issues and schematic testbench creation use the corresponding sibling skills.
---

# Virtuoso Layout

负责版图读取、器件放置、匹配与布线、pins/vias、GDS 和 DRC/LVS/PEX。物理验证完成后，将后仿真测量交给 [virtuoso-testbench](../virtuoso-testbench/SKILL.md)，参数调优交给 [virtuoso-params](../virtuoso-params/SKILL.md)。

## 前置检查

先读 [平台约定](../virtuoso-connect/references/platform.md) 和 [环境配置协议](../virtuoso-connect/references/environment.md)，读取共享本地配置，按需 [连接](../virtuoso-connect/SKILL.md)。明确 lib/cell/view、PDK、工艺绑定、原理图版本、目标面积/匹配/电流/寄生要求。技术绑定从数据库查询，不相信历史库状态。

读 [layout-python-api.md](references/layout-python-api.md)、[layout-skill-api.md](references/layout-skill-api.md) 并核对实际安装签名。技术绑定接口见 [library-python-api.md](../virtuoso-testbench/references/library-python-api.md)。

## 编辑流程

1. 读取层级、真实器件和 terminal 几何、合法 layer/purpose、制造网格、viaDefs 和现有布局。不要按截图猜连接坐标。
2. 制定放置与走线策略，说明需要的对称、匹配、共心、guard ring、电源与敏感信号约束。规则来自配置所选的实际 PDK，不写死其他工艺的数值。
3. 默认 `modify()`，新视图才用 `create()`；先核对是否会覆盖。用已确认 PCell 和参数生成器件，避免手绘替代复杂工艺器件。
4. Python 坐标用 tuple/list，SKILL 坐标由 API builder 生成。label/via/PCell 能否脚本创建由实际函数与当前版本验证，不继承旧 cookbook 的“必须 GUI”结论。
5. 使用符合工艺规则的走线方向与网格；直角布线是常用起点，但允许方向与角度由 PDK 决定。pin label 放在正确层/形状上，label 不自动等于有完整电气 terminal 的 pin。
6. 保存、读回几何与端口并截图检查；缩放造成 tiny shapes 不显示时先读 shape 数量和 bbox，不重复创建。

## 验证与交付

按 [verification.md](references/verification.md) 准备 stream map / deck / top cell，导出本次新 GDS 并检查当前 run 日志。分别报告 DRC、LVS、PEX 状态，不能由某一项通过推出其他项通过。没有工具、license 或 deck 时可交付布局与检查计划，状态明确为未运行。

布局改动后重新生成相关验证结果，禁止把旧 PEX 当当前版图结果。交付包含版图位置、GDS、当前验证日志、未解决项，以及用户要求的后仿真状态。
