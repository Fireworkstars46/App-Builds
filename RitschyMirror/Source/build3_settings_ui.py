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

# Settings UI: build label, responsive bottom grid, new behavior settings, diagnostics controls.
patch('SettingsForm.cs',
'''    private CheckBox _minimizeMainSettingsCheck = null!;
    private bool _settingsRestoreInProgress;''',
'''    private CheckBox _minimizeMainSettingsCheck = null!;
    private CheckBox _debugModeCheck = null!;
    private CheckBox _closeSettingsToTrayCheck = null!;
    private CheckBox _startMinimizedCheck = null!;
    private CheckBox _openSettingsAtStartupCheck = null!;
    private CheckBox _notificationsCheck = null!;
    public event Action? ExitAppRequested;
    public event Action? SafeSelfTestRequested;
    public event Action? OpenLogsRequested;
    public event Action? OpenDiagnosticsRequested;
    public event Action? ExportDiagnosticsRequested;
    private bool _settingsRestoreInProgress;''')
patch('SettingsForm.cs',
'''        Text = $"RitschyMirror — Settings  v{AppInfo.Version}";
        Icon = AppIcon.Load(small: false);
        ClientSize = new Size(620, 780);
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(520, 420);''',
'''        Text = $"RitschyMirror — Settings  {AppInfo.BuildLabel}";
        Icon = AppIcon.Load(small: false);
        StartPosition = FormStartPosition.CenterScreen;
        var wa0 = Screen.PrimaryScreen?.WorkingArea ?? new Rectangle(0, 0, 800, 600);
        ClientSize = new Size(Math.Min(620, Math.Max(360, wa0.Width - 24)),
                              Math.Min(780, Math.Max(320, wa0.Height - 24)));
        MinimumSize = new Size(Math.Min(520, Math.Max(360, wa0.Width - 24)),
                               Math.Min(420, Math.Max(320, wa0.Height - 24)));''')
patch('SettingsForm.cs',
'''        var wa = Screen.PrimaryScreen?.WorkingArea;
        if (wa is { } a && Height > a.Height - 16) Height = a.Height - 16;

        _panel = new Panel { Dock = DockStyle.Fill, AutoScroll = true, Padding = new Padding(8) };
        var bottom = new Panel { Dock = DockStyle.Bottom, Height = 48, BackColor = SystemColors.ControlLight };
        Controls.Add(_panel);
        Controls.Add(bottom);

        _loading = true;
        BuildSourceTarget();
        BuildImage();
        BuildCrop();
        BuildConnection();
        BuildAbout();
        _loading = false;

        var start = new Button { Text = "Start / Stop", Location = new Point(12, 9), Width = 120, Height = 30 };
        start.Click += (_, _) => { if (_engine.IsRunning) _engine.Stop(); else StartWithCheck(); };
        var restart = new Button { Text = "Restart (display)", Location = new Point(140, 9), Width = 160, Height = 30 };
        restart.Click += (_, _) => { _engine.Stop(); StartWithCheck(); };
        var close = new Button { Text = "Close", Location = new Point(308, 9), Width = 110, Height = 30 };
        close.Click += (_, _) => Close();
        var update = new Button { Text = "↻ Check for updates", Location = new Point(426, 9), Width = 172, Height = 30 };
        update.Click += (_, _) => CheckForUpdates(update);
        bottom.Controls.AddRange(new Control[] { start, restart, close, update });''',
'''        var wa = Screen.PrimaryScreen?.WorkingArea;
        if (wa is { } a)
        {
            if (Height > a.Height - 16) Height = Math.Max(MinimumSize.Height, a.Height - 16);
            if (Width > a.Width - 16) Width = Math.Max(MinimumSize.Width, a.Width - 16);
        }

        _panel = new Panel { Dock = DockStyle.Fill, AutoScroll = true, Padding = new Padding(8) };
        var bottom = new TableLayoutPanel
        {
            Dock = DockStyle.Bottom,
            Height = 78,
            BackColor = SystemColors.Control,
            ColumnCount = 2,
            RowCount = 2,
            Padding = new Padding(6),
        };
        bottom.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
        bottom.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50));
        bottom.RowStyles.Add(new RowStyle(SizeType.Percent, 50));
        bottom.RowStyles.Add(new RowStyle(SizeType.Percent, 50));
        Controls.Add(_panel);
        Controls.Add(bottom);

        _loading = true;
        BuildSourceTarget();
        BuildImage();
        BuildCrop();
        BuildConnection();
        BuildDiagnostics();
        BuildAbout();
        _loading = false;

        Button BottomButton(string text) => new() { Text = text, Dock = DockStyle.Fill, Margin = new Padding(4) };
        var start = BottomButton("Start / Stop");
        start.Click += (_, _) => { if (_engine.IsRunning) _engine.Stop(); else StartWithCheck(); };
        var restart = BottomButton("Restart display");
        restart.Click += (_, _) => { _engine.Stop(); StartWithCheck(); };
        var update = BottomButton("Check for updates");
        update.Click += (_, _) => CheckForUpdates(update);
        var exit = BottomButton("Exit App");
        exit.Click += (_, _) => ExitAppRequested?.Invoke();
        bottom.Controls.Add(start, 0, 0);
        bottom.Controls.Add(restart, 1, 0);
        bottom.Controls.Add(update, 0, 1);
        bottom.Controls.Add(exit, 1, 1);''')
