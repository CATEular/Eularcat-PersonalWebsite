# 本机能力记录（2026-10-08）

范围：Windows Python3.11.15、bridge0.7.0、远端 IC6.1.8/Spectre18.1；只在当时配置指定的工作区与工作库测试；具体环境、库/PDK 名与路径在本地配置中维护。不构成其它版本或其它 PDK 的保证。

| 能力 | 结果与使用方式 |
|---|---|
| SSH/bridge/CIW | 成功；CLI start/status、只读 execute_skill |
| schematic 创建/编辑 | 成功；RC、TB、MOS 端子读回；连续导线重画后 RC 仿真复验 |
| 多拐点画线 | 默认 route/full 接口会忽略后续拐点；逐段两点绘制可用，见 drawing-style |
| CDF 参数更新 | r/c、w/l/fingers 可写入；单位格式可能变化；MOS w/wf 派生值不一致，不能宣称有效尺寸正确 |
| MOS B 端连通 | stub helper 本机可用；连续 B/S 接 VSS 也已读回，不沿用旧资料的永久禁用说法 |
| symbol 生成 | 高层包装层失败：dbFindOpenCellViewByName 不存在；下述原生入口成功，端口 IN/OUT/VSS 和 pinOrder 已核对 |
| ADE 配置/异步仿真 | AC 与 OSC tran、变量、输出、保存、run_and_wait 成功；OSC scalar 三项与 OCEAN 一致 |
| ADE 结构化结果表 | 本机 read_results 返回空字典；不能作有效测量。单 test/corner/point 的 exact-history scalar fallback 已成功 |
| 独立 OCEAN | 具体 history 的 PSF AC 带宽与 OSC tran 频率/摆幅/供电功耗读取成功，OSC CSV 周期均值与电流时间积分交叉核对通过 |
| 波形导出 | 显式 history 和 analysis 的 export_waveform 成功 |
| layout | METAL1/METAL2 rectangle、label、via 的 Python API 与 .il 加载均成功；实际 viaDef 为 M2_M1 |
| 整库/层级复制 | 仅离线保护逻辑与语法检查；未执行远端整库复制 |
| DRC/LVS/PEX/GDS | 未做实机验证或 signoff，不标为通过 |

## symbol 已验证替代入口

仅对明确的新建 symbol 或已授权重建对象调用，然后读回端口顺序：

```lisp
schPinListToSymbol("<configured_work_library>" "<cell>" "symbol"
  schSchemToPinList("<configured_work_library>" "<cell>" "schematic"))
```

## 结果目录和单点读回

maeSetEnvOption projectDir 不是本机有效控制入口。当前安装的 Cadence anasimhelp/appA.html 记录：

```lisp
envGetVal("asimenv.startup" "projectDir")
envSetVal("asimenv.startup" "projectDir" 'string "<configured_simulation_root>")
axlGetResultsLocation(axlGetMainSetupDB("<session>"))
```

保存原 startup 值，每次实际运行前确认目录。OSC 测试发现：仅在 GUI 打开前设置、随后提前恢复会使后续仿真重新读全局值，实际 history 写往旧目录。必须在运行后再次用 axl getter/作业元数据核对实际位置；保留最终可编辑会话时保留可继续运行的授权目录设置。不写用户 .cdsenv/.cdsinit，不盲改已有会话 root。

只有确认单 test/corner/point 时才用：

```lisp
maeOpenResults(?session "<session>" ?history "<本轮history>")
maeGetOutputValue("BW" "AC")
maeCloseResults()
```

多角点/sweep 需遍历所有点；推荐独立 OCEAN 与点元数据映射。不能从 done 回调或空结果表推断达标。

## 返回值的实测差异

find_skill 返回 list[dict]。decode_skill_output 只解引号，不解析 SKILL list；结构化读取用 fetch 的实际字段契约。get_skill_more_info 本机缓存可能异常/返回 None，改用已安装文档或 doc-search。run_shell_command 输出是 csh 返回值，不是 stdout；取 stdout 用已核对 SSH runner 或文件回传。upload/download 必须查 .ok，不能假定失败一定抛异常。

证据保存在本次工作副本的 validation 目录：live-followup.json、live-maestro.json、wired-schematics.json、live-hybrid.json、逐轮 OCEAN 日志/JSON。生产技能目录不包含完整 Cadence 手册或原始 PDK 模型。


## OSC 与闭环新增实测

