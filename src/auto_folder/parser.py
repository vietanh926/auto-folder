"""Parse common directory-tree text into a list of filesystem nodes."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Node:
    name: str
    level: int
    is_dir: bool


_TREE_MARKERS = ("├──", "└──", "+--", "\\--")


def _clean_name(raw: str) -> str:
    """Remove tree decoration, Markdown formatting, and comments."""
    line = raw.split("#", 1)[0].rstrip()

    marker_pos = None
    marker_len = 0
    for marker in _TREE_MARKERS:
        pos = line.find(marker)
        if pos != -1 and (marker_pos is None or pos < marker_pos):
            marker_pos = pos
            marker_len = len(marker)

    if marker_pos is not None:
        line = line[marker_pos + marker_len :]

    line = line.strip().replace("**", "")
    line = line.replace("`", "")
    line = line.replace("\\_", "_")
    return line.strip()


def _level(raw: str) -> int:
    """Infer depth from the common 4-column tree indentation."""
    line = raw
    marker_positions = [line.find(m) for m in _TREE_MARKERS if line.find(m) != -1]
    if marker_positions:
        prefix = line[: min(marker_positions)]
    else:
        prefix = re.match(r"^[\s│|]*", line).group(0)

    prefix = prefix.replace("│", " ").replace("|", " ").replace("\t", "    ")
    return max(0, len(prefix) // 4)


def parse_tree(text: str) -> list[Node]:
    """Parse tree text. Blank and decoration-only lines are ignored."""
    nodes: list[Node] = []

    for raw in text.splitlines():
        if not raw.strip() or raw.strip() in {"│", "|"}:
            continue

        name = _clean_name(raw)
        if not name:
            continue

        is_dir = name.endswith(("/", "\\"))
        name = name.rstrip("/\\")
        if not name:
            continue

        # Normalize a common Markdown typo copied from formatted text.
        name = name.replace("**init**.py", "__init__.py")
        nodes.append(Node(name=name, level=_level(raw), is_dir=is_dir))

    return nodes
