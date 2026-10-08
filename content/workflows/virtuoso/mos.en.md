---
title: "MOS: drawing a device is only the first check"
description: Actual MOS wiring, body/source connectivity, CDF readback and an unresolved width derivation mismatch
---

## What this record verifies

A real MOS schematic and device readback exist: G connects to IN, D to OUT, B and S to VSS. The record checks CDF edits, unit presentation and body connectivity; it **does not include standalone DC/AC/transient performance curves for this device**. Date: 2026-10-08.

The [OSC's 10 MOS devices](../osc/) did participate in transient simulation, but that cannot validate this separate multi-finger device's dimensions or current curves.

![Actual MOS schematic with G/IN, D/OUT and B/S/VSS](/assets/virtuoso/mos-schematic.png "Cropped/redacted screenshot preserving terminals, wiring and parameter values.")

## Conversation 1: create and read back

**Demonstration input**

> Use $virtuoso-testbench to place a real NMOS from my PDK in the designated library. Wire G to IN, D to OUT and B/S to VSS. Read back actual CDF and connectivity and report whether dimensions agree.

Connect verifies transport. Testbench queries real terminals and CDF rather than guessing coordinates from a screenshot, then Check & Saves and reads terminal nets:

| Terminal | Readback net |
|---|---|
| G | IN |
| D | OUT |
| B | VSS |
| S | VSS |

Body/source connectivity passed. The checked environment supported direct body wiring and a helper entry; historical claims of permanent API unavailability should not be treated as universal.

## Conversation 2: successful writes do not prove electrical size

**Demonstration input**

> Change W/L and fingers, but inspect derived CDF fields and the generated simulation netlist rather than reporting only that the write succeeded.

| Field | Actual readback |
|---|---|
| l | 180.0n |
| w | 4u |
| wf | 8u |
| fingers | 2 |
| m | 1 |
| simM | 2 |

The `w`/`wf` derivation is inconsistent in this record, so effective width is not verified. PDK definitions of total width, finger width, finger count and simulation multiplicity differ. Inspect this device's callbacks and netlisting behavior. A writable field or a visible value is insufficient electrical evidence.

**Appropriate response example**

> Wiring and field readback are complete, but effective width still needs checking. I will inspect the actual CDF definitions, trigger legal callbacks and compare the new netlist's w/l/m before labeling dimensions verified.

That is a handling example; the multi-finger mismatch was not marked resolved in this record.

## Why the OSC example is different

The OSC uses one finger and m = 1 with widths parameterized by wn/wp. Generated Spectre dimensions for all 10 MOS devices, length and load ICs were checked, and transient measurements were independently repeated.

That verifies this single-finger example, not other multiplicities or PDKs. Params should rely on testbench size/netlist verification before interpreting measured changes.

## Extend this to a MOS simulation project

These are **future, unexecuted prompts**:

> Resolve and verify the dimension mapping first. Use $virtuoso-testbench to create VGS/VDS sources, define body bias and run IDS–VGS and IDS–VDS sweeps. Save current and operating points, bind curves to the exact history and report actual netlist dimensions.

> Use $virtuoso-helper to explain cutoff, linear and saturation regions based on actual model and operating-point evidence.

> Once measurements are trustworthy, use $virtuoso-params to tune within legal voltage and dimension ranges, stating current, transconductance or power goals and independently validating the selection.

This case demonstrates “readback exposes a problem → state the evidence limit → ask for the next verification step.” Add performance curves only after they actually exist.
