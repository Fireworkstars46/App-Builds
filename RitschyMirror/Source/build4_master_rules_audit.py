"""RitschyMirror Build 4 static/release audit against current MASTER_RULES.md.

This is intentionally STATIC evidence only. Functional behavior is proved by the
installed Safe Self-Test and installer/update tests in CI; callback existence is
never reported here as a functional PASS.
"""
import os, re
from pathlib import Path

root = Path(os.environ['RITSCHY_SOURCE'])
installer = Path(os.environ['RITSCHY_INSTALLER'])
workflow = Path(os.environ.get('RITSCHY_WORKFLOW', '.github/workflows/build-ritschy-mirror.yml'))
master = Path(os.environ.get('MASTER_RULES_PATH', 'MASTER_RULES.md'))
report = Path(os.environ.get('RITSCHY_BUILD4_AUDIT_REPORT', root/'BUILD4-MASTER-RULES-AUDIT.txt'))

files = {p.name:p.read_text(encoding='utf-8',errors='ignore') for p in root.glob('*.cs')}
for extra in ['MirrorTool.csproj','app.manifest']:
    ep=root/extra
    if ep.exists(): files[extra]=ep.read_text(encoding='utf-8',errors='ignore')
all_cs='\n'.join(v for k,v in files.items() if k.endswith('.cs'))
iss=installer.read_text(encoding='utf-8')
yml=workflow.read_text(encoding='utf-8') if workflow.exists() else ''
rules=master.read_text(encoding='utf-8') if master.exists() else ''

lines=[
    'RitschyMirror 1.3.2 Build 4 — current MASTER_RULES.md STATIC audit',
    'Evidence type: static/source/release-contract checks only; functional PASS claims are excluded.',
    '',
]
pass_n=fail_n=na_n=0

def check(desc, cond, detail=''):
    global pass_n, fail_n
    if cond:
        pass_n+=1; lines.append('PASS: '+desc)
    else:
        fail_n+=1; lines.append('FAIL: '+desc + ((' | '+detail) if detail else ''))

def na(desc, reason):
    global na_n
    na_n+=1; lines.append('N/A: '+desc+' | '+reason)

def has(file, text): return text in files.get(file,'')

def ordered(text, *needles):
    pos=-1
    for n in needles:
        pos=text.find(n,pos+1)
        if pos<0: return False
    return True

# Master source and applicability.
check('current MASTER_RULES.md is available to the audit', rules.startswith('# Master App / Script Development Rules'))
check('master rules include stale-writer/shared-state rule', 'prevent stale instances from overwriting newer committed changes' in rules)
check('master rules include runtime multi/single transition rule', 'switching between multi-instance and single-instance modes at runtime' in rules)
check('master rules include immediate-vs-restart setting rule', 'Settings intended to take effect immediately' in rules)
check('master rules require functional Safe Self-Test rather than callback existence', 'A callback/function existing is not a functional PASS' in rules)
na('multi-instance shared-state stale-writer runtime behavior', 'RitschyMirror is intentionally single-instance and has no multi-instance mode')
na('runtime multi-instance/single-instance transition behavior', 'RitschyMirror intentionally has no runtime multi-instance toggle')

# Version/identity/update preservation.
check('normal version remains 1.3.2', '<Version>1.3.2</Version>' in files.get('MirrorTool.csproj','') or '1.3.2' in files.get('MirrorTool.csproj',''))
check('continuing Build number is 4', has('AppInfo.cs','public const int BuildNumber = 4;'))
check('installer normal version remains 1.3.2', '#define MyAppVersion "1.3.2"' in iss)
check('installer Build number is 4', '#define MyBuildNumber "4"' in iss)
check('installer AppId is preserved', 'AppId={{8F2C6A14-9B3D-4E7A-AC51-1D9E2F6B0C77}' in iss)
check('install path is preserved', r'DefaultDirName={localappdata}\Programs\RitschyMirror' in iss)
check('installer remains least privilege', 'PrivilegesRequired=lowest' in iss)
check('mirror_config default remains only-if-missing and uninstall-preserved', 'onlyifdoesntexist uninsneveruninstall' in iss)
check('no blanket UninstallDelete section', re.search(r'(?mi)^\s*\[UninstallDelete\]\s*$',iss) is None)
check('startup registry identity remains RitschyMirror-only HKCU Run', 'Root: HKCU;' in iss and 'ValueName: "RitschyMirror"' in iss and 'CurrentVersion\\Run' in iss)
check('Start Menu shortcuts target permanent installed EXE', iss.count('Filename: "{app}\\{#MyAppExeName}"') >= 2)
check('shortcut icon paths target permanent installed EXE', iss.count('IconFilename: "{app}\\{#MyAppExeName}"') >= 3)

