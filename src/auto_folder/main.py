"""Command-line interface for auto-folder."""

from pathlib import Path

from . import __version__
from .creator import create_structure
from .parser import parse_tree


def _print_banner() -> None:
    print()
    print("AUTO-FOLDER")
    print(f"Version {__version__}")
    print("-" * 42)
    print("Paste your folder structure below.")
    print("Press ENTER on an empty line when finished.")
    print("Press Ctrl+C to cancel.")
    print()


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

    nodes = parse_tree("\n".join(lines))
    if not nodes:
        print("No valid folders or files found.")
        return 1

    root = Path.cwd()
    directories, files = create_structure(nodes, root)

    print("\nCreated:")
    for path in directories:
        print(f"  [DIR ] {path.relative_to(root)}")
    for path in files:
        print(f"  [FILE] {path.relative_to(root)}")

    print(f"\nDone: {len(directories)} folders, {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
