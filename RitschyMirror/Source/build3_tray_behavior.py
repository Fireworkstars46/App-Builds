from pathlib import Path
import os
root=Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new, count=1):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=count:
        raise RuntimeError(f"{path}: anchor count {n}, expected {count}: {old[:120]!r}")
    p.write_text(s.replace(old,new,count),encoding="utf-8")
    print("patched", path)

# TrayContext comprehensive behavior and diagnostics.
patch('TrayContext.cs',
'''    private readonly ToolStripMenuItem _settingsMinimizeTrayItem;
''',
'''    private readonly ToolStripMenuItem _settingsMinimizeTrayItem;
    private readonly ToolStripMenuItem _debugModeItem;
    private readonly ToolStripMenuItem _safeSelfTestItem;
    private readonly ToolStripMenuItem _notificationsItem;
    private readonly ExplorerRecoveryWindow _explorerRecovery;
''')
patch('TrayContext.cs',
'''    [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    // Single-Instance''',
'''    [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);
    [System.Runtime.InteropServices.DllImport("user32.dll", CharSet = System.Runtime.InteropServices.CharSet.Unicode)]
    private static extern uint RegisterWindowMessage(string lpString);

    private sealed class ExplorerRecoveryWindow : NativeWindow, IDisposable
    {
        private readonly uint _taskbarCreated;
        private readonly Action _recover;
        public ExplorerRecoveryWindow(Action recover)
        {
            _recover = recover;
            _taskbarCreated = RegisterWindowMessage("TaskbarCreated");
            CreateHandle(new CreateParams { Caption = "RitschyMirror.TrayRecovery" });
        }
        protected override void WndProc(ref Message m)
        {
            if (_taskbarCreated != 0 && unchecked((uint)m.Msg) == _taskbarCreated) _recover();
            base.WndProc(ref m);
        }
        public void Dispose() { try { DestroyHandle(); } catch { } }
    }

    // Single-Instance''')
patch('TrayContext.cs',
'''        menu.Items.Add(new ToolStripMenuItem("Open log", null, (_, _) => OpenLog()));
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(new ToolStripMenuItem("Exit", null, (_, _) => Quit()));''',
'''        _debugModeItem = new ToolStripMenuItem("Debug Mode: OFF", null, (_, _) => ToggleDebugMode());
        menu.Items.Add(_debugModeItem);
        _safeSelfTestItem = new ToolStripMenuItem("Run Safe Self-Test", null, (_, _) => RunSafeSelfTest());
        menu.Items.Add(_safeSelfTestItem);
        _notificationsItem = new ToolStripMenuItem("Tray notifications: ON", null, (_, _) => ToggleNotifications());
        menu.Items.Add(_notificationsItem);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(new ToolStripMenuItem("Open Logs", null, (_, _) => OpenLog()));
        menu.Items.Add(new ToolStripMenuItem("Open Diagnostics", null, (_, _) => OpenDiagnostics()));
        menu.Items.Add(new ToolStripMenuItem("Export Logs / Diagnostic Report", null, (_, _) => ExportDiagnostics()));
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(new ToolStripMenuItem("Exit App", null, (_, _) => RequestFullAppExit("tray Exit App")));''')
patch('TrayContext.cs',
'''        _tray.BalloonTipClicked += (_, _) => { if (_pendingUpdateUrl != null) OpenUrl(_pendingUpdateUrl); };

        Win32Window.PreviewMinimizeSettingChanged += OnPreviewMinimizeSettingChanged;''',
'''        _tray.BalloonTipClicked += (_, _) => { if (_pendingUpdateUrl != null) OpenUrl(_pendingUpdateUrl); };
        _explorerRecovery = new ExplorerRecoveryWindow(() =>
        {
            try
            {
                _tray.Visible = false;
                _tray.Visible = true;
                _engine.Log("[TRAY] Explorer/taskbar restart detected; notification icon restored.");
            }
            catch (Exception ex) { _engine.Log("[TRAY] Explorer recovery failed: " + ex.Message); }
        });

        Win32Window.PreviewMinimizeSettingChanged += OnPreviewMinimizeSettingChanged;''')
patch('TrayContext.cs',
'''        _engine = new MirrorEngine(_baseDir);

        _iconOn = AppIcon.LoadStatus(running: true);''',
'''        _engine = new MirrorEngine(_baseDir);
        _engine.Log($"[STARTUP] {AppInfo.Name} {AppInfo.BuildLabel} starting.");
        _engine.Log("[SETTINGS] Loaded app_settings.json and mirror_config.json from the RitschyMirror application directory.");

        _iconOn = AppIcon.LoadStatus(running: true);''')
