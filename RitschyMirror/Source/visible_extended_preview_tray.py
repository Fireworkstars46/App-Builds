"""Keep the projector VISIBLE on an extended HDMI display while its TASKBAR
BUTTON is removed; the existing notification-area tray icon stays available.

Distinct from Tray Preview 1's 'Hide preview to tray' action: that hides the
entire projector. Here the projector remains a normal Windows top-level
window with the same frame, snap, capture, renderer, input and HDMI output.
We use the Windows Shell's ITaskbarList.DeleteTab rather than WS_EX_TOOLWINDOW:
changing the latter would alter the ordinary browser-like window caption,
system minimize/maximize buttons, and possibly snapping. The Shell taskbar
list call only controls its entry on the taskbar; it does not hide the HWND.

The existing TrayContext drives a small periodic reconciliation, so the
option works on an already-running mirror and after the preview is recreated.
The preview's owning native UI thread handles the message/COM operation; the
tray thread never directly manipulates another thread's window.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    f = root / path
    s = f.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, got {count}: {old[:120]!r}")
    f.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("MirrorConfig.cs",
'''    [JsonPropertyName("preview_open_on")] public string PreviewOpenOn { get; set; } = "remember";''',
'''    [JsonPropertyName("preview_open_on")] public string PreviewOpenOn { get; set; } = "remember";
    // Keep the displayed projector on its extended monitor but remove ONLY
    // its taskbar button; the app's existing NotifyIcon stays in the tray.
    [JsonPropertyName("hide_preview_taskbar_button")]
    public bool HidePreviewTaskbarButton { get; set; } = true;''')

patch("SettingsForm.cs",
'''        Note("Minimize the normal Windows preview to the tray; restore it from the tray's Show preview menu.");''',
'''        Note("Minimize hides the whole preview; Show preview on the tray restores it.");
        CheckRow("Hide preview taskbar button (keep preview visible)",
                 _cfg.HidePreviewTaskbarButton,
                 v => _cfg.HidePreviewTaskbarButton = v);
        Note("The preview can stay visible on Extended display without a Windows taskbar button.");''')

patch("Win32Window.cs",
'''    private const uint WmPreviewTrayVisibility = 0x8051; // WM_APP + 0x51''',
'''    private const uint WmPreviewTrayVisibility = 0x8051; // WM_APP + 0x51
    private const uint WmPreviewTaskbarButton = 0x8052; // WM_APP + 0x52

    // This interface is ONLY for a button in the Windows taskbar. It does
    // NOT affect the preview HWND visibility, compositor, or tray NotifyIcon.
    [ComImport, Guid("56FDF344-FD6D-11d0-958A-006097C9A090")]
    private class ShellTaskbarList { }

    [ComImport, Guid("56FDF342-FD6D-11d0-958A-006097C9A090"),
     InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    private interface IShellTaskbarList
    {
        void HrInit();
        void AddTab(IntPtr hwnd);
        void DeleteTab(IntPtr hwnd);
        void ActivateTab(IntPtr hwnd);
        void SetActiveAlt(IntPtr hwnd);
    }

    public static IntPtr PreviewHandle =>
        FindWindow(ClassName, "RitschyMirror");

    public static bool RequestPreviewTaskbarButton(bool showButton)
    {
        IntPtr hwnd = PreviewHandle;
        return hwnd != IntPtr.Zero &&
               PostMessage(hwnd, WmPreviewTaskbarButton,
                           showButton ? new IntPtr(1) : IntPtr.Zero, IntPtr.Zero);
    }

    private static void ApplyShellTaskbarButton(IntPtr hwnd, bool showButton)
    {
        IShellTaskbarList? shell = null;
        try
        {
            shell = (IShellTaskbarList)new ShellTaskbarList();
            shell.HrInit();
            if (showButton) shell.AddTab(hwnd);
            else shell.DeleteTab(hwnd);
        }
        catch (Exception)
        {
            // Windows Explorer can restart or refuse a shell taskbar call;
            // leave the actual preview untouched and retry via tray timer.
        }
        finally
        {
            if (shell != null)
                try { Marshal.FinalReleaseComObject(shell); } catch { }
        }
    }''')

patch("Win32Window.cs",
'''            case WmPreviewTrayVisibility:
                // This executes on the preview's true owning UI thread.''',
'''            case WmPreviewTaskbarButton:
                // Do not hide/minimize/move the preview. This is executed
                // on the HWND owning UI thread, even during a native drag.
                ApplyShellTaskbarButton(hWnd, wParam != IntPtr.Zero);
                return IntPtr.Zero;
            case WmPreviewTrayVisibility:
                // This executes on the preview's true owning UI thread.''')

patch("TrayContext.cs",
'''    private bool? _lastRunning;          // nur bei Statuswechsel Icon tauschen''',
'''    private bool? _lastRunning;          // nur bei Statuswechsel Icon tauschen
    private IntPtr _lastTaskbarPreview = IntPtr.Zero;
    private bool? _lastTaskbarHidden;
    private int _taskbarHeartbeat;''')

patch("TrayContext.cs",
'''        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";
        bool hasPreview = Win32Window.PreviewExists;''',
'''        _toggleItem.Text = running ? "Stop mirror" : "Start mirror";

        // Independently of 'Hide preview to tray': remove its TASKBAR entry
        // while leaving the projector visible wherever Windows placed it,
        // including HDMI TO USB in Extend mode. Reassert periodically because
        // Explorer or a window restore can add a taskbar button again.
        IntPtr previewHandle = Win32Window.PreviewHandle;
        if (previewHandle != IntPtr.Zero)
        {
            bool hideTaskbarButton = MirrorConfig.Load(_engine.ConfigPath).HidePreviewTaskbarButton;
            if (previewHandle != _lastTaskbarPreview ||
                _lastTaskbarHidden != hideTaskbarButton ||
                ++_taskbarHeartbeat >= 5)
            {
                Win32Window.RequestPreviewTaskbarButton(!hideTaskbarButton);
                _lastTaskbarPreview = previewHandle;
                _lastTaskbarHidden = hideTaskbarButton;
                _taskbarHeartbeat = 0;
            }
        }
        else
        {
            _lastTaskbarPreview = IntPtr.Zero;
            _lastTaskbarHidden = null;
            _taskbarHeartbeat = 0;
        }

        bool hasPreview = Win32Window.PreviewExists;''')

print("Separate taskbar-only Hide setting: projector remains visible on extended HDMI, one existing tray icon, real normal Windows frame")
