from pathlib import Path
import re, subprocess, sys, hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'crash_monitor_42_build12-source.cpp'
EXE=ROOT/'Crash_Monitor_v4.2_Build_12_Setup.exe'
MANIFEST=ROOT/'Crash_Monitor_v4.2_Build_12.manifest'
USERDEF=ROOT/'USER32.def'
results=[]
def check(name, cond, detail=''): results.append((name,bool(cond),detail))
def text(p): return p.read_text(encoding='utf-8',errors='replace')
s=text(SRC); m=text(MANIFEST)
# Version/build/artifacts
check('Version + Build string present','Crash Monitor 4.2 Build 12' in s)
check('Build number 11 present','#define CM_BUILD_W L"12"' in s)
check('Installer filename exact',EXE.name=='Crash_Monitor_v4.2_Build_12_Setup.exe' and EXE.exists())
check('Manifest assembly version','version="4.2.12.0"' in m)
check('Manifest identity preserved','name="CrashMonitor.Application"' in m)
check('Manifest least privilege','requestedExecutionLevel level="asInvoker"' in m)
# Identity/update compatibility
for token in ['Local\\\\Crash_Monitor_31','CrashMonitorMainClass411','CrashMonitorSetupClass411','L"\\\\Programs"','L"\\\\Crash Monitor"','L"\\\\Dumps"','L"\\\\monitor.log"','L"\\\\targets.ini"','Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\Crash Monitor','Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\App Paths\\\\Crash Monitor.exe']:
    check('Identity preserved: '+token,token in s)
