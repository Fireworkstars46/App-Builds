# Program Diagnostic Monitor v1.0.18 Build 19

## Recovery status
Build 19 is a corrective/recovery release produced from the preserved v1.0.15 source, the verified v1.0.17 Build 17 compiled baseline, and the documented Build 16-18 requirements. The original Build 18 source/release attachments expired and are not being fabricated or relabeled.

## Preserved behavior and identity
- `ProgramDiagnosticMonitorIsolatedWindow` main-window identity.
- Dedicated `%LOCALAPPDATA%\Programs\ProgramDiagnosticMonitor-Isolated` install path.
- Dedicated `%LOCALAPPDATA%\ProgramDiagnosticMonitor-Isolated` data namespace.
- Existing isolated uninstall identity and in-place update behavior.
- Passive wait/attach monitoring; the monitor never launches the target.
- 30-second same-run MAIN-process restart watch.
- Automatic freeze/lag detection and performance trace.
- Protected-peer isolation for Crash Monitor and RitschyMirror unless explicitly selected.

## Build 19 hardening
- MAIN target process handles use `PROCESS_QUERY_LIMITED_INFORMATION` only.
- No `OpenThread`, `GetThreadTimes`, thread snapshots, stack walking, or thread suspension.
- Cross-process module enumeration disabled.
- Broad Application event-log scanning disabled.
- System-wide TCP/UDP owner-table enumeration disabled.
- Target token/integrity inspection disabled.
- Recursive watched-folder scanning disabled.
- Wait Chain Traversal is dynamically resolved and limited to hung MAIN UI thread IDs, capped at four per freeze event.
- Same-family helper refresh is bounded and lightweight; helpers are excluded from deep scans.
- 150 ms bounded `WM_NULL` responsiveness probe retained.

## Settings / diagnostics / tray
- Bounded rotating project-local logs.
- Debug Mode and Safe Self-Test.
- Settings window and Settings ↔ main UI synchronization.
- Minimize-to-Tray and Close/X-to-Tray vs Exit.
- Start Minimized, Open Settings at startup, Start Paused, notifications, and configurable tray click behavior.
- Tray recovery after Explorer/taskbar restart.
- Remembered window geometry with off-screen recovery and Reset Window Layout.
- Logs, Diagnostics, and Export Diagnostic Report access.
- Atomic settings writes and merge-under-mutex stale-writer protection for concurrent instances sharing settings.

## Installer / uninstall
- Per-user installer; no elevation request added.
- Existing data/settings/log/diagnostic folders preserved during upgrade.
- Optional app launch happens only after Finish.
- Embedded app/uninstaller SHA-256 verified by setup before install.
- Uninstaller guards deletion to exact isolated project roots and preserves Logs/Diagnostics as recovery evidence.

## Validation
Static/release audit: **100 PASS, 0 FAIL**.

A clean rebuild from the Build 19 source ZIP produced byte-identical deterministic main EXE, uninstaller, and setup binaries.

The in-app Safe Self-Test is implemented with explicit PASS/FAIL/SKIPPED/NOT TESTED results and isolated temporary test data. It was not physically executed on Windows in the Linux build environment, so this release does not claim physical Windows GUI/tray/Explorer-restart/WCT behavior was exercised there.
