"""Plan a schematic-hierarchy clone; --execute writes a fresh destination."""
import argparse
import json
import re
import shlex
import tempfile
import uuid
from pathlib import Path
from clone_policy import design_name, remote_path, reject_collisions, reject_overlap


class CheckedClient:
    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):
        attr = getattr(self.client, name)
        if name not in ("execute_skill", "run_shell_command", "upload_file", "download_file"):
            return attr
        def call(*args, **kwargs):
            result = attr(*args, **kwargs)
            if not result.ok or result.errors:
                raise RuntimeError(f"{name} failed: {result.errors}; {result.output}")
            return result
        return call


def remote_text(client, command):
    remote = f"/tmp/vw_clone_probe_{uuid.uuid4().hex}.txt"
    with tempfile.TemporaryDirectory(prefix="vw_clone_") as directory:
        local = Path(directory) / "probe.txt"
        script = "set -e; " + command + " > " + shlex.quote(remote)
        client.run_shell_command("bash -c " + shlex.quote(script))
        client.download_file(remote, local)
        return local.read_text(encoding="utf-8").strip()


def lib_path(client, lib):
    raw = client.execute_skill(f'ddGetObj("{design_name(lib)}")~>readPath').output.strip().strip('"')
    remote_path(raw)
    canonical = remote_text(client, "readlink -f -- " + shlex.quote(raw))
    return str(remote_path(canonical))


def make_plan(client, src_lib, src_cell, dst_lib, helpers):
    for value in (src_lib, src_cell, dst_lib):
        design_name(value)
    if src_lib == dst_lib or helpers.is_external_lib(dst_lib):
        raise ValueError("destination must differ from source and must not be external/PDK")
    if client.execute_skill(f'ddGetObj("{src_lib}" "{src_cell}")').output.strip() == "nil":
        raise ValueError("source cell is missing")
    pairs = helpers.scan_hierarchy(client, src_lib, src_cell)
    if (src_lib, src_cell) not in pairs:
        raise ValueError("hierarchy scan did not return the root")
    project, external = helpers.classify_pairs(pairs)
    if not project:
        raise ValueError("no project-owned cells")
    reject_collisions(project)
    paths = {lib: lib_path(client, lib) for lib in sorted({p[0] for p in project} | {dst_lib})}
    reject_overlap(paths[dst_lib], [paths[lib] for lib in paths if lib != dst_lib])
    for lib, cell in project:
        if client.execute_skill(f'ddGetObj("{lib}" "{cell}")').output.strip() == "nil":
            raise ValueError(f"unresolved dependency: {lib}/{cell}")
    blocked = remote_text(client, f"find {shlex.quote(paths[dst_lib])} -mindepth 1 \\( -type d -o -type l -o -name '*.cdslck*' \\) -print")
    if blocked:
        raise ValueError("destination is not an empty unlocked library: " + blocked)
    return {"source": [src_lib, src_cell], "destination": dst_lib,
            "project": project, "external": external, "paths": paths,
            "scope": "schematic-declared hierarchy; config-only and file dependencies require review",
            "excluded": ["*.cdslck*", "*%", "calibre_*", "av_extracted", "av_netlist", "starrc_*", "TB results and run snapshots"]}


def copy_cells(client, plan):
    lines = ["#!/bin/bash", "set -euo pipefail"]
    exclusions = ["*.cdslck*", "*%", "calibre_*", "av_extracted", "av_netlist", "starrc_*"]
    for lib, cell in plan["project"]:
        source = plan["paths"][lib] + "/" + cell
        destination = plan["paths"][plan["destination"]] + "/" + cell
        options = list(exclusions)
        if (lib, cell) == tuple(plan["source"]):
            options += ["results/", "Interactive.*.state", "ExplorerRun.*.state", "GlobalOpt.*.state", "MonteCarlo.*.state"]
        lines.append("mkdir -- " + shlex.quote(destination))
        args = " ".join("--exclude=" + shlex.quote(pattern) for pattern in options)
        lines.append(f"rsync -aL {args} -- {shlex.quote(source + '/')} {shlex.quote(destination + '/')}")
        lines.append("chmod -R u+w -- " + shlex.quote(destination))
    remote = f"/tmp/vw_clone_copy_{uuid.uuid4().hex}.sh"
    with tempfile.TemporaryDirectory(prefix="vw_clone_") as directory:
        local = Path(directory) / "copy.sh"
        local.write_text("\n".join(lines) + "\n", encoding="utf-8")
        client.upload_file(local, remote)
        client.run_shell_command("bash " + shlex.quote(remote), timeout=300)


