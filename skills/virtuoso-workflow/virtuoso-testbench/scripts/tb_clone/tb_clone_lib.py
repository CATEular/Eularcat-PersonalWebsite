"""Selected librarian mechanics; see references/cloning.md for scope.

Bridge transport and SKILL errors raise. No lock deletion or shell copying is
implemented here. The checked CLI driver owns all mutations and planning.
Live full-library clone is not validated by the 2026-10-08 capability tests.
"""
import re

_EXTERNAL_EXPLICIT = {"analogLib", "basic", "cdsDefTechLib", "functional", "ahdlLib", "rfLib", "cmos_sch", "US_8ths"}
_EXTERNAL_PATTERNS = [re.compile(pattern, re.I) for pattern in
                      (r"^tsmc", r"^tcbn\d+", r"^smic", r"^gf\d+", r"^tpcn\d+")]

def sk(client, expr, timeout=30):
    result = client.execute_skill(expr, timeout=timeout)
    if not result.ok or result.errors:
        raise RuntimeError(f"SKILL failed: {result.errors}; {result.output}")
    return (result.output or "").strip()

def is_external_lib(name):
    """True if `name` is a PDK / std-cell / IP lib that should NOT be copied."""
    if name in _EXTERNAL_EXPLICIT:
        return True
    return any(p.search(name) for p in _EXTERNAL_PATTERNS)


def scan_hierarchy(client, top_lib, top_cell):
    """Walk schematic instHeaders recursively, return list of (lib, cell).

    Uses `cv~>instHeaders` (declared refs) rather than
    `cv~>instances + inst~>master` (needs master to resolve). A child
    cell's symbol view may fail to open at scan time (Verilog-A
    blocks with broken deps, cells in non-tech libs that the current
    session can't resolve), making `inst~>master` nil — scan would
    then skip the reference entirely and miss the whole subtree.
    instHeaders carry the (libName, cellName, viewName) triple
    regardless of resolvability, so we always see every declared ref.

    Still guards the parent-schematic open behind a view-existence
    probe so leaf cells (PDK primitives, ahdlLib/analogLib sources,
    Verilog-A blocks) don't emit DB-270212 warnings.
    """
    raw = sk(client, f'''
let((visited queue result)
  visited = makeTable('v nil)
  result = nil
  queue = list(list("{top_lib}" "{top_cell}"))
  while(queue
    let((top lib cell key obj cv)
      top = car(queue) queue = cdr(queue)
      lib = car(top) cell = cadr(top)
      key = strcat(lib "/" cell)
      unless(visited[key]
        visited[key] = t
        result = cons(top result)
        obj = ddGetObj(lib cell)
        cv = if(and(obj member("schematic" obj~>views~>name))
                 dbOpenCellViewByType(lib cell "schematic" nil "r")
                 nil)
        when(and(obj member("schematic" obj~>views~>name))
          unless(cv error("Cannot open expected source schematic")))
        when(cv
          foreach(ih cv~>instHeaders
            let((child_key)
              child_key = strcat(ih~>libName "/" ih~>cellName)
              unless(visited[child_key]
                queue = cons(list(ih~>libName ih~>cellName) queue))))
          dbClose(cv)))))
  reverse(result))
''', timeout=60)
    return re.findall(r'\("([^"]+)"\s+"([^"]+)"\)', raw)


def classify_pairs(pairs):
    """Split (lib,cell) list into (project_cells, external_cells)."""
    project, external = [], []
    for lib, cell in pairs:
        (external if is_external_lib(lib) else project).append((lib, cell))
    return project, external


