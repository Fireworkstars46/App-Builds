import os
from pathlib import Path
root=Path(os.environ.get('RITSCHY_SOURCE','/mnt/data/ritschy_build4_proto2'))

def repl(name, old, new, count=1):
    p=root/name; s=p.read_text(encoding='utf-8')
    if s.count(old) < count:
        raise RuntimeError(f'{name}: missing anchor {old[:100]!r}')
    s=s.replace(old,new,count)
    p.write_text(s,encoding='utf-8')
    print('patched',name)

def write(name,text):
    (root/name).write_text(text,encoding='utf-8'); print('created',name)

# Backward-compatible main Settings window geometry. Build 3 files lack these keys,
# so defaults intentionally preserve the established centered-primary behavior.
repl('AppSettings.cs',
'''    [JsonPropertyName("notifications_enabled")]
    public bool NotificationsEnabled { get; set; } = true;''',
'''    [JsonPropertyName("notifications_enabled")]
    public bool NotificationsEnabled { get; set; } = true;
    [JsonPropertyName("settings_x")] public int SettingsX { get; set; } = int.MinValue;
    [JsonPropertyName("settings_y")] public int SettingsY { get; set; } = int.MinValue;
    [JsonPropertyName("settings_width")] public int SettingsWidth { get; set; } = 0;
    [JsonPropertyName("settings_height")] public int SettingsHeight { get; set; } = 0;
    [JsonPropertyName("settings_maximized")] public bool SettingsMaximized { get; set; } = false;''')

write('SettingsWindowLayout.cs', r'''using System.Drawing;
using System.Windows.Forms;

namespace RitschyMirror;

/// <summary>Main Settings window geometry through one production path.</summary>
internal static class SettingsWindowLayout
{
    private static Rectangle PrimaryDefault(Form form)
    {
        Rectangle wa = Screen.PrimaryScreen?.WorkingArea ?? new Rectangle(0, 0, 800, 600);
        int w = Math.Min(620, Math.Max(form.MinimumSize.Width, wa.Width - 24));
        int h = Math.Min(780, Math.Max(form.MinimumSize.Height, wa.Height - 24));
        int x = wa.Left + Math.Max(0, (wa.Width - w) / 2);
        int y = wa.Top + Math.Max(0, (wa.Height - h) / 2);
        return new Rectangle(x, y, Math.Max(form.MinimumSize.Width, w), Math.Max(form.MinimumSize.Height, h));
    }

    private static Rectangle ClampToVisibleWorkingArea(Rectangle requested, Size minimum)
    {
        Screen? best = Screen.AllScreens.FirstOrDefault(s => s.WorkingArea.IntersectsWith(requested));
        best ??= Screen.PrimaryScreen ?? Screen.AllScreens.FirstOrDefault();
        Rectangle wa = best?.WorkingArea ?? new Rectangle(0, 0, 800, 600);
        int minW = Math.Min(Math.Max(1, minimum.Width), Math.Max(1, wa.Width));
        int minH = Math.Min(Math.Max(1, minimum.Height), Math.Max(1, wa.Height));
        int w = Math.Clamp(requested.Width, minW, Math.Max(minW, wa.Width));
        int h = Math.Clamp(requested.Height, minH, Math.Max(minH, wa.Height));
        int x = Math.Clamp(requested.X, wa.Left, Math.Max(wa.Left, wa.Right - w));
        int y = Math.Clamp(requested.Y, wa.Top, Math.Max(wa.Top, wa.Bottom - h));
        return new Rectangle(x, y, w, h);
    }

    public static void Restore(Form form, AppSettings app)
    {
        if (app.SettingsX == int.MinValue || app.SettingsY == int.MinValue ||
            app.SettingsWidth <= 0 || app.SettingsHeight <= 0)
            return;
        var saved = new Rectangle(app.SettingsX, app.SettingsY, app.SettingsWidth, app.SettingsHeight);
        form.StartPosition = FormStartPosition.Manual;
        form.Bounds = ClampToVisibleWorkingArea(saved, form.MinimumSize);
        if (app.SettingsMaximized) form.WindowState = FormWindowState.Maximized;
    }

    public static void CaptureAndSave(Form form, AppSettings app, string path)
    {
        Rectangle b = form.WindowState == FormWindowState.Normal ? form.Bounds : form.RestoreBounds;
        if (b.Width <= 0 || b.Height <= 0) return;
        Rectangle safe = ClampToVisibleWorkingArea(b, form.MinimumSize);
        app.SettingsX = safe.X; app.SettingsY = safe.Y;
        app.SettingsWidth = safe.Width; app.SettingsHeight = safe.Height;
        app.SettingsMaximized = form.WindowState == FormWindowState.Maximized;
        app.Save(path);
        var verify = AppSettings.Load(path);
        if (verify.SettingsX != app.SettingsX || verify.SettingsY != app.SettingsY ||
            verify.SettingsWidth != app.SettingsWidth || verify.SettingsHeight != app.SettingsHeight ||
            verify.SettingsMaximized != app.SettingsMaximized)
            throw new IOException("Settings window layout was not persisted.");
    }

    public static void Reset(Form form, AppSettings app, string path)
    {
        app.SettingsX = int.MinValue; app.SettingsY = int.MinValue;
        app.SettingsWidth = 0; app.SettingsHeight = 0; app.SettingsMaximized = false;
        app.Save(path);
        var verify = AppSettings.Load(path);
        if (verify.SettingsX != int.MinValue || verify.SettingsY != int.MinValue ||
            verify.SettingsWidth != 0 || verify.SettingsHeight != 0 || verify.SettingsMaximized)
            throw new IOException("Settings window layout reset was not persisted.");
        form.WindowState = FormWindowState.Normal;
        form.StartPosition = FormStartPosition.Manual;
        form.Bounds = PrimaryDefault(form);
    }
}
''')

