"""Inspect installed bridge APIs locally; no clients, config, SSH or VM calls."""
import argparse
import importlib
import importlib.metadata
import inspect
import json
import sys
from pathlib import Path


TARGETS = {
    "virtuoso_bridge": ["VirtuosoClient.from_env", "VirtuosoClient.execute_skill",
                        "VirtuosoClient.run_shell_command", "VirtuosoClient.fetch",
                        "VirtuosoClient.fetch_one", "VirtuosoClient.upload_file",
                        "VirtuosoClient.download_file", "VirtuosoClient.load_il"],
    "virtuoso_bridge.virtuoso.schematic": ["SchematicOps.create", "SchematicOps.modify",
                                          "SchematicOps.read", "schematic_create_pin"],
    "virtuoso_bridge.virtuoso.schematic.params": ["set_instance_params"],
    "virtuoso_bridge.virtuoso.symbol": ["SymbolOps.generate_from_schematic"],
    "virtuoso_bridge.virtuoso.layout": ["LayoutOps.create", "LayoutOps.modify",
                                       "LayoutOps.export_gds", "layout_create_rect",
                                       "layout_create_path", "layout_create_label",
                                       "layout_create_via_by_name"],
    "virtuoso_bridge.virtuoso.maestro.ops": ["MaestroOps.open_gui_session",
                                            "MaestroOps.set_var", "MaestroOps.save_setup",
                                            "MaestroOps.run_and_wait", "MaestroOps.read_results",
                                            "MaestroOps.export_waveform"],
    "virtuoso_bridge.virtuoso.library": ["LibraryOps.create", "LibraryOps.get",
                                        "LibraryOps.set_technology_library"],
    "virtuoso_bridge.spectre.runner": ["SpectreSimulator.from_env",
                                      "SpectreSimulator.run_simulation"],
}


def probe():
    report = {"python": sys.executable, "python_version": sys.version.split()[0],
              "scope": "local_import_and_signature_only", "connected": False, "apis": {}}
    try:
        report["bridge_version"] = importlib.metadata.version("virtuoso_bridge")
    except importlib.metadata.PackageNotFoundError:
        report["bridge_version"] = None
    for module_name, names in TARGETS.items():
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            report["apis"][module_name] = {"error": f"{type(exc).__name__}: {exc}"}
            continue
        for name in names:
            key = f"{module_name}.{name}"
            try:
                obj = module
                for part in name.split("."):
                    obj = getattr(obj, part)
                report["apis"][key] = {"signature": str(inspect.signature(obj)),
                                      "source": inspect.getsourcefile(obj)}
            except Exception as exc:
                report["apis"][key] = {"error": f"{type(exc).__name__}: {exc}"}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = probe()
    data = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data + "\n", encoding="utf-8")
    else:
        print(data)
    return 1 if any("error" in entry for entry in report["apis"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
