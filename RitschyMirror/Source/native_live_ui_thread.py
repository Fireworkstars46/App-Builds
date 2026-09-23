"""Native Windows frame with live capture using a separate HWND/message-pump thread.

Runs after resize_screen_bounds_only.py. RitschyMirror's original window was
created on the render thread. Native Windows drag/resize enters a modal
message loop inside DefWindowProc, so that same thread cannot render a new
frame until the mouse button is released. Create ONLY the native windowed
preview HWND on a dedicated GUI thread and pump Windows messages there.
The existing capture/D3D render loop stays on its own thread. This preserves
standard Windows title bar, resize handles, minimize/maximize/restore, cross-
monitor movement, taskbar, and Win10 Aero Snap, while rendering continues.

Smooth live drag and fullscreen retain their existing single-thread mode;
no second visible window is created. The native UI thread must also own
DestroyWindow; the renderer posts WM_CLOSE and joins during cleanup.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    file = root / path
    content = file.read_text(encoding="utf-8")
    matches = content.count(old)
    if matches != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {matches}: {old[:120]!r}")
    file.write_text(content.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("Win32Window.cs",
'''    public bool Running { get; private set; } = true;''',
'''    // Read by the render worker and written by the owning native UI thread.
    public volatile bool Running = true;
    private Thread? _nativeUiThread;

    /// <summary>
    /// Create one real, ordinary Windows preview HWND on its OWN UI thread.
    /// Native move/resize may run DefWindowProc's modal move loop on that
    /// thread without stopping the capture/render loop on the engine thread.
    /// </summary>
    public static Win32Window CreateLiveNativePreview(string title, int x, int y,
            int width, int height, bool borderless, bool projectorBorderless = false)
    {
        Win32Window? created = null;
        Exception? creationError = null;
        using var ready = new ManualResetEventSlim(false);

        var uiThread = new Thread(() =>
        {
            try
            {
                var window = new Win32Window(title, x, y, width, height,
                                             borderless, projectorBorderless);
                window._nativeUiThread = Thread.CurrentThread;
                if (window.Hwnd == IntPtr.Zero)
                    throw new InvalidOperationException("Native preview HWND creation failed.");
                created = window;
                ready.Set();

                // Only this thread dispatches events to this HWND. Moving and
                // sizing run inside Windows' native UI modal loop; the separate
                // engine/render thread is unaffected.
                while (window.Running)
                {
                    window.PumpMessages();
                    if (window.Running) Thread.Sleep(1);
                }
                window.Destroy(); // owning thread, never renderer thread
            }
            catch (Exception ex)
            {
                creationError = ex;
                ready.Set();
                if (created != null && created.Hwnd != IntPtr.Zero)
                    created.Destroy();
            }
        })
        {
            IsBackground = true,
            Name = "RitschyMirror Native Preview UI"
        };
        uiThread.SetApartmentState(ApartmentState.STA);
        uiThread.Start();
        if (!ready.Wait(10000))
            throw new TimeoutException("Timed out waiting for the native preview window.");
        if (creationError != null)
            throw new InvalidOperationException("Failed to create native preview window.", creationError);
        if (created == null)
            throw new InvalidOperationException("Native preview UI thread did not create a window.");
        return created;
    }''')

patch("Win32Window.cs",
'''    public void PumpMessages()
    {
        while (PeekMessage(out var msg, IntPtr.Zero, 0, 0, 1 /*PM_REMOVE*/))''',
'''    public void PumpMessages()
    {
        // The rendering worker never consumes native UI thread messages or
        // enters DefWindowProc's blocking Windows move/resize loop.
        if (_nativeUiThread != null && Thread.CurrentThread != _nativeUiThread)
            return;
        while (PeekMessage(out var msg, IntPtr.Zero, 0, 0, 1 /*PM_REMOVE*/))''')

patch("Win32Window.cs",
'''    public void Destroy()
    {
        DisableCursorBlock();
        var h = Hwnd;''',
'''    public void Destroy()
    {
        if (_nativeUiThread is Thread ui && Thread.CurrentThread != ui)
        {
            // DestroyWindow must run on the thread which created the HWND.
            // Let that thread process WM_CLOSE and drain its own WM_QUIT.
            if (Hwnd != IntPtr.Zero)
                PostMessage(Hwnd, 0x0010 /*WM_CLOSE*/, IntPtr.Zero, IntPtr.Zero);
            if (ui.IsAlive && !ui.Join(5000))
                throw new TimeoutException("Native preview UI did not finish closing.");
            return;
        }
        DisableCursorBlock();
        var h = Hwnd;''')

patch("Win32Window.cs",
'''    [DllImport("user32.dll")] private static extern bool PostThreadMessage(uint idThread, uint Msg, IntPtr wParam, IntPtr lParam);''',
'''    [DllImport("user32.dll")] private static extern bool PostThreadMessage(uint idThread, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);''')

patch("MirrorEngine.cs",
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH,
                                     borderless, projectorBorderless: projector && cfg.ProjectorBorderless)
        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,''',
'''        // A native window on the SAME thread as capture cannot update during
        // DefWindowProc's modal drag/resize. Dedicated UI thread keeps the
        // ordinary Windows frame while capture/render continues independently.
        // Borderless projector, smooth manual dragging, and fullscreen retain
        // their original window lifecycle. Exactly ONE preview HWND is made.
        bool liveNativeWindow = windowed && cfg.NativePreviewWindow &&
                                !(projector && cfg.ProjectorBorderless);
        var window = liveNativeWindow
            ? Win32Window.CreateLiveNativePreview("RitschyMirror", x, y, outW, outH,
                     borderless, projectorBorderless: false)
            : new Win32Window("RitschyMirror", x, y, outW, outH,
                     borderless, projectorBorderless: projector && cfg.ProjectorBorderless)
        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,''')

# The conditional expression above is used as an object-initializer target:
# C# only accepts 'new ... { }', not 'conditional { }'. Apply settings in a
# separate statement after creating the one window.
patch("MirrorEngine.cs",
'''        {
            NativeMoveResize = windowed && cfg.NativePreviewWindow,
            KeepOnDisplay = windowed && !cfg.NativePreviewWindow && cfg.KeepPreviewOnDisplay,
        };
        if (windowed)''',
'''        ;
        window.NativeMoveResize = windowed && cfg.NativePreviewWindow;
        window.KeepOnDisplay = windowed && !cfg.NativePreviewWindow && cfg.KeepPreviewOnDisplay;
        if (liveNativeWindow)
            Log("[WINDOW] Standard Windows frame/message loop on dedicated UI thread; rendering continues on engine thread during native move/resize.");
        if (windowed)''')

patch("SettingsForm.cs",
'''        Note("Preview image may pause during a native drag until mouse release.");''',
'''        Note("Normal Windows now uses a separate UI thread: capture/render can continue during native move and resize.");
        Note("Normal Windows retains titlebar, buttons, Aero Snap and cross-screen dragging.");''')

print("Dedicated native HWND UI thread enabled; browser-like native drag and live rendering separated")
