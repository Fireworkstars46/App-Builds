"""Native Live 2: keep actual frame updates through ordinary Win32 live sizing.

Apply after native_live_ui_thread.py. A normal Win32 titlebar drag enters a
modal move/size loop on the dedicated UI thread, not the render thread.
A second problem remained: WM_SIZE arrives repeatedly during edge resizing,
and the engine called DXGI ResizeBuffers AND wrote preview geometry/config
repeatedly during that interactive loop, disrupting flip-model presentation.
Keep Present running with the previous backbuffers while the OS stretches
their content during live resizing; resize once, to the final client size,
after mouse release. Save geometry only after the interaction ends.

For monitor capture, continue rendering new frames during the drag. Do not
modify the capture source, HDMI target, recursion, FPS limit, saved display
topology, or the separate Smooth live drag path. One native HWND only.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    f = root / path
    s = f.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {n}: {old[:125]!r}")
    f.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("Win32Window.cs",
'''    private Thread? _nativeUiThread;

    /// <summary>''',
'''    private Thread? _nativeUiThread;
    // Set by the native HWND's UI thread; checked by the independent
    // capture/render thread. Avoid swapping buffers inside a live Windows
    // WM_ENTERSIZEMOVE .. WM_EXITSIZEMOVE interaction.
    private volatile bool _nativeInteractiveMoveSize;
    public bool NativeInteractiveMoveSize => _nativeInteractiveMoveSize;

    /// <summary>''')

patch("Win32Window.cs",
'''    private IntPtr InstanceWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
    {
        switch (msg)
        {
            case 0x0084: // WM_NCHITTEST:''',
'''    private IntPtr InstanceWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
    {
        switch (msg)
        {
            case 0x0231: // WM_ENTERSIZEMOVE: native non-client modal loop begins
                if (_nativeUiThread != null)
                    _nativeInteractiveMoveSize = true;
                break;
            case 0x0232: // WM_EXITSIZEMOVE: resume one final buffer resize/save
                if (_nativeUiThread != null)
                {
                    _nativeInteractiveMoveSize = false;
                    UpdateGeometry();
                    GeometryDirty = true;
                }
                break;
            case 0x0084: // WM_NCHITTEST:''')

patch("MirrorEngine.cs",
'''            if (windowed && window.GeometryDirty
                && window.ReadSavedGeometry(out int px, out int py,''',
'''            // Avoid writing the JSON config continuously during Windows'
            // modal move/resize (or forcing hot reload for every pixel).
            // One geometry snapshot is saved after WM_EXITSIZEMOVE.
            if (windowed && !window.NativeInteractiveMoveSize &&
                window.GeometryDirty
                && window.ReadSavedGeometry(out int px, out int py,''')

patch("MirrorEngine.cs",
'''            if (windowed && !window.IsMinimized)
            {
                int newW = window.ClientWidth, newH = window.ClientHeight;
                if (newW > 0 && newH > 0)
                    resized = renderer.Resize(newW, newH);
            }''',
'''            // DXGI flip-model ResizeBuffers is expensive and can leave the
            // compositor showing a blank/stale image when called on every
            // WM_SIZE while Windows is running its native drag/resize loop.
            // Keep producing/presenting NEW frames using the existing buffers
            // during the gesture; DWM scales the preview to the changing
            // client rectangle. ResizeBuffers once at final mouse release.
            if (windowed && !window.IsMinimized &&
                !window.NativeInteractiveMoveSize)
            {
                int newW = window.ClientWidth, newH = window.ClientHeight;
                if (newW > 0 && newH > 0)
                    resized = renderer.Resize(newW, newH);
            }''')

patch("SettingsForm.cs",
'''        Note("Normal Windows now uses a separate UI thread: capture/render can continue during native move and resize.");''',
'''        Note("Normal Windows: a separate UI thread keeps video rendering during native drag/resize.");
        Note("While resizing, Windows stretches live frames; the preview buffer updates once on release.");''')

print("Native Live 2: avoid DXGI ResizeBuffers and config disk writes during live native drag/resize")