# Isolation / AV / permissions.
for term in ['CreateRemoteThread','WriteProcessMemory','VirtualAllocEx','SetWindowsHookEx(','DebugActiveProcess(','MiniDumpWriteDump(','GetClipboardData','SetClipboardData']:
    check('no invasive runtime primitive: '+term, term.lower() not in all_cs.lower())
for other in ['Crash Monitor','CrashMonitor','Program Diagnostic Monitor','ProgramDiagnostic']:
    check('no runtime coupling to other custom app: '+other, other.lower() not in all_cs.lower())
check('no shared TEMP dependency in runtime source', 'Path.GetTempPath' not in all_cs and '%TEMP%' not in all_cs and '%TMP%' not in all_cs)
check('manifest least privilege is explicit', 'requestedExecutionLevel level="asInvoker" uiAccess="false"' in files.get('app.manifest',''))
check('existing hotkey stays RegisterHotKey rather than keyboard hook', 'RegisterHotKey' in files.get('TrayContext.cs','') and 'SetWindowsHookEx' not in all_cs)

# Persistence / settings architecture.
check('atomic verified settings writer exists', has('SettingsPersistence.cs','WriteTextAtomicVerified'))
check('atomic writer uses project-local sibling temp file', has('SettingsPersistence.cs','string temp = full + ".write-"'))
check('atomic writer performs read-back verification', has('SettingsPersistence.cs','File.ReadAllText(full') and has('SettingsPersistence.cs','Settings verification failed after write'))
check('AppSettings Save uses atomic verified writer', has('AppSettings.cs','SettingsPersistence.WriteTextAtomicVerified'))
check('AppSettings Save no longer silently swallows write failure', 'public void Save(string path)\n    {\n        try' not in files.get('AppSettings.cs',''))
check('MirrorConfig Save uses atomic verified writer', has('MirrorConfig.cs','SettingsPersistence.WriteTextAtomicVerified'))
check('MirrorConfig MergePatch uses atomic verified writer', files.get('MirrorConfig.cs','').count('SettingsPersistence.WriteTextAtomicVerified') >= 2)
check('shared duplicate-setting production setters exist', all(x in files.get('SettingsActions.cs','') for x in ['SetNotifications','SetMainSettingsMinimizeToTray','SetDebugLogging','SetHidePreviewTaskbarButton','SetMinimizePreviewToTray']))
check('Settings UI uses shared duplicate-setting setters', files.get('SettingsForm.cs','').count('SettingsActions.Set') >= 5)
check('tray uses shared duplicate-setting setters', files.get('TrayContext.cs','').count('SettingsActions.Set') >= 5)
check('preview context uses shared minimize-to-tray setter', 'SettingsActions.SetMinimizePreviewToTray' in files.get('Win32Window.cs',''))
check('restart-required HTTP agent setting is explicitly labeled', 'Agent/bind/port changes require restarting the app.' in files.get('SettingsForm.cs',''))
check('restart-required Copy mode is explicitly labeled', 'Copy mode (SDR colors, no image adjustments; restart required)' in files.get('SettingsForm.cs',''))

# Window/layout rules.
check('main Settings X/Y/W/H/maximized fields are backward-compatible settings', all(k in files.get('AppSettings.cs','') for k in ['settings_x','settings_y','settings_width','settings_height','settings_maximized']))
check('main Settings geometry restore uses production helper', 'SettingsWindowLayout.Restore(this, _app);' in files.get('SettingsForm.cs',''))
check('main Settings geometry persistence uses production helper', 'SettingsWindowLayout.CaptureAndSave' in files.get('SettingsForm.cs',''))
check('off-screen layout recovery clamps to a visible Screen working area', 'ClampToVisibleWorkingArea' in files.get('SettingsWindowLayout.cs','') and 'Screen.AllScreens' in files.get('SettingsWindowLayout.cs',''))
check('default/reset main Settings layout uses OS primary monitor', 'Screen.PrimaryScreen?.WorkingArea' in files.get('SettingsWindowLayout.cs',''))
check('Reset Settings Window Layout control exists', 'Reset Settings Window Layout' in files.get('SettingsForm.cs',''))
check('Reset Preview Window Layout control exists', 'Reset Preview Window Layout' in files.get('SettingsForm.cs',''))
check('Settings content remains scrollable', 'AutoScroll = true' in files.get('SettingsForm.cs',''))
check('Settings retains safe minimum size', 'MinimumSize = new Size' in files.get('SettingsForm.cs',''))
check('bottom Exit App remains visible in responsive bottom layout', 'BottomButton("Exit App")' in files.get('SettingsForm.cs','') and 'TableLayoutPanel' in files.get('SettingsForm.cs',''))
check('UI uses SystemColors for native theme-readable bottom area', 'SystemColors.Control' in files.get('SettingsForm.cs',''))

