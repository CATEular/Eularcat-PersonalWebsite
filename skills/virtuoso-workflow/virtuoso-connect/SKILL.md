---
name: virtuoso-connect
description: Connect ChatGPT or Codex to a Cadence Virtuoso VM through virtuoso_bridge; discover Python and bridge configuration, verify connectivity, inspect installed API signatures, and diagnose SSH, CIW, or blocking-dialog failures. Use for connection and transport problems, not circuit optimization or design editing.
---

# Virtuoso Connect

负责本机 → SSH → 虚拟机 → Virtuoso CIW 的连接与诊断。连接成功后将任务交给对应领域技能；这里不修改电路、PDK 或仿真设置。

## ChatGPT / Codex 执行约定

- 先读 [platform.md](references/platform.md)。使用当前会话实际提供的文件、命令或电脑操作工具，不假定 Claude Code、Antigravity 的工具、后台参数或斜杠命令存在。
- 本机 Python 调用 `virtuoso_bridge`，SKILL 在远端 CIW 执行；本机路径和虚拟机路径分别记录。桥接库是外部运行依赖，本技能不实现通信服务。
- 写调用前核对实际安装源码或签名；用 [api_probe.py](scripts/api_probe.py) 做纯本地探测，无需连接虚拟机。接口参考与实机不一致时，以当前安装代码、Cadence 文档及最小验证为准，不猜接口。
- 已验证过连接、绘图、ADE 调参、版图基础操作和独立 OCEAN 读取；具体版本边界、成功入口及未测试范围见 [runtime-capabilities.md](references/runtime-capabilities.md)，当前环境从本地配置读回。

## 连接流程

1. 按 [环境配置协议](references/environment.md) 读取本技能目录中的 `config.local.json`（或用户明确指定的配置），从中取得解释器、bridge 配置文件、主机、工作范围和 PDK 信息。主技能不存个人路径；先复用已有环境，不重装到全局 Python。
2. 使用 [workflow_config.py](scripts/workflow_config.py) 明确选择配置中的 bridge `.env` 并核对端点；配置缺失或字段无效时定位缺项，不回退到历史机器。用当前 CLI 帮助核对行为。只检查必要字段，不打印密码、私钥或整个 `.env`；仅在缺少配置时初始化。
3. 在所选环境内检查 CLI 帮助、启动桥接并查询状态。PowerShell 下通过解释器或 `.venv/Scripts/` 程序的绝对路径执行；不用 Bash 的 `source`，不拼接多层引号的 `python -c`。
4. 隧道连通与 CIW 已监听是两个独立条件。若远端需要加载初始化 `.il`，使用当前启动输出中的路径，不硬编码历史 `/tmp` 路径。有可用且已授权的 CIW 操作渠道时执行，否则向用户给出准确的 CIW 指令。
5. 用 `getCurrentTime()` 等只读调用验证 `result.ok` 和非错误输出；记录 bridge 版本、解释器、配置来源及连接状态。远端版本未查到时标记未知。
6. 保留本次建立的服务和隧道供后续操作使用。不要在命令退出后假定后台进程仍然存活；独立检查其状态。

多行 SKILL 优先保存 `.py` 或 `.il` 文件。CLI `eval --stdin` 是否可用由当前版本验证，不能继承旧版的永久禁用结论。

## 故障处理

读 [recovery.md](references/recovery.md)，按本机程序、SSH、端口转发、远端监听、CIW 模态对话框逐层定位。连接超时不等于电路失败。只处理已识别、属于本次操作的对话框；不批量确认未知弹窗，不自动删除设计锁文件，不终止其他用户的进程。

## 转交

- 参数扫描、优化 → [virtuoso-params](../virtuoso-params/SKILL.md)。
- 原理图、symbol、ADE、测试平台和设计库复制 → [virtuoso-testbench](../virtuoso-testbench/SKILL.md)。
- layout、DRC/LVS/PEX → [virtuoso-layout](../virtuoso-layout/SKILL.md)。
- 快捷键、菜单、解释和文档查询 → [virtuoso-helper](../virtuoso-helper/SKILL.md)。

函数检索细节见 [skill-finder-python-api.md](references/skill-finder-python-api.md)。只有需要查询远端函数文档时才使用连接，不为纯文件检查启动虚拟机服务。
