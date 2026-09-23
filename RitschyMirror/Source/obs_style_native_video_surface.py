"""OBS-style native projector: one normal top-level Win32 window, with an
independent child video presentation surface on a dedicated UI thread.

Apply after native_live_drag_resize_v2.py. We keep the same WGC/DXGI capture,
single visible projector, 60/120/unlimited FPS, Lightshot and screenshot
options, saved geometry, and extended HDMI output. A separate child HWND is
NOT a second projector: it lives inside the normal framed parent and is used
only as the swapchain's presentation surface. Parent UI messages (including
Windows' native modal move/size loop) never run on the D3D capture thread.
The child is resized directly by WM_SIZE and the old video buffers remain
valid throughout the drag, so new frames can be presented while Windows
scales the surface. Recreate backbuffers just once after WM_EXITSIZEMOVE.

While the native window is being moved/resized, repaint the last captured
texture at the user-selected frame limit even if WGC temporarily supplies no
NEW capture frame. New capture frames replace that texture immediately;
this avoids an unpainted child surface during Windows compositor transitions.

This does not replace OBS itself and can't validate physical HDMI/card
performance in CI: the user still needs to test during a real mouse drag.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    file = root / path
    s = file.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly 1 anchor; found {count}: {old[:140]!r}")
    file.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

# This window is strictly an ordinary framed Windows TOP-LEVEL window; the
# video surface lives in its client area, like a projector video widget.
# Use the existing (rooted) class callback for the unregistered child HWND:
# StaticWndProc safely delegates unknown child handles to DefWindowProc.
patch("Win32Window.cs",
'''    public bool NativeInteractiveMoveSize => _nativeInteractiveMoveSize;

    /// <summary>''',
'''    public bool NativeInteractiveMoveSize => _nativeInteractiveMoveSize;
    private IntPtr _videoSurfaceHwnd;
    public IntPtr PresentationHwnd => _videoSurfaceHwnd != IntPtr.Zero ? _videoSurfaceHwnd : Hwnd;

    // Run exclusively on the HWND-owning UI thread, BEFORE publishing the
    // parent preview to the independent render thread.
    private void CreateNativeVideoSurface()
    {
        if (_nativeUiThread != Thread.CurrentThread || Hwnd == IntPtr.Zero)
            throw new InvalidOperationException("Native video surface requires its owning UI thread.");
        if (!GetClientRect(Hwnd, out RECT r))
            throw new InvalidOperationException("Could not measure native preview client rectangle.");
        int width = Math.Max(1, r.Right - r.Left);
        int height = Math.Max(1, r.Bottom - r.Top);
        _videoSurfaceHwnd = CreateWindowEx(
            0, ClassName, "", 0x54000000u /*WS_CHILD|WS_VISIBLE|WS_CLIPSIBLINGS*/,
            0, 0, width, height, Hwnd, IntPtr.Zero,
            GetModuleHandle(null), IntPtr.Zero);
        if (_videoSurfaceHwnd == IntPtr.Zero)
            throw new System.ComponentModel.Win32Exception(
                Marshal.GetLastWin32Error(), "Could not create projector video surface.");
        // The parent has a SINGLE displayed video area. No new top-level or
        // mirrored window is created, even with recursive projector selected.
        UpdateNativeVideoSurface();
    }

    private void UpdateNativeVideoSurface()
    {
        if (_videoSurfaceHwnd == IntPtr.Zero || Hwnd == IntPtr.Zero ||
            !GetClientRect(Hwnd, out RECT r))
            return;
        int w = r.Right - r.Left, h = r.Bottom - r.Top;
        if (w <= 0 || h <= 0) return; // minimized: keep the last valid buffers
        SetWindowPos(_videoSurfaceHwnd, IntPtr.Zero, 0, 0, w, h,
                     0x0014 /*SWP_NOZORDER | SWP_NOACTIVATE*/);
    }

    /// <summary>''')

patch("Win32Window.cs",
'''                window._nativeUiThread = Thread.CurrentThread;
                if (window.Hwnd == IntPtr.Zero)
                    throw new InvalidOperationException("Native preview HWND creation failed.");
                created = window;
                ready.Set();''',
'''                window._nativeUiThread = Thread.CurrentThread;
                if (window.Hwnd == IntPtr.Zero)
                    throw new InvalidOperationException("Native preview HWND creation failed.");
                window.CreateNativeVideoSurface(); // ready means renderer can attach safely
                created = window;
                ready.Set();''')

# A real browser/projector only needs its parent titlebar for hit-testing.
# The video child is driven by WM_SIZE even while DefWindowProc is inside
# its native moving/resizing modal loop.
patch("Win32Window.cs",
'''            case 0x0003: // WM_MOVE
            case 0x0005: // WM_SIZE (including maximize and restore)
                UpdateGeometry();
                break;''',
'''            case 0x0003: // WM_MOVE
                UpdateGeometry();
                break;
            case 0x0005: // WM_SIZE (including maximize and restore)
                UpdateNativeVideoSurface();
                UpdateGeometry();
                break;''')

# The render thread owns the swapchain and all D3D resource lifetimes. Its
# presentation HWND is now the embedded video surface (for native framed
# windowed previews only). Smooth mode/fullscreen still draw to the parent.
patch("MirrorEngine.cs",
'''        var renderer = new Renderer(factory, device, context, window.Hwnd,
                                    clientW, clientH, cfg.CopyMode ? 8 : cfg.OutputBitDepth);''',
'''        var renderer = new Renderer(factory, device, context, window.PresentationHwnd,
                                    clientW, clientH, cfg.CopyMode ? 8 : cfg.OutputBitDepth);
        if (liveNativeWindow)
            Log("[PROJECTOR] Framed parent on UI thread; separate embedded video swapchain surface; dedicated capture/render thread.");''')

# Flush a new live frame at the configured FPS during native move/resize even
# when WGC has no new frame at a particular iteration. The old source texture
# is valid; never pretend that a re-presented frame is a NEW capture frame.
patch("MirrorEngine.cs",
'''            if (capture.Srv != null && (hasNewFrame || resized))
            {
                if (cfg.DebugLogging) DebugPulse("renderer.Render");''',
'''            // A native UI gesture must not prevent drawing the already
            // captured source into the child HWND. No extra frame injection
            // is needed for Smooth drag or borderless/fullscreen preview.
            bool nativeVideoRefresh = liveNativeWindow &&
                window.NativeInteractiveMoveSize && framesRendered > 0;
            if (capture.Srv != null && (hasNewFrame || resized || nativeVideoRefresh))
            {
                if (cfg.DebugLogging) DebugPulse("renderer.Render");''')

# The debug log needs enough information to tell whether later reported
# freezes happen in WGC capture, rendering, DXGI Present or DWM/HDMI output.
patch("MirrorEngine.cs",
'''                        $"preview_maximized={window.IsMaximized}, " +
                        $"preview_minimized={window.IsMinimized}.");''',
'''                        $"preview_maximized={window.IsMaximized}, " +
                        $"preview_minimized={window.IsMinimized}, " +
                        $"native_drag_resize={window.NativeInteractiveMoveSize}, " +
                        $"presentation_surface={(liveNativeWindow ? "embedded-child" : "top-level")}, " +
                        $"buffer_size={renderer.Width}x{renderer.Height}.");''')

patch("SettingsForm.cs",
'''        Note("While resizing, Windows stretches live frames; the preview buffer updates once on release.");''',
'''        Note("During native resize, the embedded projector video stays on a separate render thread.");
        Note("The normal Windows frame, buttons, snapping, and one visible preview remain unchanged.");''')

print("OBS-style embedded video surface built: 1 normal parent, 1 child video HWND, dedicated UI and rendering, live resize diagnostics")
