# Sources and attribution

This suite reorganizes workflow instructions for ChatGPT/Codex into five roles. It includes reusable scripts and selected API references, not the Virtuoso bridge implementation, Cadence software, PDK files or private environment configuration.

- Bridge implementation and original API reference material: [Arcadia-1/virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite). Its MIT copyright and license notice is retained in [LICENSE.bridge](LICENSE.bridge). Install the external bridge separately and verify the installed API; this suite's recorded validation used bridge 0.7.0.
- Isolated OCEAN worker design reference: [lixunqi12/virtuoso-agent](https://github.com/lixunqi12/virtuoso-agent). The AC/OSC measurement scripts in this suite are independently written implementations of this execution pattern. This suite does not install that project's LLM clients.
- `virtuoso-helper` retains summarized guidance attributed by the source skill to Cadence *Basics of Analog Flow: A Design-Oriented Approach — Rapid Adoption Kit*. No original Cadence PDF or licensed design database is distributed. Check your installed Cadence documentation and bindkeys for exact behavior.
- GP proposals use NumPy, SciPy and scikit-learn. They do not run BoTorch or prove a global optimum.

Real OSC/RC measurements shown on the website are selected records from the 2026-10-08 validation. They are specific schematic-level examples. MOS CDF inspection found a width derivation mismatch; layout signoff and hierarchical cloning were not fully verified on the live environment.
