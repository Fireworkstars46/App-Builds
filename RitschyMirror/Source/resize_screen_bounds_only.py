"""Limit live edge resizing to the selected monitor without restricting movement.

Runs after fix_tall_window_vertical_drag.py. Moving the whole window keeps
the existing cross-display / partial-off-screen behavior. At the start of
a smooth resize, normalize the preview into the work area of the screen at
the pointer, then clamp dragged edges to that work area independently of
the KeepOnDisplay MOVEMENT option. Prevents windows growing off any edge
during live resizing while keeping the normal title bar and render loop.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(before)
    if n != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {before[:130]!r}")
    p.write_text(s.replace(before, after, 1), encoding="utf-8")
    print("Patched", path)

patch("Win32Window.cs",
'''                    if (hit >= 10 && hit <= 17) // HTLEFT..HTBOTTOMRIGHT
                    {
                        _resizeHit = hit;
                        _resizeStartPoint = origin;
                        _resizeStartRect = rect;
                        _manualResize = true;
                        SetCapture(hWnd);
                        return IntPtr.Zero;
                    }''',
'''                    if (hit >= 10 && hit <= 17) // HTLEFT..HTBOTTOMRIGHT
                    {
                        // The pointer selects which monitor the resize should
                        // stay inside. This is intentionally independent of
                        // KeepOnDisplay, which only governs whole-window moves.
                        _gestureBounds = System.Windows.Forms.Screen.FromPoint(
                            new System.Drawing.Point(origin.X, origin.Y)).WorkingArea;
                        var area = _gestureBounds;
                        if (area.Width <= 0 || area.Height <= 0)
                            return IntPtr.Zero;

                        // Moving may have left some of the preview outside the
                        // screen. Bring it inside at resize START so all four
                        // edges, including those not being dragged, are visible.
                        int w = Math.Min(rect.Right - rect.Left, area.Width);
                        int h = Math.Min(rect.Bottom - rect.Top, area.Height);
                        int sx = Math.Clamp(rect.Left, area.Left, area.Right - w);
                        int sy = Math.Clamp(rect.Top, area.Top, area.Bottom - h);
                        if (sx != rect.Left || sy != rect.Top ||
                            w != rect.Right - rect.Left ||
                            h != rect.Bottom - rect.Top)
                        {
                            SetWindowPos(hWnd, IntPtr.Zero, sx, sy, w, h,
                                         0x0014 /*NOZORDER | NOACTIVATE*/);
                            if (!GetWindowRect(hWnd, out rect))
                                return IntPtr.Zero;
                        }

                        _resizeHit = hit;
                        _resizeStartPoint = origin;
                        _resizeStartRect = rect;
                        _manualResize = true;
                        SetCapture(hWnd);
                        return IntPtr.Zero;
                    }''')

patch("Win32Window.cs",
'''                    if (KeepOnDisplay)
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
                    SetWindowPos(hWnd, IntPtr.Zero, l, t, r - l, b - t,''',
'''                    // ALWAYS constrain resizing to the monitor selected when
                    // the edge drag began. Whole-window movement still uses
                    // the user's separate KeepOnDisplay setting.
                    int minW = Math.Min(320, _gestureBounds.Width);
                    int minH = Math.Min(240, _gestureBounds.Height);
                    if (left)
                        l = Math.Clamp(l, _gestureBounds.Left, r - minW);
                    if (right)
                        r = Math.Clamp(r, l + minW, _gestureBounds.Right);
                    if (top)
                        t = Math.Clamp(t, _gestureBounds.Top, b - minH);
                    if (bottom)
                        b = Math.Clamp(b, t + minH, _gestureBounds.Bottom);
                    if (l < _gestureBounds.Left || r > _gestureBounds.Right ||
                        t < _gestureBounds.Top || b > _gestureBounds.Bottom ||
                        r <= l || b <= t)
                        return IntPtr.Zero;
                    SetWindowPos(hWnd, IntPtr.Zero, l, t, r - l, b - t,''')

patch("SettingsForm.cs",
'''        Note("With one-display confinement OFF, smooth drag can cross displays.");''',
'''        Note("With one-display confinement OFF, smooth drag can cross displays.");
        Note("Live resizing always stays within the screen where the resize starts.");''')

print("Live window MOVE remains unchanged; live RESIZE now stays within one screen")
