import os
from pathlib import Path
root = Path(os.environ['RITSCHY_SOURCE'])
def read(name): return (root/name).read_text(encoding='utf-8')
def write(name, text): (root/name).write_text(text, encoding='utf-8')
def repl(name, old, new, count=1):
    p=root/name; s=p.read_text(encoding='utf-8')
    if s.count(old) < count: raise RuntimeError(f'{name}: anchor missing: {old[:100]!r}')
    s=s.replace(old,new,count); p.write_text(s,encoding='utf-8'); print('patched',name)

# Atomic verified settings writes.
repl('AppSettings.cs',
'''    public void Save(string path)\n    {\n        try { File.WriteAllText(path, JsonSerializer.Serialize(this, WriteOpts)); } catch { }\n    }''',
'''    public void Save(string path)\n    {\n        SettingsPersistence.WriteTextAtomicVerified(path, JsonSerializer.Serialize(this, WriteOpts));\n    }''')

repl('MirrorConfig.cs',
'    public void Save(string path) => File.WriteAllText(path, JsonSerializer.Serialize(this, WriteOpts));',
'    public void Save(string path) => SettingsPersistence.WriteTextAtomicVerified(path, JsonSerializer.Serialize(this, WriteOpts));')
repl('MirrorConfig.cs',
'''        File.WriteAllText(path, current.ToJsonString(WriteOpts));\n        return current;''',
'''        SettingsPersistence.WriteTextAtomicVerified(path, current.ToJsonString(WriteOpts));\n        return JsonNode.Parse(File.ReadAllText(path)) as JsonObject\n            ?? throw new IOException("Merged mirror_config.json could not be read back.");''')

# Program: use event-before-mutex coordinator; initialize WinForms in self-test; shared exit primitive.
program = read('Program.cs')
program = program.replace('private const string MutexName = "RitschyMirror.SingleInstance.Mutex";',
                          'internal const string MutexName = "RitschyMirror.SingleInstance.Mutex";')
old = '''        if (safeSelfTest)\n        {\n            // Safe Test Mode never starts the agent, renderer, tray icon or global hotkey.\n            // It touches only a unique app-local Diagnostics/SelfTestTemp directory.\n            try\n            {\n                bool ok = DiagnosticsManager.RunSafeSelfTest(AppContext.BaseDirectory, out _, out _);\n                Environment.ExitCode = ok ? 0 : 2;\n            }\n            catch (Exception ex)\n            {\n                try { DiagnosticsManager.WriteCrashReport(AppContext.BaseDirectory, ex, "--safe-self-test"); } catch { }\n                Environment.ExitCode = 3;\n            }\n            return;\n        }'''
new = '''        bool selfTestExitChild = Array.Exists(args, a => string.Equals(a, "--safe-self-test-exit-child", StringComparison.OrdinalIgnoreCase));\n        if (safeSelfTest || selfTestExitChild)\n        {\n            // Safe Test Mode never starts the agent, renderer, tray icon or global hotkey.\n            try { SetProcessDpiAwarenessContext(new IntPtr(-4)); } catch { }\n            Application.EnableVisualStyles();\n            Application.SetCompatibleTextRenderingDefault(false);\n            if (selfTestExitChild)\n            {\n                using var timer = new System.Windows.Forms.Timer { Interval = 25 };\n                using var ctx = new ApplicationContext();\n                timer.Tick += (_, _) => { timer.Stop(); ExitApplicationContext(ctx); };\n                timer.Start();\n                Application.Run(ctx);\n                return;\n            }\n            try\n            {\n                bool ok = DiagnosticsManager.RunSafeSelfTest(AppContext.BaseDirectory, out _, out _);\n                Environment.ExitCode = ok ? 0 : 2;\n            }\n            catch (Exception ex)\n            {\n                try { DiagnosticsManager.WriteCrashReport(AppContext.BaseDirectory, ex, "--safe-self-test"); } catch { }\n                Environment.ExitCode = 3;\n            }\n            return;\n        }'''
if old not in program: raise RuntimeError('Program selftest anchor missing')
program=program.replace(old,new,1)
old2='''        // Single-Instance: läuft schon eine Kopie, bitten wir sie nur, die Einstellungen\n        // zu öffnen, und beenden uns. Verhindert doppelte Tray-Icons + Agent-Port-Konflikt.\n        using var mutex = new Mutex(initiallyOwned: true, MutexName, out bool createdNew);\n        if (!createdNew)\n        {\n            try { EventWaitHandle.OpenExisting(ShowSettingsEvent).Set(); } catch { }\n            return;\n        }'''
new2='''        // Single-instance coordinator creates the show event first so a relaunch\n        // during early startup cannot lose its restore request.\n        using var instance = new SingleInstanceCoordinator(MutexName, ShowSettingsEvent);\n        if (!instance.IsPrimary)\n        {\n            try { instance.SignalShowSettings(); } catch { }\n            return;\n        }'''
if old2 not in program: raise RuntimeError('Program mutex anchor missing')
program=program.replace(old2,new2,1)
program=program.replace('Application.Run(new TrayContext(args));\n        GC.KeepAlive(mutex);  // Mutex bis App-Ende am Leben halten',
                        'Application.Run(new TrayContext(args, instance.ShowSettingsEvent));\n        GC.KeepAlive(instance);  // Mutex/event remain alive until app exit')
