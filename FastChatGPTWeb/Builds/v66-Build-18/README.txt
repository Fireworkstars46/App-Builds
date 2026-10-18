Fast ChatGPT Web — Version 66 • Build 18
=========================================

Corrective build status
-----------------------
Build 18 is required by the newest MASTER_RULES.md because Fast ChatGPT Web intentionally supports multiple live instances that share settings.ini. Build 17 correctly prevented the newer instances closed during single-instance consolidation from rewriting settings, but a different stale-writer case remained possible while Multi-instance mode stayed ON: an older/stale instance could later save or close and overwrite a newer setting committed by another still-open instance.

Build 18 fixes only that shared-settings conflict and adds matching Safe Self-Test coverage. All Build 17 multi-instance behavior remains intentionally unchanged.

Build 18 change — shared settings/state conflict protection
-----------------------------------------------------------
- Multiple instances continue to share the established:
  %LOCALAPPDATA%\FastChatGPTWeb\settings.ini
- Normal settings saves now use a project-unique per-user named mutex:
  Local\FastChatGPTWeb.Settings.v1
  so two Fast ChatGPT Web instances do not write settings.ini concurrently.
- Before a normal shared-settings save, the app reloads the latest committed settings from disk.
- Each instance keeps a local baseline representing the settings state it last loaded/committed.
- The save path merges only values that this instance changed relative to that baseline onto the newest disk state.
- Therefore a stale instance closing or saving cannot overwrite unrelated newer values written by another instance.
- Local window placement/state changes can still be saved without reverting another instance's newer app settings.
- Import Settings and Restore Defaults are explicit full-replacement actions, so they intentionally write the complete selected/default settings state.
- Atomic temp-write -> verify -> replace -> verify behavior remains in place.
- No new data path, settings format, registry identity, app identity, installer identity, login/profile path, or update identity was introduced.

Preserved Build 17 multi-instance behavior
------------------------------------------
- "Multi-instance mode (allow multiple app windows)" remains remembered and ON by default for backward compatibility with the established pre-Build-15 behavior.
- When ON, each manual launch may open another Fast ChatGPT Web instance.
- Turning Multi-instance mode OFF while multiple instances are open still deterministically keeps the oldest live Fast ChatGPT Web instance.
- Newer instances still close themselves gracefully through the normal app close path; they are not force-killed.
- Close-to-Tray is bypassed for consolidation exits and those closing newer instances do not save stale settings on exit.
- The oldest survivor still takes the normal single-instance guard before newer instances close.
- A new launch still waits for the transition gate so it cannot race ahead of the intended oldest survivor.
- Turning Multi-instance mode back ON still only permits future manual launches. It does not reopen any instance that was previously closed.
- With Multi-instance mode OFF, later launches still focus/show the surviving instance instead of leaving a second copy open.

Safe Self-Test / regression coverage
------------------------------------
Build 18 preserves all existing production-path Safe Self-Test coverage and adds two isolated shared-settings regressions using the same production merge/write logic:
- another instance commits a newer setting, then a stale instance saves a different local setting; the newer external setting must remain intact;
- another instance commits a newer setting, then a stale instance performs a close/save-style local window update; the newer committed settings must remain intact while the local window change is applied.

Existing instance-mode regression coverage remains:
- production single-instance mutex/signal primitives;
- deterministic oldest-survivor selection;
- survivor-ready handshake before newer close signals;
- startup transition-gate race prevention;
- MultiInstanceMode serializer/parser and write -> reload/read -> compare;
- Settings/UI persistence through production handlers;
- immediate Multi-instance setting persistence plus the production runtime-transition core;
- no automatic reopen after re-enabling multi-instance mode.

Preserved project identity / compatibility
------------------------------------------
- App version remains v66; separate build is Build 18.
- Stable installed EXE remains:
  %LOCALAPPDATA%\Programs\FastChatGPTWebFinal\FastChatGPTWebFinal.exe
- Install root remains:
  %LOCALAPPDATA%\Programs\FastChatGPTWebFinal\
- App data root remains:
  %LOCALAPPDATA%\FastChatGPTWeb\
- Settings remains:
  %LOCALAPPDATA%\FastChatGPTWeb\settings.ini
- WebView2 login/session profile remains:
  %LOCALAPPDATA%\FastChatGPTWeb\WebView2Profile\
- Logs remain under Logs\, diagnostics under Diagnostics\, and self-test temporary data under Temp\.
- AppUserModelID remains Local.FastChatGPTWeb.FinalIcon.v25.
- Existing Start Menu/Desktop/install-folder shortcut and uninstall identities are preserved.
- Existing ChatGPT login/session/profile data is preserved across in-place update.
- Whole-app System/Light/Dark theme, tray modes, Minimize-to-Tray, Close/X-to-Tray, startup settings, notifications, Debug Mode, Safe Test Mode, Pin/Always-on-Top, window persistence/reset, Recent Downloads, branch/OAuth handling, diagnostics, recovery, and update/uninstall behavior remain preserved.

Safety / isolation
------------------
- Per-user least privilege; no administrator requirement added.
- No service or scheduled task.
- No firewall changes or network listeners/sockets.
- No AV/SmartScreen exclusions or security disabling.
- No process killing, injection, hooks or debugger attachment.
- Instance/settings coordination uses only project-owned paths and unique Local\FastChatGPTWeb kernel names.
- Logs remain project-local, bounded and redacted.
- Safe Self-Test uses isolated project-owned temporary settings/data and does not modify the real settings.ini or WebView2 profile.

Build locally
-------------
Run:
  BUILD-REAL-SETUP-EXE.bat

Expected finished installer:
  SetupOutput\FastChatGPT_WebView_v66_Build_18_Setup.exe

The builder still uses dotnet plus normal file-copy commands and keeps installer outer compression disabled.

Required real-PC release verification
-------------------------------------
1. Run BUILD-REAL-SETUP-EXE.bat and confirm the app and setup compile successfully.
2. Install/run v66 Build 18.
3. Enable Multi-instance mode and open at least two instances.
4. Change one normal setting in one instance, then close/save from the other stale instance. Reopen/check Settings and confirm the newer committed setting was not reverted.
5. Confirm Build 17 behavior is unchanged: turn Multi-instance mode OFF and verify only the oldest instance stays open.
6. While OFF, launch again and verify the existing survivor is focused rather than another instance remaining open.
7. Turn Multi-instance mode back ON and verify closed instances do not reopen automatically; manually launch to open another instance.
8. Enable Safe Test Mode and run Safe Self-Test. DONE requires 0 FAIL and only genuinely justified SKIPPED/NOT TESTED items.

Per MASTER_RULES.md, static validation alone is not sufficient to mark Build 18 DONE.