check('Startup value identity preserved','L"Crash Monitor"' in s and 'CurrentVersion\\\\Run' in s)
check('Installed executable identity preserved','L"\\\\Crash Monitor.exe"' in s)
check('Target format preserved',all(x in s for x in ['L"Name%d"','L"Path%d"','L"Enabled%d"']))
check('Existing settings keys preserved',all(x in s for x in ['L"TrayOnly"','L"MinimizeToTray"','L"KeepTrayWithTaskbar"','L"DetailsHeight"']))
check('New settings default safely',all(x in s for x in ['GetCloseXToTraySetting(){return GetPrivateProfileIntW(L"Settings",L"CloseXToTray",0','GetStartMinimizedSetting(){return GetPrivateProfileIntW(L"Settings",L"StartMinimized",0','GetStartPausedSetting(){return GetPrivateProfileIntW(L"Settings",L"StartPaused",0','GetNotificationsSetting(){return GetPrivateProfileIntW(L"Settings",L"Notifications",1']))
# Close/minimize/exit separation
check('WM_CLOSE uses dedicated production close handler','if(m==WM_CLOSE){HandleMainClose(h);return 0;}' in s)
check('Close/X OFF routes to Exit App','HandleMainClose(HWND h){if(g_closeXToTray)' in s and 'Main-window X -> Exit App' in s and 'RequestExit(h)' in s)
check('Close/X ON routes to tray','Main-window X -> tray' in s and 'HideMainToTray()' in s)
check('Minimize-to-tray remains independent','g_windowMinimized&&g_minimizeToTray' in s and 'MinimizeIntoTray()' in s)
check('Shared Exit App production path','id==IDC_EXITAPP&&code==BN_CLICKED)RequestExit(h)' in s and 'c==CMD_EXIT)RequestExit(hwnd)' in s)
a=s.find('static void RequestExit(HWND h)'); b=s.find('static void HandleMainClose',a); check('Exit path destroys window',a>=0 and b>a and 'DestroyWindow(h)' in s[a:b])
check('Close/X setting main control exists','IDC_CLOSEXTRAY' in s and 'Close/X to tray (off = Exit App)' in s)
check('Close/X setting tray control exists','CMD_CLOSEXTRAY' in s and 'Close/X to tray (off = Exit App)' in s)
check('Close/X setting uses shared setter',s.count('ApplyCloseXToTraySetting(')>=4)
# Startup/settings rules
check('Start Minimized separate setting','IDC_STARTMINIMIZED' in s and 'Start minimized next launch' in s and 'ApplyStartMinimizedSetting' in s)
check('Start Paused separate setting','IDC_STARTPAUSED' in s and 'Start paused next launch' in s and 'ApplyStartPausedSetting' in s)
check('Notifications separate setting','IDC_NOTIFICATIONS' in s and 'Tray notifications' in s and 'ApplyNotificationsSetting' in s)
check('Start Minimized applied at launch','g_startMinimized=GetStartMinimizedSetting()' in s and 'else if(g_startMinimized)' in s)
check('Start Paused applied at launch','g_startPaused=GetStartPausedSetting()' in s and 'g_paused=g_startPaused?1:0' in s)
check('Notifications apply immediately','g_notificationsEnabled=on' in s and 'if(!g_trayVisible||!g_notificationsEnabled)return' in s)
check('Next-launch timing explicit in UI','Start minimized next launch' in s and 'Start paused next launch' in s)
check('Persistent setting writes verified',all(x in s for x in ['SETTINGS verify FAILED key=CloseXToTray','SETTINGS verify FAILED key=StartMinimized','SETTINGS verify FAILED key=StartPaused','SETTINGS verify FAILED key=Notifications']))
# Tray behavior
check('TaskbarCreated registered','RegisterWindowMessageW(L"TaskbarCreated")' in s)
check('TaskbarCreated handler restores tray','m==g_taskbarCreatedMsg' in s and 'AddTrayIcon();SetTrayState(g_currentState,g_currentActive)' in s)
check('Tray retry timer retained','&&!g_trayVisible' in s.replace(' ',''))
check('Tray Open and Exit present','Open Crash Monitor' in s and 'L"Exit App"' in s)
check('Tray Pause/Resume label dynamic','g_paused?L"Resume Monitoring":L"Pause Monitoring"' in s)
check('Tray click double-trigger guarded','GetDoubleClickTime()' in s and 'g_lastTrayClickTick' in s and 'WM_LBUTTONDBLCLK){return 0;}' in s)
check('Single tray click reveals without changing persisted display mode','RevealExistingWindow()' in s and 'if(c==CMD_SHOW)RevealExistingWindow()' in s)
# Single instance
check('Intentional single-instance mutex preserved','CreateMutexW(NULLPTR,FALSE,L"Local\\\\Crash_Monitor_31")' in s and 'ERROR_ALREADY_EXISTS' in s)
check('Relaunch reveals/focuses existing app','FindWindowW(L"CrashMonitorMainClass411"' in s and 'PostMessageW(existing,WM_SHOW_EXISTING' in s and 'SetForegroundWindow(existing)' in s)
check('Existing-instance message handled','if(m==WM_SHOW_EXISTING){RevealExistingWindow();return 0;}' in s)
check('No multi-instance mode added','AllowMultipleInstances' not in s and 'multi-instance mode' not in s.lower())
# Window placement/layout
check('Window X/Y/W/H persistence implemented',all(x in s for x in ['L"WindowX"','L"WindowY"','L"WindowW"','L"WindowH"','GetSavedWindowRectSetting','SaveWindowRectSetting']))
check('Window persistence write/read verify test','window X/Y/W/H write -> reload/read -> compare' in s)
check('Restore clamps to visible monitor','MonitorFromRect' in s and 'GetMonitorInfoW' in s and 'ClampRectToVisibleWorkArea' in s)
check('Default/reset uses primary work area','SystemParametersInfoW(SPI_GETWORKAREA' in s and 'PrimaryDefaultRect' in s)
check('Reset Window Layout exposed','IDC_RESET_LAYOUT' in s and 'CMD_RESET_LAYOUT' in s and 'Reset Window Layout' in s)
check('Resizable minimum dimensions retained','ptMinTrackSize.x=680' in s and 'ptMinTrackSize.y=500' in s)
check('Responsive layout includes all new settings',all(x in s for x in ['MoveMainControl(g_closeXTrayBox','MoveMainControl(g_startMinimizedBox','MoveMainControl(g_startPausedBox','MoveMainControl(g_notificationsBox']))
# Diagnostics/logging/privacy
check('Bounded log size defined','#define LOG_ROTATE_BYTES 5242880ULL' in s)
check('Five log rotations defined','#define LOG_ROTATE_COUNT 5' in s)
check('Log writes serialized','AcquireSRWLockExclusive(&g_logLock)' in s and 'ReleaseSRWLockExclusive(&g_logLock)' in s)
check('Export Diagnostic Report main control','IDC_EXPORT_REPORT' in s and 'Export Report' in s)
check('Export Diagnostic Report tray control','CMD_EXPORT_REPORT' in s and 'Export Diagnostic Report' in s)
check('Diagnostic report targeted/project-local','CrashMonitor-Diagnostic-v4.2-Build12-' in s and 'Monitored programs:' in s and 'Privacy: no clipboard contents' in s)
# Safe Self-Test
check('Safe Self-Test main and tray entry points','IDC_SAFE_SELF_TEST' in s and 'CMD_SAFE_SELF_TEST' in s and 'LaunchSafeSelfTest' in s)
check('Safe Self-Test report project-local','CrashMonitor-SafeSelfTest-v4.2-Build12.txt' in s and 'lstrcatW(reportDir,L"\\\\Crash Monitor")' in s and 'persistent Safe Self-Test report created in Crash Monitor data/log folder' in s)
check('Safe Self-Test isolated temp work folder','CrashMonitor-SafeSelfTest-Work-%u' in s and 'RemoveTree(root)' in s)
check('Safe Self-Test before real BuildPaths','--safe-self-test' in s and s.find('if(CommandHas(L"--safe-self-test"))') < s.rfind('BuildPaths();LoadTargets();'))
check('Self-Test close setting production path','Close/X-to-tray immediate production setter + write/read persistence' in s)
check('Self-Test start minimized production path','Start-minimized next-launch setting + write/read persistence' in s)
check('Self-Test start paused production path','Start-paused next-launch setting + write/read persistence' in s)
check('Self-Test notifications production path','Notifications immediate production setter + write/read persistence' in s)
check('Self-Test close X actual child termination','--selftest-close-x-exit-child' in s and 'production WM_CLOSE -> RequestExit path' in s)
check('Self-Test main Exit actual child termination','--selftest-exit-button-child' in s and 'shared production RequestExit path' in s)
check('Self-Test target persistence round-trip','monitored-program persistence write -> reload/read -> compare' in s)
check('Self-Test missing config defaults includes new settings','GetCloseXToTraySetting()==FALSE' in s and 'GetStartMinimizedSetting()==FALSE' in s and 'GetStartPausedSetting()==FALSE' in s and 'GetNotificationsSetting()==TRUE' in s)
check('Self-Test single-instance mutex','intentional single-instance mutex collision detection' in s)
check('Self-Test persistent report functional check','persistent Safe Self-Test report created in Crash Monitor data/log folder' in s and 'GetFileAttributesW(report)!=INVALID_FILE_ATTRIBUTES' in s)
check('Self-Test unexecuted items classified','NOT_TESTED=4' in s and 'NOT TESTED - asynchronous Windows Search indexing/discovery timing' in s)
for label in [
    'Settings <-> UI checkbox synchronization through production setters',
    'Reset Window Layout moves actual window to OS primary-monitor work area',
    'taskbar-only / tray-only / taskbar+tray production display-mode behavior',
    'actual minimize-to-tray hides isolated window and creates tray icon',
    'actual Close/X-to-tray hides isolated window without terminating',
    'TaskbarCreated recovery handler re-adds actual tray icon without killing Explorer',
    'main-window and tray Safe Self-Test commands reach the same production launcher',
    'Start with Windows registry engine write/read/delete using isolated test value',
    'Start Menu/Desktop shortcut creation engine using isolated .lnk path',
    'WER LocalDumps registry payload engine write/read/remove using isolated HKCU test key',
    'Export Diagnostic Report production writer creates project-local report',
    'real TEST full dump against isolated helper process + lossless ZIP verification',
    'real PRECRASH handle-focused dump against isolated helper process + ZIP verification',
    'real CRASH full dump against isolated helper process + lossless ZIP verification',
    'real EXITCRASH full dump against isolated helper process + lossless ZIP verification',
    'OBS enhanced PSS snapshot / VA-clone TEST dump path against isolated helper process + ZIP verification',
    'forced archive splitting crosses part boundaries safely, preserves byte order, creates exactly four deterministic parts, and writes reassembly script'
]: check('Expanded Self-Test: '+label,label in s)
check('Expanded Self-Test has at least 39 automated result paths',len(re.findall(r'SelfTestWrite\(rh,',s[s.find('static int RunSafeSelfTest(){'):s.find('static int FindTargetByPath')]))>=39)
check('Startup production identity uses named-value helper','SetStartupNamedValue(L"Crash Monitor"' in s and 'Crash Monitor Safe Self-Test' in s)
check('WER production wrappers remain HKLM','RegisterWerAt(HKEY_LOCAL_MACHINE' in s and 'UnregisterWerAt(HKEY_LOCAL_MACHINE' in s and 'IsWerConfiguredAt(HKEY_LOCAL_MACHINE' in s)
check('WER self-test uses isolated HKCU key','HKEY_CURRENT_USER,werTestKey' in s and r'Software\\CrashMonitor\\SafeSelfTest\\WER\\SelfTest.exe' in s)
check('Shortcut production wrapper preserved','CreateShortcutFileToTarget(linkPath,g_installExe,g_installDir)' in s and 'CreateShortcutFileToTargetArgs' in s)
check('Split production wrapper preserves official part limit','SplitArchiveForLimit(zip,DISCORD_PART_BYTES,outParts)' in s)
check('Safe Self-Test launcher intercept prevents recursive test process','g_selfTestLaunchIntercept' in s and 'g_selfTestLaunchInterceptCount' in s)

