# Patterns

## Context-first hotkey lookup
**When to use**: A key behaves differently across schematic, layout, and ViVA.
**How**: Identify the active editor, whether a command is active, and the selected object; then apply the matching chapter entry.
**Trade-offs**: Slower than memorizing one global map, but avoids destructive context errors.

## Inspect → edit → validate
**When to use**: Changing a device, source, gate connection, or boundary.
**How**: Select the object → press `q` → edit the relevant property → accept → run the appropriate check or inspect status.
**Trade-offs**: Adds a validation step but prevents hidden parameter/connectivity mistakes.

## Wire with a precision escape hatch
**When to use**: Schematic or manual layout routing.
**How**: Start `W`/`P`, click the source, use `S` for schematic endpoint snapping or choose the intended layout layer, then complete the route and press `Esc`.
**Trade-offs**: Manual routing gives control; default lookup is faster for connectivity-aware nets.

## Fit before changing focus
**When to use**: Moving from one net/object to another in a crowded layout or waveform.
**How**: Press `F`/`Shift+F` as appropriate, select the next object/net, then zoom in only as needed.
**Trade-offs**: Reduces lost selections and improves repeatability, at the cost of a view reset.

## Promote measurements to expressions
**When to use**: A ViVA measurement will be repeated across corners, parameter sweeps, or pre/post-layout runs.
**How**: Explore with markers (`a`, `h`, `b`, `M`), then encode the measurement in ADE Expression Builder and attach a specification.
**Trade-offs**: Requires setup time but supports regression and pass/fail comparison.
