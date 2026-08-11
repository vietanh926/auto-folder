"""Parse AI/Markdown/ASCII directory trees into filesystem nodes."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Node:
    name: str
    level: int
    is_dir: bool


_BRANCH_MARKERS = ("├──", "└──", "+--", "\\--")
_CODE_FENCE = re.compile(r"^\s*```(?:text|txt|tree|plaintext)?\s*$", re.IGNORECASE)


def _strip_comment(line: str) -> str:
    return re.split(r"\s+#\s*", line, maxsplit=1)[0].rstrip()


def _branch_level(raw: str) -> int | None:
    """Return tree depth for a line containing a branch marker."""
    positions = [raw.find(marker) for marker in _BRANCH_MARKERS if raw.find(marker) >= 0]
    if not positions:
        return None

    marker_pos = min(positions)
    prefix = raw[:marker_pos].replace("│", " ").replace("|", " ")
    prefix = prefix.replace("\t", "    ")
    return prefix.count(" ") // 4 + 1


def _indent_level(raw: str) -> int:
    prefix = re.match(r"^[\s│|]*", raw).group(0)
    prefix = prefix.replace("│", " ").replace("|", " ").replace("\t", "    ")
    return len(prefix) // 4


def _clean_name(raw: str) -> str:
    line = _strip_comment(raw)

    positions = [
        (line.find(marker), marker)
        for marker in _BRANCH_MARKERS
        if line.find(marker) >= 0
    ]
    if positions:
        marker_pos, marker = min(positions, key=lambda item: item[0])
        line = line[marker_pos + len(marker) :]
    else:
        # A plain vertical guide line has no filename.
        line = re.sub(r"^\s*[│|](?:\s*[│|])*\s*$", "", line)

    line = line.strip()

    # Undo common Markdown escaping produced by AI responses.
    line = line.replace("\\_", "_")

    # `**init**.py` -> `init.py`, then normalize the conventional Python
    # package initializer name.
    match = re.fullmatch(r"\*\*(.+?)\*\*(\..+)", line)
    if match:
        line = match.group(1) + match.group(2)

    # Strip simple Markdown code ticks around a filename.
    if len(line) >= 2 and line.startswith("`") and line.endswith("`"):
        line = line[1:-1].strip()

    if line in {"init.py", "init__.py"}:
        line = "__init__.py"

    return line.strip()


def _extract_code_block(text: str) -> str:
    lines = text.splitlines()
    blocks: list[list[str]] = []
    current: list[str] | None = None

    for line in lines:
        if _CODE_FENCE.match(line):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
        elif current is not None:
            current.append(line)

    if not blocks:
        return text

    blocks.sort(
        key=lambda block: sum(
            any(marker in line for marker in _BRANCH_MARKERS) for line in block
        ),
        reverse=True,
    )
    return "\n".join(blocks[0])


def _infer_directories(nodes: list[Node]) -> list[Node]:
    result = list(nodes)
    for index, node in enumerate(result):
        if node.is_dir:
            continue
        if index + 1 < len(result) and result[index + 1].level > node.level:
            result[index] = Node(node.name, node.level, True)
    return result


def parse_tree(text: str) -> list[Node]:
    """Parse common AI-generated project trees into filesystem nodes."""
    text = _extract_code_block(text)
    nodes: list[Node] = []

    for raw in text.splitlines():
        if not raw.strip():
            continue

        stripped = raw.strip()
        if stripped in {"│", "|", "```"}:
            continue

        name = _clean_name(raw)
        if not name:
            continue

        level = _branch_level(raw)
        if level is None:
            level = _indent_level(raw)

        is_dir = name.endswith(("/", "\\"))
        name = name.rstrip("/\\")
        if not name:
            continue

        nodes.append(Node(name=name, level=level, is_dir=is_dir))

    # A pasted tree always starts with its root at level 0. Plain text without
    # a root marker is also normalized relative to its first entry.
    if nodes and nodes[0].level != 0:
        offset = nodes[0].level
        nodes = [Node(n.name, max(0, n.level - offset), n.is_dir) for n in nodes]

    return _infer_directories(nodes)
