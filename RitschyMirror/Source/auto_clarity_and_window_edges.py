"""Optional automatic, mild SDR preview sharpening and display-edge confinement.

Apply after preview_start_display.py. The sharpen filter is in RitschyMirror's
GPU preview stage only; it does not control the capture card or Camera HD.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    src = p.read_text(encoding="utf-8")
    count = src.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one code anchor; found {count}: {old[:110]!r}")
    p.write_text(src.replace(old, new, 1), encoding="utf-8")
    print("Patched " + path)

# Keep display confinement optional; it is NOT standard Windows behavior
# (standard windows can normally be moved freely between displays).
patch("MirrorConfig.cs",
'    [JsonPropertyName("preview_open_on")] public string PreviewOpenOn { get; set; } = "remember";',
'    [JsonPropertyName("preview_open_on")] public string PreviewOpenOn { get; set; } = "remember";\n'
'    [JsonPropertyName("keep_preview_on_display")] public bool KeepPreviewOnDisplay { get; set; } = true;')

patch("MirrorConfig.cs",
'    [JsonPropertyName("copy_mode")]        public bool CopyMode { get; set; } = false;',
'    [JsonPropertyName("copy_mode")]        public bool CopyMode { get; set; } = false;\n'
'    [JsonPropertyName("auto_clarity")]     public bool AutoClarity { get; set; } = true;')

patch("MirrorConfig.cs",
'        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized", "preview_open_on",',
'        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized", "preview_open_on",\n'
'        "keep_preview_on_display",')

patch("MirrorConfig.cs",
'        "layout_mode", "crop_x", "crop_y", "crop_w", "crop_h", "show_cursor", "keep_awake",',
'        "layout_mode", "crop_x", "crop_y", "crop_w", "crop_h", "show_cursor", "keep_awake", "auto_clarity",')

patch("SettingsForm.cs",
'            _cfg.PreviewMaximized = latest.PreviewMaximized;',
'            _cfg.PreviewMaximized = latest.PreviewMaximized;')

patch("SettingsForm.cs",
'        Note("Main = Windows primary screen; Extended = selected Target monitor.");',
'        Note("Main = Windows primary screen; Extended = selected Target monitor.");\n'
'        CheckRow("Keep preview inside its current display (stop at screen edges)",\n'
'                 _cfg.KeepPreviewOnDisplay, v => _cfg.KeepPreviewOnDisplay = v);\n'
'        Note("Prevents dragging/resizing the preview onto another monitor; restart required.");')

patch("SettingsForm.cs",
'        CheckRow("Copy mode (SDR colors, no image adjustments; restart required)",\n'
'                 _cfg.CopyMode, v => _cfg.CopyMode = v);',
'        CheckRow("Copy mode (SDR colors, no image adjustments; restart required)",\n'
'                 _cfg.CopyMode, v => _cfg.CopyMode = v);\n'
'        CheckRow("Auto clarity (mild SDR text sharpening)",\n'
'                 _cfg.AutoClarity, v => _cfg.AutoClarity = v);\n'
'        Note("Helps preview text, but cannot restore capture-card compression detail.");')

# Existing Renderer ShaderParams has CopyMode in place of the last pad,
# leaving 8 bytes free in the 16-byte block.
patch("Renderer.cs",
'        public int CopyMode;',
'        public int CopyMode;\n'
'        public float AutoClarity, _padSharp;')

patch("Renderer.cs",
'            CopyMode = cfg.CopyMode ? 1 : 0,',
'''            CopyMode = cfg.CopyMode ? 1 : 0,
            // A restrained GPU unsharp filter compensates some sampling softness.
            // It adjusts slightly for source pixels reduced into a smaller viewport.
            // This is not a replacement for missing pixels or capture-card encoding.
            AutoClarity = cfg.CopyMode && cfg.AutoClarity
                ? System.Math.Clamp(
                    0.10f + 0.12f * System.Math.Max(0f,
                        System.Math.Max((float)srcW / System.Math.Max(vp.Width, 1f),
                                        (float)srcH / System.Math.Max(vp.Height, 1f)) - 1f),
                    0.10f, 0.30f)
                : 0f,''')

patch("Shaders.cs",
'    int CopyMode;           // 8-bit SDR raw color preview: skip all image corrections',
'    int CopyMode;           // 8-bit SDR raw color preview: skip all image corrections\n'
'    float AutoClarity;      // mild optional edge sharpening, 0 = disabled\n'
'    float _padSharp;')

patch("Shaders.cs",
'    if (CopyMode != 0) return float4(saturate(col), 1);',
'''    if (CopyMode != 0)
    {
        if (AutoClarity > 0.0)
        {
            // A small 4-neighbor unsharp pass in the source pixel space.
            // Clamp limits and low gain avoid strong halos on small UI text.
            uint srcW, srcH;
            Src.GetDimensions(srcW, srcH);
            float2 uvStep = 1.0 / max(float2(srcW, srcH), float2(1.0, 1.0));
            float3 neighboring =
                (Src.Sample(Smp, suv + float2(uvStep.x, 0)).rgb +
                 Src.Sample(Smp, suv - float2(uvStep.x, 0)).rgb +
                 Src.Sample(Smp, suv + float2(0, uvStep.y)).rgb +
                 Src.Sample(Smp, suv - float2(0, uvStep.y)).rgb) * 0.25;
            float3 detail = col - neighboring;
            // Avoid raising near-zero ringing on otherwise smooth image regions.
            col = saturate(col + AutoClarity * detail);
        }
        return float4(saturate(col), 1);
    }''')

# Current custom drag intercepts native edge/snap interaction. Clamp its output
# geometry to a single display's WORKING area instead, with gentle 12px snap.
# The gesture's display is sampled ONCE when it starts; it cannot drift to the
# next monitor when the cursor crosses the edge.
patch("Win32Window.cs",
'    private bool _manualResize;',
'    public bool KeepOnDisplay { get; set; } = true;\n'
'    private System.Drawing.Rectangle _gestureBounds;\n'
'    private bool _manualResize;')

patch("Win32Window.cs",
'                if (!IsZoomed(hWnd) && GetCursorPos(out POINT origin)\n'
'                    && GetWindowRect(hWnd, out RECT rect))\n'
'                {\n'
'                    if (hit == 2 /*HTCAPTION*/)',
'                if (!IsZoomed(hWnd) && GetCursorPos(out POINT origin)\n'
'                    && GetWindowRect(hWnd, out RECT rect))\n'
'                {\n'
'                    _gestureBounds = System.Windows.Forms.Screen.FromHandle(hWnd).WorkingArea;\n'
'                    if (hit == 2 /*HTCAPTION*/)')

patch("Win32Window.cs",
'''                    SetWindowPos(hWnd, IntPtr.Zero,
                                 cursor.X - _dragOffsetX, cursor.Y - _dragOffsetY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;''',
'''                    int moveX = cursor.X - _dragOffsetX;
                    int moveY = cursor.Y - _dragOffsetY;
                    if (KeepOnDisplay && GetWindowRect(hWnd, out RECT current))
                    {
                        int w = current.Right - current.Left;
                        int h = current.Bottom - current.Top;
                        // Allow windows larger than the working area to remain
                        // operable without negative clamp ranges.
                        int maxX = Math.Max(_gestureBounds.Left, _gestureBounds.Right - w);
                        int maxY = Math.Max(_gestureBounds.Top, _gestureBounds.Bottom - h);
                        moveX = Math.Clamp(moveX, _gestureBounds.Left, maxX);
                        moveY = Math.Clamp(moveY, _gestureBounds.Top, maxY);
                        const int snapPx = 12;
                        if (moveX - _gestureBounds.Left <= snapPx) moveX = _gestureBounds.Left;
                        else if (maxX - moveX <= snapPx) moveX = maxX;
                        if (moveY - _gestureBounds.Top <= snapPx) moveY = _gestureBounds.Top;
                        else if (maxY - moveY <= snapPx) moveY = maxY;
                    }
                    SetWindowPos(hWnd, IntPtr.Zero, moveX, moveY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;''')

patch("Win32Window.cs",
'''                    if (bottom) b = Math.Max(t + 240, b + dy);
                    SetWindowPos(hWnd, IntPtr.Zero, l, t, r - l, b - t,''',
'''                    if (bottom) b = Math.Max(t + 240, b + dy);
                    if (KeepOnDisplay)
                    {
                        // Don't cross the captured gesture's display boundary
                        // while resizing by an edge or corner.
                        if (left) l = Math.Max(_gestureBounds.Left, l);
                        if (right) r = Math.Min(_gestureBounds.Right, r);
                        if (top) t = Math.Max(_gestureBounds.Top, t);
                        if (bottom) b = Math.Min(_gestureBounds.Bottom, b);
                        // Screen can be smaller than minimum 320x240; never
                        // send an invalid or inverted rectangle to SetWindowPos.
                        if (r <= l || b <= t) return IntPtr.Zero;
                    }
                    SetWindowPos(hWnd, IntPtr.Zero, l, t, r - l, b - t,''')

patch("MirrorEngine.cs",
'        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless);',
'        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)\n'
'        {\n'
'            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,\n'
'        };')

print("Added optional preview auto-clarity and screen-edge containment")
