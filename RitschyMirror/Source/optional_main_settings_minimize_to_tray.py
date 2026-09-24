"""Independent ON/OFF Minimize-to-Tray for the MAIN Settings form.

The renderer preview already has its own "Minimize preview to tray" option in
mirror_config.json. This patch adds a separate app_settings.json choice for
the ordinary WinForms main Settings window. It does not conflate/minimize the
renderer, hide extended HDMI output, or alter preview taskbar visibility.

Settings checkbox and existing tray menu share the same AppSettings object.
The tray's Settings action and double click can restore a hidden/minimized
SettingsForm instead of only calling Activate() on an invisible window.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])
def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected unique anchor, got {n}: {old[:145]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("AppSettings.cs",
'''    [JsonPropertyName("autostart_mirror")] public bool AutostartMirror { get; set; } = false;''',
'''    [JsonPropertyName("autostart_mirror")] public bool AutostartMirror { get; set; } = false;
    // Main WinForms Settings window only. Distinct from the native renderer's
    // mirror_config.json "minimize_preview_to_tray" switch.
    [JsonPropertyName("minimize_settings_to_tray")]
    public bool MinimizeSettingsToTray { get; set; } = false;''')

patch("SettingsForm.cs",
'''    private readonly Panel _panel;
    private int _y = 12;''',
'''    private readonly Panel _panel;
    private CheckBox _minimizeMainSettingsCheck = null!;
    private int _y = 12;''')

patch("SettingsForm.cs",
'''        MinimumSize = new Size(520, 420);
        // Auf kleinen/kurzen''',
'''        MinimumSize = new Size(520, 420);
        Resize += (_, _) =>
        {
            if (WindowState == FormWindowState.Minimized && _app.MinimizeSettingsToTray)
            {
                // Hide the MAIN Settings form only; RitschyMirror and its
                // projector HWND continue running. The tray host retains the
                // form instance and can restore it with the Settings action.
                Hide();
                _engine.Log("[TRAY] Main Settings window hidden by its Minimize button.");
            }
        };
        // Auf kleinen/kurzen''')

patch("SettingsForm.cs",
'''        Note("Agent-/Bind-/Port-Änderungen wirken nach App-Neustart.");
    }''',
'''        Note("Agent-/Bind-/Port-Änderungen wirken nach App-Neustart.");
        _minimizeMainSettingsCheck = CheckRow(
            "Minimize MAIN Settings window to tray when clicking —",
            _app.MinimizeSettingsToTray,
            v => _app.MinimizeSettingsToTray = v,
            app: true);
        Note("ON hides only this Settings window; OFF uses normal Windows minimize.");
        Note("Reopen it from the RitschyMirror tray icon > Open / Restore Settings.");
    }

    // Used by the tray host when the setting changes from the tray menu.
    // _loading protects the checkbox from saving/recursing during a sync.
    public void SyncMainSettingsMinimizeFromApp()
    {
        if (IsDisposed || _minimizeMainSettingsCheck == null) return;
        if (_minimizeMainSettingsCheck.Checked == _app.MinimizeSettingsToTray) return;
        bool prior = _loading;
        _loading = true;
        try { _minimizeMainSettingsCheck.Checked = _app.MinimizeSettingsToTray; }
        finally { _loading = prior; }
    }''')

patch("TrayContext.cs",
'''    private readonly ToolStripMenuItem _minimizeToTrayItem;''',
'''    private readonly ToolStripMenuItem _minimizeToTrayItem;
    private readonly ToolStripMenuItem _settingsMinimizeTrayItem;''')

patch("TrayContext.cs",
'''        menu.Items.Add(_minimizeToTrayItem);
        menu.Items.Add(new ToolStripMenuItem("Settings", null, (_, _) => OpenSettings()));''',
'''        menu.Items.Add(_minimizeToTrayItem);
        _settingsMinimizeTrayItem = new ToolStripMenuItem(
            "Minimize MAIN Settings window to tray: OFF",
            null, (_, _) => ToggleMainSettingsMinimizeToTray());
        menu.Items.Add(_settingsMinimizeTrayItem);
        menu.Items.Add(new ToolStripMenuItem("Open / Restore Settings", null,
            (_, _) => OpenSettings()));''')

patch("TrayContext.cs",
'''            // Bring back a preview hidden using the actual Minimize button.
            // When the preview is already on screen, retain the established
            // double-click shortcut for Settings.
            if (Win32Window.PreviewHidden)
                Win32Window.RequestPreviewVisibility(true);
            else
                OpenSettings();''',
'''            // If the main Settings form was hidden to tray, restore it first.
            // The explicit Show preview tray menu still restores the renderer.
            if (_settings is { IsDisposed: false, Visible: false })
                OpenSettings();
            else if (Win32Window.PreviewHidden)
                Win32Window.RequestPreviewVisibility(true);
            else
                OpenSettings();''')

patch("TrayContext.cs",
'''    private void OpenSettings()
    {
        if (_settings is { IsDisposed: false })
        {
            _settings.SyncTaskbarButtonFromConfig();
            _settings.Activate();
            return;
        }''',
'''    private void OpenSettings()
    {
        if (_settings is { IsDisposed: false })
        {
            _settings.SyncTaskbarButtonFromConfig();
            _settings.SyncMinimizeToTrayFromConfig();
            _settings.SyncMainSettingsMinimizeFromApp();
            // Activate alone cannot restore a minimized or hidden WinForms
            // Form. Restore its actual WindowState and visibility first.
            if (_settings.WindowState == FormWindowState.Minimized)
                _settings.WindowState = FormWindowState.Normal;
            if (!_settings.Visible)
                _settings.Show();
            _settings.Activate();
            return;
        }''')

patch("TrayContext.cs",
'''    private void ToggleMinimizeToTraySetting()
    {''',
'''    private void ToggleMainSettingsMinimizeToTray()
    {
        _app.MinimizeSettingsToTray = !_app.MinimizeSettingsToTray;
        _app.Save(_appSettingsPath);
        _settings?.SyncMainSettingsMinimizeFromApp();
        _engine.Log($"[TRAY] Main Settings minimize-to-tray: enabled={_app.MinimizeSettingsToTray}.");
        RefreshUi();
    }

    private void ToggleMinimizeToTraySetting()
    {''')

patch("TrayContext.cs",
'''        _minimizeToTrayItem.Text = minimizeToTray
            ? "Minimize preview to tray: ON (click for OFF)"
            : "Minimize preview to tray: OFF (click for ON)";
        _settings?.SyncMinimizeToTrayFromConfig();''',
'''        _minimizeToTrayItem.Text = minimizeToTray
            ? "Minimize preview to tray: ON (click for OFF)"
            : "Minimize preview to tray: OFF (click for ON)";
        _settings?.SyncMinimizeToTrayFromConfig();

        // The main Settings form and native projector are completely separate
        // windows and use independent minimize-to-tray preferences.
        _settingsMinimizeTrayItem.Checked = _app.MinimizeSettingsToTray;
        _settingsMinimizeTrayItem.Text = _app.MinimizeSettingsToTray
            ? "Minimize MAIN Settings window to tray: ON (click for OFF)"
            : "Minimize MAIN Settings window to tray: OFF (click for ON)";
        _settings?.SyncMainSettingsMinimizeFromApp();''')

print("Independent Settings-window minimize-to-tray switch added to main GUI and tray, with correct hidden-form restoration")
