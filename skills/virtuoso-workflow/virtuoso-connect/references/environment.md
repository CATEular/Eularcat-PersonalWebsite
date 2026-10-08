# 本地环境配置协议

五个技能共享 `virtuoso-connect/config.local.json`。个人路径、主机/用户名/端口、PDK、库与模型信息只维护在这一个文件，主技能、脚本和公共参考不保存个人环境常量。公开下载附 config.example.json；使用者复制为 config.local.json 并填写自己的环境。

Agent 在任何依赖环境的操作前读取配置：用户显式指定文件 → `VIRTUOSO_WORKFLOW_CONFIG` 环境变量 → 相对于本技能目录的 `config.local.json`。当前任务的明确指示优先于默认配置。纯概念解释无需配置或连接。文件缺失、字段为空或路径无效时定位缺项，不能回退到文档中的历史机器；新增环境由使用者填入自己的本地配置。

| 配置键 | 用途 |
|---|---|
| `schema_version` | 当前为1 |
| `local.bridge_python` / `local.scientific_python` | bridge 与科学计算解释器，可分开 |
| `local.bridge_source` / `local.bridge_env_file` | 实际安装源码与 bridge 凭据配置的文件位置 |
| `local.skill_root` / `local.skill_scanner_root` / `local.project_workspace` | 安装、发现及项目目录 |
| `bridge` | SSH 地址/用户/端口、隧道端口与可选 profile |
| `remote.work_root` / `remote.cds_lib` | 默认远端工作范围与库注册文件 |
| `remote.simulation_root` / `remote.ocean_worker_root` | 仿真与隔离测量产物目录 |
| `remote.executables.ocean` / `remote.executables.spectre` | 远端可执行文件 |
| `design` | 默认工作库、库目录、technology |
| `pdk` | PDK 库/目录、器件 cell、模型路径与已有 ADE sections |
| `verified_environment` / `last_verified_design` | 上次核验的版本、设计与结果位置；是历史记录，不代替当前读回 |

配置不等于扩大授权；默认工作库不允许 Agent 操作所有库。每次读回实际库绑定与模型配置。`inherited_ade_sections` 记录已有测试平台的设置，不能把全部 sections 自动应用到任何新电路。不修改 PDK；不改注册库的目录来整理文件。

自带 [workflow_config.py](../scripts/workflow_config.py) 使用标准库 JSON 读取配置，提供 `load_config()`、`require(config, "字段.路径")` 和 `make_client()`。后者按本地配置明确选择原来的 bridge `.env`，检查端点是否一致，再创建客户端；不改写原 `.env`。升级 bridge 后核对相关接口签名。

PowerShell 中先用文件工具读 JSON，取 `local.bridge_python` 为解释器，再执行所需脚本。套件目录由文件位置推导，不依赖当前工作目录。例如：

```powershell
& $bridgePython "$connectSkill/scripts/api_probe.py"
```

这里两个变量来自已读取的配置和当前技能位置，不是全局系统变量。OCEAN 提取器默认从同一配置取可执行文件，也允许显式 `ocean_bin` 参数；具体 PSF 与本次输出目录由调用方按实际任务提供。

个人配置已经加入本技能 `.gitignore`。发布通用技能时保留技能、脚本及通用参考，个人配置由使用者自行处理；不打包项目日志、旧技能归档、完整 `.env`、密钥或 PDK 内容。凭据仍由 bridge 的现有机制管理，不复制进本配置或报告。
