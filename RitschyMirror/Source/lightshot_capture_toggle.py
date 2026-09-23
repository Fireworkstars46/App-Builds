"""Allow Lightshot / Print Screen to capture the RitschyMirror preview.

Applied AFTER native_window_main_preview.py in the English installer build.

The previous build unconditionally used WDA_EXCLUDEFROMCAPTURE on its
preview HWND. Many screenshot applications (including Lightshot on common
Windows capture paths) therefore omitted the preview. Make exclusion an
explicit opt-in, default OFF, and allow switching it live from Settings.

NOTE: When a monitor source is also displaying the preview, opt-out of
exclusion makes recursive mirror feedback possible. This tradeoff is shown
in settings and logged. The user can instead position the preview on the
HDMI target or capture a specific app window to avoid that feedback.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one code anchor, found {count}: {old[:110]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("MirrorConfig.cs",
'    [JsonPropertyName("native_preview_window")] public bool NativePreviewWindow { get; set; } = true;',
'''    [JsonPropertyName("native_preview_window")] public bool NativePreviewWindow { get; set; } = true;
    // Opt-in: OFF makes the preview visible to Lightshot and Print Screen.
    [JsonPropertyName("hide_preview_from_screenshots")] public bool HidePreviewFromScreenshots { get; set; } = false;''')

patch("MirrorConfig.cs",
'        "keep_preview_on_display", "native_preview_window",',
'        "keep_preview_on_display", "native_preview_window", "hide_preview_from_screenshots",')

patch("SettingsForm.cs",
'''        Note("Preview image may pause during a native drag until mouse release.");
        CheckRow("Keep preview inside one display (smooth drag mode only)",''',
'''        Note("Preview image may pause during a native drag until mouse release.");
        CheckRow("Hide preview from screenshots (prevents mirror feedback)",
                 _cfg.HidePreviewFromScreenshots,
                 v => _cfg.HidePreviewFromScreenshots = v);
        Note("OFF: Lightshot can screenshot the preview. ON: Windows capture hides it.");
        Note("OFF + preview on captured main screen can cause endless mirror-in-mirror.");
        CheckRow("Keep preview inside one display (smooth drag mode only)",''')

patch("Win32Window.cs",
'''    public bool ExcludeFromDesktopCapture()
    {
        // WDA_EXCLUDEFROMCAPTURE (Windows 10 version 2004+). The physical
        // HDMI output still shows this window; only Windows capture APIs
        // such as WGC omit it. False means the OS refused the request.
        return Hwnd != IntPtr.Zero &&
               SetWindowDisplayAffinity(Hwnd, 0x11 /*WDA_EXCLUDEFROMCAPTURE*/);
    }''',
'''    public bool SetPreviewCaptureExclusion(bool hide)
    {
        // WDA_NONE (0) restores ordinary screenshot visibility.
        // WDA_EXCLUDEFROMCAPTURE (0x11) can prevent recursive WGC
        // monitor feedback, but also hides the preview from Lightshot.
        // HWND belongs to this renderer thread; call on that thread.
        return Hwnd != IntPtr.Zero &&
               SetWindowDisplayAffinity(Hwnd, hide ? 0x11u : 0u);
    }''')

patch("MirrorEngine.cs",
'''        if (windowed && captureMode == "monitor")
        {
            bool hiddenFromWgc = window.ExcludeFromDesktopCapture();
            Log(hiddenFromWgc
                ? "[PREVIEW] Excluded preview window from Windows Graphics Capture to prevent recursive mirroring."
                : "[PREVIEW] WARNING: Windows refused preview capture exclusion. If preview overlaps the captured main display, mirror feedback may occur; move it to HDMI target.");
        }''',
'''        if (windowed)
        {
            bool captureAffinitySet = window.SetPreviewCaptureExclusion(cfg.HidePreviewFromScreenshots);
            if (!captureAffinitySet)
                Log("[PREVIEW] WARNING: Could not set capture visibility for preview window.");
            else if (cfg.HidePreviewFromScreenshots)
                Log("[PREVIEW] Hidden from Windows screenshots/capture to prevent recursive mirroring.");
            else
                Log("[PREVIEW] Screenshot visibility ON: Lightshot may capture the live preview.");
            if (!cfg.HidePreviewFromScreenshots && captureMode == "monitor" &&
                debugSourceDisplay >= 0 && GetWindowRect(window.Hwnd, out RECT screenshotRect))
            {
                var d = displays[debugSourceDisplay];
                if (screenshotRect.Left < d.R && screenshotRect.Right > d.L &&
                    screenshotRect.Top < d.B && screenshotRect.Bottom > d.T)
                    Log("[PREVIEW] WARNING: Screenshot visibility is ON and preview overlaps captured SOURCE monitor. Endless recursive mirror feedback may occur. To avoid it, move preview onto HDMI target, capture only a different app window, or enable Hide preview from screenshots.");
            }
        }''')

patch("MirrorEngine.cs",
'''                $"native_preview_window={cfg.NativePreviewWindow}.");''',
'''                $"native_preview_window={cfg.NativePreviewWindow}, " +
                $"hide_preview_from_screenshots={cfg.HidePreviewFromScreenshots}.");''')

patch("MirrorEngine.cs",
'''                    cfg.LowLatency = nc.LowLatency;
                    cfg.DebugLogging = nc.DebugLogging;''',
'''                    cfg.LowLatency = nc.LowLatency;
                    if (cfg.HidePreviewFromScreenshots != nc.HidePreviewFromScreenshots)
                    {
                        cfg.HidePreviewFromScreenshots = nc.HidePreviewFromScreenshots;
                        if (windowed)
                            Log(window.SetPreviewCaptureExclusion(cfg.HidePreviewFromScreenshots)
                                ? "[PREVIEW] Screenshot exclusion changed: " + (cfg.HidePreviewFromScreenshots ? "ON (hidden)." : "OFF (Lightshot visible).")
                                : "[PREVIEW] WARNING: Could not change screenshot exclusion.");
                    }
                    cfg.DebugLogging = nc.DebugLogging;''')

print("Added live screenshot-visibility switch, default ON for Lightshot capture")
