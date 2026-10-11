"""Static audit for RitschyMirror 1.3.2 Build 3 against CURRENT project instructions.

Runs after all source patches. It does not change app behavior; it fails the build
when required safety/isolation/logging/debug/test/UI/tray/startup/update contracts
are missing. Compiler + installed --safe-self-test provide separate dynamic checks.
"""
import os, re
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])
installer = Path(os.environ["RITSCHY_INSTALLER"])
report = Path(os.environ.get("RITSCHY_BUILD3_AUDIT_REPORT", root / "BUILD3-CURRENT-INSTRUCTIONS-AUDIT.txt"))

files = {p.name: p.read_text(encoding="utf-8", errors="ignore") for p in root.glob("*.cs")}
all_cs = "\n".join(files.values())
# Ignore explanatory comments for invasive-primitive checks; actual source tokens
# and string literals remain scanned. This avoids audit false positives from comments
# such as "do not use SetWindowsHookEx(...)" while still blocking a real import/call.
scan_cs = re.sub(r"/\*.*?\*/", "", all_cs, flags=re.S)
scan_cs = re.sub(r"//[^\n]*", "", scan_cs)
csproj = (root / "MirrorTool.csproj").read_text(encoding="utf-8", errors="ignore")
iss = installer.read_text(encoding="utf-8")
errors = []
checks = []

def require(condition, label):
    if condition: checks.append("PASS: " + label)
    else: errors.append("FAIL: " + label)

def contains(file, *needles):
    text = files.get(file, "")
    return all(n in text for n in needles)

# Version/build + identity/update compatibility.
require(contains("AppInfo.cs", "BuildNumber = 3", "BuildLabel"), "normal version retains separate continuing Build 3 identity")
require('<Version>1.3.2</Version>' in csproj, "normal application version remains 1.3.2")
require('AppId={{8F2C6A14-9B3D-4E7A-AC51-1D9E2F6B0C77}' in iss, "installer AppId preserved")
require('DefaultDirName={localappdata}\\Programs\\RitschyMirror' in iss, "install path preserved")
require('PrivilegesRequired=lowest' in iss, "installer remains least privilege")
require('Flags: onlyifdoesntexist uninsneveruninstall' in iss, "mirror_config.json preserved across update/uninstall")
require(not re.search(r"(?mi)^\s*\[UninstallDelete\]\s*$", iss), "no blanket uninstall deletion of user data")
require('ValueName: "RitschyMirror"' in iss and 'Root: HKCU' in iss, "startup registry identity remains RitschyMirror-only HKCU")

# App settings compatibility + old behavior defaults.
app = files.get("AppSettings.cs", "")
for key in ("minimize_settings_to_tray", "close_settings_to_tray", "start_minimized_to_tray", "open_settings_at_startup", "notifications_enabled"):
    require(key in app, f"backward-compatible app setting present: {key}")
require('CloseSettingsToTray { get; set; } = false' in app, "main X default preserves Build 2 Exit behavior")
require('StartMinimizedToTray { get; set; } = true' in app and 'OpenSettingsAtStartup { get; set; } = false' in app,
        "startup defaults preserve Build 2 tray-only behavior")
require('NotificationsEnabled { get; set; } = true' in app, "notification default preserves existing behavior")

# Bounded project-specific logging and privacy.
eng = files.get("MirrorEngine.cs", "")
require('MaxLogBytes' in eng and 'LogArchiveCount = 3' in eng and 'RotateLogsIfNeeded' in eng, "mirror.log is bounded with local rotation")
require('yyyy-MM-dd HH:mm:ss.fff' in eng and 'AppInfo.BuildLabel' in eng, "log entries carry timestamps and version + Build")
require('[ENGINE] Start requested.' in eng and '[ENGINE] Stop requested.' in eng, "important engine lifecycle actions are logged")
require('cfg.WindowTitle' not in '\n'.join(line for line in eng.splitlines() if 'Log(' in line), "selected window titles are not written to logs")
require('SanitizeText(msg)' in eng, "log text sanitizes user/profile paths")

