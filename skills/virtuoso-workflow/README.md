# Eularcat Virtuoso workflow / 五个技能，一段工程对话

Connect → create a testbench → measure → tune from feedback → independently validate → leave editable results. Layout and UI help join when needed.

| Skill | Responsibility |
|---|---|
| virtuoso-connect | Python/bridge/SSH/CIW connectivity and diagnosis |
| virtuoso-testbench | Schematics, symbols, testbenches, ADE and one-shot simulation |
| virtuoso-params | Sequential agent/GP proposals, history and independent validation |
| virtuoso-layout | Physical design and separate DRC/LVS/PEX checks |
| virtuoso-helper | UI, menus, hotkeys, concepts and documentation |

## 让 Agent 安装 / Ask your agent to install

把下面这段话交给有本地文件和终端能力的 Codex 或 Agent：

> 请从 https://github.com/CATEular/Eularcat-PersonalWebsite 的 main 分支读取 skills/virtuoso-workflow/README.md 和 export-manifest.json，按文件清单下载这套 Virtuoso 工作流。先检查五个 SKILL.md 和脚本，再把 virtuoso-connect、virtuoso-testbench、virtuoso-params、virtuoso-layout、virtuoso-helper 放到同一个技能父目录；Codex 可使用用户级 ~/.agents/skills/ 或项目级 .agents/skills/。不要覆盖同名技能或已有 config.local.json；若发现旧版，先列出差异。把 config.example.json 复制为 virtuoso-connect/config.local.json，帮我确认并填写自己的 Python、bridge .env 位置、虚拟机连接、授权工作库、PDK 和仿真目录，不猜路径、不输出凭据。先复用已有 virtuoso_bridge；没有时按外部 bridge 官方说明在独立 Python 环境安装，核对当前版本接口。安装后验证五个技能可发现、相对引用完整，使用 api_probe.py 检查本地 API，再按 virtuoso-connect 做只读连接验证，报告成功项与缺失配置。

Public downloads do not require a GitHub login. Keep all five skill folders as siblings: their references point to one another. Install optional libraries only if using GP proposals or YAML-based cloning helpers:

```sh
python -m pip install -r requirements-optional.txt
```

## Validated environment / 已验证环境

这套工作流围绕 VMware 上运行 Virtuoso 的 Linux 虚拟机开发与验证，支持 Agent 通过 bridge／SSH 操作虚拟机。CentOS／Red Hat 原生主机上直接运行 Virtuoso 的方式尚未尝试，暂不列为已验证环境。

This workflow was developed and validated around Virtuoso running in a Linux virtual machine on VMware, with the agent connecting through the bridge and SSH. Running Virtuoso directly on a native CentOS or Red Hat host has not been tried and is not a validated setup.

## Dependencies and configuration

The skills are instructions and helper scripts. Actual execution requires a local-capable agent, Python, external [virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite), SSH access, running licensed Virtuoso/Spectre/OCEAN, and a PDK you are authorized to use. A browser-only chat cannot reach a private VM simply by reading SKILL.md.

Use the bridge's documented `init`, `start` and `status` flow and the exact CIW `load(...)` line returned by your installation. The private `.env` remains separate. This suite's `config.local.json` points to it; it does not replace it or store passwords. Fill every field needed by your operation. Configuration precedence: explicit path → `VIRTUOSO_WORKFLOW_CONFIG` → `virtuoso-connect/config.local.json`. Read [environment.md](virtuoso-connect/references/environment.md).

The example configuration contains empty fields, not a ready-to-run environment. `workflow_config.py` validates the schema and requested fields; it does not verify that every path, license or PDK model is usable. `api_probe.py` checks the installed local Python API without connecting to the VM.

Recorded validation used bridge 0.7.0, IC 6.1.8 and Spectre 18.1. The OCEAN readers depend on an internal SSH runner; inspect compatibility after upgrading. Use the current installed API rather than assuming a version-specific fallback works everywhere.

## Start a project

1. `$virtuoso-connect` — read my local config and verify a read-only CIW command.
2. `$virtuoso-testbench` — create a compact continuously wired RC testbench; run AC and return exact-history data.
3. `$virtuoso-params` — use the measurements to choose the next legal parameter point; preserve the best feasible point and independently rerun it.
4. `$virtuoso-helper` — explain how to continue editing the ADE variables.
5. `$virtuoso-layout` — inspect my technology and plan layout when I explicitly request it; report each verification status separately.

## What the download includes

The explicit [export-manifest.json](export-manifest.json) lists every exported product file. The ZIP contains the manifest itself, instructions, scripts, configuration example and attribution. It excludes private configs, credentials, PDK models, project logs and development agent presets. See [ATTRIBUTION.md](ATTRIBUTION.md) and [runtime-capabilities.md](virtuoso-connect/references/runtime-capabilities.md) for provenance and verification limits.
