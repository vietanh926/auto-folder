$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "=== Building Auto-Folder for Windows ===" -ForegroundColor Cyan

python -m pip install --upgrade pip
python -m pip install pyinstaller

# Clean generated output only. Do NOT remove the build/ directory because
# build/ contains installer.iss, which is needed by Inno Setup.
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "auto-folder.spec") {
    Remove-Item -Force "auto-folder.spec"
}

python -m PyInstaller `
  --onefile `
  --name auto-folder `
  --clean `
  --noconfirm `
  --paths src `
  src/auto_folder/main.py

if (-not (Test-Path "dist\auto-folder.exe")) {
    throw "PyInstaller failed: dist\auto-folder.exe was not created."
}

Write-Host "Built: dist/auto-folder.exe" -ForegroundColor Green