settings = files.get("SettingsForm.cs", "")
tray = files.get("TrayContext.cs", "")
program = files.get("Program.cs", "")
diag = files.get("DiagnosticsManager.cs", "")

require('[SETTINGS] mirror_config.json saved' in settings and '[SETTINGS] app_settings.json saved' in settings,
        "Settings UI saves are logged without dumping settings contents")
require('[STARTUP]' in tray and '[SHUTDOWN]' in tray, "application startup/shutdown are logged")
require('Crashes' in diag and 'DiagnosticsDirectory' in diag, "crash diagnostics are outside normal log rotation")
require('Window titles, clipboard data, keystrokes, messages, tokens and passwords are not included.' in diag,
        "diagnostic report explicitly excludes sensitive unrelated content")

# Debug/Test.
mirror = files.get("MirrorConfig.cs", "")
require('DebugLogging { get; set; } = false' in mirror, "Debug Mode is OFF by default")
require('Debug Mode' in settings and 'Debug Mode: OFF' in tray, "Debug Mode controls exist in Settings and tray")
require('Run Safe Self-Test' in settings and 'Run Safe Self-Test' in tray, "Safe Self-Test controls exist in Settings and tray")
require('--safe-self-test' in program and 'Safe Test Mode never starts the agent, renderer, tray icon or global hotkey' in program,
        "command-line Safe Test Mode bypasses normal runtime services")
require('SelfTestTemp-' in diag and 'app_settings.json' in diag and 'mirror_config.json' in diag and 'Directory.Delete(temp, recursive: true)' in diag,
        "self-test performs isolated app-settings/mirror-settings read-write-delete cleanup")
require('ValidateUiLayoutContract' in diag and 'ValidateUiLayoutContract' in settings, "self-test includes Settings/UI layout contract")
require('Open Logs' in tray and 'Open Diagnostics' in tray and 'Export Logs / Diagnostic Report' in tray,
        "tray exposes logs, diagnostics, and export")
require('Open Logs' in settings and 'Open Diagnostics' in settings and 'Export Logs / Diagnostic Report' in settings,
        "Settings exposes logs, diagnostics, and export")

# UI/layout/readability.
require('AutoScroll = true' in settings, "Settings content is scrollable")
require('new TableLayoutPanel' in settings and 'RowCount = 2' in settings and 'ColumnCount = 2' in settings,
        "bottom commands use responsive 2x2 layout")
require('Exit App' in settings, "visible bottom Exit App control exists")
require('MaximumSize = new Size(560, 0)' in settings and 'SystemColors.GrayText' in settings,
        "long notes wrap and use system-readable colors")
require('WorkingArea' in settings and 'Math.Min(620' in settings and 'Math.Min(780' in settings,
        "Settings startup size is bounded to working area")

# Tray/taskbar behavior.
for label in ("Minimize preview to tray", "Minimize MAIN Settings window to tray", "Open / Restore Settings", "Exit App", "Debug Mode", "Run Safe Self-Test", "Open Logs", "Open Diagnostics", "Export Logs / Diagnostic Report", "Tray notifications"):
    require(label in tray, f"tray item present: {label}")
require('CloseSettingsToTray' in tray and 'HideMainSettingsToTray("Main Settings X setting")' in tray,
        "Close/X to Tray vs Exit behavior is configurable")
require('OpenSettingsAtStartup' in tray and 'StartMinimizedToTray' in tray,
        "Open Settings at startup and Start Minimized to Tray are implemented")
require('AutostartMirror' in tray and 'Start mirroring when app opens' in settings,
        "start paused/stopped vs automatic mirroring setting remains available")
require('_tray.MouseClick' in tray and '_tray.DoubleClick' in tray and 'ShowOrStartPreviewFromTray' in tray,
        "single-click and established double-click tray behavior are wired")
