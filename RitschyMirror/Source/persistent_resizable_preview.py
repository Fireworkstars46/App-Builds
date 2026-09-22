"""Persistent custom preview size + live maximization/restore + nonblocking edge resizing.

Runs after smooth_drag_and_fps.py in the Windows GitHub Actions workflow.
Only windowed output is affected; capture and color modes are unchanged.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    f = root / path
    s = f.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {count}: {old[:100]!r}")
    f.write_text(s.replace(old, new, 1), encoding="utf-8")
    print(f"Updated {path}")

# Keep the saved normal/restored window rectangle separate from Test window defaults.
# Maximize state is saved independently, so restoring always returns to the custom dimensions.
patch("MirrorConfig.cs",
'    [JsonPropertyName("window_height")]    public int WindowHeight { get; set; } = 720;',
'''    [JsonPropertyName("window_height")]    public int WindowHeight { get; set; } = 720;
    [JsonPropertyName("preview_x")]        public int PreviewX { get; set; } = int.MinValue;
    [JsonPropertyName("preview_y")]        public int PreviewY { get; set; } = int.MinValue;
    [JsonPropertyName("preview_width")]    public int PreviewWidth { get; set; } = 0;
    [JsonPropertyName("preview_height")]   public int PreviewHeight { get; set; } = 0;
    [JsonPropertyName("preview_maximized")] public bool PreviewMaximized { get; set; } = false;''')

patch("MirrorConfig.cs",
'        "window_width", "window_height", "output_width", "output_height",',
'        "window_width", "window_height", "output_width", "output_height",\n'
'        "preview_x", "preview_y", "preview_width", "preview_height", "preview_maximized",')

# Settings window has its own older loaded copy of the config. Do not overwrite
# the newest persisted geometry when the user changes a different UI setting.
patch("SettingsForm.cs",
'    private void SaveCfg() { if (_loading) return; try { _cfg.Save(_engine.ConfigPath); } catch { } }',
'''    private void SaveCfg()
    {
        if (_loading) return;
        try
        {
            var latest = MirrorConfig.Load(_engine.ConfigPath);
            _cfg.PreviewX = latest.PreviewX;
            _cfg.PreviewY = latest.PreviewY;
            _cfg.PreviewWidth = latest.PreviewWidth;
            _cfg.PreviewHeight = latest.PreviewHeight;
            _cfg.PreviewMaximized = latest.PreviewMaximized;
            _cfg.Save(_engine.ConfigPath);
        }
        catch { }
    }''')

patch("SettingsForm.cs",
'        Note("Display/mode/bit depth/window changes require a restart.");',
'        Note("Display/mode/bit depth/window changes require a restart.");\n'
'        Note("Preview remembers the size you drag it to and restores it after maximizing.");')

# Geometry is recorded on the same thread that owns the native HWND.
# Prefer client pixel dimensions for swap-chain buffers (not the outer frame).
patch("Win32Window.cs",
'    private int _dragOffsetX, _dragOffsetY;',
'''    private int _dragOffsetX, _dragOffsetY;
    private bool _manualResize;
    private int _resizeHit;
    private POINT _resizeStartPoint;
    private RECT _resizeStartRect;
    private RECT _normalRect;
    private bool _normalRectValid;
    private bool _maximized;
    public bool GeometryDirty { get; private set; }

    public bool IsMinimized => Hwnd != IntPtr.Zero && IsIconic(Hwnd);
    public bool IsMaximized => Hwnd != IntPtr.Zero && IsZoomed(Hwnd);
    public int ClientWidth
    {
        get
        {
            if (Hwnd == IntPtr.Zero || !GetClientRect(Hwnd, out RECT r)) return 0;
            return Math.Max(0, r.Right - r.Left);
        }
    }
    public int ClientHeight
    {
        get
        {
            if (Hwnd == IntPtr.Zero || !GetClientRect(Hwnd, out RECT r)) return 0;
            return Math.Max(0, r.Bottom - r.Top);
        }
    }

    public void Maximize() { if (Hwnd != IntPtr.Zero) ShowWindow(Hwnd, 3 /*SW_MAXIMIZE*/); }

    public bool ReadSavedGeometry(out int x, out int y, out int width, out int height,
                                  out bool maximized)
    {
        x = _normalRect.Left; y = _normalRect.Top;
        width = _normalRect.Right - _normalRect.Left;
        height = _normalRect.Bottom - _normalRect.Top;
        maximized = _maximized;
        return _normalRectValid && width >= 320 && height >= 240;
    }

    public void GeometrySaved() => GeometryDirty = false;

    private void UpdateGeometry()
    {
        if (Hwnd == IntPtr.Zero || IsIconic(Hwnd)) return;
        bool max = IsZoomed(Hwnd);
        if (!max && GetWindowRect(Hwnd, out RECT r)
                 && r.Right > r.Left && r.Bottom > r.Top)
        {
            if (!_normalRectValid || r.Left != _normalRect.Left || r.Top != _normalRect.Top
                || r.Right != _normalRect.Right || r.Bottom != _normalRect.Bottom)
            {
                _normalRect = r;
                _normalRectValid = true;
                if (!_manualDrag && !_manualResize) GeometryDirty = true;
            }
        }
        if (_maximized != max)
        {
            _maximized = max;
            GeometryDirty = true;
        }
    }''')
patch("Win32Window.cs",
'        if (Hwnd != IntPtr.Zero) { lock (s_lock) s_windows[Hwnd] = this; }',
'''        if (Hwnd != IntPtr.Zero)
        {
            if (GetWindowRect(Hwnd, out RECT r))
            {
                _normalRect = r;
                _normalRectValid = true;
            }
            lock (s_lock) s_windows[Hwnd] = this;
        }''')

# A titlebar move or border drag must not enter the system's blocking modal
# sizing/moving loop on the rendering thread.
patch("Win32Window.cs",
'''            case 0x00A1: // WM_NCLBUTTONDOWN: titlebar drag without modal system move loop
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
                break;''',
'''            case 0x00A1: // WM_NCLBUTTONDOWN: do not enter DefWindowProc's modal move/size loop
            {
                int hit = wParam.ToInt32();
                if (!IsZoomed(hWnd) && GetCursorPos(out POINT origin)
                    && GetWindowRect(hWnd, out RECT rect))
                {
                    if (hit == 2 /*HTCAPTION*/)
                    {
                        _dragOffsetX = origin.X - rect.Left;
                        _dragOffsetY = origin.Y - rect.Top;
                        _manualDrag = true;
                        SetCapture(hWnd);
                        return IntPtr.Zero;
                    }
                    if (hit >= 10 && hit <= 17) // HTLEFT..HTBOTTOMRIGHT
                    {
                        _resizeHit = hit;
                        _resizeStartPoint = origin;
                        _resizeStartRect = rect;
                        _manualResize = true;
                        SetCapture(hWnd);
                        return IntPtr.Zero;
                    }
                }
                break;
            }
            case 0x0200: // WM_MOUSEMOVE
                if (_manualDrag && GetCursorPos(out POINT cursor))
                {
                    SetWindowPos(hWnd, IntPtr.Zero,
                                 cursor.X - _dragOffsetX, cursor.Y - _dragOffsetY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;
                }
                if (_manualResize && GetCursorPos(out POINT cursorResize))
                {
                    int dx = cursorResize.X - _resizeStartPoint.X;
                    int dy = cursorResize.Y - _resizeStartPoint.Y;
                    int l = _resizeStartRect.Left, t = _resizeStartRect.Top;
                    int r = _resizeStartRect.Right, b = _resizeStartRect.Bottom;
                    bool left = _resizeHit is 10 or 13 or 16;
                    bool right = _resizeHit is 11 or 14 or 17;
                    bool top = _resizeHit is 12 or 13 or 14;
                    bool bottom = _resizeHit is 15 or 16 or 17;
                    if (left) l = Math.Min(r - 320, l + dx);
                    if (right) r = Math.Max(l + 320, r + dx);
                    if (top) t = Math.Min(b - 240, t + dy);
                    if (bottom) b = Math.Max(t + 240, b + dy);
                    SetWindowPos(hWnd, IntPtr.Zero, l, t, r - l, b - t,
                                 0x0014 /*NOZORDER | NOACTIVATE*/);
                    return IntPtr.Zero;
                }
                break;
            case 0x0202: // WM_LBUTTONUP
            case 0x00A2: // WM_NCLBUTTONUP
                if (_manualDrag || _manualResize)
                {
                    _manualDrag = false;
                    _manualResize = false;
                    UpdateGeometry();
                    GeometryDirty = true;
                    ReleaseCapture();
                    return IntPtr.Zero;
                }
                break;
            case 0x0215: // WM_CAPTURECHANGED: cancelled by Windows
                if (_manualDrag || _manualResize)
                {
                    _manualDrag = false;
                    _manualResize = false;
                    UpdateGeometry();
                    GeometryDirty = true;
                }
                break;
            case 0x0003: // WM_MOVE
            case 0x0005: // WM_SIZE (including maximize and restore)
                UpdateGeometry();
                break;''')

patch("Win32Window.cs",
'    [DllImport("user32.dll")] private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);',
'''    [DllImport("user32.dll")] private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] private static extern bool GetClientRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] private static extern bool IsZoomed(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern bool IsIconic(IntPtr hWnd);''')

# Resize swap-chain back buffers to actual preview client size rather than
# stretching a fixed 1280x720 buffer when maximized/custom resized.
patch("Renderer.cs",
'''    private void CreateRtv()
    {
        using var backBuffer = _swapChain.GetBuffer<ID3D11Texture2D>(0);
        _rtv = _device.CreateRenderTargetView(backBuffer);
    }
''',
'''    private void CreateRtv()
    {
        using var backBuffer = _swapChain.GetBuffer<ID3D11Texture2D>(0);
        _rtv = _device.CreateRenderTargetView(backBuffer);
    }

    public bool Resize(int width, int height)
    {
        // Minimized windows have a zero-sized client area; keep the old
        // buffers until they become visible again.
        if (width <= 0 || height <= 0 || (width == Width && height == Height))
            return false;
        _ctx.UnsetRenderTargets();
        _ctx.ClearState(); // release any backbuffer SRV/RTV pipeline references
        _rtv.Dispose();
        _ctx.Flush();
        _swapChain.ResizeBuffers(2, (uint)width, (uint)height,
                                 Format.Unknown, SwapChainFlags.None).CheckError();
        Width = width;
        Height = height;
        CreateRtv();
        return true;
    }
''')

patch("MirrorEngine.cs",
'''            x = dst.L + 30; y = dst.T + 30;
            outW = cfg.WindowWidth; outH = cfg.WindowHeight; borderless = false;''',
'''            x = dst.L + 30; y = dst.T + 30;
            outW = cfg.WindowWidth; outH = cfg.WindowHeight; borderless = false;
            if (cfg.PreviewWidth >= 320 && cfg.PreviewWidth <= 8192
                && cfg.PreviewHeight >= 240 && cfg.PreviewHeight <= 8192)
            {
                bool intersectsDisplay = displays.Any(d =>
                    cfg.PreviewX < d.R - 64 && cfg.PreviewX + cfg.PreviewWidth > d.L + 64
                    && cfg.PreviewY < d.B - 64 && cfg.PreviewY + cfg.PreviewHeight > d.T + 64);
                if (intersectsDisplay)
                {
                    x = cfg.PreviewX; y = cfg.PreviewY;
                    outW = cfg.PreviewWidth; outH = cfg.PreviewHeight;
                }
            }''')

patch("MirrorEngine.cs",
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless);
        Log("Schritt: Renderer/Swapchain...");
        var renderer = new Renderer(factory, device, context, window.Hwnd, outW, outH, cfg.CopyMode ? 8 : cfg.OutputBitDepth);''',
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless);
        if (windowed && cfg.PreviewMaximized) window.Maximize();
        Log("Schritt: Renderer/Swapchain...");
        int clientW = Math.Max(1, window.ClientWidth);
        int clientH = Math.Max(1, window.ClientHeight);
        var renderer = new Renderer(factory, device, context, window.Hwnd,
                                    clientW, clientH, cfg.CopyMode ? 8 : cfg.OutputBitDepth);''')

patch("MirrorEngine.cs",
'''        while (window.Running && !_stop)
        {
            window.PumpMessages();

            // Config-Hot-Reload''',
'''        while (window.Running && !_stop)
        {
            window.PumpMessages();
            if (!window.Running || _stop) break;

            // Window placement is saved independently of the capture settings.
            // Save the normal (restored) rectangle even when currently maximized.
            // MergePatch retains unrelated settings changed in the GUI.
            if (windowed && window.GeometryDirty
                && window.ReadSavedGeometry(out int px, out int py,
                                            out int pw, out int ph, out bool maximized))
            {
                try
                {
                    MirrorConfig.MergePatch(ConfigPath, new System.Text.Json.Nodes.JsonObject
                    {
                        ["preview_x"] = px,
                        ["preview_y"] = py,
                        ["preview_width"] = pw,
                        ["preview_height"] = ph,
                        ["preview_maximized"] = maximized,
                    });
                    window.GeometrySaved();
                    lastCfgWrite = SafeWriteTime();
                }
                catch (Exception ex) { Log("Could not save preview size: " + ex.Message); }
            }

            // Resize back buffers when a native window was maximized, restored,
            // or manually resized. The native message pump remains non-blocking.
            bool resized = false;
            if (windowed && !window.IsMinimized)
            {
                int newW = window.ClientWidth, newH = window.ClientHeight;
                if (newW > 0 && newH > 0)
                    resized = renderer.Resize(newW, newH);
            }
            if (window.IsMinimized) { Thread.Sleep(16); continue; }

            // Config-Hot-Reload''')

patch("MirrorEngine.cs",
'            if (capture.Srv != null && hasNewFrame)',
'            if (capture.Srv != null && (hasNewFrame || resized))')

print("Resizable persistent window geometry and responsive max/restore patch applied")
