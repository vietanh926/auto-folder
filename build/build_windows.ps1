$ErrorActionPreference = 'Stop'

python -m pip install --upgrade pip
python -m pip install pyinstaller

Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item -Force auto-folder.spec -ErrorAction SilentlyContinue

python -m PyInstaller `
  --onefile `
  --name auto-folder `
  --clean `
  --noconfirm `
  src/auto_folder/main.py

Write-Host "Built: dist/auto-folder.exe"
