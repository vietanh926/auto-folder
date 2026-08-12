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

function FindPathDelimiter(const Value: string; StartPos: Integer): Integer;
var
  I: Integer;
begin
  Result := 0;
  for I := StartPos to Length(Value) do begin
    if Value[I] = PathDelimiter then begin
      Result := I;
      Exit;
    end;
  end;
end;

function PathContainsAutoFolder(const Value: string): Boolean;
var
  StartPos: Integer;
  EndPos: Integer;
  Entry: string;
  AppPath: string;
begin
  Result := False;
  AppPath := NormalizePathEntry(ExpandConstant('{app}'));
  StartPos := 1;

  while StartPos <= Length(Value) do begin
    EndPos := FindPathDelimiter(Value, StartPos);
    if EndPos = 0 then
      EndPos := Length(Value) + 1;

    Entry := NormalizePathEntry(Copy(Value, StartPos, EndPos - StartPos));
    if (Entry <> '') and (CompareText(Entry, AppPath) = 0) then begin
      Result := True;
      Exit;
    end;

    StartPos := EndPos + 1;
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
  ResultPath: string;
  StartPos: Integer;
  EndPos: Integer;
  Entry: string;
  AppPath: string;
begin
  CurrentPath := GetUserPath();
  AppPath := NormalizePathEntry(ExpandConstant('{app}'));
  ResultPath := '';
  StartPos := 1;

  while StartPos <= Length(CurrentPath) do begin
    EndPos := FindPathDelimiter(CurrentPath, StartPos);
    if EndPos = 0 then
      EndPos := Length(CurrentPath) + 1;

    Entry := NormalizePathEntry(Copy(CurrentPath, StartPos, EndPos - StartPos));
    if (Entry <> '') and (CompareText(Entry, AppPath) <> 0) then begin
      if ResultPath <> '' then
        ResultPath := ResultPath + PathDelimiter;
      ResultPath := ResultPath + Entry;
    end;

    StartPos := EndPos + 1;
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
