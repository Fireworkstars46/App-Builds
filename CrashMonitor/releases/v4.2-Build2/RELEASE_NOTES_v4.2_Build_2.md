# Crash Monitor v4.2 Build 2

## Release type
Corrective MASTER_RULES compliance build. Build 2 was required because Build 1 lacked a production Safe Self-Test entry point, mixed static wiring checks with functional PASS evidence, and used separate duplicated paths for several immediate Settings/tray controls.

## Changes
- Added a real Windows Safe Self-Test via the tray and `--safe-self-test`.
- Added isolated production-path checks for settings/data persistence, log rotation, monitored-program reload/compare, Pause runtime state, and the established single-instance mutex.
- Consolidated duplicate Settings/tray controls through shared production setters for Start with Windows, Pause, Minimize to tray, and taskbar+tray behavior.
- Added write/read-back verification for persistent immediate settings.
- Preserved Explorer/taskbar tray-icon recovery introduced in Build 1.
- Preserved all established crash-monitoring, WER, OBS enhanced dump, ZIP/splitting, UI, installer/uninstaller, shortcut, path, identity, and data behavior.

## Compatibility and identity
- App version: 4.2
- Build: 2
- Install path: `%LOCALAPPDATA%\Programs\Crash Monitor\Crash Monitor.exe`
- Data path: `%LOCALAPPDATA%\Crash Monitor`
- Settings: `%LOCALAPPDATA%\Crash Monitor\targets.ini`
- Dumps: `%LOCALAPPDATA%\Crash Monitor\Dumps`
- Mutex: `Local\Crash_Monitor_31`
- Signing state: unsigned baseline preserved; no new signing identity/key created.
- In-place Update / Repair path preserved.

## Release artifacts
- `Crash_Monitor_v4.2_Build_2_Setup.exe` — one binary that acts as setup when run outside the install path and as the installed Crash Monitor application after setup copies it to the established install path.
- `Crash_Monitor_v4.2_Build_2_Source.zip`
- Static/release, MASTER_RULES, AV-safety, and Safe Self-Test reports
- SHA-256 checksum manifest
- Build/recovery metadata and this release history

## Verification status at archival time
- Static/release audit: 86 PASS / 0 FAIL.
- Windows Safe Self-Test and interactive Windows checks have not yet been executed in the build environment.
- Permanent GitHub archival does not change Version or Build.
- Project tracker remains NOT DONE until the required Windows runtime/interactive checks complete with 0 FAIL.
