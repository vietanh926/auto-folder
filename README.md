# Auto-Folder

**Turn AI-generated project structures into real folders and files in seconds.**

Auto-Folder is a lightweight, cross-platform command-line tool for developers who frequently copy project architectures from AI assistants, documentation, or technical designs.

Instead of manually creating dozens of directories and empty files, run `auto-folder`, paste the structure, review a preview, and Auto-Folder builds the project skeleton in the current directory.

## Why Auto-Folder?

AI coding assistants are great at designing project structures, but turning this:

```text
order-sync/
├── app/
│   ├── config.py
│   ├── database.py
│   └── services/
│       └── sync_service.py
├── tests/
│   └── test_sync.py
├── requirements.txt
└── main.py
```

into actual folders and files is still repetitive manual work.

Auto-Folder is designed to make that workflow nearly instant:

```text
auto-folder
        ↓
paste the structure
        ↓
press Enter on an empty line
        ↓
review the preview
        ↓
confirm
        ↓
project skeleton created
```

## Design goals

- **Simple:** one command and paste.
- **Fast:** no manual folder/file creation.
- **Lightweight:** the end-user package contains only what is required to run Auto-Folder.
- **AI-friendly:** handle common tree formats produced by AI assistants and Markdown.
- **Safe:** preview before creation, never overwrite existing files by default, and reject unsafe paths.
- **Portable:** run without requiring Python, pip, or development tools after installation.
- **Cross-platform:** designed to support Windows, Linux, and macOS from the same core codebase.

## Supported input

Auto-Folder supports common structures such as:

- Unicode trees using `├──`, `└──`, and `│`.
- ASCII trees using `+--`, `\\--`, and `|`.
- Folder names with or without a trailing `/` when the structure provides enough context.
- Files without extensions such as `Dockerfile`, `Makefile`, and `LICENSE`.
- Hidden files such as `.env`, `.gitignore`, and `.dockerignore`.
- Comments after entries, such as `config.py # environment configuration`.
- Common Markdown artifacts such as escaped underscores and formatting around names.
- Nested folders and files.
- Empty folders explicitly represented in the tree.
- Markdown code blocks containing the directory tree.

## Example

Run from the directory where the project should be created:

```text
auto-folder
```

Then paste:

```text
order-sync/
│
├── app/
│   ├── __init__.py
│   ├── config.py                 # Environment configuration
│   ├── database.py               # Database connection
│   └── api/
│       ├── __init__.py
│       └── routes.py
│
├── tests/
│   └── test_sync.py
│
├── .env
├── requirements.txt
└── main.py
```

Press Enter on an empty line.

Auto-Folder shows a preview such as:

```text
Preview:
[DIR ] order-sync/
    [DIR ] app/
        [FILE] __init__.py
        [FILE] config.py
        [FILE] database.py
        [DIR ] api/
            [FILE] __init__.py
            [FILE] routes.py
    [DIR ] tests/
        [FILE] test_sync.py
    [FILE] .env
    [FILE] requirements.txt
    [FILE] main.py

5 folders, 8 files

Create this structure? [Y/n]:
```

Nothing is created until the user confirms.

## Safety

Auto-Folder validates the parsed structure before modifying the filesystem.

It rejects unsafe or invalid paths, including:

- Parent-directory traversal such as `../outside`.
- Absolute or nested paths embedded inside a single tree entry.
- Invalid Windows filename characters.
- Windows reserved names such as `CON`, `PRN`, and `NUL`.
- Invalid tree indentation.

Existing files are not overwritten by default.

## Development

Requires Python 3.10+ during development.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
```

Run locally:

```text
auto-folder
```

The project uses automated GitHub Actions tests on Windows to catch parser, validation, and filesystem regressions.

## Packaging

Auto-Folder is developed in Python, but Python is **not required for end users**.

Windows releases are packaged as a standalone executable using PyInstaller:

```text
End user
└── auto-folder.exe
```

Development-only files such as `tests/`, test dependencies, source files, virtual environments, caches, and build metadata are not included in the standalone executable.

The goal is to keep the application small and simple while avoiding unnecessary runtime dependencies.

## Cross-platform

The core application is intentionally kept platform-independent so the same parser, validator, and creator can be reused across operating systems.

The target release formats are:

```text
Auto-Folder
├── Windows → auto-folder.exe
├── Linux   → auto-folder
└── macOS   → auto-folder
```

Platform-specific packaging and installation are kept separate from the core application.

## License

MIT
