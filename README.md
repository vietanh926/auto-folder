# Auto-Folder

**Turn AI-generated project structures into real folders and files in seconds.**

Auto-Folder is a lightweight command-line tool for developers who frequently copy project architectures from AI assistants, documentation, or technical designs.

Instead of manually creating dozens of directories and empty files, run `auto-folder`, paste the structure, and Auto-Folder builds the project skeleton in the current directory.

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
project skeleton created
```

## Design goals

- **Simple:** one command and paste.
- **Fast:** no manual folder/file creation.
- **Lightweight:** the final Windows application should contain only what is required to run Auto-Folder.
- **AI-friendly:** handle common tree formats produced by AI assistants and Markdown.
- **Safe:** never overwrite existing files by default and never allow paths to escape the current working directory.
- **Portable:** the final Windows release should run without requiring Python, pip, or other development tools.

## Supported input

The parser is being designed to support common structures such as:

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

```cmd
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

Auto-Folder creates the structure without overwriting existing files.

## Development

Requires Python 3.10+ during development.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pytest
pytest
```

Run locally:

```powershell
auto-folder
```

## Packaging philosophy

The repository contains source code and tests for development, but these are **not intended to ship with the end-user application**.

The release build will package only the runtime application:

```text
End user installation
└── auto-folder.exe
```

Development-only files such as `tests/`, test dependencies, source files, virtual environments, caches, and build metadata will remain outside the final executable.

The goal is a small standalone Windows executable with no Python installation required.

## Roadmap

- [x] Interactive tree input
- [x] Basic tree parser
- [x] Filesystem creator
- [x] Basic parser/creator tests
- [ ] Comprehensive AI/Markdown tree parsing
- [ ] Safe path validation
- [ ] Better error handling
- [ ] Dry-run mode
- [ ] Standalone Windows `.exe`
- [ ] Minimize executable size and runtime dependencies
- [ ] Windows installer
- [ ] Automatically add `auto-folder` to PATH
- [ ] Release automation
- [ ] Versioned GitHub releases

## License

MIT
