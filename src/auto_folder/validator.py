"""Validate parsed nodes before touching the filesystem."""

from pathlib import Path
import re

from .parser import Node

_INVALID_PARTS = {"", ".", ".."}
_WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def _validate_name(name: str) -> None:
    if name in _INVALID_PARTS:
        raise ValueError(f"Invalid path component: {name!r}")

    if "/" in name or "\\" in name:
        raise ValueError(f"Nested path is not allowed inside a node name: {name!r}")

    if any(ord(ch) < 32 for ch in name):
        raise ValueError(f"Control character in path: {name!r}")

    if re.search(r'[<>:"|?*]', name):
        raise ValueError(f"Invalid Windows filename characters: {name!r}")

    if name.endswith((" ", ".")):
        raise ValueError(f"Windows path cannot end with a space or dot: {name!r}")

    stem = name.split(".", 1)[0].upper()
    if stem in _WINDOWS_RESERVED:
        raise ValueError(f"Reserved Windows filename: {name!r}")


def validate_nodes(nodes: list[Node]) -> None:
    """Validate names, levels, and tree structure before filesystem writes."""
    if not nodes:
        raise ValueError("No folders or files were found.")

    if nodes[0].level != 0:
        raise ValueError("The first tree entry must be at level 0.")

    previous_level = -1
    for node in nodes:
        if node.level < 0:
            raise ValueError(f"Invalid tree level: {node.level}")
        if node.level > previous_level + 1:
            raise ValueError(
                f"Invalid tree indentation near {node.name!r}: "
                f"level jumped from {previous_level} to {node.level}."
            )
        _validate_name(node.name)
        previous_level = node.level


def resolve_node_path(root: Path, parents: list[Path], node: Node) -> Path:
    """Resolve a node and guarantee that it remains inside root."""
    parent = parents[-1] if parents else root
    root_resolved = root.resolve()
    candidate = (parent / node.name).resolve()

    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"Path escapes the working directory: {node.name!r}") from exc

    return candidate
