"""Tray controls for the preview window (OBS Projector 3).

The app has an existing NotifyIcon/long-running TrayContext. This adds explicit
Show preview and Hide preview to tray controls. In normal framed windowed mode
the native Minimize button hides only the preview HWND and leaves the app and
mirror service alive in the existing notification area. Restoring from the
tray uses PostMessage to the actual native HWND-owning UI thread, never
cross-thread ShowWindow or DestroyWindow. Do not create another NotifyIcon,
duplicate process, second preview HWND, or alter monitor configuration.

Windows decides if an app's existing tray icon stays in the visible
notification area; users can pin it by dragging it out of the ^ overflow.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, got {n}: {old[:130]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print("Patched",path)

patch("Win32Window.cs",
'''    public IntPtr PresentationHwnd => _videoSurfaceHwnd != IntPtr.Zero ? _videoSurfaceHwnd : Hwnd;

    // Run exclusively''',
'''    public IntPtr PresentationHwnd => _videoSurfaceHwnd != IntPtr.Zero ? _videoSurfaceHwnd : Hwnd;

    // The existing tray icon remains owned by TrayContext; no secondary icon
    // or cloned mirror session is created. FindWindow searches TOP-LEVEL
    // windows only, so it does not accidentally target the embedded child
    // video surface that shares the same registered Win32 class.
    private const uint WmPreviewTrayVisibility = 0x8051; // WM_APP + 0x51

    public static bool PreviewExists =>
        FindWindow(ClassName, "RitschyMirror") != IntPtr.Zero;

    public static bool PreviewHidden
    {
        get
        {
            IntPtr h = FindWindow(ClassName, "RitschyMirror");
            return h != IntPtr.Zero && !IsWindowVisible(h);
        }
    }

    public static bool RequestPreviewVisibility(bool show)
    {
        IntPtr h = FindWindow(ClassName, "RitschyMirror");
        return h != IntPtr.Zero &&
               PostMessage(h, WmPreviewTrayVisibility,
                           show ? new IntPtr(1) : IntPtr.Zero, IntPtr.Zero);
    }

    // Run exclusively''')

patch("Win32Window.cs",
'''            case 0x0010: // WM_CLOSE''',
'''            case WmPreviewTrayVisibility:
                // This executes on the preview's true owning UI thread.
                // SW_HIDE takes it out of the taskbar, without destroying the
                // DXGI swapchain or exiting the mirror render loop.
                if (wParam != IntPtr.Zero)
                {
                    ShowWindow(hWnd, 9 /*SW_RESTORE*/);
                    ShowWindow(hWnd, 5 /*SW_SHOW*/);
                    SetForegroundWindow(hWnd);
                }
                else
                {
                    ShowWindow(hWnd, 0 /*SW_HIDE*/);
                }
                return IntPtr.Zero;
            case 0x0112: // WM_SYSCOMMAND
                if (NativeMoveResize &&
                    (wParam.ToInt64() & 0xFFF0L) == 0xF020L /*SC_MINIMIZE*/)
                {
                    // In the normal framed preview, the real Windows
                    // minimize button now hides to the existing tray.
                    // Close still stops only the preview as before.
                    ShowWindow(hWnd, 0 /*SW_HIDE*/);
                    return IntPtr.Zero;
                }
                break;
            case 0x0010: // WM_CLOSE''')

patch("Win32Window.cs",
'''    [DllImport("user32.dll")] private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);''',
'''    [DllImport("user32.dll")] private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")] private static extern bool IsWindowVisible(IntPtr hWnd);
    // PostMessage is already declared by native_live_ui_thread.py.
    [DllImport("user32.dll")] private static extern bool SetForegroundWindow(IntPtr hWnd);''')

patch("TrayContext.cs",
'''    private readonly ToolStripMenuItem _toggleItem;
    private readonly System.Windows.Forms.Timer _uiTimer;''',
'''    private readonly ToolStripMenuItem _toggleItem;
    private readonly ToolStripMenuItem _showPreviewItem;
    private readonly ToolStripMenuItem _hidePreviewItem;
    private readonly System.Windows.Forms.Timer _uiTimer;''')

patch("TrayContext.cs",
'''        menu.Items.Add(_toggleItem);
        menu.Items.Add(new ToolStripMenuItem("Settings…",''',
'''        menu.Items.Add(_toggleItem);
        _showPreviewItem = new ToolStripMenuItem("Show preview", null,
            (_, _) => Win32Window.RequestPreviewVisibility(true));
        _hidePreviewItem = new ToolStripMenuItem("Hide preview to tray", null,
            (_, _) => Win32Window.RequestPreviewVisibility(false));
        menu.Items.Add(_showPreviewItem);
        menu.Items.Add(_hidePreviewItem);
        menu.Items.Add(new ToolStripMenuItem("Settings",''')

patch("TrayContext.cs",
'''        _tray.DoubleClick += (_, _) => OpenSettings();''',
'''        _tray.DoubleClick += (_, _) =>
        {
            // Bring back a preview hidden using the actual Minimize button.
            // When the preview is already on screen, retain the established
            // double-click shortcut for Settings.
            if (Win32Window.PreviewHidden)
                Win32Window.RequestPreviewVisibility(true);
            else
                OpenSettings();
        };''')

patch("TrayContext.cs",
'''        _toggleItem.Text = running ? "Stop mirroring" : "Start mirroring";''',
'''        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";
        bool hasPreview = Win32Window.PreviewExists;
        bool hidden = hasPreview && Win32Window.PreviewHidden;
        _showPreviewItem.Enabled = hasPreview && hidden;
        _hidePreviewItem.Enabled = hasPreview && !hidden;''')

patch("SettingsForm.cs",
'''        Note("Fit layout's picture and black padding update continuously to match live window size.");''',
'''        Note("Fit layout's picture and black padding update continuously to match live window size.");
        Note("Minimize the normal Windows preview to the tray; restore it from the tray's Show preview menu.");''')

print("Added working tray Show/Hide preview menu and native Minimize-to-tray for the existing single-instance icon")
