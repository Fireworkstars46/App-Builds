"""Two double-clicks on the EXISTING tray icon open the video preview.

First double-click shows/restores main Settings, as before.
A SECOND double-click on the same icon within 10 seconds shows/restores the
renderer preview. If renderer X stopped mirroring, it first starts the engine;
the next tray UI tick activates the new preview once its HWND exists.
Single left-click continues to restore Settings; right-click context menu
unchanged. Keep main Settings X full-exit and renderer X preview-only.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected exactly 1 anchor, found {n}: {old[:150]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("TrayContext.cs",
'''    private bool _appExitRequested;''',
'''    private bool _appExitRequested;
    // Two distinct DoubleClick events (four mouse clicks) on the same
    // notification icon. This is a short gesture, not a permanent toggle.
    private DateTime _lastTrayDoubleClickUtc = DateTime.MinValue;
    private bool _previewShowPendingFromTray;''')

patch("TrayContext.cs",
'''        _tray.DoubleClick += (_, _) => OpenSettings();''',
'''        _tray.DoubleClick += (_, _) =>
        {
            var now = DateTime.UtcNow;
            bool secondDoubleClick = (now - _lastTrayDoubleClickUtc)
                <= TimeSpan.FromSeconds(10);
            _lastTrayDoubleClickUtc = secondDoubleClick
                ? DateTime.MinValue : now;
            if (secondDoubleClick)
                ShowOrStartPreviewFromTray();
            else
                OpenSettings();
        };''')

patch("TrayContext.cs",
'''    private void ToggleMainSettingsMinimizeToTray()
    {''',
'''    private void ShowOrStartPreviewFromTray()
    {
        // A second double-click always SHOWS the preview, never toggles or
        // minimizes either window. The renderer may have been hidden by its
        // minus button or fully STOPPED by its own X button.
        if (Win32Window.PreviewExists)
        {
            _previewShowPendingFromTray = false;
            if (!Win32Window.RequestPreviewVisibility(true))
                _engine.Log("[TRAY] Could not send Show preview to its native window.");
            return;
        }
        _previewShowPendingFromTray = true;
        if (!_engine.IsRunning)
        {
            var err = _engine.Preflight();
            if (err != null)
            {
                _previewShowPendingFromTray = false;
                _engine.Log("[TRAY] Could not start preview from second double-click: " + err);
                _tray.ShowBalloonTip(4000, "RitschyMirror", err + ".", ToolTipIcon.Warning);
                return;
            }
            _engine.Start();
            _engine.Log("[TRAY] Second double-click started mirroring to reopen preview.");
        }
        // If the engine is starting / reinitializing, wait for its HWND
        // instead of creating a duplicate mirror session.
        RefreshUi();
    }

    private void ToggleMainSettingsMinimizeToTray()
    {''')

patch("TrayContext.cs",
'''    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''',
'''    private void RefreshUi()
    {
        // MirrorEngine.Start creates the native preview asynchronously.
        // Once it exists, fulfill the pending second double-click exactly
        // once; otherwise the window could be left hidden on the HDMI monitor.
        if (_previewShowPendingFromTray && Win32Window.PreviewExists)
        {
            if (Win32Window.RequestPreviewVisibility(true))
                _previewShowPendingFromTray = false;
        }
        bool running = _engine.IsRunning;''')

print("Tray single-click restores Settings; first double-click shows Settings; second double-click within 10 s shows or starts preview, without toggling minimize.")
