"""User-clicked X in EITHER window exits RitschyMirror entirely.

The tray host is the single application lifetime owner. The WinForms main
Settings X requests host Quit on its own UI thread, and native video preview
WM_CLOSE notifies that same host without blocking the preview's independent
UI thread. The renderer's ordinary cleanup also sends WM_CLOSE: mark that
internal path first so a Stop / Restart (display), or a device reinit, does
NOT accidentally exit the entire app. Minimize-to-tray switches still affect
the MINUS buttons only. No process-kill shortcuts or forced exit.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path
    s=p.read_text(encoding="utf-8")
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {old[:165]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("Win32Window.cs",
'''    private Thread? _nativeUiThread;''',
'''    private Thread? _nativeUiThread;
    private volatile bool _engineInitiatedClose;
    // The tray host owns the process lifetime. On a genuine user close,
    // request an app exit on the WinForms UI thread; native preview UI
    // MUST NOT directly join the render thread or call Application.Exit.
    public static event Action? PreviewUserClosed;''')

patch("Win32Window.cs",
'''    public void Destroy()
    {
        if (_nativeUiThread is Thread ui && Thread.CurrentThread != ui)''',
'''    public void Destroy()
    {
        // Engine.Stop / Restart / device-loss cleanup uses WM_CLOSE to wake
        // the dedicated native UI thread. Suppress the user-X callback for
        // that INTERNAL WM_CLOSE, even if it is delivered asynchronously.
        _engineInitiatedClose = true;
        if (_nativeUiThread is Thread ui && Thread.CurrentThread != ui)''')

patch("Win32Window.cs",
'''            case 0x0010: // WM_CLOSE
                Running = false;
                DestroyWindow(hWnd);
                return IntPtr.Zero;''',
'''            case 0x0010: // WM_CLOSE
                // The user clicked the renderer X (or Alt+F4): shut down the
                // whole application. Internal renderer cleanup still posts
                // WM_CLOSE, but only after marking _engineInitiatedClose.
                if (!_engineInitiatedClose)
                {
                    try { PreviewUserClosed?.Invoke(); }
                    catch { /* Never crash the native HWND message pump. */ }
                }
                Running = false;
                DestroyWindow(hWnd);
                return IntPtr.Zero;''')

patch("TrayContext.cs",
'''    private bool? _lastRunning;          // nur bei Statuswechsel Icon tauschen''',
'''    private bool? _lastRunning;          // nur bei Statuswechsel Icon tauschen
    private bool _appExitRequested;''')

patch("TrayContext.cs",
'''        // Single-Instance: auf das „Einstellungen zeigen"-Signal einer zweiten Instanz lauschen.''',
'''        // Native renderer X originates on a SEPARATE HWND thread. Only the
        // WinForms tray UI thread may coordinate quitting both windows.
        Win32Window.PreviewUserClosed += OnRendererUserClosed;

        // Single-Instance: auf das „Einstellungen zeigen"-Signal einer zweiten Instanz lauschen.''')

patch("TrayContext.cs",
'''        _settings.FormClosed += (_, _) => _settings = null;
        _settings.Show();''',
'''        // X on the MAIN Settings form also quits the entire app. Ignore
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
        _settings.Show();''')

patch("TrayContext.cs",
'''    private void Quit()
    {
        _uiTimer.Stop();''',
'''    private void OnRendererUserClosed()
    {
        // Never stop/join MirrorEngine on its native HWND-owning UI thread:
        // renderer cleanup may need to join that same native thread.
        try { _marshal.BeginInvoke((Action)(() => RequestFullAppExit("Renderer X"))); }
        catch { /* Application may already be exiting. */ }
    }

    private void RequestFullAppExit(string source)
    {
        if (_appExitRequested) return;
        _appExitRequested = true;
        _engine.Log("[EXIT] Full app shutdown requested by " + source + ".");
        // BeginInvoke also defers quitting outside the FormClosing callback.
        // A second click while exiting is ignored by the guard above.
        try { _marshal.BeginInvoke((Action)Quit); } catch { Quit(); }
    }

    private void Quit()
    {
        if (!_appExitRequested) _appExitRequested = true;
        // Quit removes the native preview callback BEFORE Engine.Stop sends
        // its own internal WM_CLOSE. Stop/Restart on their own remain safe.
        Win32Window.PreviewUserClosed -= OnRendererUserClosed;
        _uiTimer.Stop();''')

print("X on main Settings or preview requests an orderly FULL app quit, but Stop/Restart and minus-button minimize retain their independent behavior")