patch('TrayContext.cs',
'''                _tray.BalloonTipTitle = "RitschyMirror — Update available";
                _tray.BalloonTipText = $"Version {r.LatestVersion} is available. Click to open.";
                _tray.ShowBalloonTip(6000);''',
'''                ShowNotification(6000, "RitschyMirror — Update available",
                    $"Version {r.LatestVersion} is available. Click to open.", ToolTipIcon.Info);''')
patch('TrayContext.cs',
'''                _tray.ShowBalloonTip(4000, "RitschyMirror", err + ".", ToolTipIcon.Warning);''',
'''                ShowNotification(4000, "RitschyMirror", err + ".", ToolTipIcon.Warning);''')
patch('TrayContext.cs',
'''        // Direkt die Einstellungen oeffnen (z.B. eigene „Einstellungen"-Verknuepfung / Test).
        if (args != null && Array.Exists(args, a => string.Equals(a, "--settings", StringComparison.OrdinalIgnoreCase)))
            OpenSettings();

        StartUpdateCheck();''',
'''        // Explicit Settings shortcut always shows. Automatic startup opening is independently
        // configurable; StartMinimizedToTray preserves the old tray-only startup by default.
        bool explicitSettings = args != null && Array.Exists(args,
            a => string.Equals(a, "--settings", StringComparison.OrdinalIgnoreCase));
        if (explicitSettings)
            OpenSettings();
        else if (_app.OpenSettingsAtStartup)
        {
            OpenSettings();
            if (_app.StartMinimizedToTray) _settings?.HideMainSettingsToTray("startup setting");
        }

        StartUpdateCheck();''')
patch('TrayContext.cs',
'''            _settings.SyncMainSettingsMinimizeFromApp();
            // Explicit non-toggling restore;''',
'''            _settings.SyncMainSettingsMinimizeFromApp();
            _settings.SyncDebugModeFromConfig();
            // Explicit non-toggling restore;''')
patch('TrayContext.cs',
'''        _settings = new SettingsForm(_engine, _appSettingsPath, _app);
        // X on the MAIN Settings form also quits the entire app. Ignore
        // application-driven closes (for example during ExitThread).
        _settings.FormClosing += (_, e) =>
        {
            if (e.CloseReason == CloseReason.UserClosing && !_appExitRequested)
            {
                e.Cancel = true;
                RequestFullAppExit("Main Settings X");
            }
        };
        _settings.FormClosed += (_, _) => _settings = null;
        _settings.Show();''',
'''        _settings = new SettingsForm(_engine, _appSettingsPath, _app);
        _settings.ExitAppRequested += () => RequestFullAppExit("Settings Exit App button");
        _settings.SafeSelfTestRequested += RunSafeSelfTest;
        _settings.OpenLogsRequested += OpenLog;
        _settings.OpenDiagnosticsRequested += OpenDiagnostics;
        _settings.ExportDiagnosticsRequested += ExportDiagnostics;
        _settings.FormClosing += (_, e) =>
        {
            if (e.CloseReason == CloseReason.UserClosing && !_appExitRequested)
            {
                e.Cancel = true;
                if (_app.CloseSettingsToTray)
                    _settings?.HideMainSettingsToTray("Main Settings X setting");
                else
                    RequestFullAppExit("Main Settings X");
            }
        };
        _settings.FormClosed += (_, _) => _settings = null;
        _settings.Show();
        _engine.Log("[UI] Main Settings opened.");''')
