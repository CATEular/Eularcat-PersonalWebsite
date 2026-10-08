# Virtuoso Hotkey Cheatsheet

## Choose by intent

| If you need to… | Use |
|---|---|
| Place a component | `i` |
| Edit selected object | `q` |
| Reveal a hidden form | `F3` |
| Wire a schematic | `W` → `S` for snapping → `Esc` |
| Add a schematic pin | `P` → set direction/name → `Esc` |
| Remove an object | `Delete` |
| Mirror during placement | `Shift+R` |
| Select/copy a whole schematic | `Ctrl+A` → `C` |
| Move layout geometry | `M` → `N` if snap mode needs changing |
| Align layout edges | `A` |
| Resize PR Boundary | Make selectable → `S` |
| Route a selected net automatically | Navigator Nets → right-click → Route with Default Lookup |
| Route manually in layout | Select Palette layer → `P` |
| Fit layout | `F` or `Shift+F` according to context |
| Measure waveform time/frequency | `a` |
| Measure waveform level | `h` |
| Mark settling interval | `b` |
| Restore full waveform | `f` |

## Decision rules

- **Form missing?** Press `F3` before reopening or abandoning the operation.
- **Command not responding?** Press `Esc` once or twice, confirm the active editor, then retry.
- **Wire endpoint imprecise?** In schematic use `S`; in layout verify the drawing layer and use `P`.
- **Layout move feels wrong?** Press `N` during `M` to change snap mode.
- **Boundary cannot be resized?** Make PR Boundary selectable, then use `S`.
- **Net still open after routing?** Check Navigator’s XL Status; do not trust visual contact alone.
- **Measurement will be reused?** Convert exploratory markers into an ADE expression and specification.

## Context warning

The RAK’s keys are defaults, not universal guarantees. Local `.cdsinit`, PDK, site bindkeys, and release-specific contexts may override these mappings.
