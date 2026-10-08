# Chapter 1: Initial Setup

## Core Idea
A usable Virtuoso project begins with a correctly referenced `cds.lib`, a valid PDK, and accessible libraries in the Library Manager.

## Commands & APIs
- `tar -xzvf BAF_RAK.tar.gz` — unpack the RAK database.
- `cd BAF_RAK` — enter the project directory.
- `virtuoso &` — start Virtuoso from an xterm.
- CIW → **Tools > Library Path Editor** — edit library references.
- **Edit > Add Library** — add `gpdk045` and `assura` directories.
- **File > Save As** — save the generated `cds.lib` into the project directory.
- CIW → **Tools > Library Manager** — verify libraries and categories.

## Key Concepts
- **CIW**: Command Interpreter Window, the main Virtuoso control window.
- **cds.lib**: Library definition file mapping logical library names to directories.
- **PDK**: Process Design Kit containing devices, models, constraints, and verification decks.
- **GPDK**: Generic PDK used as a representative process.

## Workflow
1. Unpack and enter `BAF_RAK`.
2. Start Virtuoso.
3. Add the process and verification libraries in Library Path Editor.
4. Save the library definitions into the project directory.
5. Confirm the libraries and device categories in Library Manager.

## Anti-patterns
- Starting design work before verifying the PDK path; forms and simulation models may be incomplete.
- Editing `cds.lib` blindly; inspect the generated definitions first.

## Key Takeaways
1. Keep the project-local `cds.lib` with the design database.
2. Check that the required library, process models, and verification libraries are visible before creating cells.
3. The RAK uses the 45 nm GPDK and assumes the required Cadence tools and licenses are on `PATH`.
