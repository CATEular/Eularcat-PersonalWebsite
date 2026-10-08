---
name: virtuoso-helper
description: Explain Virtuoso workflows, menus, configurable hotkeys, ADE and ViVA usage, and Cadence documentation; help the user understand errors or choose a task-specific sibling skill. Use for human guidance and reference lookup, not automatic design mutation or parameter search.
---

# Virtuoso Helper

负责用户帮助：快捷键、菜单、概念、界面操作流程、错误解释和文档定位。纯解释不启动 bridge；用户要求实际执行时再转交相应技能，继续完成已授权任务。

涉及用户环境、文件位置或实际执行时，按 [环境配置协议](../virtuoso-connect/references/environment.md) 读取共享本地配置；主技能不保存个人路径、主机或 PDK 库名。纯通用帮助无需配置。

## 选择帮助方式

- 快捷键查询：确认 active editor（schematic / Layout XL / ViVA）、是否有活动命令、当前选择；同一个键在不同上下文含义不同。
- 流程教学：给最短可操作步骤，说明怎样判断完成；需要截图时只用当前工具真实取得的截图，不猜用户屏幕。
- API 查询：先查对应领域本地参考和安装签名；远端文档检索通过 [virtuoso-connect](../virtuoso-connect/SKILL.md)。
- 错误诊断：区分连接、接口、PDK、设计和验证问题；引用实际错误，不把历史经验当普遍限制。
- EDA 文档书签：读 [documentation.md](references/documentation.md)。仅在用户要求处理文档时加载 PDF 技能和依赖，不自动整理无关文档。

## 操作知识来源

快捷键和六章流程来自旧 `virtuoso_hotkey_helper`，其记录来源为 Cadence *Basics of Analog Flow: A Design-Oriented Approach — Rapid Adoption Kit*（141 页，Virtuoso 6.1.8 ISR18 等版本）。这是来源元数据；本套件没有原始 PDF，未逐页复核。当前 bindkeys、版本和 PDK 优先。

- [初始环境与库](chapters/ch01-initial-setup.md)
- [原理图编辑](chapters/ch02-schematic-editor.md)
- [ADE 与波形](chapters/ch03-simulation-waveforms.md)
- [Layout XL](chapters/ch04-layout-xl.md)
- [布线](chapters/ch05-routing.md)
- [DRC/LVS 与后仿真](chapters/ch06-verification-postlayout.md)
- [cheatsheet.md](cheatsheet.md)、[glossary.md](glossary.md)、[patterns.md](patterns.md)

## 任务归属

| 请求 | 使用 |
|---|---|
| 连虚拟机、隧道/CIW 超时 | [virtuoso-connect](../virtuoso-connect/SKILL.md) |
| 扫描/优化 W/L、偏置、补偿 | [virtuoso-params](../virtuoso-params/SKILL.md) |
| 画原理图、做 TB/ADE、跑单次仿真、复制库 | [virtuoso-testbench](../virtuoso-testbench/SKILL.md) |
| 放置布线、GDS、DRC/LVS/PEX | [virtuoso-layout](../virtuoso-layout/SKILL.md) |

这些是任务边界，不是必须依次运行的流水线。需要完整电路架构设计时可调用环境中实际可用的 analog 设计技能；本套件不虚构那些能力，也不强制普通界面操作先做完整设计审查。
