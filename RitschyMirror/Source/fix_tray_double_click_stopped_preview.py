"""Fix tray preview double-click unexpectedly restarting stopped mirroring.

A SECOND double-click is RESTORE ONLY: show the renderer window if there
is an existing, actively running mirror session AND its native preview HWND
still exists. When mirroring is stopped (e.g. preview X), do nothing: only
the explicit Start mirror control is allowed to begin a new session.
A first double-click still opens/restores main Settings. No pending
auto-show after Start, and no change to either X/minimize behavior.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path;s=p.read_text(encoding="utf-8");n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {n}: {old[:160]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("TrayContext.cs",
'''    private DateTime _lastTrayDoubleClickUtc = DateTime.MinValue;
    private bool _previewShowPendingFromTray;''',
'''    private DateTime _lastTrayDoubleClickUtc = DateTime.MinValue;''')

patch("TrayContext.cs",
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
    }''',
'''    private void ShowOrStartPreviewFromTray()
    {
        // Restore the EXISTING running renderer only. Preview X is an
        // intentional STOP; tray double-click must never override it by
        // starting a new mirror session (or showing a stale closing HWND).
        if (!_engine.IsRunning || !Win32Window.PreviewExists)
        {
            _engine.Log("[TRAY] Second double-click: preview not running; leave mirroring stopped.");
            return;
        }
        if (!Win32Window.RequestPreviewVisibility(true))
            _engine.Log("[TRAY] Could not restore the existing preview window.");
    }''')

patch("TrayContext.cs",
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
        bool running = _engine.IsRunning;''',
'''    private void RefreshUi()
    {
        bool running = _engine.IsRunning;''')

print("Tray second double-click now restores a RUNNING preview only; stopped mirroring remains stopped until explicit Start.")
