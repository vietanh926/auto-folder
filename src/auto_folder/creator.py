"""Create filesystem structures from parsed tree nodes."""

from pathlib import Path

from .parser import Node


def create_structure(nodes: list[Node], root: Path) -> tuple[list[Path], list[Path]]:
    """Create nodes below root and return (directories, files)."""
    directories: list[Path] = []
    files: list[Path] = []
    stack: list[tuple[int, Path]] = []

    for node in nodes:
        while stack and stack[-1][0] >= node.level:
            stack.pop()

        parent = stack[-1][1] if stack else root
        path = parent / node.name

        if node.is_dir:
            path.mkdir(parents=True, exist_ok=True)
            directories.append(path)
            stack.append((node.level, path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            files.append(path)

    return directories, files
