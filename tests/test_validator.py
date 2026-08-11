from pathlib import Path

import pytest

from auto_folder.parser import parse_tree
from auto_folder.validator import resolve_node_path, validate_nodes


def test_reject_parent_traversal():
    nodes = parse_tree("project/\n└── ../outside/\n")
    with pytest.raises(ValueError):
        validate_nodes(nodes)


def test_reject_nested_path_in_name():
    nodes = parse_tree("project/\n└── app/config.py\n")
    with pytest.raises(ValueError):
        validate_nodes(nodes)


def test_reject_windows_invalid_characters():
    nodes = parse_tree("project/\n└── bad:file.txt\n")
    with pytest.raises(ValueError):
        validate_nodes(nodes)


def test_reject_reserved_windows_names():
    nodes = parse_tree("project/\n└── CON\n")
    with pytest.raises(ValueError):
        validate_nodes(nodes)


def test_reject_invalid_tree_jump():
    nodes = parse_tree("project/\n        main.py\n")
    with pytest.raises(ValueError):
        validate_nodes(nodes)


def test_resolve_node_stays_inside_root(tmp_path: Path):
    root = tmp_path.resolve()
    node = parse_tree("project/\n└── main.py\n")[1]
    path = resolve_node_path(root, [root / "project"], node)
    assert path == root / "project" / "main.py"
