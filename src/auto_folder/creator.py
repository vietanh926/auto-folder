"""Create filesystem structures from validated parsed tree nodes."""

from pathlib import Path

from .parser import Node
from .validator import resolve_node_path, validate_nodes


def create_structure(nodes: list[Node], root: Path) -> tuple[list[Path], list[Path]]:
    """Validate and create nodes below root without overwriting files."""
    root = root.resolve()
    validate_nodes(nodes)

    directories: list[Path] = []
    files: list[Path] = []
    stack: list[tuple[int, Path]] = []

    for node in nodes:
        while stack and stack[-1][0] >= node.level:
            stack.pop()

        parents = [item[1] for item in stack]
        path = resolve_node_path(root, parents, node)

        if node.is_dir:
            path.mkdir(parents=True, exist_ok=True)
            directories.append(path)
            stack.append((node.level, path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.touch()
            files.append(path)

    return directories, files
