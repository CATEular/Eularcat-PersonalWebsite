# Chapter 3: ADE, Expressions, and Waveforms

## Core Idea
ADE Explorer/Assembler organizes analyses and outputs; ViVA markers and zoom controls turn plotted waveforms into repeatable measurements.

## Key Commands
- Use the green run icon to start simulation.
- Use the Results/Outputs views to evaluate expressions and inspect scalar results.
- ViVA `a`: vertical marker near a time/frequency point.
- ViVA `h`: horizontal marker at a voltage/current level.
- ViVA `b`: second marker for settling or interval measurements.
- ViVA `f`: fit the complete signal again.
- `Ctrl` + scroll wheel: zoom the waveform view.
- `M`: place a marker on an AC curve, such as near 0 dB.

## Workflow
1. Define analyses in ADE.
2. Add outputs or reusable expressions using the Expression Builder.
3. Run the simulation.
4. Use `a`, `h`, and `b` to mark relevant edges, levels, and settling intervals.
5. Use `f` to reset the plot and repeat measurements consistently.
6. Add specifications so passing and failing results are visually distinguishable.

## Concepts
- **Expression Builder**: structured editor for reusable output formulas.
- **Scalar expression**: a single computed value rather than a plotted waveform.
- **Specification**: limit/target attached to an output for pass/fail evaluation.
- **ViVA**: waveform visualization and analysis environment.

## Anti-patterns
- Measuring a waveform without first defining the time/frequency context.
- Leaving old analysis outputs in a reused test when changing the analysis type.
- Relying on a single visual cursor instead of reusable expressions for regression work.

## Key Takeaways
1. Use expressions for measurements that must be repeated or compared.
2. Use markers for exploratory measurement; promote stable measurements into ADE expressions.
3. Reset the view with `f` before comparing signals or taking a second measurement.