require('ContextMenuStrip' in tray and 'menu.Opening' in tray, "standard focus-dismissable tray menu is retained")
require('RegisterWindowMessage("TaskbarCreated")' in tray and 'Explorer/taskbar restart detected' in tray,
        "Explorer/taskbar restart tray recovery is explicitly wired")
require('Hide preview taskbar button' in tray and 'Hide preview taskbar button' in settings,
        "preview taskbar-only/tray behavior remains configurable")
require('RestoreMainSettingsFromTray' in tray and 'RestoreMainSettingsFromTray' in settings,
        "tray cannot trap the main Settings window without a restore path")

# Shortcut/shell contract.
require('Name: "{group}\\RitschyMirror"' in iss and 'Filename: "{app}\\{#MyAppExeName}"' in iss,
        "Start Menu shortcut targets permanent installed EXE")
require('IconFilename: "{app}\\{#MyAppExeName}"' in iss, "shortcut icon path is explicit and permanent")
require('Name: "{autodesktop}\\RitschyMirror"' in iss and 'Tasks: desktopicon' in iss, "desktop shortcut task remains optional")
require('SetCurrentProcessExplicitAppUserModelID' not in scan_cs, "no unsupported/unneeded AppUserModelID API import introduced")

# Safety/isolation (complements reliability_av_safety.py).
for forbidden in ("CreateRemoteThread", "WriteProcessMemory", "VirtualAllocEx", "SetWindowsHookEx(", "DebugActiveProcess(", "MiniDumpWriteDump(", "Clipboard.", "GetClipboardData", "SetClipboardData", "powershell.exe", "pwsh.exe", "cmd.exe", "schtasks", "CreateService"):
    require(forbidden.lower() not in scan_cs.lower(), f"no invasive runtime primitive: {forbidden}")
for other in ("Crash Monitor", "CrashMonitor", "Program Diagnostic Monitor", "ProgramDiagnostic"):
    require(other.lower() not in scan_cs.lower(), f"no runtime coupling to other custom app: {other}")
require('Path.GetTempPath' not in scan_cs and 'GetTempPath' not in scan_cs, "no shared TEMP dependency; self-test/exports stay RitschyMirror-local")
require('RegisterHotKey' in tray and 'SetWindowsHookEx' not in tray and 'GetAsyncKeyState' not in tray,
        "existing Ctrl+Alt+T remains documented RegisterHotKey rather than a keyboard hook")

# Callback/static wiring counts; compiler will catch signatures/types.
for name in ("ToggleDebugMode", "RunSafeSelfTest", "OpenDiagnostics", "ExportDiagnostics", "ShowNotification"):
    require(len(re.findall(rf"\b{name}\s*\(", tray)) >= 2, f"tray callback is defined and referenced: {name}")
for name in ("BuildDiagnostics", "SyncDebugModeFromConfig", "HideMainSettingsToTray", "ValidateUiLayoutContract"):
    require(len(re.findall(rf"\b{name}\s*\(", settings)) >= 1, f"Settings callback/helper exists: {name}")

report_lines = [
    "RitschyMirror 1.3.2 Build 3 — CURRENT Custom Instructions Static Audit",
    f"Timestamp: {__import__('datetime').datetime.now().astimezone().isoformat()}",
    "",
    *checks,
    *errors,
    "",
    "NOT RUNTIME-VERIFIED BY THIS STATIC STEP:",
    "- Actual Explorer.exe restart recovery visual behavior (wiring is checked statically).",
    "- Real GPU/capture-card rendering, native preview dragging/resizing, and actual tray click timing.",
    "- SmartScreen/Bitdefender reputation verdicts; no unsigned build can guarantee those.",
    "- Windows theme appearance beyond native WinForms/SystemColors (RitschyMirror has no custom theme system).",
    "",
    "RESULT: " + ("PASS" if not errors else "FAIL"),
]
report.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
print(report.read_text(encoding="utf-8"))
if errors:
    raise SystemExit("Current-instructions audit failed with %d issue(s)" % len(errors))
