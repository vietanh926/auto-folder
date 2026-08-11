from pathlib import Path

from auto_folder.creator import create_structure
from auto_folder.parser import parse_tree


def test_create_structure(tmp_path: Path):
    nodes = parse_tree(
        """project/\n├── app/\n│   ├── main.py\n│   └── config.py\n└── README.md\n"""
    )

    directories, files = create_structure(nodes, tmp_path)

    assert (tmp_path / "project").is_dir()
    assert (tmp_path / "project" / "app").is_dir()
    assert (tmp_path / "project" / "app" / "main.py").is_file()
    assert (tmp_path / "project" / "app" / "config.py").is_file()
    assert (tmp_path / "project" / "README.md").is_file()
    assert len(directories) == 2
    assert len(files) == 3


def test_existing_files_are_not_overwritten(tmp_path: Path):
    existing = tmp_path / "project" / "main.py"
    existing.parent.mkdir(parents=True)
    existing.write_text("keep me", encoding="utf-8")

    nodes = parse_tree("project/\n└── main.py\n")
    create_structure(nodes, tmp_path)

    assert existing.read_text(encoding="utf-8") == "keep me"
