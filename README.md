# Auto-Folder

**Turn an AI-generated project tree into real folders and files in seconds.**

Auto-Folder lets you copy a project structure from ChatGPT, Claude, Gemini, documentation, or a text file and create it on your computer automatically.

## 📥 Download

### Windows

1. Open the **Releases** page.
2. Download:

```text
   auto-folder-setup.exe
```

3. Run the installer.
4. Follow the installation steps.
5. When installation is finished, you can close the installer.

> You do **not** need to install Python, Git, or any other programming tools.

## 🚀 How to use

After installing Auto-Folder:

1. Open **Command Prompt (CMD)** or **PowerShell**.
2. Go to the folder where you want to create your project.
3. Run:

```text
auto-folder
```

4. Paste your project tree.
5. Press **Enter on an empty line** when you finish pasting.
6. Check the preview.
7. Confirm with `Y` to create the structure.

### Example

Paste this:

```text
my-project/
├── app/
│   ├── main.py
│   └── config.py
├── tests/
│   └── test_main.py
├── data/
└── README.md
```

Auto-Folder will create:

```text
my-project/
├── app/
│   ├── main.py
│   └── config.py
├── tests/
│   └── test_main.py
├── data/
└── README.md
```

## 🤖 Works with AI-generated trees

You can paste directory trees directly from AI assistants.

For example:

```text
pytorch-template/
│
├── train.py
├── test.py
├── config.json
│
├── base/
│   ├── base_data_loader.py
│   ├── base_model.py
│   └── base_trainer.py
│
├── data_loader/
│   └── data_loaders.py
│
├── model/
│   ├── model.py
│   ├── metric.py
│   └── loss.py
│
└── utils/
    ├── util.py
    └── ...
```

`...` and `…` are treated as placeholders and **will not create files or folders**.

## ✨ What it supports

Auto-Folder understands common directory tree formats, including:

- Unicode trees: `├──`, `└──`, `│`
- ASCII trees: `+--`, `\\--`, `|`
- Markdown code blocks
- Comments after filenames
- Markdown formatting around filenames
- Hidden files such as `.env` and `.gitignore`
- Files without extensions such as `Dockerfile` and `LICENSE`
- Nested folders and files
- `...` and `…` placeholders

## 🔒 Safe by default

Before creating anything, Auto-Folder shows a preview and asks for confirmation.

It also protects against unsafe paths and does not overwrite existing files by default.

## 🗑️ Uninstall

To remove Auto-Folder:

**Windows Settings → Apps → Installed apps → Auto-Folder → Uninstall**

The uninstaller also removes Auto-Folder's entry from your **User PATH**, so uninstalling does not leave an unnecessary PATH entry behind.

## 🔄 Updating

When a new version is released:

1. Download the latest `auto-folder-setup.exe` from **Releases**.
2. Run the installer.
3. Install the new version.

You do not need Python or Git.

## 🖥️ Supported platforms

Currently available:

- ✅ Windows

Planned:

- Linux
- macOS

The core application is designed to be cross-platform, while packaging and installation are handled separately for each operating system.

## 🛠️ For developers

If you want to develop or build Auto-Folder from source, see the project files and GitHub Actions configuration in the repository.

Development requires Python 3.10+.

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
```

## 📄 License

MIT
