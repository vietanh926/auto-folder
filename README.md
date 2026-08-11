# auto-folder

Create folders and files from a pasted directory tree.

## Development

Requires Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Then run:

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

## Roadmap

- robust Markdown/tree parsing
- dry-run mode
- overwrite/skip controls
- Windows executable
- Windows installer that adds `auto-folder` to PATH
