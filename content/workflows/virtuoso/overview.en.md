---
title: Virtuoso workflow through multiple conversations
description: Five skills, an engineering conversation, real OSC/RC/MOS cases, and installation from GitHub
---

## Combine skills across turns

Describe a goal, let the agent clarify conditions and execute, inspect the drawing and measurements, then request the next change. Connection state, design variables, run history and saved recommendations connect those turns. The skills are task roles rather than five mandatory sequential stages.

| Need | Skill | Handoff |
|---|---|---|
| Python, SSH, tunnel or CIW connection | virtuoso-connect | testbench or layout after connection |
| Schematic, symbol, testbench and ADE | virtuoso-testbench | params after a trustworthy baseline |
| Measurement-driven sizing or bias tuning | virtuoso-params | Independent validation and editable delivery |
| Placement, routing and physical checks | virtuoso-layout | testbench for post-layout simulation |
| UI, menus, hotkeys, concepts or errors | virtuoso-helper | Continue the original project after guidance |

A skill is workflow guidance and supporting scripts. Cadence **SKILL** is a scripting language. The external `virtuoso_bridge` provides communication; Spectre performs circuit simulation. These skills do not replace licensed EDA software or your own PDK.

### virtuoso-connect

Use for first-time connection or transport diagnosis.

> Use $virtuoso-connect to read my local config, inspect Python and the installed bridge API, then verify SSH, the tunnel and CIW. Work only in my designated workspace and report each successful check and missing field.

The agent selects the configured interpreter and `.env`, checks the tunnel and remote listener separately, and verifies a read-only CIW command. It reports versions, configuration source and scope without printing secrets. A reachable port alone does not prove Virtuoso is ready.

### virtuoso-testbench

Use for DUT/symbol/TB creation or editing, ADE configuration, a single simulation, result export and project-hierarchy copying.

> Use $virtuoso-testbench to create a compact RC low-pass testbench with R = 2 kΩ, C = 1 pF and unit AC input. Use continuous terminal-to-terminal wires, verify connectivity, save, run AC, and return this run's bandwidth and waveform.

The agent reads actual terminals, CDF fields and installed API signatures, checks symbol ports and the generated netlist, and records supply, stimulus, load, models, corner and measurement definitions. Deliveries include editable drawings, setup, run IDs and measured data bound to the exact history/test/corner/point. Ongoing tuning belongs to params. Hierarchical copying needs an explicit plan and separate simulation-equivalence checks.

### virtuoso-params

Use when a circuit and trustworthy measurements already exist.

> Use $virtuoso-params to tune this OSC within the specified bounds, keeping Wp = 2 × Wn. Analyze each result, run only one candidate at a time and retain the best measured feasible point. Include independent validation in the budget and leave final Maestro/ViVA views open.

Define units, bounds, constraints, corner and a finite budget; save a baseline. Each candidate includes a reason and is measured before selecting the next one.

| Strategy | Decision source | Evidence |
|---|---|---|
| Agent reasoning, default | Current agent examines circuit, operating points and history | Hypothesis, parameter change and real measurement |
| GP proposal | Gaussian processes refitted from valid observations | Training data and predicted candidate, separate from measurements |
| Hybrid | GP proposes; agent checks physical relationships | Acceptance/revision reason and measured feedback |

The GP script uses scikit-learn, not BoTorch. A pool of 512 candidates is scored by the surrogate; only one is simulated. The legacy grid/random search remains a compatibility entry and is not agent reasoning. Missing metrics, failed runs, non-finite values and history mismatches are invalid evaluations.

Deliver baseline/final values, round-by-round reasons, measurements, budget, independent validation and untested conditions. The OSC example selected greater frequency accuracy at slightly higher power than an earlier feasible point, rather than optimizing every metric at once.

### virtuoso-layout

Use for physical design after schematic review, or existing-layout edits.

> Use $virtuoso-layout to inspect this circuit's technology, PCell terminals, layers and vias. Propose compact placement, supplies and sensitive routing. Report DRC, LVS and PEX separately and identify checks that were not run.

The agent reads current binding, manufacturing grid, legal layers and viaDefs before applying PDK-specific rules. DRC, LVS and PEX answer different questions and need separate fresh evidence. Deliver editable geometry, pins, GDS and logs, or identify missing tools/licenses/decks. The OSC example did not include layout; only basic rectangles, labels and vias were tested.

### virtuoso-helper

Use at any point for UI guidance, menus, hotkeys, terminology or errors.

> Use $virtuoso-helper to explain how schematic wn/wp expressions relate to Maestro variables and how to keep tuning. State the editor context and how I can verify completion; do not guess my screen.

Deliver concrete steps and explanations. Bindkeys depend on editor and local customization. Pure guidance does not start a bridge; execution requests are handed to the appropriate sibling skill. Six summarized chapters and a cheatsheet retain the source skill's attribution to Cadence's *Basics of Analog Flow* RAK; the original PDF is not distributed.

## Install and start

### Give your agent one installation prompt

