#define MyAppName "Auto-Folder"
#define MyAppVersion GetEnv("GITHUB_REF_NAME")
#define MyAppPublisher "vietanh926"
#define MyAppExeName "auto-folder.exe"

[Setup]
AppId={{B4B0B9A4-6E3C-4A0C-9D4A-5D8B7A5F6E21}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\AutoFolder
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=auto-folder-setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
Uninstallable=yes

[Files]
Source: "..\dist\auto-folder.exe"; DestDir: "{app}"; Flags: ignoreversion

[Code]
const
  PathEnvKey = 'Environment';
  PathEnvName = 'Path';
  PathDelimiter = ';';

function GetUserPath(): string;
var
  Value: string;
begin
  if RegQueryStringValue(HKEY_CURRENT_USER, PathEnvKey, PathEnvName, Value) then
    Result := Value
  else
    Result := '';
end;

procedure SetUserPath(const Value: string);
begin
  RegWriteStringValue(HKEY_CURRENT_USER, PathEnvKey, PathEnvName, Value);
end;

function NormalizePathEntry(const Value: string): string;
begin
  Result := RemoveBackslashUnlessRoot(Trim(Value));
end;

function PathContainsAutoFolder(const Value: string): Boolean;
var
  Parts: TArrayOfString;
  I: Integer;
  Entry: string;
begin
  Result := False;
  Parts := SplitString(Value, PathDelimiter);
  for I := 0 to GetArrayLength(Parts) - 1 do begin
    Entry := NormalizePathEntry(Parts[I]);
    if CompareText(Entry, NormalizePathEntry(ExpandConstant('{app}'))) = 0 then begin
      Result := True;
      Exit;
    end;
  end;
end;

procedure AddToUserPath;
var
  CurrentPath: string;
  AppPath: string;
begin
  CurrentPath := GetUserPath();
  AppPath := NormalizePathEntry(ExpandConstant('{app}'));

  if not PathContainsAutoFolder(CurrentPath) then begin
    if CurrentPath <> '' then
      CurrentPath := CurrentPath + PathDelimiter;
    CurrentPath := CurrentPath + AppPath;
    SetUserPath(CurrentPath);
  end;
end;

procedure RemoveFromUserPath;
var
  CurrentPath: string;
  Parts: TArrayOfString;
  ResultPath: string;
  I: Integer;
  Entry: string;
  AppPath: string;
begin
  CurrentPath := GetUserPath();
  AppPath := NormalizePathEntry(ExpandConstant('{app}'));
  Parts := SplitString(CurrentPath, PathDelimiter);
  ResultPath := '';

  for I := 0 to GetArrayLength(Parts) - 1 do begin
    Entry := NormalizePathEntry(Parts[I]);
    if (Entry <> '') and (CompareText(Entry, AppPath) <> 0) then begin
      if ResultPath <> '' then
        ResultPath := ResultPath + PathDelimiter;
      ResultPath := ResultPath + Entry;
    end;
  end;

  SetUserPath(ResultPath);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    AddToUserPath();
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
    RemoveFromUserPath();
end;