program=program.replace('\n    }\n}', '\n    }\n\n    internal static void ExitApplicationContext(ApplicationContext context) => context.ExitThread();\n}', 1)
write('Program.cs', program)

# TrayContext: shared show event, click arbiter, startup plan, shared setters, common exit primitive.
tray=read('TrayContext.cs')
tray=tray.replace('    private DateTime _lastTrayDoubleClickUtc = DateTime.MinValue;\n', '')
tray=tray.replace('    private readonly ToolStripMenuItem _notificationsItem;\n', '    private readonly ToolStripMenuItem _notificationsItem;\n    private readonly TrayClickCoordinator _trayClickCoordinator;\n')
tray=tray.replace('    private EventWaitHandle? _showEvent;\n', '    private EventWaitHandle? _showEvent;\n    private readonly bool _ownsShowEvent;\n')
tray=tray.replace('    public TrayContext(string[]? args = null)\n    {', '    public TrayContext(string[]? args = null, EventWaitHandle? sharedShowEvent = null)\n    {')
old_handlers='''        // A left click of the existing notification icon ALWAYS raises\n        // (or restores) main Settings. Never toggle/hide it on a subsequent\n        // click; renderer restoration remains under Show preview.\n        _tray.MouseClick += (_, e) =>\n        {\n            if (e.Button == MouseButtons.Left) OpenSettings();\n        };\n        _tray.DoubleClick += (_, _) =>\n        {\n            var now = DateTime.UtcNow;\n            bool secondDoubleClick = (now - _lastTrayDoubleClickUtc)\n                <= TimeSpan.FromSeconds(10);\n            _lastTrayDoubleClickUtc = secondDoubleClick\n                ? DateTime.MinValue : now;\n            if (secondDoubleClick)\n                ShowOrStartPreviewFromTray();\n            else\n                OpenSettings();\n        };'''
new_handlers='''        // Defer a single click for the Windows double-click interval so the same\n        // physical double-click never runs both single- and double-click actions.\n        _trayClickCoordinator = new TrayClickCoordinator(OpenSettings, ShowOrStartPreviewFromTray);\n        _tray.MouseClick += (_, e) => _trayClickCoordinator.OnMouseClick(e.Button);\n        _tray.DoubleClick += (_, _) => _trayClickCoordinator.OnDoubleClick();'''
if old_handlers not in tray: raise RuntimeError('tray click handlers anchor missing')
tray=tray.replace(old_handlers,new_handlers,1)
old_show='''        // Single-Instance: auf das „Einstellungen zeigen"-Signal einer zweiten Instanz lauschen.\n        try\n        {\n            _showEvent = new EventWaitHandle(false, EventResetMode.AutoReset, Program.ShowSettingsEvent);\n            _showReg = ThreadPool.RegisterWaitForSingleObject(\n                _showEvent, (_, _) => { try { _marshal.BeginInvoke((Action)OpenSettings); } catch { } },\n                null, -1, executeOnlyOnce: false);\n        }\n        catch { /* ohne Signalisierung läuft die App trotzdem (Single-Instance via Mutex greift weiter) */ }'''
new_show='''        // Single-instance show signal is created by Program before the mutex decision,\n        // eliminating the early-startup lost-signal race.\n        try\n        {\n            _showEvent = sharedShowEvent ?? new EventWaitHandle(false, EventResetMode.AutoReset, Program.ShowSettingsEvent);\n            _ownsShowEvent = sharedShowEvent == null;\n            _showReg = ThreadPool.RegisterWaitForSingleObject(\n                _showEvent, (_, _) => { try { _marshal.BeginInvoke((Action)OpenSettings); } catch { } },\n                null, -1, executeOnlyOnce: false);\n        }\n        catch\n        {\n            _ownsShowEvent = false;\n            // Mutex still enforces single-instance behavior if the restore signal cannot be created.\n        }'''
if old_show not in tray: raise RuntimeError('tray show event anchor missing')
tray=tray.replace(old_show,new_show,1)
# Startup plan replaces autostart block + explicit settings block.
old_auto='''        if (_app.AutostartMirror)\n        {\n            var err = _engine.Preflight();\n            if (err == null) _engine.Start();\n            else _engine.Log("Automatic mirroring skipped: " + err);\n        }'''
new_auto='''        var startup = StartupBehavior.Resolve(_app, args);\n        if (startup.AutostartMirror)\n        {\n            var err = _engine.Preflight();\n            if (err == null) _engine.Start();\n            else _engine.Log("Automatic mirroring skipped: " + err);\n        }'''
if old_auto not in tray: raise RuntimeError('autostart block missing')
tray=tray.replace(old_auto,new_auto,1)
old_open='''        // Explicit Settings shortcut always shows. Automatic startup opening is independently\n        // configurable; StartMinimizedToTray preserves the old tray-only startup by default.\n        bool explicitSettings = args != null && Array.Exists(args,\n            a => string.Equals(a, "--settings", StringComparison.OrdinalIgnoreCase));\n        if (explicitSettings)\n            OpenSettings();\n        else if (_app.OpenSettingsAtStartup)\n        {\n            OpenSettings();\n            if (_app.StartMinimizedToTray) _settings?.HideMainSettingsToTray("startup setting");\n        }'''
new_open='''        // Startup decision is centralized so production behavior and Safe Self-Test\n        // exercise the same rules. Explicit --settings always shows normally.\n        if (startup.OpenSettings)\n        {\n            OpenSettings();\n            if (startup.HideSettingsToTray) _settings?.HideMainSettingsToTray("startup setting");\n        }'''
if old_open not in tray: raise RuntimeError('startup open block missing')
tray=tray.replace(old_open,new_open,1)
# Shared settings setters.
tray=tray.replace('''    private void ToggleNotifications()\n    {\n        _app.NotificationsEnabled = !_app.NotificationsEnabled;\n        _app.Save(_appSettingsPath);''', '''    private void ToggleNotifications()\n    {\n        try\n        {\n            SettingsActions.SetNotifications(_app, _appSettingsPath, !_app.NotificationsEnabled);''')
tray=tray.replace('''        _settings?.SyncMainSettingsMinimizeFromApp();\n        RefreshUi();\n    }\n\n    private void ToggleDebugMode()''', '''        _settings?.SyncMainSettingsMinimizeFromApp();\n            RefreshUi();\n        }\n        catch (Exception ex) { _engine.Log("[SETTINGS] Could not change tray notifications: " + ex.Message); }\n    }\n\n    private void ToggleDebugMode()''', 1)
tray=tray.replace('''            bool next = !MirrorConfig.Load(_engine.ConfigPath).DebugLogging;\n            MirrorConfig.MergePatch(_engine.ConfigPath,\n                new System.Text.Json.Nodes.JsonObject { ["debug_logging"] = next });''', '''            bool next = !MirrorConfig.Load(_engine.ConfigPath).DebugLogging;\n            SettingsActions.SetDebugLogging(_engine.ConfigPath, next);''')
tray=tray.replace('''            MirrorConfig.MergePatch(_engine.ConfigPath, new System.Text.Json.Nodes.JsonObject\n            {\n                ["hide_preview_taskbar_button"] = hideButton,\n            });\n            // MergePatch has a whitelist: verify the exact saved value before\n            // manipulating Windows so a failed save never flashes then reverts.\n            bool saved = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;\n            if (saved != hideButton)\n            {\n                _engine.Log("[TASKBAR] Could not persist taskbar button preference; leaving it unchanged.");\n                return;\n            }''', '''            SettingsActions.SetHidePreviewTaskbarButton(_engine.ConfigPath, hideButton);\n            bool saved = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;''')
tray=tray.replace('''    private void ToggleMainSettingsMinimizeToTray()\n    {\n        _app.MinimizeSettingsToTray = !_app.MinimizeSettingsToTray;\n        _app.Save(_appSettingsPath);''', '''    private void ToggleMainSettingsMinimizeToTray()\n    {\n        try\n        {\n            SettingsActions.SetMainSettingsMinimizeToTray(\n                _app, _appSettingsPath, !_app.MinimizeSettingsToTray);''')
tray=tray.replace('''        _engine.Log($"[TRAY] Main Settings minimize-to-tray: enabled={_app.MinimizeSettingsToTray}.");\n        RefreshUi();\n    }\n\n    private void ToggleMinimizeToTraySetting()''', '''            _engine.Log($"[TRAY] Main Settings minimize-to-tray: enabled={_app.MinimizeSettingsToTray}.");\n            RefreshUi();\n        }\n        catch (Exception ex) { _engine.Log("[TRAY] Main Settings minimize-to-tray toggle failed: " + ex.Message); }\n    }\n\n    private void ToggleMinimizeToTraySetting()''', 1)
tray=tray.replace('''            MirrorConfig.MergePatch(_engine.ConfigPath,\n                new System.Text.Json.Nodes.JsonObject\n                {\n                    ["minimize_preview_to_tray"] = next,\n                });\n            if (MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray != next)\n            {\n                _engine.Log("[TRAY] Minimize-to-tray toggle could not be saved.");\n                return;\n            }''', '''            SettingsActions.SetMinimizePreviewToTray(_engine.ConfigPath, next);''')
# Quit cleanup owns event conditionally and disposes click coordinator; shared exit helper.
tray=tray.replace('        try { _showEvent?.Dispose(); } catch { }', '        if (_ownsShowEvent) try { _showEvent?.Dispose(); } catch { }')
tray=tray.replace('        _tray.Visible = false;\n        _tray.Dispose();', '        _tray.Visible = false;\n        _trayClickCoordinator.Dispose();\n        _tray.Dispose();')
tray=tray.replace('        ExitThread();', '        Program.ExitApplicationContext(this);')
write('TrayContext.cs', tray)

