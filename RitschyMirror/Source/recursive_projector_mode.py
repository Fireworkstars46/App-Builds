"""Add an OBS-style single-HWND recursive projector preview.

Runs after lightshot_capture_toggle.py. A recursive tunnel is an optical
feedback of the ONE existing preview on a captured desktop. The pictures of
window frames seen in the feedback are image pixels, not separate HWNDs.

Projector mode keeps the existing monitor-capture/render pipeline, opts out
of WDA_EXCLUDEFROMCAPTURE so Lightshot and the monitor source can both see the
preview. The existing user FPS setting (30, 60, 120, unlimited) applies
unchanged. Optional borderless projector has
Win32 nonclient hit testing for mouse drag and edge resize without drawing
a title bar. Normal browser-like window mode remains available.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {n}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("MirrorConfig.cs",
'    [JsonPropertyName("hide_preview_from_screenshots")] public bool HidePreviewFromScreenshots { get; set; } = false;',
'''    [JsonPropertyName("hide_preview_from_screenshots")] public bool HidePreviewFromScreenshots { get; set; } = false;
    // Recursion is intentionally permitted; it does not create extra windows.
    [JsonPropertyName("recursive_projector")] public bool RecursiveProjector { get; set; } = false;
    [JsonPropertyName("projector_borderless")] public bool ProjectorBorderless { get; set; } = true;''')

patch("MirrorConfig.cs",
'        "keep_preview_on_display", "native_preview_window", "hide_preview_from_screenshots",',
'        "keep_preview_on_display", "native_preview_window", "hide_preview_from_screenshots", "recursive_projector", "projector_borderless",')

patch("SettingsForm.cs",
'''        CheckRow("Hide preview from screenshots (prevents mirror feedback)",
                 _cfg.HidePreviewFromScreenshots,
                 v => _cfg.HidePreviewFromScreenshots = v);''',
'''        ComboRow("Preview style", new[] { "Normal preview", "Recursive projector (OBS-style)" },
                 _cfg.RecursiveProjector ? "Recursive projector (OBS-style)" : "Normal preview",
                 s => _cfg.RecursiveProjector = s == "Recursive projector (OBS-style)");
        CheckRow("Borderless projector (no repeating title bars)",
                 _cfg.ProjectorBorderless, v => _cfg.ProjectorBorderless = v);
        Note("Projector uses the SAME preview window: no extra windows are created.");
        Note("To get the tunnel: source = Main monitor, preview opens on = Main.");
        Note("Projector is visible to Lightshot, even if Hide preview is checked.");
        Note("Projector obeys the selected FPS limit (30, 60, 120 or unlimited).");
        Note("Style/borderless changes need restart; high FPS may increase GPU load.");
        CheckRow("Hide preview from screenshots (prevents mirror feedback)",
                 _cfg.HidePreviewFromScreenshots,
                 v => _cfg.HidePreviewFromScreenshots = v);''')

# The existing Win32Window creates exactly one HWND per render session. Reuse
# it in a projector-specific borderless style; fullscreen borderless is
# unchanged and remains topmost only in the existing output mode.
patch("Win32Window.cs",
'''    public Win32Window(string title, int x, int y, int width, int height, bool borderless)''',
'''    public Win32Window(string title, int x, int y, int width, int height,
                       bool borderless, bool projectorBorderless = false)''')

patch("Win32Window.cs",
'''        uint style = borderless ? 0x80000000 /*WS_POPUP*/ : 0x00CF0000 /*WS_OVERLAPPEDWINDOW*/;
        uint exStyle = borderless ? 0x00000008u /*WS_EX_TOPMOST*/ : 0u;''',
'''        uint style = (borderless || projectorBorderless)
            ? 0x80000000u /*WS_POPUP*/ : 0x00CF0000u /*WS_OVERLAPPEDWINDOW*/;
        uint exStyle = borderless ? 0x00000008u /*WS_EX_TOPMOST*/ : 0u;
        _projectorBorderless = projectorBorderless;''')

patch("Win32Window.cs",
'''    public bool NativeMoveResize { get; set; } = true;''',
'''    public bool NativeMoveResize { get; set; } = true;
    private readonly bool _projectorBorderless;''')

patch("Win32Window.cs",
'''        switch (msg)
        {
            case 0x00A1: // WM_NCLBUTTONDOWN: optional true native window dragging''',
'''        switch (msg)
        {
            case 0x0084: // WM_NCHITTEST: borderless projector's draggable/resizable surface
                if (_projectorBorderless && !IsZoomed(hWnd) &&
                    GetWindowRect(hWnd, out RECT borderlessRect))
                {
                    // lParam packs signed physical screen coordinates (also
                    // handles screens positioned left/above the primary).
                    long lp = lParam.ToInt64();
                    int mx = unchecked((short)(lp & 0xffff));
                    int my = unchecked((short)((lp >> 16) & 0xffff));
                    const int edge = 9;
                    bool left = mx >= borderlessRect.Left && mx < borderlessRect.Left + edge;
                    bool right = mx < borderlessRect.Right && mx >= borderlessRect.Right - edge;
                    bool top = my >= borderlessRect.Top && my < borderlessRect.Top + edge;
                    bool bottom = my < borderlessRect.Bottom && my >= borderlessRect.Bottom - edge;
                    if (left && top) return new IntPtr(13 /*HTTOPLEFT*/);
                    if (right && top) return new IntPtr(14 /*HTTOPRIGHT*/);
                    if (left && bottom) return new IntPtr(16 /*HTBOTTOMLEFT*/);
                    if (right && bottom) return new IntPtr(17 /*HTBOTTOMRIGHT*/);
                    if (left) return new IntPtr(10 /*HTLEFT*/);
                    if (right) return new IntPtr(11 /*HTRIGHT*/);
                    if (top) return new IntPtr(12 /*HTTOP*/);
                    if (bottom) return new IntPtr(15 /*HTBOTTOM*/);
                    return new IntPtr(2 /*HTCAPTION*/);
                }
                break;
            case 0x00A1: // WM_NCLBUTTONDOWN: optional true native window dragging''')

# Honor Main/Extended/Remember as selected, still just ONE window. Window
# source and target display selections remain unchanged.
patch("MirrorEngine.cs",
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,''',
'''        bool projector = windowed && cfg.RecursiveProjector;
        var window = new Win32Window("RitschyMirror", x, y, outW, outH,
                                     borderless, projectorBorderless: projector && cfg.ProjectorBorderless)
        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,''')

patch("MirrorEngine.cs",
'''            bool captureAffinitySet = window.SetPreviewCaptureExclusion(cfg.HidePreviewFromScreenshots);
            if (!captureAffinitySet)''',
'''            bool captureAffinitySet = window.SetPreviewCaptureExclusion(
                cfg.HidePreviewFromScreenshots && !projector);
            if (projector)
                Log("[PROJECTOR] Single preview window; screen feedback intentionally allowed. " +
                    "Lightshot-visible; FPS follows selected limit (" + cfg.FpsLimit + "). Borderless=" + cfg.ProjectorBorderless);
            if (!captureAffinitySet)''')

patch("MirrorEngine.cs",
'''            else if (cfg.HidePreviewFromScreenshots)
                Log("[PREVIEW] Hidden from Windows screenshots/capture to prevent recursive mirroring.");''',
'''            else if (cfg.HidePreviewFromScreenshots && !projector)
                Log("[PREVIEW] Hidden from Windows screenshots/capture to prevent recursive mirroring.");''')

patch("MirrorEngine.cs",
'''                    if (cfg.HidePreviewFromScreenshots != nc.HidePreviewFromScreenshots)
                    {
                        cfg.HidePreviewFromScreenshots = nc.HidePreviewFromScreenshots;
                        if (windowed)
                            Log(window.SetPreviewCaptureExclusion(cfg.HidePreviewFromScreenshots)
                                ? "[PREVIEW] Screenshot exclusion changed: " + (cfg.HidePreviewFromScreenshots ? "ON (hidden)." : "OFF (Lightshot visible).")
                                : "[PREVIEW] WARNING: Could not change screenshot exclusion.");
                    }''',
'''                    if (cfg.HidePreviewFromScreenshots != nc.HidePreviewFromScreenshots)
                    {
                        cfg.HidePreviewFromScreenshots = nc.HidePreviewFromScreenshots;
                        if (windowed)
                        {
                            bool effectiveHide = cfg.HidePreviewFromScreenshots && !projector;
                            Log(window.SetPreviewCaptureExclusion(effectiveHide)
                                ? "[PREVIEW] Screenshot exclusion changed: " +
                                  (effectiveHide ? "ON (hidden)." : "OFF (Lightshot visible).")
                                : "[PREVIEW] WARNING: Could not change screenshot exclusion.");
                        }
                    }''')

patch("MirrorEngine.cs",
'''                $"hide_preview_from_screenshots={cfg.HidePreviewFromScreenshots}.");''',
'''                $"hide_preview_from_screenshots={cfg.HidePreviewFromScreenshots}, " +
                $"recursive_projector={cfg.RecursiveProjector}, projector_borderless={cfg.ProjectorBorderless}.");''')

# Retain the existing FPS-limit calculation from smooth_drag_and_fps.py.
# Projector now follows the same 30/60/120/unlimited choice as Normal preview.

print("OBS-style one-window recursive projector mode patch applied; FPS obeys user setting")