def list_instances(client, lib, cell, view="schematic"):
    """Return [(name, decl_lib, decl_cell, decl_view), ...] for every
    instance in this cellview, based on the `instHeader` declared
    references rather than the resolved `inst~>master`.

    Why instHeaders not instances+master: if a child cell lacks the
    declared view (e.g. Verilog-A block with only a `veriloga` +
    `symbol` view but declared from its parent as `symbol`), Cadence
    can still fail to populate `inst~>master` — it returns nil.
    `foreach(inst cv~>instances when(inst~>master ...))` then drops
    those insts, and `stale_instances` never sees them, so rebind
    silently skips perfectly-valid refs that only get detected in
    the post-rebind verify pass. Declaring through `instHeaders` sees
    every inst regardless of master resolvability.

    Records are separated by `;;` rather than `\\n`: the bridge's
    response serializer is inconsistent about newline handling —
    sometimes emits literal backslash-n, sometimes a single space.
    `;;` survives both.
    """
    raw = sk(client, f'''
let((obj cv out)
  obj = ddGetObj("{lib}" "{cell}")
  cv = if(and(obj member("{view}" obj~>views~>name))
           dbOpenCellViewByType("{lib}" "{cell}" "{view}" nil "r")
           nil)
  out="" when(cv
    foreach(ih cv~>instHeaders
      foreach(inst ih~>instances
        out=strcat(out sprintf(nil "%s|%s|%s|%s;;"
                               inst~>name ih~>libName
                               ih~>cellName ih~>viewName))))
    dbClose(cv)) out)
''', timeout=60)
    result = []
    for ln in raw.strip('"').split(";;"):
        parts = ln.strip().split("|")
        if len(parts) == 4:
            result.append(tuple(parts))
    return result


def stale_instances(client, lib, cell, project_libs, view="schematic"):
    """Instances whose master libName is in project_libs."""
    return [i for i in list_instances(client, lib, cell, view)
            if i[1] in project_libs]


def sync_props_batch(client, pairs, dst_lib, project_libs):
    """Sync inst-level props src->dst for ALL cells in one SKILL round trip,
    and `schCheck + dbSave` every touched dst cellview.

    Replaces per-cell loop of sync_props_src_to_dst. For each src inst
    whose master lib is in project_libs, capture (name valueType value)
    tuples and replay via dbReplaceProp on the dst inst with the same
    name. Returns total insts touched.

    **Why schCheck is inside this batch**: after rebind flips inst
    masters and sync rewrites props, the cell's `extracted` view is
    stale. Maestro / the netlister uses extracted, so sim fails with
    "check and save" errors until the user hand-clicks Check&Save in
    Virtuoso for every touched cell. `schCheck(dst_cv)` regenerates
    extracted from the now-correct schematic. We do it here (not in a
    separate pass) because we're already open in "a" mode and saving
    — free ride. Cost: schCheck recursively opens every child
    schematic for hierarchy validation; leaf cells without schematic
    (PDK primitives, Verilog-A blocks, analogLib sources) each emit a
    DB-270212 warning. Log noise is the tradeoff for avoiding manual
    UI clicks before every sim.
    """
    proj_skill = " ".join(f'"{lib}"' for lib in project_libs)
    jobs_skill = " ".join(
        f'list("{sl}" "{cell}")' for sl, cell in pairs)
    return sk(client, f'''
let((proj jobs total)
  proj = makeTable('v nil)
  foreach(lib list({proj_skill}) proj[lib] = t)
  jobs = list({jobs_skill})
  total = 0
  foreach(job jobs
    let((src_lib cell src_cv dst_cv tbl)
      src_lib = nth(0 job) cell = nth(1 job)
      src_cv = dbOpenCellViewByType(src_lib cell "schematic" nil "r")
      dst_cv = dbOpenCellViewByType("{dst_lib}" cell "schematic" nil "a")
      unless(and(src_cv dst_cv) error("Cannot open expected source/destination schematic"))
      when(and(src_cv dst_cv)
        tbl = makeTable('v nil)
        foreach(ih src_cv~>instHeaders
          when(proj[ih~>libName]
            foreach(inst ih~>instances
              tbl[inst~>name] = foreach(mapcan p inst~>prop
                when(and(p~>name p~>valueType)
                  list(list(p~>name p~>valueType p~>value)))))))
        foreach(inst dst_cv~>instances
          let((props)
            props = tbl[inst~>name]
            when(props
              foreach(p props
                dbReplaceProp(inst nth(0 p) nth(1 p) nth(2 p)))
              total = total + 1)))
        schCheck(dst_cv)
        dbSave(dst_cv))
      when(src_cv dbClose(src_cv))
      when(dst_cv dbClose(dst_cv))))
  sprintf(nil "%d" total))
''', timeout=300).strip('"')


