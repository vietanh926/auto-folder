"""Parse AI/Markdown/ASCII directory trees into filesystem nodes."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Node:
    name: str
    level: int
    is_dir: bool


_TREE_MARKERS = ("├──", "└──", "+--", "\\--")
_CODE_FENCE = re.compile(r"^\s*```(?:text|txt|tree|plaintext)?\s*$", re.IGNORECASE)


def _strip_comment(line: str) -> str:
    return re.split(r"\s+#\s*", line, maxsplit=1)[0].rstrip()


def _clean_name(raw: str) -> str:
    line = _strip_comment(raw)

    marker_pos = None
    marker_len = 0
    for marker in _TREE_MARKERS:
        pos = line.find(marker)
        if pos != -1 and (marker_pos is None or pos < marker_pos):
            marker_pos = pos
            marker_len = len(marker)

    if marker_pos is not None:
        line = line[marker_pos + marker_len :]
    else:
        line = re.sub(r"^\s*[│|](?:\s*[│|])*\s*", "", line)

    line = line.strip().replace("`", "").replace("\\_", "_")

    # AI commonly uses Markdown bold around filenames. Preserve the extension.
    match = re.fullmatch(r"\*\*(.+?)\*\*(\..+)", line)
    if match:
        stem, extension = match.groups()
        line = stem + extension

    # Some AI output renders __init__.py as **init**.py.
    if line == "init.py" or line == "init__.py":
        line = "__init__.py"

    return line.strip()


def _level(raw: str) -> int:
    """Infer depth from tree guides or plain indentation."""
    marker_positions = [raw.find(m) for m in _TREE_MARKERS if raw.find(m) != -1]
    if marker_positions:
        prefix = raw[: min(marker_positions)]
        prefix = prefix.replace("│", " ").replace("|", " ").replace("\t", "    ")
        # A branch marker itself represents one tree level.
        return len(prefix) // 4 + 1

    prefix = re.match(r"^[\s│|]*", raw).group(0)
    prefix = prefix.replace("│", " ").replace("|", " ").replace("\t", "    ")
    return len(prefix) // 4


def _is_probable_tree_line(line: str) -> bool:
    stripped = line.strip()
    return bool(
        stripped
        and (
            any(marker in line for marker in _TREE_MARKERS)
            or stripped.endswith(("/", "\\"))
            or not stripped.startswith(("Here ", "This ", "You ", "The "))
        )
    )


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
        key=lambda block: sum(any(marker in line for marker in _TREE_MARKERS) for line in block),
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
    """Parse common AI-generated project trees into nodes."""
    text = _extract_code_block(text)
    nodes: list[Node] = []

    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped in {"│", "|", "```"}:
            continue

        name = _clean_name(raw)
        if not name:
            continue

        is_dir = name.endswith(("/", "\\"))
        name = name.rstrip("/\\")
        if not name or not _is_probable_tree_line(raw):
            continue

        nodes.append(Node(name=name, level=_level(raw), is_dir=is_dir))

    # Root entries are represented at level 0; tree branches are one level below.
    for index, node in enumerate(nodes):
        if index == 0 and node.level > 0:
            nodes[index] = Node(node.name, 0, node.is_dir)

    return _infer_directories(nodes)