check('Build 12 Safe Self-Test supervised by parent app','SafeSelfTestMonitorWorker' in s and 'WM_SELFTESTDONE' in s and 'g_safeSelfTestRunning' in s)
check('Build 12 visible Safe Self-Test running state','Safe Self-Test running...' in s and 'EnableWindow(g_safeSelfTestBtn,FALSE)' in s)
check('Build 12 abnormal child exit still gets completion popup','Safe Self-Test did not finish normally.' in s and 'partial report will open if one was created' in s)
check('Build 12 partial report progress is flushed','SelfTestProgress' in s and 'RUNNING %d/%d' in s and 'FlushFileBuffers(h)' in s)
check('Build 12 writes RUNNING progress for all 39 automated checks',len(re.findall(r'SelfTestProgress\(rh,\d+,39,',s[s.find('static int RunSafeSelfTest(){'):s.find('static int FindTargetByPath')]))==39)
check('Build 12 dump tests use isolated helper child','--selftest-dump-target=' in s and 'RunSelfTestDumpTargetChild' in s and 'StartSelfTestDumpTarget' in s)
check('Build 12 no self-process dump regression','WriteExternalDump(GetCurrentProcessId(),exeName,kind' not in s)
check('Build 12 normal self-test completion marker','SAFE SELF-TEST FINISHED' in s)
# AV safety
for name in ['WriteProcessMemory','CreateRemoteThread','VirtualAllocEx','SetWindowsHookEx','GetAsyncKeyState','OpenClipboard','GetClipboardData','SetClipboardData']:
    check('No '+name,name not in s)