# Native preview right-click uses same shared setter.
win=read('Win32Window.cs')
old_native='''            bool next = !MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray;\n            MirrorConfig.MergePatch(PreviewConfigPath,\n                new System.Text.Json.Nodes.JsonObject\n                {\n                    ["minimize_preview_to_tray"] = next,\n                });\n            if (MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray == next)\n                PreviewMinimizeSettingChanged?.Invoke();'''
new_native='''            bool next = !MirrorConfig.Load(PreviewConfigPath).MinimizePreviewToTray;\n            SettingsActions.SetMinimizePreviewToTray(PreviewConfigPath, next);\n            PreviewMinimizeSettingChanged?.Invoke();'''
if old_native not in win: raise RuntimeError('native minimize menu anchor missing')
win=win.replace(old_native,new_native,1)
write('Win32Window.cs',win)

# SettingsForm: use shared setters for duplicate controls, verified app save, login helper,
# and add Reset Preview Window Layout button.
settings=read('SettingsForm.cs')
settings=settings.replace('using Microsoft.Win32;\n', '')
settings=settings.replace('    private const string RunKey = @"Software\\Microsoft\\Windows\\CurrentVersion\\Run";\n', '')
settings=settings.replace('    private bool _minimizeEditedInSettings;\n', '    private bool _minimizeEditedInSettings;\n    private bool _debugEditedInSettings;\n    private bool _mainMinimizeEditedInSettings;\n    private bool _notificationsEditedInSettings;\n')
# SaveCfg special branches
anchor='''            if (_minimizeEditedInSettings)\n            {\n                bool minimizeToTray = _cfg.MinimizePreviewToTray;\n                MirrorConfig.MergePatch(_engine.ConfigPath,\n                    new System.Text.Json.Nodes.JsonObject\n                    {\n                        ["minimize_preview_to_tray"] = minimizeToTray,\n                    });\n                if (MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray != minimizeToTray)\n                    throw new IOException("Minimize-to-tray choice was not saved.");\n                _engine.Log($"[TRAY] Main Settings minimize-to-tray changed: enabled={minimizeToTray}.");\n                return;\n            }'''
replace='''            if (_minimizeEditedInSettings)\n            {\n                bool minimizeToTray = _cfg.MinimizePreviewToTray;\n                SettingsActions.SetMinimizePreviewToTray(_engine.ConfigPath, minimizeToTray);\n                _engine.Log($"[TRAY] Preview minimize-to-tray changed from Settings: enabled={minimizeToTray}.");\n                return;\n            }\n            if (_debugEditedInSettings)\n            {\n                bool debug = _cfg.DebugLogging;\n                SettingsActions.SetDebugLogging(_engine.ConfigPath, debug);\n                _engine.Log($"[DEBUG] Debug Mode changed from Settings: enabled={debug}.");\n                return;\n            }'''
if anchor not in settings: raise RuntimeError('Settings minimize SaveCfg branch missing')
settings=settings.replace(anchor,replace,1)
settings=settings.replace('''                MirrorConfig.MergePatch(_engine.ConfigPath,\n                    new System.Text.Json.Nodes.JsonObject\n                    {\n                        ["hide_preview_taskbar_button"] = hideButton,\n                    });\n                if (MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton != hideButton)\n                    throw new IOException("Taskbar button choice was not saved.");''', '''                SettingsActions.SetHidePreviewTaskbarButton(_engine.ConfigPath, hideButton);''')
settings=settings.replace('''        finally\n        {\n            _taskbarEditedInSettings = false;\n            _minimizeEditedInSettings = false;\n        }''', '''        finally\n        {\n            _taskbarEditedInSettings = false;\n            _minimizeEditedInSettings = false;\n            _debugEditedInSettings = false;\n        }''')
# SaveApp shared duplicate flags and catch verification.
old_saveapp='''    private void SaveApp()\n    {\n        if (_loading) return;\n        _app.Save(_appSettingsPath);\n        _engine.Log("[SETTINGS] app_settings.json saved from Settings UI.");\n    }'''
new_saveapp='''    private void SaveApp()\n    {\n        if (_loading) return;\n        try\n        {\n            if (_mainMinimizeEditedInSettings)\n                SettingsActions.SetMainSettingsMinimizeToTray(_app, _appSettingsPath, _app.MinimizeSettingsToTray);\n            else if (_notificationsEditedInSettings)\n                SettingsActions.SetNotifications(_app, _appSettingsPath, _app.NotificationsEnabled);\n            else\n            {\n                _app.Save(_appSettingsPath);\n                // Read-back proves the settings file remained parseable after the write.\n                _ = AppSettings.Load(_appSettingsPath);\n            }\n            _engine.Log("[SETTINGS] app_settings.json saved and verified from Settings UI.");\n        }\n        catch (Exception ex)\n        {\n            _engine.Log("[SETTINGS] app_settings.json save failed: " + ex.Message);\n            SyncMainSettingsMinimizeFromApp();\n        }\n        finally\n        {\n            _mainMinimizeEditedInSettings = false;\n            _notificationsEditedInSettings = false;\n        }\n    }'''
if old_saveapp not in settings: raise RuntimeError('SaveApp anchor missing')
settings=settings.replace(old_saveapp,new_saveapp,1)
# Reset button after preview remember note
reset_anchor='''        Note("Display/mode/bit depth/window changes require a restart.");\n        Note("Preview remembers the size you drag it to and restores it after maximizing.");'''
reset_new='''        Note("Display/mode/bit depth/window changes require a restart.");\n        Note("Preview remembers the size you drag it to and restores it after maximizing.");\n        var resetLayout = new Button { Text = "Reset Preview Window Layout", Location = new Point(LX, _y), Width = 220, Height = 30 };\n        resetLayout.Click += (_, _) => ResetPreviewWindowLayout();\n        _panel.Controls.Add(resetLayout);\n        _y += 36;\n        Note("Resets remembered preview X/Y/size/maximized state; your other settings stay unchanged.");'''
if reset_anchor not in settings: raise RuntimeError('reset layout insertion anchor missing')
settings=settings.replace(reset_anchor,reset_new,1)
# Duplicate control flags
settings=settings.replace('''        _debugModeCheck = CheckRow("Debug Mode (extra FPS, stall and repeated-screen logging)",\n                 _cfg.DebugLogging, v => _cfg.DebugLogging = v);''', '''        _debugModeCheck = CheckRow("Debug Mode (extra FPS, stall and repeated-screen logging)",\n                 _cfg.DebugLogging, v => { _cfg.DebugLogging = v; _debugEditedInSettings = true; });''')
settings=settings.replace('''        _notificationsCheck = CheckRow("Tray notifications", _app.NotificationsEnabled,\n            v => _app.NotificationsEnabled = v, app: true);''', '''        _notificationsCheck = CheckRow("Tray notifications", _app.NotificationsEnabled,\n            v => { _app.NotificationsEnabled = v; _notificationsEditedInSettings = true; }, app: true);''')
settings=settings.replace('''            _app.MinimizeSettingsToTray,\n            v => _app.MinimizeSettingsToTray = v,\n            app: true);''', '''            _app.MinimizeSettingsToTray,\n            v => { _app.MinimizeSettingsToTray = v; _mainMinimizeEditedInSettings = true; },\n            app: true);''',1)
# Login helpers delegate to shared verified production class.
old_login='''    private static bool IsLoginAutostart()\n    {\n        try { using var k = Registry.CurrentUser.OpenSubKey(RunKey); return k?.GetValue(RunValue) != null; }\n        catch { return false; }\n    }\n\n    private void SetLoginAutostart(bool on)\n    {\n        try\n        {\n            using var k = Registry.CurrentUser.OpenSubKey(RunKey, writable: true) ?? Registry.CurrentUser.CreateSubKey(RunKey);\n            if (on) k!.SetValue(RunValue, $"\\\"{Application.ExecutablePath}\\\"");\n            else k!.DeleteValue(RunValue, throwOnMissingValue: false);\n        }\n        catch (Exception ex) { _engine.Log("Could not set login startup: " + ex.Message); }\n    }'''
new_login='''    private static bool IsLoginAutostart()\n    {\n        try { return LoginAutostart.IsEnabled(RunValue); }\n        catch { return false; }\n    }\n\n    private void SetLoginAutostart(bool on)\n    {\n        try { LoginAutostart.SetEnabled(RunValue, on, Application.ExecutablePath); }\n        catch (Exception ex) { _engine.Log("Could not set login startup: " + ex.Message); }\n    }'''
if old_login not in settings: raise RuntimeError('login methods anchor missing')
settings=settings.replace(old_login,new_login,1)
# Add reset method before RestoreMainSettingsFromTray comment.
method_anchor='''    // Guard the Resize handler while unwinding a former minimize request.\n    public void RestoreMainSettingsFromTray()'''
method_new='''    internal void ResetPreviewWindowLayout()\n    {\n        try\n        {\n            SettingsActions.ResetPreviewWindowLayout(_engine.ConfigPath);\n            _cfg = MirrorConfig.Load(_engine.ConfigPath);\n            _engine.Log("[WINDOW] Preview window layout reset from Settings UI.");\n        }\n        catch (Exception ex)\n        {\n            _engine.Log("[WINDOW] Preview window layout reset failed: " + ex.Message);\n        }\n    }\n\n    // Guard the Resize handler while unwinding a former minimize request.\n    public void RestoreMainSettingsFromTray()'''
if method_anchor not in settings: raise RuntimeError('restore method anchor missing')
settings=settings.replace(method_anchor,method_new,1)
write('SettingsForm.cs', settings)


print('Build 4 MASTER_RULES core source patch applied')