本地配置所记录的验证 PDK、1.8V、TT27℃，五级 CMOS环振、10 MOS和5个参数化负载电容，直接端子连线。按用户进一步要求，最终排版由级间距5缩至1.75、上下管间距4缩至1.0；几何改动前后所有端子分组、CDF参数和IC一致。单指 fingers=m=1，w=wn/wp、wf=wn*1/wp*1，生成 Spectre 网表 w=wn/wp，L180n已核对；不能由此推断其它指数组合正确。

500ns transient、maxstep50ps、skipdc=yes，C1IC1.8V、其余0V起振；稳定100–500ns。Maestro Frequency_Hz/Vpp_V/Power_W 标量与独立 OCEAN 和原始 CSV 一致。maeSetSpec 本机不能同时传 gt 与 lt；频率范围用原生 `?range list("90M" "110M")`，按本机官方文档验证。

每轮只仿真一个点：147.923MHz基线→Agent增负载101.345MHz→Agent缩尺寸100.907MHz/0.757mW→GP约束EI探索92.727MHz→数据回填重训GP探索125.897MHz。后者超频而被排除，最佳保留。模型提案仅使用实际有效观测，512个点只在代理模型评分，不执行512次仿真。实际后端由 SKILL/ADE 启动 Spectre、独立 OCEAN读取结果；纯 OCEAN仿真循环仍未实测。仅TT原理图示例，不包含PVT、相噪、版图或签核。

观察到单点评估约24–25秒：ADE run/wait约8秒，其中Spectre约3.2–3.6秒，OCEAN进程启动/读取与两条CSV回传约13.4–13.6秒。说明传输与启动开销值得优化，但尚未做纯OCEAN后端A/B对比，不能断言两路线速度相同或固定加速比。


OSC最终Agent周期模型精调为 Wn/Wp=1.3/2.6µm、L180nm、每级C480fF；独立第7次评估、history `Interactive.6` 复测得到 100.480076MHz、1.801465Vpp、0.822851mW，全部TT约束通过。共6个搜索点（含2个GP候选）+1次独立复测；最高预算12次，初次独立验证后7次结束；用户进一步要求紧凑后再固定最佳参数确认1次，合计8次。参数保留应用，最终GUI按用户工作流交付。


## 最终 Maestro / ViVA 展示的本机替代入口

OSC独立复测后，原生 openResults(exact_psf) / selectResult('tran) / awvCreatePlotWindow / awvPlotWaveform 已成功显示最终OUT，currentWindow + xLimit(list(100n 150n)) 显示几个稳态周期。主 Maestro编辑会话保留，maeRestoreHistory(准确history) 显示三项绿色pass，wn/wp/cload读回与独立验证一致。

本机 bridge 的 open_waveform_viewer 包装层向 maeOpenSetup 传 ?application，IC618本机签名不接受而失败。不要盲用；上述直接精确PSF入口已实测。

对ViVA调用generic screenshot虽然.ok，但得到0字节文件，不能作成功证据。使用原生 OCEAN 图形导出并核对文件大小和图像：

```lisp
saveGraphImage(?window cwFinalPlot
  ?fileName "<configured_work_library_path>/<unique_final_wave>.png"
  ?enableTitle t ?enableLegend t ?enableAxes t ?enableGrids t)
```

本机官方文档 oceanref/chap8.html#saveGraphImage。已生成并视觉检查最终100–150ns OUT波形。Maestro generic截图正常。终态保留准确原理图窗口、Maestro editing会话与ViVA窗口；不执行close/purge或恢复基线。


原理图 GUI 旧窗口在几何编辑后出现像素缓冲未刷新：hiZoomIn/schZoomFit改变返回bbox，hiRedraw/hiFlush和截图仍显示旧的局部电路。保存已编辑的目标cell，**仅关闭自己的该原理图窗口**，用已核验 geOpen 同cell编辑模式重新打开，resize+fit后完整5级和标签正常。不要关闭Maestro或ViVA，不删除锁、不改PDK display；旧窗口截图不能当作当前OA绘图的完整证据。最终原理图窗口47，经视觉查看确认紧凑且完整。

最终更紧凑版本（级间距1.75、上下间距1.0）后，第8次固定最优参数确认history `Interactive.7`，频率/摆幅/功耗与第7次独立复测完全一致；原7轮优化状态与记录完整保留，排版后确认单独存档。最终Maestro与ViVA绑定Interactive.7，原理图保持完整可编辑。