# Restore and persist geometry through the real form lifecycle.
repl('SettingsForm.cs',
'''        bottom.Controls.Add(update, 0, 1);
        bottom.Controls.Add(exit, 1, 1);''',
'''        bottom.Controls.Add(update, 0, 1);
        bottom.Controls.Add(exit, 1, 1);

        SettingsWindowLayout.Restore(this, _app);
        ResizeEnd += (_, _) =>
        {
            try { SettingsWindowLayout.CaptureAndSave(this, _app, _appSettingsPath); }
            catch (Exception ex) { _engine.Log("[WINDOW] Main Settings layout save failed: " + ex.Message); }
        };
        FormClosing += (_, _) =>
        {
            try { SettingsWindowLayout.CaptureAndSave(this, _app, _appSettingsPath); }
            catch (Exception ex) { _engine.Log("[WINDOW] Main Settings layout save failed on close: " + ex.Message); }
        };''')

# Reset both remembered preview and main Settings layouts from explicit controls.
repl('SettingsForm.cs',
'''        var resetLayout = new Button { Text = "Reset Preview Window Layout", Location = new Point(LX, _y), Width = 220, Height = 30 };
        resetLayout.Click += (_, _) => ResetPreviewWindowLayout();
        _panel.Controls.Add(resetLayout);
        _y += 36;''',
'''        var resetLayout = new Button { Text = "Reset Preview Window Layout", Location = new Point(LX, _y), Width = 220, Height = 30 };
        resetLayout.Click += (_, _) => ResetPreviewWindowLayout();
        var resetSettingsLayout = new Button { Text = "Reset Settings Window Layout", Location = new Point(LX + 228, _y), Width = 220, Height = 30 };
        resetSettingsLayout.Click += (_, _) => ResetSettingsWindowLayout();
        _panel.Controls.Add(resetLayout);
        _panel.Controls.Add(resetSettingsLayout);
        _y += 36;''')