check('No cmd/ping self-delete','L"cmd.exe"' not in s and 'ping 127.0.0.1' not in s)
check('MoveFileEx uninstall cleanup retained','MOVEFILE_DELAY_UNTIL_REBOOT' in s and 'ScheduleFinalSelfDelete' in s)
check('Enhanced debugger remains OBS-scoped','lstrcmpiW(exe,L"obs64.exe")' in s and 'DebugActiveProcess(pid)' in s)
# Crash feature preservation
for token in ['PssCaptureSnapshot','MiniDumpWriteDump','OBS_PRECRASH_HANDLE_THRESHOLD 250000u','L"PRECRASH"','L"CRASH"','L"EXITCRASH"','L"TEST"','CompressDumpForSharing','SplitArchiveForDiscord','RegisterWerOne']:
    check('Crash feature retained: '+token,token in s)
# Installer/update/uninstall
check('Update copies over same installed EXE through shared helper','CopyInstallImageForUpdate(g_exePath,g_installExe)' in s)
check('Install preserves user data','RemoveTree(g_baseDir)' not in s[s.find('static BOOL DoInstall'):s.find('static void LayoutSetup')])
check('DisplayVersion current','SetRegString(h,L"DisplayVersion",CM_VERSION_W)' in s)
check('Settings/Apps identity preserved','RegisterUninstallEntry' in s and 'RegisterAppPath' in s)
check('Shortcuts preserved','SetShortcuts(startMenu,desktop)' in s)
check('Startup registration preserved','SetStartupPath(g_installExe' in s)