patch('SettingsForm.cs',
'''            _cfg.Save(_engine.ConfigPath);
            SyncTaskbarButtonFromConfig();''',
'''            _cfg.Save(_engine.ConfigPath);
            _engine.Log("[SETTINGS] mirror_config.json saved from Settings UI.");
            SyncTaskbarButtonFromConfig();''')
patch('SettingsForm.cs',
'''    private void SaveApp() { if (_loading) return; _app.Save(_appSettingsPath); }''',
'''    private void SaveApp()
    {
        if (_loading) return;
        _app.Save(_appSettingsPath);
        _engine.Log("[SETTINGS] app_settings.json saved from Settings UI.");
    }''')
patch('SettingsForm.cs',
'''        _panel.Controls.Add(new Label { Text = text, Location = new Point(LX, _y), AutoSize = true, ForeColor = Color.DimGray });''',
'''        _panel.Controls.Add(new Label
        {
            Text = text,
            Location = new Point(LX, _y),
            AutoSize = true,
            MaximumSize = new Size(560, 0),
            ForeColor = SystemColors.GrayText,
        });''')
patch('SettingsForm.cs',
'''        CheckRow("Debug logging (FPS, stalls and repeated-screen detection)",
                 _cfg.DebugLogging, v => _cfg.DebugLogging = v);''',
'''        _debugModeCheck = CheckRow("Debug Mode (extra FPS, stall and repeated-screen logging)",
                 _cfg.DebugLogging, v => _cfg.DebugLogging = v);
        Note("Debug Mode is OFF by default; normal warnings/errors still remain in the bounded log.");''')
patch('SettingsForm.cs',
'''        CheckRow("Start mirroring when app opens", _app.AutostartMirror, v => _app.AutostartMirror = v, app: true);
        var al = new CheckBox { Text = "Start app when signing in to Windows", Location = new Point(LX, _y), AutoSize = true, Checked = IsLoginAutostart() };''',
'''        CheckRow("Start mirroring when app opens", _app.AutostartMirror, v => _app.AutostartMirror = v, app: true);
        Note("OFF = start paused/stopped; ON = start the mirror automatically.");
        _openSettingsAtStartupCheck = CheckRow("Open Settings/main window at startup", _app.OpenSettingsAtStartup,
            v => _app.OpenSettingsAtStartup = v, app: true);
        _startMinimizedCheck = CheckRow("Start Settings minimized to tray when it is opened at startup", _app.StartMinimizedToTray,
            v => _app.StartMinimizedToTray = v, app: true);
        Note("Start Minimized only affects automatic startup opening; explicit Open Settings always shows it.");
        _notificationsCheck = CheckRow("Tray notifications", _app.NotificationsEnabled,
            v => _app.NotificationsEnabled = v, app: true);
        var al = new CheckBox { Text = "Start app when signing in to Windows", Location = new Point(LX, _y), AutoSize = true, Checked = IsLoginAutostart() };''')
