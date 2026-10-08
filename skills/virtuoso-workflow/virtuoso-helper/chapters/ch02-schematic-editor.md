# Chapter 2: Schematic Editor

## Core Idea
Use context-sensitive bindkeys to place devices, wire connectivity, create pins, edit properties, and validate the schematic efficiently.

## Hotkeys
- `i`: open Add Instance; type library/cell fields and place the component.
- `Shift+R`: mirror an instance during placement.
- `Esc`: exit placement or another active command.
- `W`: start wiring. Click a start point, add corners or terminals, and double-click/press Enter to finish in free space.
- `S`: snap to the nearest pin or wire endpoint while wiring.
- `Delete`: remove a net or component.
- `P`: add pins and set name/direction.
- `q`: edit instance/source properties.
- `F3`: reveal an Add Instance form hidden behind another window.
- `Ctrl+A`, then `C`: select and copy the design.

## Reference Table
| Goal | Sequence |
|---|---|
| Place a MOS device | `i` → choose library/cell → Hide → click locations → `Esc` |
| Mirror while placing | `i` → position instance → `Shift+R` → click |
| Wire terminals | `W` → click source → corners/terminal → double-click or `Enter` |
| Snap a wire endpoint | Start `W`, then press `S` near the target |
| Add pins | `P` → name/direction → place pins → `Esc` |
| Edit a parameter | Select object → `q` → change field → OK |
| Validate | Click Check and Save; inspect CIW or schematic markers |

## Mental Models
- Treat `Esc` as the universal “leave the current interactive mode” key.
- Treat `q` as the object-inspection key: select first, then inspect/edit.
- Treat `W` and `P` as connectivity primitives: wires connect internal nodes, pins define external connectivity.

## Anti-patterns
- Leaving a placement or wiring command active before starting another operation.
- Wiring by eye when `S` can snap to the exact pin or endpoint.
- Changing device properties without checking units and calculated parameters.

## Key Takeaways
1. Use `i`, `W`, `P`, and `q` as the core schematic cycle.
2. Use `Shift+R` during placement instead of manually repairing orientation later.
3. Check and save before moving to symbol generation or simulation.
