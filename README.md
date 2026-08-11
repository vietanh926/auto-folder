# auto-folder

A tiny Windows-friendly CLI that creates folders and files from a pasted directory tree.

## Current status

**v0.1.0 — development**

The project currently contains the parser, filesystem creator, interactive CLI, and tests. The next milestone is packaging it as a standalone Windows executable and then creating a Windows installer that adds `auto-folder` to PATH.

## Development

Requires Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pytest
pytest
```

Run the CLI:

```powershell
auto-folder
```

Paste a tree such as:

```text
order-sync/
│
├── app/
│   ├── __init__.py
│   ├── config.py # environment configuration
│   └── api/
│       ├── __init__.py
│       └── routes.py
│
├── tests/
│   └── test_sync.py
│
├── requirements.txt
└── main.py
```

Press Enter on an empty line to create it in the current directory.

## Product roadmap

- [x] Interactive tree input
- [x] Parse common tree characters
- [x] Ignore comments
- [x] Handle common Markdown artifacts
- [x] Basic parser/creator tests
- [ ] Dry-run mode
- [ ] Safe path validation
- [ ] Better error messages
- [ ] Standalone Windows `.exe`
- [ ] Windows installer
- [ ] Automatically add command to PATH
- [ ] Release automation
