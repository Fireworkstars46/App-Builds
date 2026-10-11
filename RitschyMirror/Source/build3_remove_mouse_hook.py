"""Replace the legacy fullscreen-block low-level mouse hook with ClipCursor.

The previous completed build used WH_MOUSE_LL/SetWindowsHookEx to keep the
pointer off the HDMI target display. That is unnecessarily invasive and can
look AV-sensitive. Build 3 preserves the fullscreen_block purpose with the
documented ClipCursor API instead: while that mode is active the pointer is
confined to the source/non-target display rectangle, and ClipCursor(NULL)
releases it during normal renderer cleanup. No keyboard/mouse event capture,
hook thread, input logging, or process manipulation remains.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new, count=1):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != count:
        raise RuntimeError(f"{path}: expected {count} anchor(s), found {n}: {old[:140]!r}")
    p.write_text(s.replace(old, new, count), encoding="utf-8")
    print("patched", path)

patch("Win32Window.cs",
'''    // ── Maus-Sperre (output_mode "fullscreen_block") ─────────────────────
    // Low-Level-Maus-Hook haelt den Cursor aus dem Ziel-Display-Rechteck. Funktioniert
    // auf JEDEM Setup (auch Cross-Adapter), ohne echtes Exclusive-Fullscreen.
    private LowLevelMouseProc? _mouseProc;
    private IntPtr _mouseHook = IntPtr.Zero;
    private RECT _blockRect;
    private bool _inReposition;
    // Eigener Thread NUR für den Maus-Hook (siehe EnableCursorBlock).
    private Thread? _hookThread;
    private volatile uint _hookThreadId;
''',
'''    // ── Cursor confinement (output_mode "fullscreen_block") ───────────────
    // Build 3 intentionally uses documented ClipCursor rather than a global
    // low-level mouse hook. MirrorEngine passes the allowed SOURCE/non-target
    // display rectangle. Cleanup always releases confinement.
    private bool _cursorClipped;
''')

old_methods = '''    /// <summary>
    /// Cursor aus dem Rechteck (l,t,r,b in Bildschirm-Koordinaten) heraushalten.
    ///
    /// Der WH_MOUSE_LL-Hook läuft auf einem EIGENEN, schlanken Thread (nur GetMessage-Loop) —
    /// NICHT auf dem Render-Thread. Grund: ein Low-Level-Maus-Hook wird auf dem installierenden
    /// Thread dispatcht und braucht eine flotte Message-Pump. Liefe er auf dem Render-Thread,
    /// würde er nur ~1×/Frame bedient (Present(vsync) blockiert dazwischen) → die Maus würde
    /// systemweit auf Render-Kadenz gedrosselt + ruckeln. Auf dem dedizierten Thread kehrt der
    /// Callback sofort zurück → Cursor bleibt smooth (volle Polling-Rate), Sperre bleibt.
    /// </summary>
    public void EnableCursorBlock(int l, int t, int r, int b)
    {
        _blockRect = new RECT { Left = l, Top = t, Right = r, Bottom = b };
        if (_hookThread != null) return;
        _mouseProc = MouseHookProc; // als Feld halten (GC)

        using var ready = new ManualResetEventSlim(false);
        _hookThread = new Thread(() =>
        {
            _hookThreadId = GetCurrentThreadId();
            _mouseHook = SetWindowsHookEx(14 /*WH_MOUSE_LL*/, _mouseProc!, GetModuleHandle(null), 0);
            ready.Set();
            // Schlanke Loop — tut nichts außer den Hook-Callback prompt zu bedienen.
            while (GetMessage(out var msg, IntPtr.Zero, 0, 0) > 0)
            {
                TranslateMessage(ref msg);
                DispatchMessage(ref msg);
            }
            if (_mouseHook != IntPtr.Zero) { UnhookWindowsHookEx(_mouseHook); _mouseHook = IntPtr.Zero; }
        }) { IsBackground = true, Name = "MirrorMouseHook" };
        _hookThread.Start();
        ready.Wait(2000); // bis Hook installiert ist
    }

    public void DisableCursorBlock()
    {
        var t = _hookThread;
        if (t != null)
        {
            // WM_QUIT an den Hook-Thread → GetMessage-Loop endet → Unhook dort.
            if (_hookThreadId != 0) PostThreadMessage(_hookThreadId, 0x0012 /*WM_QUIT*/, IntPtr.Zero, IntPtr.Zero);
            if (Thread.CurrentThread != t) t.Join(2000);
            _hookThread = null;
            _hookThreadId = 0;
        }
        _mouseProc = null;
    }

    private IntPtr MouseHookProc(int nCode, IntPtr wParam, IntPtr lParam)
    {
        if (nCode >= 0 && !_inReposition && wParam.ToInt32() == 0x0200 /*WM_MOUSEMOVE*/)
        {
            var data = Marshal.PtrToStructure<MSLLHOOKSTRUCT>(lParam);
            int x = data.pt_x, y = data.pt_y;
            if (x >= _blockRect.Left && x < _blockRect.Right && y >= _blockRect.Top && y < _blockRect.Bottom)
            {
                // Auf die naechstgelegene Aussenkante schieben (kleinste Eindringtiefe).
                int dl = x - _blockRect.Left, dr = _blockRect.Right - x;
                int dt = y - _blockRect.Top,  db = _blockRect.Bottom - y;
                int min = System.Math.Min(System.Math.Min(dl, dr), System.Math.Min(dt, db));
                int nx = x, ny = y;
                if (min == dl)      nx = _blockRect.Left - 1;
                else if (min == dr) nx = _blockRect.Right;
                else if (min == dt) ny = _blockRect.Top - 1;
                else                ny = _blockRect.Bottom;
                _inReposition = true;
                SetCursorPos(nx, ny);
                _inReposition = false;
                return new IntPtr(1); // Bewegung schlucken
            }
        }
        return CallNextHookEx(_mouseHook, nCode, wParam, lParam);
    }
'''
new_methods = '''    /// <summary>
    /// Confine the pointer to an ALLOWED display rectangle while fullscreen_block
    /// is active. This uses documented ClipCursor only; it does not observe,
    /// intercept, log, or suppress individual mouse events.
    /// </summary>
    public void EnableCursorBlock(int l, int t, int r, int b)
    {
        var allowed = new RECT { Left = l, Top = t, Right = r, Bottom = b };
        _cursorClipped = ClipCursor(ref allowed);
    }

    public void DisableCursorBlock()
    {
        if (!_cursorClipped) return;
        ClipCursor(IntPtr.Zero);
        _cursorClipped = false;
    }
'''
patch("Win32Window.cs", old_methods, new_methods)

patch("Win32Window.cs",
'''    private delegate IntPtr WndProcDelegate(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);
    private delegate IntPtr LowLevelMouseProc(int nCode, IntPtr wParam, IntPtr lParam);
''',
'''    private delegate IntPtr WndProcDelegate(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);
''')

patch("Win32Window.cs",
'''    [StructLayout(LayoutKind.Sequential)]
    private struct MSLLHOOKSTRUCT
    {
        public int pt_x;
        public int pt_y;
        public uint mouseData;
        public uint flags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelMouseProc lpfn, IntPtr hMod, uint dwThreadId);
    [DllImport("user32.dll")] private static extern bool UnhookWindowsHookEx(IntPtr hhk);
    [DllImport("user32.dll")] private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] private static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] private static extern bool GetCursorPos(out POINT lpPoint);
''',
'''    [DllImport("user32.dll")] private static extern bool ClipCursor(ref RECT lpRect);
    [DllImport("user32.dll")] private static extern bool ClipCursor(IntPtr lpRect);
    [DllImport("user32.dll")] private static extern bool GetCursorPos(out POINT lpPoint);
''')

patch("Win32Window.cs",
'''    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetMessage(out MSG lpMsg, IntPtr hWnd, uint wMsgFilterMin, uint wMsgFilterMax);
    [DllImport("user32.dll")] private static extern bool PostThreadMessage(uint idThread, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("kernel32.dll")] private static extern uint GetCurrentThreadId();
''',
'''    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetMessage(out MSG lpMsg, IntPtr hWnd, uint wMsgFilterMin, uint wMsgFilterMax);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
''')

# Build an allowed source/non-target display rectangle once, then use it for the
# existing fullscreen_block and exclusive-fallback paths.
patch("MirrorEngine.cs",
'''        // Maus-Sperre / Exclusive je nach output_mode
        bool exclusive = false;
''',
'''        // Cursor confinement / Exclusive depending on output_mode.
        // Safer Build 3 implementation: confine to the source/non-target display
        // with ClipCursor; never install a low-level mouse hook.
        void EnableSafeCursorConfinement()
        {
            int allowedIndex = (debugSourceDisplay >= 0 && debugSourceDisplay != dstIdx)
                ? debugSourceDisplay : -1;
            if (allowedIndex < 0)
            {
                for (int i = 0; i < displays.Count; i++)
                    if (i != dstIdx) { allowedIndex = i; break; }
            }
            if (allowedIndex < 0)
            {
                Log("Cursor confinement skipped: no non-target display is available.");
                return;
            }
            var allowed = displays[allowedIndex];
            window.EnableCursorBlock(allowed.L, allowed.T, allowed.R, allowed.B);
            Log($"Cursor confinement active on allowed Display {allowedIndex} via ClipCursor.");
        }

        // Maus-Sperre / Exclusive je nach output_mode
        bool exclusive = false;
''')
patch("MirrorEngine.cs", 'window.EnableCursorBlock(dst.L, dst.T, dst.R, dst.B);', 'EnableSafeCursorConfinement();', count=2)

# Fail immediately if any hook code survived the transformation.
final = (root / "Win32Window.cs").read_text(encoding="utf-8")
for forbidden in ("SetWindowsHookEx", "UnhookWindowsHookEx", "CallNextHookEx", "LowLevelMouseProc", "MSLLHOOKSTRUCT", "MirrorMouseHook"):
    if forbidden in final:
        raise RuntimeError(f"AV-sensitive mouse-hook token still present: {forbidden}")
if "ClipCursor" not in final:
    raise RuntimeError("ClipCursor replacement missing")
print("Replaced fullscreen-block low-level mouse hook with documented ClipCursor confinement")