# Tray / close / startup / single-instance.
check('single-instance coordinator creates show event before mutex', ordered(files.get('SingleInstanceCoordinator.cs',''), 'ShowSettingsEvent = new EventWaitHandle', '_mutex = new Mutex'))
check('Program uses single-instance coordinator and secondary signals existing instance', 'new SingleInstanceCoordinator(MutexName, ShowSettingsEvent)' in files.get('Program.cs','') and 'instance.SignalShowSettings()' in files.get('Program.cs',''))
check('startup decisions use one shared production resolver', 'StartupBehavior.Resolve(_app, args)' in files.get('TrayContext.cs',''))
check('tray click coordinator defers single click', 'Timer' in files.get('TrayClickCoordinator.cs','') and '_singleTimer.Start()' in files.get('TrayClickCoordinator.cs',''))
check('tray double-click cancels pending single-click action', '_singleTimer.Stop();' in files.get('TrayClickCoordinator.cs',''))
check('TrayContext routes click/double-click through coordinator', '_trayClickCoordinator.OnMouseClick' in files.get('TrayContext.cs','') and '_trayClickCoordinator.OnDoubleClick' in files.get('TrayContext.cs',''))
check('old direct single-click OpenSettings handler is absent', '_tray.MouseClick += (_, e) => { if (e.Button == MouseButtons.Left) OpenSettings();' not in files.get('TrayContext.cs',''))
check('Explorer/taskbar restart recovery remains wired', 'RegisterWindowMessage("TaskbarCreated")' in files.get('TrayContext.cs',''))
check('main Settings close-to-tray vs Exit uses shared decision path', 'MainSettingsCloseBehavior.Resolve' in files.get('TrayContext.cs',''))
check('shared application exit primitive exists', 'ExitApplicationContext(ApplicationContext context)' in files.get('Program.cs',''))
check('production Quit uses shared application exit primitive', 'Program.ExitApplicationContext(this);' in files.get('TrayContext.cs',''))

# Logging / diagnostics / privacy.
check('bounded mirror.log rotation remains present', 'MaxLogBytes' in files.get('MirrorEngine.cs','') and 'LogArchiveCount' in files.get('MirrorEngine.cs','') and 'RotateLogsIfNeeded' in files.get('MirrorEngine.cs',''))
check('logs include Version+Build', 'AppInfo.BuildLabel' in files.get('MirrorEngine.cs',''))
check('diagnostic text sanitizes profile/local/user identity', all(x in files.get('DiagnosticsManager.cs','') for x in ['%USERPROFILE%','%LOCALAPPDATA%','%USERNAME%']))
check('crash reports live outside normal mirror.log rotation', 'DiagnosticsDirectory(baseDir), "Crashes"' in files.get('DiagnosticsManager.cs',''))
check('diagnostic exports remain project-local', 'DiagnosticsDirectory(baseDir)' in files.get('DiagnosticsManager.cs',''))

