#define MyAppVersion "1.3.2"
#define MyAppName "RitschyMirror"
#define MyAppExeName "RitschyMirror.exe"
#define SrcDir SourcePath + "..\..\_upstream\ritschy-mirror"

[Setup]
; Same application ID and install location as the original version.
AppId={{8F2C6A14-9B3D-4E7A-AC51-1D9E2F6B0C77}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion} (English)
AppPublisher=RitschyRigz (unofficial English translation)
AppPublisherURL=https://github.com/RitschyRigz/ritschy-mirror
VersionInfoVersion={#MyAppVersion}
VersionInfoProductName={#MyAppName}
VersionInfoDescription=RitschyMirror unofficial English setup
DefaultDirName={localappdata}\Programs\RitschyMirror
DisableProgramGroupPage=yes
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
OutputDir={#SrcDir}\EnglishInstaller
OutputBaseFilename=RitschyMirror-English-Setup-{#MyAppVersion}
SetupIconFile={#SrcDir}\assets\app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName} (English)
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "autostart"; Description: "Start RitschyMirror when I sign in to Windows"; GroupDescription: "Startup:"; Flags: unchecked

[Files]
Source: "{#SrcDir}\EnglishBuild\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\installer\default_config\mirror_config.json"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Icons]
Name: "{group}\RitschyMirror"; Filename: "{app}\{#MyAppExeName}"; Comment: "Screen Mirror Tool"
Name: "{group}\RitschyMirror Settings"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--settings"
Name: "{group}\{cm:UninstallProgram,RitschyMirror}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\RitschyMirror"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "RitschyMirror"; ValueData: """{app}\{#MyAppExeName}"""; Tasks: autostart; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch RitschyMirror"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