def verify_no_stale_batch(client, dst_lib, parents, project_libs):
    """For every parent cell, report any instHeader still pointing at a
    project lib. One SKILL round trip for the whole parent list.
    Returns {parent: [(libName, cellName, viewName, count), ...]}.
    """
    proj_skill = " ".join(f'"{lib}"' for lib in project_libs)
    parents_skill = " ".join(f'"{p}"' for p in parents)
    raw = sk(client, f'''
let((proj out)
  proj = makeTable('v nil)
  foreach(lib list({proj_skill}) proj[lib] = t)
  out = ""
  foreach(parent list({parents_skill})
    let((cv)
      cv = dbOpenCellViewByType("{dst_lib}" parent "schematic" nil "r")
      unless(cv error("Cannot open copied schematic for verification"))
      when(cv
        foreach(ih cv~>instHeaders
          when(proj[ih~>libName]
            out = strcat(out sprintf(nil "%s|%s|%s|%s|%d;;"
              parent ih~>libName ih~>cellName ih~>viewName length(ih~>instances)))))
        dbClose(cv))))
  out)
''', timeout=120).strip('"')
    result = {p: [] for p in parents}
    for rec in raw.split(";;"):
        rec = rec.strip()
        if rec.count("|") != 4:
            continue
        parent, lib, cell, view, cnt = rec.split("|")
        result[parent].append((lib, cell, view, int(cnt)))
    return result


def rebind_all_in_cell(client, parent_lib, parent_cell, project_libs,
                       dst_lib=None):
    """Batch delete+recreate every stale instance in one SKILL round trip.

    Previously rebind_instance was called per stale inst — one open,
    delete, create, save, close cycle per call. For a cell with 34
    stale insts that's 34 round trips at ~400ms each = ~13s for one
    parent. Batching opens the parent cv once, does all N rebinds
    inside a single `foreach`, and saves+closes once.

    SKILL.md #6 warned against foreach+dbDelete+dbCreate batching
    due to silent crashes — but that specifically concerned deeply
    nested `let/when/if/return`. The form below is flat `let + when`
    only, no `return`, no nested `if`, and has been validated to
    produce identical rebind results to the per-inst path.
    """
    if dst_lib is None:
        dst_lib = parent_lib
    stale = stale_instances(client, parent_lib, parent_cell, project_libs)
    if not stale:
        return 0, 0
    jobs_skill = " ".join(
        f'list("{iname}" "{dst_lib}" "{dut_cell}" "{view}")'
        for iname, _old, dut_cell, view in stale)
    out = sk(client, f'''
let((cv jobs n_ok n_fail)
  n_ok = 0  n_fail = 0
  cv = dbOpenCellViewByType("{parent_lib}" "{parent_cell}" "schematic" nil "a")
  unless(cv error("Cannot open copied schematic for rebind"))
  when(cv
    jobs = list({jobs_skill})
    foreach(job jobs
      let((iname dst_lib dut_cell view inst xy orient nm)
        iname = nth(0 job)  dst_lib = nth(1 job)
        dut_cell = nth(2 job)  view = nth(3 job)
        inst = car(setof(x cv~>instances equal(x~>name iname)))
        when(null(inst) n_fail = n_fail + 1)
        when(inst
          xy = inst~>xy
          orient = inst~>orient
          nm = dbOpenCellViewByType(dst_lib dut_cell view nil "r")
          when(null(nm) n_fail = n_fail + 1)
          when(nm
            dbDeleteObject(inst)
            if(dbCreateInst(cv nm iname xy orient) then
              n_ok = n_ok + 1
            else
              n_fail = n_fail + 1)
            dbClose(nm)))))
    dbSave(cv)
    dbClose(cv))
  sprintf(nil "%d|%d" n_ok n_fail))
''', timeout=120).strip('"')
    try:
        ok, fail = out.split("|")
        return int(ok), int(fail)
    except (ValueError, AttributeError):
        return 0, len(stale)
