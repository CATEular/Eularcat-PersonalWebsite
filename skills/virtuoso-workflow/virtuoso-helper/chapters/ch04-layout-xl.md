# Chapter 4: Layout XL

## Core Idea
Layout XL maintains schematic/layout connectivity while providing bindkeys for fit, move, align, stretch, and property editing.

## Hotkeys
- `Shift+F`: display all layers / fit the layout.
- `M`: move a device or group.
- `A`: invoke Align and select corresponding edges.
- `N`: change snap mode during Move.
- `S`: stretch a selectable PR Boundary edge.
- `Q`: edit instance properties.
- `F`: zoom out to the full design.
- `Shift+LMB`: select multiple pins or instances.

## Reference Table
| Goal | Sequence |
|---|---|
| Generate layout devices | Connectivity → Generate → All From Source |
| Fit layout | `Shift+F` or `F` depending on desired fit command |
| Move objects | `M` → select object → position; use `N` to change snap mode |
| Align edges | `A` → select first edge → select matching edge |
| Resize boundary | Make PR Boundary selectable → `S` → select edge → drag |
| Edit device properties | `Q` → select parameter/instance → modify → OK |
| Select all pins in a form | `Shift+LMB` across the listed pins |

## Worked Example
To align the capacitor with M2, select the top border of M2 after pressing `A`, then select the top border of the capacitor. Virtuoso aligns the selected edges. For placement, use `M`; if snapping is inconvenient, press `N` while the move command is active.

## Anti-patterns
- Stretching the PR Boundary while it remains non-selectable.
- Moving one member of an abutted group independently when the group must remain matched.
- Assuming `F` and `Shift+F` are interchangeable in every editor/context; verify the active command.

## Key Takeaways
1. Use connectivity-aware selection to correlate schematic and layout objects.
2. Use `M`, `A`, and `S` for the basic geometry loop.
3. Use `N` in-command rather than abandoning a precise move to change snap behavior.