def patch_bindings(client, plan):
    dst = plan["destination"]
    base = plan["paths"][dst] + "/" + plan["source"][1]
    config_exprs, maestro_exprs = [], []
    for lib in sorted({lib for lib, _ in plan["project"]}):
        pattern = re.escape(lib)
        config_exprs += [f"s#design {pattern}\\.#design {dst}.#g", f"s#cell {pattern}\\.#cell {dst}.#g"]
        maestro_exprs += [f"s#<value>{pattern}</value>#<value>{dst}</value>#g", f's#"{pattern}"#"{dst}"#g']
    config_args = " ".join("-e " + shlex.quote(expr) for expr in config_exprs)
    maestro_args = " ".join("-e " + shlex.quote(expr) for expr in maestro_exprs)
    cfg, maestro = base + "/config/expand.cfg", base + "/maestro"
    script = ("set -e\n" + f"if [ -f {shlex.quote(cfg)} ]; then sed -i {config_args} -- {shlex.quote(cfg)}; fi\n" +
              f"for state in {shlex.quote(maestro)}/maestro.sdb {shlex.quote(maestro)}/active.state {shlex.quote(maestro)}/test_states/*.state; do\n" +
              f'  if [ -f "$state" ]; then sed -i {maestro_args} -- "$state"; fi\n' + "done\n")
    client.run_shell_command("bash -c " + shlex.quote(script))


def execute_plan(client, plan, helpers):
    copy_cells(client, plan)
    patch_bindings(client, plan)
    dst = plan["destination"]
    libs = sorted({lib for lib, _ in plan["project"]})
    schematic_pairs = []
    for lib, cell in plan["project"]:
        if client.execute_skill(f'ddGetObj("{lib}" "{cell}" "schematic")').output.strip() != "nil":
            schematic_pairs.append((lib, cell))
            if client.execute_skill(f'ddGetObj("{dst}" "{cell}" "schematic")').output.strip() == "nil":
                raise RuntimeError(f"copied schematic missing: {cell}")
            _, failed = helpers.rebind_all_in_cell(client, dst, cell, libs)
            if failed:
                raise RuntimeError(f"rebind failed in {cell}; retain destination for diagnosis")
    helpers.sync_props_batch(client, schematic_pairs, dst, libs)
    stale = helpers.verify_no_stale_batch(client, dst, [cell for _, cell in schematic_pairs], libs)
    if any(stale.values()):
        raise RuntimeError("stale source references: " + repr(stale))
    return {"structural_clone_checked": True, "simulation_equivalence_verified": False, "stale": stale}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src_lib")
    parser.add_argument("src_cell")
    parser.add_argument("dst_lib")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--external-lib", action="append", default=[])
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    from virtuoso_bridge import VirtuosoClient
    import tb_clone_lib as helpers
    for lib in args.external_lib:
        helpers._EXTERNAL_EXPLICIT.add(design_name(lib))
    client = CheckedClient(VirtuosoClient.from_env())
    plan = make_plan(client, args.src_lib, args.src_cell, args.dst_lib, helpers)
    report = {"plan": plan, "executed": False}
    if args.execute:
        plan = make_plan(client, args.src_lib, args.src_cell, args.dst_lib, helpers)
        report["result"] = execute_plan(client, plan, helpers)
        report["executed"] = True
    text = json.dumps(report, ensure_ascii=True, indent=2)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
