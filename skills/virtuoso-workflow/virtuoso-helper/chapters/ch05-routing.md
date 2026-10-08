# Chapter 5: Routing and Physical Editing

## Core Idea
Routing combines navigator-driven connectivity with manual wire creation. Set gate connections and layers deliberately before routing.

## Hotkeys and Commands
- `Q`: edit instance properties, including Gate Connection.
- `P`: start Create Wire after selecting the correct drawing layer.
- `M`: move devices or routing objects.
- `F`: fit the full layout before selecting another net.
- Navigator → Nets → right-click net → Route with Default Lookup: autoroute a connectivity-aware net.

## Workflow
1. Display Nets in Navigator and inspect XL Status for opens.
2. Select a net such as `INP` to highlight its schematic/layout endpoints.
3. Use `Q` on multi-finger devices to set Gate Connection, e.g. Top.
4. For default routing, right-click the net and choose Route with Default Lookup.
5. For manual routing, choose a layer in Palette, press `P`, and select the source and destination edges.
6. Change wire width or other properties from inside the active command when needed.

## Reference Table
| Situation | Best action |
|---|---|
| Need a connectivity-aware route | Navigator Nets → right-click → Route with Default Lookup |
| Need to configure a device gate | `Q` → select Parameter tab → Gate Connection |
| Need a manual route | Palette layer → `P` → select edges/terminals |
| Need to inspect incomplete nets | Navigator Nets → inspect XL Status opens |
| Need to route a different net | `F` → select next net in Navigator |

## Anti-patterns
- Routing before resolving gate-connection orientation.
- Using the wrong drawing layer for a manual wire.
- Ignoring XL Status after a route; an apparent connection may still contain opens.

## Key Takeaways
1. Navigator is the source of truth for which net needs attention.
2. Configure gate connections before autorouting multi-finger devices.
3. Use default lookup for fast connectivity-aware routes; use `P` for controlled manual routes.