Visit the [five-skill source directory on GitHub](https://github.com/CATEular/Eularcat-PersonalWebsite/tree/main/skills/virtuoso-workflow), or open the [GitHub ZIP page](https://github.com/CATEular/Eularcat-PersonalWebsite/blob/main/public/downloads/virtuoso-workflow.zip) and download the raw file. The public repository requires no login.

```text
Read skills/virtuoso-workflow/README.md and export-manifest.json from the main branch
of https://github.com/CATEular/Eularcat-PersonalWebsite and download the listed files.
Review all five SKILL.md files, scripts and dependencies. Install virtuoso-connect,
virtuoso-testbench, virtuoso-params, virtuoso-layout and virtuoso-helper as siblings
in a supported skill directory. Codex supports ~/.agents/skills/ for user skills
and .agents/skills/ for project skills. Do not overwrite same-name skills or an
existing config.local.json; show differences first if an older version exists.
Copy config.example.json to virtuoso-connect/config.local.json. Help me identify
and fill my own Python, bridge .env location, VM, authorized library, PDK and
simulation paths without guessing or printing credentials. Reuse an existing
virtuoso_bridge; if missing, follow its official setup in a separate Python
environment and inspect API compatibility. Verify skill discovery and relative
references, run api_probe.py locally, then perform a read-only connection check
with virtuoso-connect. Report completed checks and remaining configuration gaps.
```

Keep the five folders together because their relative references depend on sibling paths. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations. Start a fresh conversation, or restart the app if newly installed skills do not appear.

### Install three separate layers

1. **Skills:** instructions, references and helper scripts.
2. **Bridge:** Python and the external [virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite).
3. **EDA environment:** SSH-accessible VM/Linux host, running Virtuoso, Spectre/OCEAN, licenses and an authorized PDK.

A browser-only chat without local file and execution capabilities cannot access a private VM just by reading SKILL.md.

For a new bridge environment on Windows, use a dedicated local working folder:

```powershell
git clone https://github.com/Arcadia-1/virtuoso-bridge-lite.git
cd virtuoso-bridge-lite
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -e .
& ./.venv/Scripts/virtuoso-bridge.exe --help
& ./.venv/Scripts/virtuoso-bridge.exe init
```

Fill the private bridge `.env` using your installed version's help, then run `start`/`status` and load the exact CIW command printed by `start`. Reuse working installations. These steps follow the [bridge documentation](https://github.com/Arcadia-1/virtuoso-bridge-lite); verify current signatures and command behavior locally.

### One shared private configuration

All five skills read `virtuoso-connect/config.local.json`. The download supplies an example with empty fields, not a runnable environment.

| Section | Supply your own |
|---|---|
| local | Python interpreters, bridge source/.env and skill/project directories |
| bridge | SSH host/user/port, forwarded ports and optional profile |
| remote | Authorized workspace, cds.lib, result/OCEAN directories and executables |
| design | Work library, path and technology |
| pdk | Authorized library, device map, model path and valid sections |

Precedence: explicit configuration → `VIRTUOSO_WORKFLOW_CONFIG` → default local file. Bridge credentials remain in its separate `.env`; the workflow references only its location. Schema validation does not verify connectivity, every path, licenses or model usability.

Agent reasoning needs no additional model API client. GP proposals need NumPy/SciPy/scikit-learn; YAML cloning helpers need PyYAML. Install only for your intended use:

```sh
python -m pip install -r requirements-optional.txt
```

### A first exercise

Verify read-only connectivity, then try the [RC case](./rc/). Once AC/OCEAN readback works, change one parameter and independently rerun it. Move on to the [OSC conversation](./osc/) after the measurement chain is trustworthy.

## Deliver a project you can continue

- Editable drawings with compact, continuous wiring.
- Measurements bound to exact result IDs; evaluate every required test/corner/point.
- Saved recommended dimensions with units, supply, load, corner and conditions; retain parameter expressions.
- Selected values applied in ADE and independently rerun, with final Maestro results and ViVA waveform from the same history left open.
- Explicit untested conditions. The OSC record covers TT schematic simulation, not PVT, phase noise, physical design or tapeout signoff.

## Download contents and references

GitHub provides inspectable source and a ZIP with an [explicit manifest](https://github.com/CATEular/Eularcat-PersonalWebsite/blob/main/skills/virtuoso-workflow/export-manifest.json) and attribution. No private config, credentials, PDK model, project log or website development preset is included.

Recorded validation used bridge 0.7.0, IC 6.1.8 and Spectre 18.1. OCEAN readers depend on an internal bridge SSH runner; inspect compatibility after upgrades. Version-specific fallback APIs are not universal guarantees.

Worker isolation was informed by [virtuoso-agent](https://github.com/lixunqi12/virtuoso-agent). This workflow launches Spectre through SKILL/ADE and uses isolated OCEAN for result reading. A pure-OCEAN simulation backend was not compared directly for speed, and GP was not shown to outperform agent reasoning.
