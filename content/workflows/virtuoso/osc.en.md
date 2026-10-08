---
title: "OSC: a request, eight real evaluations, an editable result"
description: A five-stage CMOS ring oscillator with agent/GP tuning, independent validation and final Maestro delivery
---

## What was completed

This workflow was developed and validated around Virtuoso running in a Linux virtual machine on VMware, with the agent connecting through the bridge and SSH. Running Virtuoso directly on a native CentOS or Red Hat host has not been tried and is not a validated setup.

A real five-stage CMOS ring oscillator was created and simulated, tuned using measured feedback, independently rerun and delivered with editable views. Final measurements: **100.480 MHz**, **1.801 Vpp**, **0.823 mW**. Validation date: 2026-10-08.

This record covers **TT schematic-level verification**, not OSC layout, PVT, phase noise or tapeout signoff. Demonstration prompts are edited from actual requests and records; private environment identifiers are omitted.

![Actual final OUT waveform over 100–150 ns](/assets/virtuoso/osc-waveform.png "Native ViVA waveform from Interactive.7; the full transient run is 500 ns.")

## Conversation 1: define a measurable task

**Your input**

> Build an OSC to test the workflow, at schematic level first. Propose the specifications. Leave the final waveform, parameters and Maestro open so I can continue editing.

**Agent response**

> Use a five-stage CMOS ring at 1.8 V, TT and 27 °C. Target 100 MHz ±10%, at least 1.6 V swing and at most 3 mW average power. Parameterize Wn/Wp and each stage's load, keeping L = 180 nm and Wp = 2 × Wn.

Connect establishes the verified transport. Testbench queries actual MOS terminals, creates 10 MOS devices and five loads and configures supply and ADE. Helper can explain the topology, variable expressions or UI at any turn.

| Condition | This example |
|---|---|
| Topology | Five CMOS inverter stages, 10 MOS devices |
| Supply / corner / temperature | 1.8 V / TT / 27 °C |
| Tunable variables | Wn, Wp and Cload; Wp = 2 × Wn |
| Length / fingers | L = 180 nm; one finger, m = 1 |
| Frequency | 90–110 MHz, with final refinement toward 100 MHz |
| Swing / average power | ≥1.6 V / ≤3 mW |
| Evaluations | Finite search/validation budget; eight real runs completed |

## Conversation 2: revise the drawing

**Your input**

> Make it more compact, with continuous terminal-to-terminal wires for ordinary signals and readable parameter labels.

**Agent action**

Tighten the stage and complementary-device spacing using actual glyphs and labels, move loads close to outputs and shorten supplies/feedback. Check & Save, compare parameters and terminal/net connectivity, then rerun the fixed final values after the geometry changes.

![Actual compact OSC schematic with saved recommended values](/assets/virtuoso/osc-schematic.png "Cropped/redacted screenshot; wiring, parameter expressions and recommended values are preserved.")

`wn` and `wp` are **width W**, not length L. Maestro values are `wn = 1.3u`, `wp = 2.6u` and `cload = 480f`. Keep the expressions in the schematic and preserve the width ratio when editing.

## Conversation 3: measure the baseline

**Your input**

> Measure this exact history with OCEAN before choosing the next point. Return frequency, swing and supply power, not old results.

```text
Set and save Maestro variables through SKILL
→ ADE launches Spectre transient
→ Locate the exact history/test/corner/point PSF
→ Isolated OCEAN reads OUT and supply current
→ Export raw CSV and JSON metrics
→ Cross-check Maestro scalars, average periods and current integration
```

Run length is 500 ns, maximum step 50 ps, stable measurement window 100–500 ns. Explicit startup IC sets one capacitor to 1.8 V and the others to 0 V with `skipdc=yes`. Frequency uses half-supply rising edges, cross-checked against mean stable periods.

Power uses DC supply voltage and source current with the Spectre positive-terminal sign convention checked. A time-varying supply would require integration of instantaneous V×I.

The 2/4 µm, 500 fF baseline measured **147.923 MHz and 1.281 mW**, outside the frequency range.

## Conversation 4: choose one new point from each result

**Your input**

> Avoid a Cartesian sweep. Choose the next point from measured feedback; combine agent reasoning and Bayesian proposals if useful. Retain the best point and explain the method used.

| Run | Decision | Wn/Wp (µm) | C/stage (fF) | Frequency (MHz) | Power (mW) | Frequency feasible |
|---|---|---|---|---|---|---|
| 1 | Baseline | 2/4 | 500 | 147.923 | 1.281 | No |
| 2 | Agent: larger load | 2/4 | 740 | 101.345 | 1.280 | Yes |
| 3 | Agent: smaller devices and matching load | 1.2/2.4 | 440 | 100.907 | 0.757 | Yes |
| 4 | Constrained GP/EI proposal | 1.2/2.4 | 480 | 92.727 | 0.758 | Yes |
| 5 | GP refit after feedback | 1.2/2.4 | 350 | 125.897 | 0.758 | No |
| 6 | Agent: local measured-period model | 1.3/2.6 | 480 | 100.480 | 0.823 | Yes |
| 7 | Independent validation | 1.3/2.6 | 480 | 100.480 | 0.823 | Yes |
| 8 | Confirmation after compacting geometry | 1.3/2.6 | 480 | 100.480 | 0.823 | Yes |

Three measured observations preceded two constrained Matérn GP/EI proposals. The GP was refitted after feedback. A pool of 512 points was scored only by the surrogate; one candidate was simulated each turn. Neither GP exploration improved the earlier point, and the over-frequency candidate was rejected. Agent reasoning then used measured periods for refinement.

Run 6 reduced frequency error from approximately 0.907% at run 3 to **0.4801%**, while increasing power from 0.757 to about 0.823 mW. The selected point favors proximity to 100 MHz within the power limit. If the goal were solely minimum power inside the frequency range, run 3 would remain a relevant candidate. No global optimum or universal GP speed advantage is claimed.

## Conversation 5: save the result in the project

**Your input**

> Apply the selected values and independently rerun. Leave schematic, waveform and Maestro open. Save recommended dimensions beside the circuit so they remain available after closing ADE.

- Exact measurements: 100.480076 MHz, 1.801465 Vpp and 0.822851 mW.
- Run 7 independently validated the point; run 8 reproduced it after geometry changes. Final views use `Interactive.7`.
- `Recommended (verified)` annotations store dimensions, load, supply, TT/27 °C, measured results, date and history.
- ADE variables and annotations were read back. Parameter expressions remain and the final editable views stay open.

![Actual final Maestro metrics and ViVA waveform](/assets/virtuoso/osc-maestro.png "Three passing metrics and the final Interactive.7 waveform. The private title bar is cropped.")

## Continue the same project

> Use $virtuoso-helper to explain how to change these variables and what needs reverification under new conditions.

> Use $virtuoso-testbench to configure the required PVT corners from actual model sections, then $virtuoso-params to report worst-case measurements. Do not mark unrun corners as passing.

> Use $virtuoso-layout to plan devices and supplies, report DRC/LVS/PEX separately, then hand extracted simulation to testbench.

These are follow-up examples, not completed work in this record.

## Was OCEAN faster?

The tested backend launched Spectre through SKILL/ADE and used isolated OCEAN to read results. OCEAN can also run simulations, but a pure-OCEAN backend was not directly benchmarked against ADE here. See [Cadence's discussion of schematic netlisting and OCEAN runs](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/38480/post-layout-simulation-using-ocean-script).