repl('SettingsForm.cs',
'''    internal void ResetPreviewWindowLayout()
    {
        try
        {
            SettingsActions.ResetPreviewWindowLayout(_engine.ConfigPath);
            _cfg = MirrorConfig.Load(_engine.ConfigPath);
            _engine.Log("[WINDOW] Preview window layout reset from Settings UI.");
        }
        catch (Exception ex)
        {
            _engine.Log("[WINDOW] Preview window layout reset failed: " + ex.Message);
        }
    }
''',
'''    internal void ResetPreviewWindowLayout()
    {
        try
        {
            SettingsActions.ResetPreviewWindowLayout(_engine.ConfigPath);
            _cfg = MirrorConfig.Load(_engine.ConfigPath);
            _engine.Log("[WINDOW] Preview window layout reset from Settings UI.");
        }
        catch (Exception ex)
        {
            _engine.Log("[WINDOW] Preview window layout reset failed: " + ex.Message);
        }
    }

    internal void ResetSettingsWindowLayout()
    {
        try
        {
            SettingsWindowLayout.Reset(this, _app, _appSettingsPath);
            _engine.Log("[WINDOW] Main Settings window layout reset from Settings UI.");
        }
        catch (Exception ex)
        {
            _engine.Log("[WINDOW] Main Settings window layout reset failed: " + ex.Message);
        }
    }
''')

repl('SettingsForm.cs',
'''    public void HideMainSettingsToTray(string reason)
    {
        if (IsDisposed) return;
        ShowInTaskbar = false;''',
'''    public void HideMainSettingsToTray(string reason)
    {
        if (IsDisposed) return;
        try { SettingsWindowLayout.CaptureAndSave(this, _app, _appSettingsPath); }
        catch (Exception ex) { _engine.Log("[WINDOW] Main Settings layout save failed before tray hide: " + ex.Message); }
        ShowInTaskbar = false;''')

# Expand functional Safe Self-Test coverage for geometry, actual settings hide/restore,
# diagnostics buttons, and explicit manual/interactive SKIPPED items.
diag=(root/'DiagnosticsManager.cs').read_text(encoding='utf-8')
diag=diag.replace(
'''                NotificationsEnabled = false,
            };''',
'''                NotificationsEnabled = false,
                SettingsX = 140, SettingsY = 160, SettingsWidth = 580, SettingsHeight = 700, SettingsMaximized = true,
            };''',1)
diag=diag.replace(
'''                app2.StartMinimizedToTray && !app2.OpenSettingsAtStartup && !app2.NotificationsEnabled)''',
'''                app2.StartMinimizedToTray && !app2.OpenSettingsAtStartup && !app2.NotificationsEnabled &&
                app2.SettingsX == 140 && app2.SettingsY == 160 && app2.SettingsWidth == 580 &&
                app2.SettingsHeight == 700 && app2.SettingsMaximized)''',1)

anchor='''                var issues = SettingsForm.ValidateUiLayoutContract().ToList();'''
insert='''                // Main Settings remembered X/Y/W/H and recovery use the same production layout helper.
                form.WindowState = FormWindowState.Normal;
                form.Bounds = new Rectangle(wa.Left + 20, wa.Top + 20,
                    Math.Min(Math.Max(form.MinimumSize.Width, 540), wa.Width),
                    Math.Min(Math.Max(form.MinimumSize.Height, 520), wa.Height));
                SettingsWindowLayout.CaptureAndSave(form, app, appPath);
                var layoutSaved = AppSettings.Load(appPath);
                if (layoutSaved.SettingsWidth == form.Width && layoutSaved.SettingsHeight == form.Height &&
                    layoutSaved.SettingsX == form.Left && layoutSaved.SettingsY == form.Top)
                    Pass("main Settings X/Y/W/H production capture persists and reloads");
                else Fail("main Settings X/Y/W/H production capture persists and reloads");

                layoutSaved.SettingsX = int.MaxValue / 2; layoutSaved.SettingsY = int.MaxValue / 2;
                layoutSaved.SettingsWidth = 580; layoutSaved.SettingsHeight = 520; layoutSaved.SettingsMaximized = false;
                layoutSaved.Save(appPath);
                SettingsWindowLayout.Restore(form, layoutSaved);
                if (Screen.AllScreens.Any(sc => sc.WorkingArea.IntersectsWith(form.Bounds)))
                    Pass("main Settings remembered layout recovers off-screen geometry to visible working area");
                else Fail("main Settings remembered layout recovers off-screen geometry to visible working area");

''' + anchor
if anchor not in diag: raise RuntimeError('Diagnostics geometry anchor missing')
diag=diag.replace(anchor,insert,1)

