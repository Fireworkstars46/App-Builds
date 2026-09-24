"""Make renderer X stop ONLY the renderer while main Settings X still exits all.

After Both X Exit 1, native preview WM_CLOSE raised PreviewUserClosed,
which instructed TrayContext.Quit() and also closed the main Settings form.
For the requested semantics the renderer WM_CLOSE simply sets Running=false,
destroys its own HWND and lets the existing MirrorEngine session stop; it
must never ask the tray host to quit. The main Settings FormClosing handler
continues to request full app shutdown. Minimize-to-tray switches unchanged.
"""
import os
from pathlib import Path
root=Path(os.environ["RITSCHY_SOURCE"])
def patch(path,old,new):
    p=root/path;s=p.read_text(encoding="utf-8");n=s.count(old)
    if n!=1:raise RuntimeError(f"{path}: expected exactly one anchor, found {n}: {old[:150]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8");print("Patched",path)

patch("Win32Window.cs",
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
                return IntPtr.Zero;''',
'''            case 0x0010: // WM_CLOSE
                // Renderer/preview X (and Alt+F4) stop ONLY the current
                // mirroring session. Keep the WinForms main Settings window,
                // notification icon and tray host alive, so mirroring may be
                // started again without restarting RitschyMirror.
                Running = false;
                DestroyWindow(hWnd);
                return IntPtr.Zero;''')

patch("TrayContext.cs",
'''        Win32Window.PreviewUserClosed += OnRendererUserClosed;''',
'''        // Preview X intentionally does NOT request app shutdown.
        // Main Settings X retains the dedicated full-exit FormClosing handler.''')

patch("TrayContext.cs",
'''        Win32Window.PreviewUserClosed -= OnRendererUserClosed;''',
'''        // Renderer X closes just the preview; there is no exit callback
        // to detach from the native video window.''')

print("Renderer X stops ONLY mirroring; main Settings X still closes entire RitschyMirror app.")
