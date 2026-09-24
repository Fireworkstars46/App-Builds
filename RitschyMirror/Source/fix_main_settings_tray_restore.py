"""Fix main Settings form 'restore from tray then immediately hide again' race.

The WinForms Resize callback previously called Hide() SYNCHRONOUSLY while
Windows was still applying WS_MINIMIZE. Restoring a hidden form required
setting its WindowState while that same callback was live, causing transient
minimized/hidden state and stale taskbar buttons. Separate a deferred hide
from an explicit guarded restore; handle RitschyMirror notification icon
left-click as RESTORE, never a visibility toggle. This affects only the main
Settings WinForms form, not the HDMI renderer or either separate minus switch.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path;s=p.read_text(encoding="utf-8");n=s.count(old)
    if n!=1:raise RuntimeError(f"{path}: expected one anchor, found {n}: {old[:160]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8");print("Patched",path)

patch("SettingsForm.cs",
'''    private CheckBox _minimizeMainSettingsCheck = null!;
    private int _y = 12;''',
'''    private CheckBox _minimizeMainSettingsCheck = null!;
    private bool _settingsRestoreInProgress;
    private bool _settingsHidePending;
    private int _y = 12;''')

patch("SettingsForm.cs",
'''        Resize += (_, _) =>
        {
            if (WindowState == FormWindowState.Minimized && _app.MinimizeSettingsToTray)
            {
                // Hide the MAIN Settings form only; RitschyMirror and its
                // projector HWND continue running. The tray host retains the
                // form instance and can restore it with the Settings action.
                Hide();
                _engine.Log("[TRAY] Main Settings window hidden by its Minimize button.");
            }
        };''',
'''        Resize += (_, _) =>
        {
            if (_settingsRestoreInProgress || _settingsHidePending ||
                WindowState != FormWindowState.Minimized || !_app.MinimizeSettingsToTray)
                return;

            // Do NOT synchronously Hide() inside WinForms' Resize triggered
            // by the native minimize message: it can reenter state changes
            // and make the next tray restore appear to minimize again.
            _settingsHidePending = true;
            BeginInvoke((Action)(() =>
            {
                _settingsHidePending = false;
                if (IsDisposed || _settingsRestoreInProgress ||
                    !_app.MinimizeSettingsToTray ||
                    WindowState != FormWindowState.Minimized) return;
                // Remove the stale taskbar button while actually hidden.
                ShowInTaskbar = false;
                Hide();
                _engine.Log("[TRAY] Main Settings hidden to tray after minimize finished.");
            }));
        };''')

patch("SettingsForm.cs",
'''    // Used by the tray host when the setting changes from the tray menu.
    // _loading protects the checkbox from saving/recursing during a sync.
    public void SyncMainSettingsMinimizeFromApp()
    {''',
'''    // Only this method restores main Settings from the notification icon.
    // Make it unambiguously a SHOW action, never a click-to-toggle action.
    // Guard the Resize handler while unwinding a former minimize request.
    public void RestoreMainSettingsFromTray()
    {
        if (IsDisposed) return;
        _settingsRestoreInProgress = true;
        try
        {
            if (!ShowInTaskbar) ShowInTaskbar = true;
            if (!Visible) Show();
            if (WindowState == FormWindowState.Minimized)
                WindowState = FormWindowState.Normal;
            BringToFront();
            Activate();
            _engine.Log($"[TRAY] Main Settings restore requested: visible={Visible}, state={WindowState}.");
        }
        finally { _settingsRestoreInProgress = false; }
    }

    // Used by the tray host when the setting changes from the tray menu.
    // _loading protects the checkbox from saving/recursing during a sync.
    public void SyncMainSettingsMinimizeFromApp()
    {''')

patch("TrayContext.cs",
'''        _tray.DoubleClick += (_, _) =>
        {
            // If the main Settings form was hidden to tray, restore it first.
            // The explicit Show preview tray menu still restores the renderer.
            if (_settings is { IsDisposed: false, Visible: false })
                OpenSettings();
            else if (Win32Window.PreviewHidden)
                Win32Window.RequestPreviewVisibility(true);
            else
                OpenSettings();
        };''',
'''        // A left click of the existing notification icon ALWAYS raises
        // (or restores) main Settings. Never toggle/hide it on a subsequent
        // click; renderer restoration remains under Show preview.
        _tray.MouseClick += (_, e) =>
        {
            if (e.Button == MouseButtons.Left) OpenSettings();
        };
        _tray.DoubleClick += (_, _) => OpenSettings();''')

patch("TrayContext.cs",
'''            // Activate alone cannot restore a minimized or hidden WinForms
            // Form. Restore its actual WindowState and visibility first.
            if (_settings.WindowState == FormWindowState.Minimized)
                _settings.WindowState = FormWindowState.Normal;
            if (!_settings.Visible)
                _settings.Show();
            _settings.Activate();
            return;''',
'''            // Explicit non-toggling restore; the Form protects against
            // Resize/Hide reentrancy and clears the stale taskbar state.
            _settings.RestoreMainSettingsFromTray();
            return;''')

print("Main Settings tray Restore is now a guarded SHOW with deferred Hide and proper taskbar-button cleanup")
