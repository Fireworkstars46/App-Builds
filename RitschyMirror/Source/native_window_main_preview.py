"""Honor Main preview placement and give preview normal browser-like Win32 window behavior.

Runs after fix_debug_startup.py. Fixes the previous unconditional
preview-on-HDMI safety override. Uses the Win10 2004+ display-affinity API
to exclude the preview from WGC desktop captures when available so that
placing the preview on the captured main screen need not recurse.
Native Windows move/resize (including crossing monitors and Snap) is
the default. During the native modal drag/resize loop the preview can
temporarily pause until mouse release; 'Smooth drag' remains available.
"""
import os
from pathlib import Path
root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor; found {count}: {old[:105]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("MirrorConfig.cs",
'    [JsonPropertyName("keep_preview_on_display")] public bool KeepPreviewOnDisplay { get; set; } = true;',
'''    [JsonPropertyName("keep_preview_on_display")] public bool KeepPreviewOnDisplay { get; set; } = false;
    [JsonPropertyName("native_preview_window")] public bool NativePreviewWindow { get; set; } = true;''')

patch("MirrorConfig.cs",
'        "keep_preview_on_display",',
'        "keep_preview_on_display", "native_preview_window",')

patch("SettingsForm.cs",
'''        CheckRow("Keep preview inside its current display (stop at screen edges)",
                 _cfg.KeepPreviewOnDisplay, v => _cfg.KeepPreviewOnDisplay = v);
        Note("Prevents dragging/resizing the preview onto another monitor; restart required.");''',
'''        ComboRow("Preview window movement",
                 new[] { "Normal Windows (browser-like)", "Smooth live drag" },
                 _cfg.NativePreviewWindow
                     ? "Normal Windows (browser-like)" : "Smooth live drag",
                 s => _cfg.NativePreviewWindow = s == "Normal Windows (browser-like)");
        Note("Normal Windows: drag between screens and use window snapping. Restart required.");
        Note("Preview image may pause during a native drag until mouse release.");
        CheckRow("Keep preview inside one display (smooth drag mode only)",
                 _cfg.KeepPreviewOnDisplay, v => _cfg.KeepPreviewOnDisplay = v);''')

patch("Win32Window.cs",
'''    public bool KeepOnDisplay { get; set; } = true;''',
'''    public bool KeepOnDisplay { get; set; } = false;
    // Standard Win32 titlebar and resize borders, equivalent to other
    // normal app windows. Native OS dragging enters a modal move/size
    // loop, briefly pausing rendering while the left mouse button is held.
    public bool NativeMoveResize { get; set; } = true;

    public bool ExcludeFromDesktopCapture()
    {
        // WDA_EXCLUDEFROMCAPTURE (Windows 10 version 2004+). The physical
        // HDMI output still shows this window; only Windows capture APIs
        // such as WGC omit it. False means the OS refused the request.
        return Hwnd != IntPtr.Zero &&
               SetWindowDisplayAffinity(Hwnd, 0x11 /*WDA_EXCLUDEFROMCAPTURE*/);
    }

    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool SetWindowDisplayAffinity(IntPtr hwnd, uint affinity);''')

patch("Win32Window.cs",
'''            case 0x00A1: // WM_NCLBUTTONDOWN: do not enter DefWindowProc's modal move/size loop
            {
                int hit = wParam.ToInt32();''',
'''            case 0x00A1: // WM_NCLBUTTONDOWN: optional true native window dragging
            {
                // Fall through to DefWindowProc for native titlebar movement,
                // cross-display dragging, native edge resize and Aero Snap.
                // Do not SetCapture or run manual edge constraints in this mode.
                if (NativeMoveResize) break;
                int hit = wParam.ToInt32();''')

# No longer override the user's Preview opens on = Main selection. Instead,
# a window on the source is excluded from WGC monitor capture, if available.
patch("MirrorEngine.cs",
'''        // A captured screen must NOT contain its own preview. Merely warning
        // is insufficient: the GPU will recursively paint the same screen.
        // When Source and Target differ, move the preview to Target regardless
        // of saved geometry or the older 'Preview opens on: Main' preference.
        // Leave Windows in Extend; do not modify display topology.
        if (windowed && captureMode == "monitor" && debugSourceDisplay >= 0)
        {
            var sourceBounds = displays[debugSourceDisplay];
            bool overlapsCapturedDisplay =
                x < sourceBounds.R && x + outW > sourceBounds.L &&
                y < sourceBounds.B && y + outH > sourceBounds.T;
            if (overlapsCapturedDisplay && debugSourceDisplay != dstIdx)
            {
                x = dst.L + Math.Max(0, (dst.R - dst.L - outW) / 2);
                y = dst.T + Math.Max(0, (dst.B - dst.T - outH) / 2);
                Log("[SAFETY] Preview placement overlapped captured source; opening on HDMI target instead to prevent recursive mirroring.");
            }
        }

        Log("Step: Creating window...");
        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,
        };''',
'''        // Honor Preview opens on=Main even when source is the main display.
        // Windows desktop capture must exclude its own preview to avoid a
        // recursive mirror; this is handled with display affinity below.
        Log("Step: Creating window...");
        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,
            KeepOnDisplay = windowed && !cfg.NativePreviewWindow && cfg.KeepPreviewOnDisplay,
        };
        if (windowed && captureMode == "monitor")
        {
            bool hiddenFromWgc = window.ExcludeFromDesktopCapture();
            Log(hiddenFromWgc
                ? "[PREVIEW] Excluded preview window from Windows Graphics Capture to prevent recursive mirroring."
                : "[PREVIEW] WARNING: Windows refused preview capture exclusion. If preview overlaps the captured main display, mirror feedback may occur; move it to HDMI target.");
        }''')

# The debug log already records effective and selected preview settings.
patch("MirrorEngine.cs",
'''                $"keep_preview_on_display={cfg.KeepPreviewOnDisplay}.");''',
'''                $"keep_preview_on_display={cfg.KeepPreviewOnDisplay}, " +
                $"native_preview_window={cfg.NativePreviewWindow}.");''')

print("Main preview selection now respected; native cross-display window movement enabled")
