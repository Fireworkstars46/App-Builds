"""Performance and window-drag improvements for English RitschyMirror Copy Mode.

Applied after translate.py, enable_monitor_fallback.py, and add_copy_mode.py.
The render window no longer enters the Win32 modal move loop when dragged by its
titlebar. Output size remains fixed while moving, so the capture card sees a
continuously updated image. Optional frame limiter and newest-frame mode.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def replace(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    num = s.count(old)
    if num != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {num}: {old[:120]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print(f"Updated {path}")

# Separate numeric FPS cap; zero means no software cap. Keep VSync independently.
replace("MirrorConfig.cs",
'    [JsonPropertyName("vsync")]            public bool Vsync { get; set; } = true;',
'    [JsonPropertyName("vsync")]            public bool Vsync { get; set; } = true;\n'
'    [JsonPropertyName("fps_limit")]        public int FpsLimit { get; set; } = 60;\n'
'    [JsonPropertyName("low_latency")]      public bool LowLatency { get; set; } = true;')
replace("MirrorConfig.cs",
'        "exposure", "saturation", "contrast", "gamma", "content_offset_y", "vsync",',
'        "exposure", "saturation", "contrast", "gamma", "content_offset_y", "vsync", "fps_limit", "low_latency",')

replace("SettingsForm.cs",
'        CheckRow("VSync", _cfg.Vsync, v => _cfg.Vsync = v);',
'        CheckRow("VSync", _cfg.Vsync, v => _cfg.Vsync = v);\n'
'        ComboRow("FPS limit", new[] { "30", "60", "120", "unlimited" },\n'
'                 _cfg.FpsLimit <= 0 ? "unlimited" : _cfg.FpsLimit.ToString(),\n'
'                 s => _cfg.FpsLimit = s == "unlimited" ? 0 : int.Parse(s));\n'
'        CheckRow("Low latency (prefer newest captured frame)",\n'
'                 _cfg.LowLatency, v => _cfg.LowLatency = v);')

# Let the renderer use the newest WGC frame instead of displaying queued stale frames.
replace("WindowCapture.cs",
'    private readonly DirectXPixelFormat _captureFormat;',
'    private readonly DirectXPixelFormat _captureFormat;\n'
'    private bool _lowLatency;')
replace("WindowCapture.cs",
'bool showCursor, bool copySdr = false)\n        : this(device, hwnd, inputIsHdr, showCursor, captureMonitor: false, copySdr: copySdr)',
'bool showCursor, bool copySdr = false, bool lowLatency = true)\n        : this(device, hwnd, inputIsHdr, showCursor, captureMonitor: false, copySdr: copySdr,\n               lowLatency: lowLatency)')
replace("WindowCapture.cs",
'bool showCursor, bool captureMonitor, bool copySdr = false)',
'bool showCursor, bool captureMonitor, bool copySdr = false, bool lowLatency = true)')
replace("WindowCapture.cs",
'        _showCursor = showCursor;\n        _captureFormat =',
'        _showCursor = showCursor;\n        _lowLatency = lowLatency;\n        _captureFormat =')
replace("WindowCapture.cs",
"""        using var frame = pool.TryGetNextFrame();
        if (frame is null) return false; // noch kein neues Frame (kein Fehler)

        using var surface = frame.Surface;
        using var tex = GetTextureFromSurface(surface);
        var desc = tex.Description;

        EnsureTarget(desc);
        ctx.CopyResource(_copyTex!, tex);
        Width = (int)desc.Width;
        Height = (int)desc.Height;

        // Fenstergröße geändert → Frame-Pool für die FOLGE-Frames nachziehen (dieses Frame ist schon kopiert).
        var content = frame.ContentSize;
        if (content.Width > 0 && content.Height > 0 && (content.Width != _poolW || content.Height != _poolH))
        {
            _poolW = content.Width; _poolH = content.Height;
            try { pool.Recreate(_d3dDevice, _captureFormat, 2, content); } catch { /* nächster Versuch */ }
        }
        return true;
