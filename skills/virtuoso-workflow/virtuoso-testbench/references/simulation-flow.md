# 仿真、会话和结果绑定

本套件的维护流程优先于历史 API 示例中的批量 purge、force-close 或“取最新 history”操作。仅控制明确属于本次任务的对象。

## 会话所有权

先识别指定 lib/cell 的已开会话，保护用户未保存设置。查询配置可用背景会话；当前 bridge 的回调等待流程通常使用 GUI 会话。`open_gui_session()` 的生命周期实现可能清理其他会话，调用前查当前源码；有其他用户工作窗口时复用准确目标或用核验过的精确打开流程。不要直接取 `car(maeGetSessions())` 当目标。

## 一次评估

1. 固定 test、corner、分析、刺激、负载与模型组合，记录本轮变量值。
2. 原理图改动完成 Check & Save；保存 Maestro setup，避免旧值运行。
3. 使用当前版本支持的异步 run 和等待机制。不要在会阻塞 CIW 事件循环的调用里使用 `?waitUntilDone t`；超时先判断仿真进度与 GUI 弹窗。
4. 保存本次返回的 history 和完成状态。返回 history 名称不等于仿真成功；核对作业日志、仿真状态、所有要求点的有效指标。
5. 调用 `read_results(..., history=history)`，保留 test/corner/point 到输出的映射。详见 [maestro-python-api.md](maestro-python-api.md)。
6. 导出波形也显式指定 history 与分析，确认实际 resultsDir 属于这轮 history。远端文件名和本地目录按 run/test/point 唯一命名；固定 `/tmp` 文件可能与其他导出冲突。
7. 检查缺失波形、表达式错误、单位、有效测量区间。需要原始波形时设置适当的 signal save；不要盲目 save all 大量数据。
8. 保留最终结果的可编辑会话。用户本人的默认交付要求是打开最终参数对应的原理图、Maestro 数值/设计变量和 ViVA 波形，核对它们来自同一 final history，留给用户继续修改。只关闭本次明确不再需要的临时会话；用户原来打开的会话保留，失败日志和运行证据保留供诊断。

## OCEAN 与测量

实测接口差异和结果目录控制见 [runtime-capabilities.md](../../virtuoso-connect/references/runtime-capabilities.md)。本机结构化结果表返回空字典，已验证单点 exact-history 标量 fallback；重复调参可采用 [独立 OCEAN 工作流](ocean-skill-flow.md)，保持主 CIW 响应。

用实际安装版本的信号和 result API；大小写、函数空间和 result 类型不能混淆。先枚举实际 signals，再使用正确的路径。旧技能对 `vf`、`VF`、`v` 的结论不构成跨版本规则。

低频增益必须按输入/输出传递关系定义；只在 AC 输入幅度确认为 1 且接法匹配时，可由输出直接推导。PM 要测适当的 loop gain、穿越点和相位定义，不能把所有 AC 输出都按 `180 + phase` 套用。

参数优化期间每轮使用独立 history。若模型、测量或保存策略变更，将其视为新评估配置，重新建立可比较的基线。

最终图像导出也核对文件非空并视觉查看；transport `.ok` 不保证截图有效。本机 ViVA 的 generic screenshot 返回0字节，改用原生 `saveGraphImage`，准确调用见 [能力记录](../../virtuoso-connect/references/runtime-capabilities.md)。