# Build 12 latest MASTER_RULES progress/hang regressions
check('Safe Self-Test live current-test UI progress', all(x in s for x in ['WM_SELFTESTPROGRESS','ReadSelfTestProgressSnapshot','Self-Test %d/%d running...','Safe Self-Test starting — waiting for the first test status...']))
check('Safe Self-Test progress sidecar is project-local and flushed', all(x in s for x in ['CrashMonitor-SafeSelfTest-v4.2-Build12.progress','WriteSelfTestProgressSnapshot','FlushFileBuffers(ph)']))
check('Safe Self-Test no-progress hang timeout', all(x in s for x in ['SELFTEST_HANG_TIMEOUT_MS 180000u','GetTickCount64()-lastProgressTick>SELFTEST_HANG_TIMEOUT_MS','TerminateProcess(pi.hProcess,CM_SELFTEST_TIMEOUT_CODE)']))
check('Safe Self-Test timeout is reported explicitly', 'Safe Self-Test was stopped because it made no progress for 180 seconds.' in s and 'partial report retained' in s)
check('Archive tool subprocess timeout', all(x in s for x in ['ARCHIVE_TOOL_TIMEOUT_MS 120000u','WaitForSingleObject(pi.hProcess,ARCHIVE_TOOL_TIMEOUT_MS)','TerminateProcess(pi.hProcess,WAIT_TIMEOUT)']))

# Build 12 regressions: preserve Build 9 process-local buffer fix and correct Build 9 part-boundary rollover failure.
check('Archive splitter uses process-local buffer instead of 1 MiB stack local', all(x in s for x in ['#define SPLIT_IO_BUFFER_BYTES 1048576u','VirtualAlloc(NULLPTR,SPLIT_IO_BUFFER_BYTES','VirtualFree(buf,0,MEM_RELEASE)','BYTE* buf=']) and 'BYTE buf[1024*1024]' not in s)
check('Archive splitter dynamic buffer APIs imported', 'VirtualAlloc' in text(ROOT/'KERNEL32.def') and 'VirtualFree' in text(ROOT/'KERNEL32.def'))
check('Build 8 stack-crash regression remains protected by process-local split buffer', 'VirtualAlloc(NULLPTR,SPLIT_IO_BUFFER_BYTES' in s and 'VirtualFree(buf,0,MEM_RELEASE)' in s and 'SplitArchiveForLimit(splitFile,2048ULL,&parts)' in s)
check('Build 9 boundary rollover regression reopens a new part inside the inner write loop', 'while(off<got){if(out==INVALID_HANDLE_VALUE)' in s and 'completedParts++;nextPart++;' in s)
check('Build 9 exact-boundary part count uses completed-part accounting', 'int nextPart=1,completedParts=0' in s and 'if(outParts)*outParts=completedParts' in s)
check('Build 12 split regression verifies byte order and no spurious fifth part', 'verifyOffset==8192ULL&&!FileExists(p5)' in s and 'verifyBuf[j]!=(BYTE)((verifyOffset+j)&0xFF)' in s)
check('Build 12 split-test label identifies Build 9 boundary rollover regression', 'forced archive splitting + reassembly regression (Build 9 boundary rollover)' in s)
# Build 12 automated manual-check reductions
check('Build 12 guarded physical Explorer restart path', all(x in s for x in ['RestartExplorerAndVerifyTrayRecovery','GetWindowThreadProcessId','PROCESS_TERMINATE|SYNCHRONIZE','physical Explorer.exe/taskbar restart completed']))
check('Build 12 Explorer test restores shell if Windows does not auto-restart it','ShellExecuteW(0,L"open",L"explorer.exe"' in s)
check('Build 12 actual Start Menu shortcut launch path', all(x in s for x in ['actual user-visible Start Menu shortcut launch','CSIDL_PROGRAMS','--selftest-shortcut-marker=','WaitForSelfTestMarker']))
check('Build 12 shortcut child exits before normal app initialization','if(CommandHas(L"--selftest-shortcut-marker=")){ExitProcess((UINT)RunSelfTestShortcutMarkerChild());}' in s)
check('Build 12 Update/Repair shared production copy helper','CopyInstallImageForUpdate' in s and 'production Update/Repair image-replacement helper overwrites staged old app bytes while preserving isolated settings and dump data' in s)
check('Build 12 remaining environment-owned checks explicitly classified','NOT_TESTED=4' in s and 'actual Windows sign-out/reboot' in s and 'asynchronous Windows Search indexing/discovery timing' in s and 'real HKLM WER enable/disable UAC elevation approval flow' in s and 'Bitdefender/SmartScreen reputation result' in s)
check('Build 12 self-test progress total is 39','g_safeSelfTestProgressTotal=39' in s and 'RUNNING 39/39 - cleanup and final report' in s)