""",
"""        var frame = pool.TryGetNextFrame();
        if (frame is null) return false;

        if (_lowLatency)
        {
            // The WGC pool holds up to two frames. Discard older queued frames
            // and use the newest one, limiting preview latency when the GPU is busy.
            for (int n = 0; n < 2; n++)
            {
                var newer = pool.TryGetNextFrame();
                if (newer is null) break;
                frame.Dispose();
                frame = newer;
            }
        }
        using (frame)
        {
            using var surface = frame.Surface;
            using var tex = GetTextureFromSurface(surface);
            var desc = tex.Description;

            EnsureTarget(desc);
            ctx.CopyResource(_copyTex!, tex);
            Width = (int)desc.Width;
            Height = (int)desc.Height;

            var content = frame.ContentSize;
            if (content.Width > 0 && content.Height > 0 && (content.Width != _poolW || content.Height != _poolH))
            {
                _poolW = content.Width; _poolH = content.Height;
                try { pool.Recreate(_d3dDevice, _captureFormat, 2, content); }
                catch { /* retry after the next frame */ }
            }
            return true;
        }
""")
replace("WindowCapture.cs",
'        _showCursor = cfg.ShowCursor;\n        try { if (_session != null) _session.IsCursorCaptureEnabled = _showCursor; } catch { }',
'        _showCursor = cfg.ShowCursor;\n        try { if (_session != null) _session.IsCursorCaptureEnabled = _showCursor; } catch { }')
# LowLatency must update even if ShowCursor did not change. Replace original condition first.
replace("WindowCapture.cs",
'        if (cfg.ShowCursor == _showCursor) return;\n        _showCursor = cfg.ShowCursor;',
'        _lowLatency = cfg.LowLatency;\n        if (cfg.ShowCursor == _showCursor) return;\n        _showCursor = cfg.ShowCursor;')

replace("MirrorEngine.cs",
'capture = new WindowCapture(device, hwnd, winHdr, cfg.ShowCursor, copySdr: cfg.CopyMode);',
'capture = new WindowCapture(device, hwnd, winHdr, cfg.ShowCursor,\n                                            copySdr: cfg.CopyMode, lowLatency: cfg.LowLatency);')
replace("MirrorEngine.cs",
'captureMonitor: true, copySdr: true);',
'captureMonitor: true, copySdr: true, lowLatency: cfg.LowLatency);')
replace("MirrorEngine.cs",
'capture = new WindowCapture(device, hmonitor, src.Hdr, cfg.ShowCursor, captureMonitor: true);',
'capture = new WindowCapture(device, hmonitor, src.Hdr, cfg.ShowCursor,\n                                                captureMonitor: true, lowLatency: cfg.LowLatency);')

# Windowed output starts on the destination display instead of temporarily
# appearing on the captured primary desktop (which creates a mirror-in-mirror).
replace("MirrorEngine.cs",
'            x = 100; y = 100; outW = cfg.WindowWidth; outH = cfg.WindowHeight; borderless = false;',
'            x = dst.L + 30; y = dst.T + 30;\n'
'            outW = cfg.WindowWidth; outH = cfg.WindowHeight; borderless = false;')

replace("MirrorEngine.cs",
'                    cfg.Vsync = nc.Vsync;',
'                    cfg.Vsync = nc.Vsync;\n'
'                    cfg.FpsLimit = nc.FpsLimit;\n'
'                    cfg.LowLatency = nc.LowLatency;')

replace("MirrorEngine.cs",
"""        long framesRendered = 0;
        var sessionResult = SessionResult.Stopped;""",
"""        long framesRendered = 0;
        long nextFrameAt = 0;
        int lastFrameLimit = -1;
        var sessionResult = SessionResult.Stopped;""")

replace("MirrorEngine.cs",
"""            try { capture.TryAcquire(context); }
            catch (Exception ex)""",
"""            bool hasNewFrame;
            try { hasNewFrame = capture.TryAcquire(context); }
            catch (Exception ex)""")

replace("MirrorEngine.cs",
"""            if (capture.Srv != null)
            {
                renderer.Render(capture, cfg);
                renderer.Present(cfg.Vsync);
                framesRendered++;
            }
