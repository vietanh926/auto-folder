"""Command-line interface for auto-folder."""

from pathlib import Path

from auto_folder import __version__
from auto_folder.creator import create_structure
from auto_folder.parser import parse_tree
from auto_folder.validator import validate_nodes


def _print_banner() -> None:
    print()
    print("AUTO-FOLDER")
    print(f"Version {__version__}")
    print("-" * 42)
    print("Paste your folder structure below.")
    print("Press ENTER on an empty line when finished.")
    print("Press Ctrl+C to cancel.")
    print()


def _print_preview(nodes) -> None:
    print("\nPreview:")
    for node in nodes:
        indent = "    " * node.level
        icon = "[DIR ]" if node.is_dir else "[FILE]"
        suffix = "/" if node.is_dir else ""
        print(f"{indent}{icon} {node.name}{suffix}")

    directories = sum(node.is_dir for node in nodes)
    files = len(nodes) - directories
    print(f"\n{directories} folders, {files} files")


def _confirm() -> bool:
    while True:
        answer = input("\nCreate this structure? [Y/n]: ").strip().lower()
        if answer in {"", "y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter Y or N.")


def main() -> int:
    _print_banner()
    lines: list[str] = []

    try:
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130

    if not lines:
        print("Cancelled: no structure provided.")
        return 0

    try:
        nodes = parse_tree("\n".join(lines))
        if not nodes:
            print("No valid folders or files found.")
            return 1

        validate_nodes(nodes)
    except ValueError as exc:
        print(f"\nError: {exc}")
        return 1

    _print_preview(nodes)

    try:
        if not _confirm():
            print("Cancelled. Nothing was changed.")
            return 0
    except KeyboardInterrupt:
        print("\nCancelled. Nothing was changed.")
        return 130

    root = Path.cwd()
    try:
        directories, files = create_structure(nodes, root)
    except (OSError, ValueError) as exc:
        print(f"\nError: {exc}")
        return 1

    print("\nCreated:")
    for path in directories:
        print(f"  [DIR ] {path.relative_to(root)}")
    for path in files:
        print(f"  [FILE] {path.relative_to(root)}")

    print(f"\nDone: {len(directories)} folders, {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
