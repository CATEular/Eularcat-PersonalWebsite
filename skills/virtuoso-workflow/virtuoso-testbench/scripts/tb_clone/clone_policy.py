"""Pure clone input checks, suitable for offline verification."""
import re
from pathlib import PurePosixPath


def design_name(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value) or value in (".", ".."):
        raise ValueError(f"unsupported design name: {value!r}")
    return value


def remote_path(value):
    if not isinstance(value, str) or not re.fullmatch(r"/[A-Za-z0-9_./-]+", value):
        raise ValueError(f"unsupported remote path: {value!r}")
    path = PurePosixPath(value)
    if str(path) == "/" or ".." in path.parts:
        raise ValueError("root and parent traversal are not allowed")
    return path


def reject_overlap(destination, sources):
    dest = remote_path(destination)
    for value in sources:
        src = remote_path(value)
        if dest == src or dest in src.parents or src in dest.parents:
            raise ValueError(f"source and destination overlap: {src} / {dest}")


def reject_collisions(pairs):
    owners = {}
    for lib, cell in pairs:
        design_name(lib)
        design_name(cell)
        if cell in owners and owners[cell] != lib:
            raise ValueError(f"same cell name from different source libraries: {owners[cell]}/{cell} and {lib}/{cell}")
        owners[cell] = lib