""",
"""            if (capture.Srv != null && hasNewFrame)
            {
                renderer.Render(capture, cfg);
                renderer.Present(cfg.Vsync);
                framesRendered++;

                // Limit output FPS without blocking the window message pump for
                // long periods. No extra wait if VSync/processing already ran late.
                int limit = cfg.FpsLimit is 30 or 60 or 120 ? cfg.FpsLimit : 0;
                if (limit != lastFrameLimit)
                {
                    nextFrameAt = 0;
                    lastFrameLimit = limit;
                }
                if (limit > 0)
                {
                    long interval = System.Diagnostics.Stopwatch.Frequency / limit;
                    long now = System.Diagnostics.Stopwatch.GetTimestamp();
                    if (nextFrameAt == 0 || nextFrameAt < now - interval)
                        nextFrameAt = now;
                    nextFrameAt += interval;
                    long remaining = nextFrameAt - now;
                    if (remaining > 0)
                    {
                        int waitMs = (int)(remaining * 1000L / System.Diagnostics.Stopwatch.Frequency);
                        if (waitMs > 1)
                        {
                            // Brief sleeps avoid excessive GPU use without making
                            // a drag of the output window wait on a blocking modal loop.
                            Thread.Sleep(waitMs - 1);
                        }
                    }
                }
            }
            else
            {
                // WGC often has no new frame for an unchanged desktop. Do not
                // re-present the same texture in a tight CPU/GPU spin loop.
                Thread.Sleep(1);
            }
""")

# Win32's default titlebar dragging enters a modal move loop inside
# DefWindowProc, blocking the render thread until mouse release. For plain
# titlebar movement handle capture/move ourselves so PumpMessages returns.
replace("Win32Window.cs",
'    public bool Running { get; private set; } = true;',
'    public bool Running { get; private set; } = true;\n'
'    private bool _manualDrag;\n'
'    private int _dragOffsetX, _dragOffsetY;')
replace("Win32Window.cs",
"""        switch (msg)
        {
            case 0x0010: // WM_CLOSE""",
"""        switch (msg)
        {
            case 0x00A1: // WM_NCLBUTTONDOWN: titlebar drag without modal system move loop
                if (wParam.ToInt32() == 2 /*HTCAPTION*/
                    && GetCursorPos(out POINT origin)
                    && GetWindowRect(hWnd, out RECT rect))
                {
                    _dragOffsetX = origin.X - rect.Left;
                    _dragOffsetY = origin.Y - rect.Top;
                    _manualDrag = true;
                    SetCapture(hWnd);
                    return IntPtr.Zero;
                }
                break;
            case 0x0200: // WM_MOUSEMOVE: continue rendering while repositioning
                if (_manualDrag && GetCursorPos(out POINT cursor))
                {
                    SetWindowPos(hWnd, IntPtr.Zero,
                                 cursor.X - _dragOffsetX, cursor.Y - _dragOffsetY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;
                }
                break;
            case 0x0202: // WM_LBUTTONUP
            case 0x00A2: // WM_NCLBUTTONUP
                if (_manualDrag)
                {
                    _manualDrag = false;
                    ReleaseCapture();
                    return IntPtr.Zero;
                }
                break;
            case 0x0215: // WM_CAPTURECHANGED (cancelled by Windows)
                _manualDrag = false;
                break;
            case 0x0010: // WM_CLOSE""")
replace("Win32Window.cs",
'    private struct RECT { public int Left, Top, Right, Bottom; }',
'    private struct RECT { public int Left, Top, Right, Bottom; }\n\n'
'    [StructLayout(LayoutKind.Sequential)]\n'
'    private struct POINT { public int X, Y; }')
replace("Win32Window.cs",
'    [DllImport("user32.dll")] private static extern bool SetCursorPos(int X, int Y);',
'    [DllImport("user32.dll")] private static extern bool SetCursorPos(int X, int Y);\n'
'    [DllImport("user32.dll")] private static extern bool GetCursorPos(out POINT lpPoint);\n'
'    [DllImport("user32.dll")] private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);\n'
'    [DllImport("user32.dll")] private static extern IntPtr SetCapture(IntPtr hWnd);\n'
'    [DllImport("user32.dll")] private static extern bool ReleaseCapture();\n'
'    [DllImport("user32.dll")] private static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter,\n'
'        int X, int Y, int cx, int cy, uint uFlags);')

print("Smooth-drag, adjustable-FPS and low-latency patch applied")
