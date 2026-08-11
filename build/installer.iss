#define AppName "Auto-Folder"
#define AppVersion "0.1.0"
#define AppPublisher "Auto-Folder"
#define AppExeName "auto-folder.exe"

[Setup]
AppId={{8A2B4B9D-0F5B-4A16-9B9A-6C2F7E2B6A01}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={localappdata}\AutoFolder
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=auto-folder-setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
ChangesEnvironment=yes

[Files]
Source: "..\dist\auto-folder.exe"; DestDir: "{app}"; Flags: ignoreversion

[Code]
procedure AddToUserPath(const Dir: string);
var
  CurrentPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath) then
    CurrentPath := '';

  if Pos(';' + Dir + ';', ';' + CurrentPath + ';') = 0 then
  begin
    if CurrentPath = '' then
      CurrentPath := Dir
    else
      CurrentPath := CurrentPath + ';' + Dir;
    RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath);
  end;
end;

procedure RemoveFromUserPath(const Dir: string);
var
  CurrentPath: string;
  NormalizedPath: string;
  Entry: string;
  ResultPath: string;
  I: Integer;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath) then
    Exit;

  ResultPath := '';
  NormalizedPath := CurrentPath + ';';
  while Pos(';', NormalizedPath) > 0 do
  begin
    I := Pos(';', NormalizedPath);
    Entry := Copy(NormalizedPath, 1, I - 1);
    Delete(NormalizedPath, 1, I);
    if (Entry <> '') and (CompareText(Entry, Dir) <> 0) then
    begin
      if ResultPath <> '' then
        ResultPath := ResultPath + ';';
      ResultPath := ResultPath + Entry;
    end;
  end;

  RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', ResultPath);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    AddToUserPath(ExpandConstant('{app}'));
end;

procedure CurUninstallStepChanged(UninstallStep: TUninstallStep);
begin
  if UninstallStep = usPostUninstall then
    RemoveFromUserPath(ExpandConstant('{app}'));
end;
