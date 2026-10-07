"""Resolve local user paths without embedding a machine-specific directory."""
import argparse
import json
import os
from pathlib import Path

def load_paths(config=None):
    selected = config or os.environ.get("ANALOG_IC_NOTES_CONFIG")
    if selected:
        config_path = Path(os.path.expandvars(str(selected))).expanduser().resolve()
        data = json.loads(config_path.read_text(encoding="utf-8-sig"))
        base = config_path.parent
    else:
        data, base = {}, Path.cwd()
    values = data.get("paths", {})
    if not isinstance(values, dict):
        raise ValueError("paths must be an object")
    result = {}
    for key, default in {"papers": "./papers", "notes": "./notes", "images": "./notes/assets"}.items():
        value = values.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"paths.{key} must be a nonempty string")
        candidate = Path(os.path.expandvars(value)).expanduser()
        result[key] = (candidate if candidate.is_absolute() else base / candidate).resolve()
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Local JSON configuration file")
    args = parser.parse_args()
    print(json.dumps({key: str(value) for key, value in load_paths(args.config).items()}, ensure_ascii=False, indent=2))