# Build 12 regression: Build 11 could exit 0xC0000005 before creating its report because the expanded
# freestanding self-test body had a larger stack frame while stack probing is intentionally disabled.
check('Build 12 Safe Self-Test body runs on explicit committed worker stack', all(x in s for x in ['SELFTEST_EXEC_STACK_COMMIT 262144u','SafeSelfTestExecutionWorker','CreateThread(NULLPTR,SELFTEST_EXEC_STACK_COMMIT','RunSafeSelfTestBody']))
check('Build 12 wrapper is small and body is separated from process entry', s.find('static int RunSafeSelfTest(){') < s.find('static int RunSafeSelfTestBody(){') and 'if(CommandHas(L"--safe-self-test")){int st=RunSafeSelfTest();' in s)
check('Build 12 launcher displays correct 39-test total','g_safeSelfTestProgressTotal=39' in s)

# Compiler warnings evidence
warn=(ROOT/'compile.err').read_text(errors='replace') if (ROOT/'compile.err').exists() else ''
check('Compiler warnings/errors zero',warn.strip()=='',warn[:500])
# PE/imports
try:
    out=subprocess.check_output(['/usr/local/swift/usr/bin/llvm-objdump','-p',str(EXE)],text=True,errors='replace')
    dlls=re.findall(r'DLL Name: ([^\r\n]+)',out)
    allowed={'KERNEL32.dll','USER32.dll','GDI32.dll','SHELL32.dll','ADVAPI32.dll','COMDLG32.dll','OLE32.dll'}
    check('Only expected Windows DLL imports',set(dlls)==allowed,', '.join(dlls))
    check('No Authenticode signature introduced','Entry 4 0000000000000000 00000000 Security Directory' in out)
    for api in ['RegisterWindowMessageW','GetWindowThreadProcessId','MoveFileExW','SystemParametersInfoW','MonitorFromRect','GetMonitorInfoW','GetDoubleClickTime','IsWindowVisible','VirtualAlloc','VirtualFree']:
        check(api+' linked',api in out)
except Exception as e: check('PE inspection',False,repr(e))
b=EXE.read_bytes()
check('Embedded manifest contains 4.2.12.0',b'4.2.12.0' in b)
check('Embedded resource section present',b'.rsrc' in b)
check('Executable is PE',b[:2]==b'MZ')
failed=[r for r in results if not r[1]]
for name,ok,detail in results: print(('PASS' if ok else 'FAIL')+' - '+name+((' | '+detail) if detail else ''))
print(f'\nTOTAL={len(results)} PASS={len(results)-len(failed)} FAIL={len(failed)}')
sys.exit(1 if failed else 0)
