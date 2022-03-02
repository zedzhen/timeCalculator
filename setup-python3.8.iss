#define MyAppName "timeCalculator"
#define MyAppVersion "1.0"
#define MyAppPublisher "zedzhen"
#define MyAppURL "https://github.com/zedzhen/timeCalculator"
#define MyAppExeName "start.exe"

[Setup]
AppId={{C9B27BEF-2991-43E8-99AC-787983885FD9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=.\LICENSE
DisableProgramGroupPage=yes
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=.
OutputBaseFilename=timeCalculator-Setup-python3.8
SetupIconFile=.\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SignTool=2022

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: ".\start.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\constant.py"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\help_tk.py"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\main.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\mywinreg.py"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\setting.py"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\python3.8\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallDelete]
Type: filesandordirs; Name: "{app}"