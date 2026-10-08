---
title: "RC: a first simulation and measurement exercise"
description: Continuous RC wiring, ADE AC, isolated OCEAN bandwidth readback and independent validation
---

## A simple but complete measurement chain

This RC case verified connection, continuous schematic wiring, ADE AC, exact-history readback, parameter changes and an independent rerun. Bandwidth changed from **79.389 MHz to 158.782 MHz**, with matching validation. Date: 2026-10-08.

It used the legacy small discrete search, **not adaptive agent/GP optimization**. The later [OSC case](../osc/) exercised that hybrid loop.

## Conversation 1: create a readable testbench

**Demonstration input**

> Use $virtuoso-connect to verify transport, then $virtuoso-testbench to create an RC low-pass at R = 2 kΩ, C = 1 pF and unit AC input. Use continuous actual wires rather than named stubs.

The agent reads analogLib device terminals, connects the input through R to OUT and C from OUT to ground, and Check & Saves. Readback verifies the R output/C top share OUT and the capacitor bottom is grounded.

![Actual continuously wired RC testbench](/assets/virtuoso/rc-schematic.png "Real schematic screenshot, cropped to remove the private title bar and library identifiers.")

This drawing was created through the interface, then simulated to check the electrical circuit behind the picture.

## Conversation 2: measure the baseline

**Demonstration input**

> Configure AC, measure OUT's 3 dB bandwidth from this history, and check its scale against the analytical formula.

**Response adapted from actual measurements**

> At 2 kΩ and 1 pF, OCEAN measures 79.389321 MHz. The ideal pole is approximately 79.577 MHz, a difference of about 0.24%; discrete frequency sampling and threshold crossing affect the numerical measurement.

$$H(j\omega)=\frac{1}{1+j\omega RC},\qquad f_{3\mathrm{dB}}=\frac{1}{2\pi RC}$$

The reader selects the exact history's AC point and finds the 3 dB drop relative to its low-frequency passband. Unit AC input allows OUT to represent the transfer response; other setups need an explicit input/output ratio.

## Conversation 3: change one parameter and rerun

**Demonstration input**

> Keep C fixed, change R to 1 kΩ and save/run again. Independently rerun that candidate rather than reading the same old data twice.

| Phase | R | C | Measured bandwidth | Ideal bandwidth | Result ID |
|---|---|---|---|---|---|
| Baseline | 2 kΩ | 1 pF | 79.389321 MHz | 79.577 MHz | Interactive.6 / AC |
| Candidate | 1 kΩ | 1 pF | 158.781749 MHz | 159.155 MHz | Interactive.7 / AC |
| Independent validation | 1 kΩ | 1 pF | 158.781749 MHz | 159.155 MHz | Interactive.8 / AC |

Halving R doubles the ideal bandwidth, consistent with the measured change. This proves the toy measurement chain works, not that a complex analog design or multi-corner optimum has been verified.

This exercise restored the 2 kΩ baseline and original startup directory afterward. The later OSC workflow followed the updated delivery preference: retain selected values and final views. Specify whether a new task is exploratory or should apply recommendations.

## Try the new sequential params interface

The following is an **unexecuted usage example**, not a rewriting of the historical RC search:

> Use $virtuoso-params to reproduce a baseline and choose the next R from measured bandwidth, keeping C fixed. Explain each change, run one point at a time, and reserve the last of three evaluations for independent validation.

> If the second point meets the goal, validate and retain it. Otherwise explain the remaining budget and the next proposed value.

Helper can explain AC amplitude, 3 dB, sample spacing and history without starting a new project.

## Keep reproducible outputs

Retain the editable schematic, AC setup, exact history/test/corner/point, OCEAN JSON, measurement definition and validation. A screenshot supports visual review but does not replace data. Private project logs and Cadence databases are not distributed with this public case.