anchor='''                var agentBox = FindCheck("Enable HTTP agent");'''
insert='''                app.MinimizeSettingsToTray = true;
                app.Save(appPath);
                form.Show();
                form.HideMainSettingsToTray("Safe Self-Test");
                bool hiddenToTray = !form.Visible && !form.ShowInTaskbar;
                form.RestoreMainSettingsFromTray();
                bool restored = form.Visible && form.ShowInTaskbar && form.WindowState != FormWindowState.Minimized;
                form.Hide();
                if (hiddenToTray && restored) Pass("main Settings hide-to-tray and restore production methods change actual window visibility/taskbar state");
                else Fail("main Settings hide-to-tray and restore production methods change actual window visibility/taskbar state",
                          $"hidden={hiddenToTray}, restored={restored}");

''' + anchor
if anchor not in diag: raise RuntimeError('Diagnostics hide/restore anchor missing')
diag=diag.replace(anchor,insert,1)

anchor='''                bool exitRequested = false;
                form.ExitAppRequested += () => exitRequested = true;'''
insert='''                var resetSettingsButton = FindButton("Reset Settings Window Layout");
                resetSettingsButton?.PerformClick();
                var afterSettingsReset = AppSettings.Load(appPath);
                var primaryWa = Screen.PrimaryScreen?.WorkingArea ?? new Rectangle(0, 0, 800, 600);
                bool resetSentinel = afterSettingsReset.SettingsX == int.MinValue && afterSettingsReset.SettingsY == int.MinValue &&
                    afterSettingsReset.SettingsWidth == 0 && afterSettingsReset.SettingsHeight == 0 && !afterSettingsReset.SettingsMaximized;
                bool onPrimary = primaryWa.IntersectsWith(form.Bounds);
                if (resetSettingsButton != null && resetSentinel && onPrimary)
                    Pass("Reset Settings Window Layout button clears saved geometry and uses OS primary working area");
                else Fail("Reset Settings Window Layout button clears saved geometry and uses OS primary working area",
                          $"button={resetSettingsButton != null}, sentinel={resetSentinel}, primary={onPrimary}");

                int safeRequests = 0, logRequests = 0, diagRequests = 0, exportRequests = 0;
                form.SafeSelfTestRequested += () => safeRequests++;
                form.OpenLogsRequested += () => logRequests++;
                form.OpenDiagnosticsRequested += () => diagRequests++;
                form.ExportDiagnosticsRequested += () => exportRequests++;
                FindButton("Run Safe Self-Test")?.PerformClick();
                FindButton("Open Logs")?.PerformClick();
                FindButton("Open Diagnostics")?.PerformClick();
                FindButton("Export Logs / Diagnostic Report")?.PerformClick();
                if (safeRequests == 1 && logRequests == 1 && diagRequests == 1 && exportRequests == 1)
                    Pass("Settings diagnostics buttons invoke their production request events exactly once");
                else Fail("Settings diagnostics buttons invoke their production request events exactly once",
                          $"self={safeRequests}, logs={logRequests}, diag={diagRequests}, export={exportRequests}");

                bool exitRequested = false;
                form.ExitAppRequested += () => exitRequested = true;'''
if anchor not in diag: raise RuntimeError('Diagnostics exit anchor missing')
diag=diag.replace(anchor,insert,1)

diag=diag.replace(
'''            Skip("physical NotifyIcon event timing and focus-dismiss behavior", "logic is production-tested above; actual Explorer shell gesture remains interactive");''',
'''            Skip("physical NotifyIcon menu/click timing, menu focus-dismiss, and Ctrl+Alt+T global hotkey delivery", "production arbitration/setter logic is tested; actual Explorer shell/hotkey delivery is interactive and environment-dependent");
            Skip("Start/Stop, Restart display, preview X/minimize/show-hide and live immediate render-setting effects", "requires a real capture source/GPU/native preview window; exercising them in Safe Test Mode would start hardware rendering");
            Skip("Check for updates, repository link, Open Logs/Open Diagnostics shell-launch visuals", "would launch external network/shell UI; underlying request/diagnostic/export production paths are tested without external windows");''',1)
(root/'DiagnosticsManager.cs').write_text(diag,encoding='utf-8')
print('patched DiagnosticsManager.cs')
print('Build 4 MASTER_RULES layout/testing follow-up applied')