patch('SettingsForm.cs',
'''        Note("ON hides only this Settings window; OFF uses normal Windows minimize.");
        Note("Reopen it from the RitschyMirror tray icon > Open / Restore Settings.");
    }
''',
'''        Note("ON hides only this Settings window; OFF uses normal Windows minimize.");
        Note("Reopen it from the RitschyMirror tray icon > Open / Restore Settings.");
        _closeSettingsToTrayCheck = CheckRow(
            "Main Settings X closes to tray instead of exiting the app",
            _app.CloseSettingsToTray,
            v => _app.CloseSettingsToTray = v,
            app: true);
        Note("OFF preserves Build 2 behavior: X exits RitschyMirror. Exit App always exits.");
    }
''')
patch('SettingsForm.cs',
'''    public void SyncMainSettingsMinimizeFromApp()
    {
        if (IsDisposed || _minimizeMainSettingsCheck == null) return;
        if (_minimizeMainSettingsCheck.Checked == _app.MinimizeSettingsToTray) return;
        bool prior = _loading;
        _loading = true;
        try { _minimizeMainSettingsCheck.Checked = _app.MinimizeSettingsToTray; }
        finally { _loading = prior; }
    }

    // ── Über / Update''',
'''    public void SyncMainSettingsMinimizeFromApp()
    {
        if (IsDisposed || _minimizeMainSettingsCheck == null) return;
        bool prior = _loading;
        _loading = true;
        try
        {
            _minimizeMainSettingsCheck.Checked = _app.MinimizeSettingsToTray;
            if (_closeSettingsToTrayCheck != null) _closeSettingsToTrayCheck.Checked = _app.CloseSettingsToTray;
            if (_startMinimizedCheck != null) _startMinimizedCheck.Checked = _app.StartMinimizedToTray;
            if (_openSettingsAtStartupCheck != null) _openSettingsAtStartupCheck.Checked = _app.OpenSettingsAtStartup;
            if (_notificationsCheck != null) _notificationsCheck.Checked = _app.NotificationsEnabled;
        }
        finally { _loading = prior; }
    }

    public void SyncDebugModeFromConfig()
    {
        if (IsDisposed || _debugModeCheck == null) return;
        bool saved = MirrorConfig.Load(_engine.ConfigPath).DebugLogging;
        bool prior = _loading;
        _loading = true;
        try { _cfg.DebugLogging = saved; _debugModeCheck.Checked = saved; }
        finally { _loading = prior; }
    }

    public void HideMainSettingsToTray(string reason)
    {
        if (IsDisposed) return;
        ShowInTaskbar = false;
        Hide();
        _engine.Log("[TRAY] Main Settings hidden to tray: " + reason + ".");
    }

    public static IEnumerable<string> ValidateUiLayoutContract()
    {
        if (LX < 0 || CX <= LX || ROW < 24) yield return "UI layout constants are invalid.";
        const int minimumContentWidth = 360;
        const int minimumContentHeight = 320;
        if (minimumContentWidth < 320 || minimumContentHeight < 280)
            yield return "UI minimum-size contract is invalid.";
    }

    private void BuildDiagnostics()
    {
        Header("Diagnostics / Safe Test");
        var run = new Button { Text = "Run Safe Self-Test", Location = new Point(LX, _y), Width = 180, Height = 30 };
        run.Click += (_, _) => SafeSelfTestRequested?.Invoke();
        var logs = new Button { Text = "Open Logs", Location = new Point(LX + 188, _y), Width = 150, Height = 30 };
        logs.Click += (_, _) => OpenLogsRequested?.Invoke();
        _panel.Controls.Add(run); _panel.Controls.Add(logs); _y += 36;
        var diag = new Button { Text = "Open Diagnostics", Location = new Point(LX, _y), Width = 180, Height = 30 };
        diag.Click += (_, _) => OpenDiagnosticsRequested?.Invoke();
        var export = new Button { Text = "Export Logs / Diagnostic Report", Location = new Point(LX + 188, _y), Width = 260, Height = 30 };
        export.Click += (_, _) => ExportDiagnosticsRequested?.Invoke();
        _panel.Controls.Add(diag); _panel.Controls.Add(export); _y += 38;
        Note("Safe Test Mode uses isolated app-local temporary settings and deletes them afterward.");
        Note("Diagnostic exports and crash reports are outside normal mirror.log rotation limits.");
    }

    // ── Über / Update''')
patch('SettingsForm.cs',
'''        Note($"{AppInfo.Name}  v{AppInfo.Version}");''',
'''        Note($"{AppInfo.Name}  {AppInfo.BuildLabel}");''')