patch('TrayContext.cs',
'''    /// <summary>
    /// Toggle taskbar BUTTON only; do not minimize, hide, or stop the''',
'''    private void ShowNotification(int timeout, string title, string text, ToolTipIcon icon)
    {
        if (!_app.NotificationsEnabled) return;
        try { _tray.ShowBalloonTip(timeout, title, text, icon); } catch { }
    }

    private void ToggleNotifications()
    {
        _app.NotificationsEnabled = !_app.NotificationsEnabled;
        _app.Save(_appSettingsPath);
        _engine.Log($"[SETTINGS] Tray notifications changed: enabled={_app.NotificationsEnabled}.");
        _settings?.SyncMainSettingsMinimizeFromApp();
        RefreshUi();
    }

    private void ToggleDebugMode()
    {
        try
        {
            bool next = !MirrorConfig.Load(_engine.ConfigPath).DebugLogging;
            MirrorConfig.MergePatch(_engine.ConfigPath,
                new System.Text.Json.Nodes.JsonObject { ["debug_logging"] = next });
            _engine.Log($"[DEBUG] Debug Mode changed: enabled={next}.");
            _settings?.SyncDebugModeFromConfig();
            RefreshUi();
        }
        catch (Exception ex) { _engine.Log("[DEBUG] Could not change Debug Mode: " + ex.Message); }
    }

    private void RunSafeSelfTest()
    {
        bool ok = DiagnosticsManager.RunSafeSelfTest(_baseDir, out string path, out string summary);
        _engine.Log($"[SELFTEST] {(ok ? "PASS" : "FAIL")}: {summary} Report={DiagnosticsManager.SanitizeText(path)}");
        ShowNotification(5000, "RitschyMirror Safe Self-Test", summary,
            ok ? ToolTipIcon.Info : ToolTipIcon.Warning);
    }

    private void OpenDiagnostics()
    {
        try
        {
            string dir = DiagnosticsManager.DiagnosticsDirectory(_baseDir);
            Directory.CreateDirectory(dir);
            Process.Start(new ProcessStartInfo("explorer.exe", $"\"{dir}\"") { UseShellExecute = true });
        }
        catch (Exception ex) { _engine.Log("[DIAGNOSTICS] Could not open diagnostics folder: " + ex.Message); }
    }

    private void ExportDiagnostics()
    {
        try
        {
            string zip = DiagnosticsManager.ExportLogsAndDiagnostics(_baseDir, _app,
                MirrorConfig.Load(_engine.ConfigPath), _engine.IsRunning);
            _engine.Log("[DIAGNOSTICS] Export created: " + DiagnosticsManager.SanitizeText(zip));
            Process.Start(new ProcessStartInfo("explorer.exe", $"/select,\"{zip}\"") { UseShellExecute = true });
        }
        catch (Exception ex)
        {
            _engine.Log("[DIAGNOSTICS] Export failed: " + ex.Message);
            ShowNotification(5000, "RitschyMirror diagnostics", "Diagnostic export failed.", ToolTipIcon.Warning);
        }
    }

    /// <summary>
    /// Toggle taskbar BUTTON only; do not minimize, hide, or stop the''')
patch('TrayContext.cs',
'''        bool running = _engine.IsRunning;
        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";
        bool taskbarIsHidden = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;''',
'''        bool running = _engine.IsRunning;
        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";
        var liveCfg = MirrorConfig.Load(_engine.ConfigPath);
        _debugModeItem.Checked = liveCfg.DebugLogging;
        _debugModeItem.Text = liveCfg.DebugLogging ? "Debug Mode: ON (click for OFF)" : "Debug Mode: OFF (click for ON)";
        _notificationsItem.Checked = _app.NotificationsEnabled;
        _notificationsItem.Text = _app.NotificationsEnabled ? "Tray notifications: ON (click for OFF)" : "Tray notifications: OFF (click for ON)";
        _settings?.SyncDebugModeFromConfig();
        bool taskbarIsHidden = liveCfg.HidePreviewTaskbarButton;''')
patch('TrayContext.cs',
'''        bool minimizeToTray = MirrorConfig.Load(_engine.ConfigPath).MinimizePreviewToTray;''',
'''        bool minimizeToTray = liveCfg.MinimizePreviewToTray;''')
patch('TrayContext.cs',
'''            bool hideTaskbarButton = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;''',
'''            bool hideTaskbarButton = liveCfg.HidePreviewTaskbarButton;''')
patch('TrayContext.cs',
'''        _uiTimer.Stop();
        Win32Window.PreviewMinimizeSettingChanged -= OnPreviewMinimizeSettingChanged;''',
'''        _engine.Log("[SHUTDOWN] RitschyMirror shutdown started.");
        _uiTimer.Stop();
        Win32Window.PreviewMinimizeSettingChanged -= OnPreviewMinimizeSettingChanged;''')
patch('TrayContext.cs',
'''        _tray.Visible = false;
        _tray.Dispose();
        try { _marshal.Dispose(); } catch { }
        ExitThread();''',
'''        _tray.Visible = false;
        _tray.Dispose();
        try { _explorerRecovery.Dispose(); } catch { }
        try { _marshal.Dispose(); } catch { }
        _engine.Log("[SHUTDOWN] RitschyMirror shutdown complete.");
        ExitThread();''')

print('Build 3 tray patch complete')