# Safe Self-Test structural requirements (functional evidence comes from execution).
d=files.get('DiagnosticsManager.cs','')
check('Safe Self-Test reports PASS/FAIL/SKIPPED counters', 'TOTAL: PASS={pass} FAIL={fail} SKIPPED={skipped}' in d)
check('Safe Self-Test uses isolated app-local SelfTestTemp', 'SelfTestTemp-' in d and 'DiagnosticsDirectory(baseDir)' in d)
check('Safe Self-Test exercises production AppSettings save/load', 'AppSettings production atomic write -> reload/read -> compare' in d)
check('Safe Self-Test exercises production MirrorConfig save/load', 'MirrorConfig production atomic write -> reload/read -> compare' in d)
check('Safe Self-Test exercises shared duplicate-setting setters', 'SettingsActions.SetDebugLogging' in d and 'SettingsActions.SetNotifications' in d)
check('Safe Self-Test exercises startup production resolver', 'StartupBehavior.Resolve' in d)
check('Safe Self-Test exercises single-instance production coordinator', 'new SingleInstanceCoordinator' in d and 'SignalShowSettings' in d)
check('Safe Self-Test exercises tray arbitration production class', 'new TrayClickCoordinator' in d and 'OnDoubleClick()' in d)
check('Safe Self-Test creates real hidden SettingsForm on isolated files', 'new SettingsForm(engine, appPath, app, uiRunValue)' in d)
check('Safe Self-Test functionally iterates real Settings checkboxes', 'FindControls<CheckBox>(form)' in d and 'cb.Checked = !beforeChecked' in d)
check('Safe Self-Test functionally iterates real Settings combo controls', 'FindControls<ComboBox>(form)' in d and 'combo.SelectedIndex = nextIndex' in d)
check('Safe Self-Test functionally iterates real Settings numeric controls', 'FindControls<NumericUpDown>(form)' in d and 'number.Value = next' in d)
check('Safe Self-Test functionally iterates real Settings text controls', 'FindControls<TextBox>(form)' in d and 'textBox.Text = next' in d)
check('Safe Self-Test exercises Reset Preview and Reset Settings buttons', 'FindButton("Reset Preview Window Layout")' in d and 'FindButton("Reset Settings Window Layout")' in d)
check('Safe Self-Test exercises actual Settings hide/restore visibility path', 'HideMainSettingsToTray("Safe Self-Test")' in d and 'RestoreMainSettingsFromTray()' in d)
check('Safe Self-Test exercises Settings diagnostics request buttons', 'Settings diagnostics buttons invoke their production request events exactly once' in d)
check('Safe Self-Test exercises isolated login-autostart registry production path', 'RitschyMirror.SafeSelfTest.' in d and 'LoginAutostart.SetEnabled' in d)
check('Safe Self-Test exercises production log rotation', 'rotation trigger' in d and 'engine.Log(' in d)
check('Safe Self-Test exercises diagnostic report and ZIP export production paths', 'CreateDiagnosticReport' in d and 'ExportLogsAndDiagnostics' in d)
check('Safe Self-Test exercises corrupt-settings recovery', 'corrupt app settings recover to defaults' in d and 'corrupt mirror settings recover to defaults' in d)
check('Safe Self-Test exercises real child-process exit path', '--safe-self-test-exit-child' in d and 'WaitForExit' in d)
check('Safe Self-Test explicitly marks interactive/hardware/reputation items SKIPPED', d.count('Skip(') >= 6)
check('Safe Self-Test does not claim callback existence as functional evidence', 'callback is defined and referenced' not in d)

# Workflow/release contract.
check('workflow applies Build 4 patch set after established Build 3 patches', all(x in yml for x in ['master_rules_build4_core_types.py','master_rules_build4_core_patch.py','master_rules_build4_selftest.py','master_rules_build4_layout.py','master_rules_build4_controls.py','master_rules_build4_controls2.py']))
check('workflow runs Build 4 current MASTER_RULES static audit', 'build4_master_rules_audit.py' in yml)
check('workflow compiles with warnings treated as errors', '-p:TreatWarningsAsErrors=true' in yml)
check('workflow uses private self-contained multi-file publish', '--self-contained true' in yml and '-p:PublishSingleFile=false' in yml)
check('workflow runs installed Safe Self-Test', '--safe-self-test' in yml and 'RESULT: PASS' in yml)
check('workflow requires Safe Self-Test FAIL=0', 'FAIL=0' in yml)
check('workflow performs Build 3 -> Build 4 in-place update test', 'build3-currentinstructions' in yml and 'Build 3 -> Build 4' in yml)
check('workflow verifies settings preservation during update', 'mirror_config.json changed during Build 3 -> Build 4 update' in yml and 'app_settings.json changed during Build 3 -> Build 4 update' in yml)
check('workflow verifies shortcuts/startup/uninstall paths', all(x in yml for x in ['Start Menu shortcuts missing','Optional desktop shortcut not created','Uninstall left shortcut behind']))

lines += ['', f'STATIC TOTAL: PASS={pass_n} FAIL={fail_n} N/A={na_n}', 'RESULT: '+('PASS' if fail_n==0 else 'FAIL'), '',
          'MANUAL/INTERACTIVE (not static PASS):',
          '- Real GPU/capture-card rendering and native preview drag/resize/taskbar behavior.',
          '- Physical Explorer tray click timing/focus-dismiss and visual TaskbarCreated recovery.',
          '- Third-party SmartScreen/Bitdefender reputation verdict for the unsigned build.']
report.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(report.read_text(encoding='utf-8'))
if fail_n: raise SystemExit(2)
