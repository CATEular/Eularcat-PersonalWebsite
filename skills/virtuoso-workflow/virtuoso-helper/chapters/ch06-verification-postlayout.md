# Chapter 6: Verification and Post-Layout

## Core Idea
The full analog flow ends with DRC/LVS, parasitic extraction, configuration, and post-layout simulation; each stage depends on the previous database and connectivity being correct.

## Major Operations
- DRC: check physical-rule compliance.
- LVS: compare layout connectivity against the schematic.
- Quantus DSPF: extract parasitic information for simulation.
- Quantus Smart View: create a post-layout representation.
- Hierarchy Editor Config View: define which schematic/layout/extracted views are used.
- ADE Assembler: run post-layout simulations and compare outputs against pre-layout results.

## Practical Sequence
1. Save the layout after editing.
2. Run DRC and resolve rule markers.
3. Run LVS and resolve shorts, opens, or device mismatches.
4. Generate DSPF or Smart View with Quantus.
5. Create a Config view in the Hierarchy Editor.
6. Launch post-layout simulations in ADE Assembler.
7. Re-evaluate expressions and specifications.

## Anti-patterns
- Treating a clean schematic as evidence that layout connectivity is correct.
- Running post-layout simulation before DRC/LVS issues are understood.
- Comparing pre- and post-layout results without using the same output expressions/specifications.

## Key Takeaways
1. Verification is a gate, not a final screenshot.
2. LVS validates correspondence; Quantus adds parasitic effects; ADE measures their impact.
3. Preserve repeatable expressions and specifications across pre- and post-layout runs.
