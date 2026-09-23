"""Allow smooth-drag overshoot and snap a partly off-screen window back on release.

Runs AFTER live_browser_snap_restore.py.  The previous Live Snap version
clamped the top continuously and maximized the window on release near
the top; neither behavior matches the requested drag-half-off-then-bounce-
back interaction.  Keep the HWND in normal/restored state and render
continuously throughout dragging. The existing maximize button remains
fully functional, and dragging a manually maximized title bar still
restores the saved normal size.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(before)
    if n != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {before[:115]!r}")
    p.write_text(s.replace(before, after, 1), encoding="utf-8")
    print("Patched", path)

# The old containment branch only runs when KeepOnDisplay is ON. Preserve
# its horizontal and resize rules but allow the upper edge to travel beyond
# the screen while the user is actively dragging. Dragging is never allowed
# to completely lose the titlebar or preview: 50% window-height overshoot.
patch("Win32Window.cs",
'''                        moveY = Math.Clamp(moveY, _gestureBounds.Top, maxY);
                        const int snapPx = 12;''',
'''                        // Permit half the window above the top edge during
                        // the gesture; return it to the work area on release.
                        int topOvershoot = Math.Max(32, h / 2);
                        moveY = Math.Clamp(moveY, _gestureBounds.Top - topOvershoot, maxY);
                        const int snapPx = 12;''')

patch("Win32Window.cs",
'''                        if (moveY - _gestureBounds.Top <= snapPx) moveY = _gestureBounds.Top;
                        else if (maxY - moveY <= snapPx) moveY = maxY;''',
'''                        // Do not magnetize the top edge during mouse motion:
                        // the snap happens only when the mouse is released.
                        if (moveY >= _gestureBounds.Top &&
                            maxY - moveY <= snapPx) moveY = maxY;''')

# When KeepOnDisplay is OFF, leave the window able to cross between monitors.
# The cursor's monitor supplies work-area top and an overshoot limit. Clamping
# the top during WM_MOUSEMOVE caused it to look pinned to the desktop's edge.
patch("Win32Window.cs",
'''                            moveY = Math.Clamp(moveY, onCursor.Top,
                                               Math.Max(onCursor.Top, onCursor.Bottom - h));''',
'''                            int topOvershoot = Math.Max(32, h / 2);
                            moveY = Math.Clamp(moveY, onCursor.Top - topOvershoot,
                                               Math.Max(onCursor.Top, onCursor.Bottom - h));''')

# Remove auto-maximize entirely; if the window's top is above its target
# screen's usable top on mouse release, snap the SAME normal-sized HWND so
# its top edge equals that exact work-area top. Restrict the vertical bottom
# to the usable area too. The browser-style drag-down restore from an
# explicitly maximized window remains in the earlier patch.
patch("Win32Window.cs",
'''                    // The native WM_SIZE event still updates backbuffer size
                    // on the next render-loop iteration, so preview stays live.
                    if (finishingTitlebarDrag && GetCursorPos(out POINT released))
                    {
                        var monitor = System.Windows.Forms.Screen.FromPoint(
                            new System.Drawing.Point(released.X, released.Y));
                        // The physical TOP edge is the browser's maximize zone.
                        // Releasing elsewhere preserves the restored dimensions.
                        if (!IsZoomed(hWnd) &&
                            released.Y <= monitor.Bounds.Top + 12 &&
                            released.Y >= monitor.Bounds.Top - 2 &&
                            released.X >= monitor.Bounds.Left &&
                            released.X < monitor.Bounds.Right)
                        {
                            ShowWindow(hWnd, 3 /*SW_MAXIMIZE*/);
                        }
                    }
                    UpdateGeometry();''',
'''                    // Snap an overshot window back AFTER the user releases
                    // the mouse, never maximize it or resize its normal rect.
                    if (finishingTitlebarDrag &&
                        !IsZoomed(hWnd) &&
                        GetWindowRect(hWnd, out RECT releasedRect))
                    {
                        var monitor = System.Windows.Forms.Screen.FromHandle(hWnd);
                        var work = monitor.WorkingArea;
                        int h = Math.Max(1, releasedRect.Bottom - releasedRect.Top);
                        int landingTop = releasedRect.Top;
                        if (releasedRect.Top < work.Top)
                            landingTop = work.Top;
                        else if (releasedRect.Bottom > work.Bottom && h <= work.Height)
                            landingTop = work.Bottom - h;
                        if (landingTop != releasedRect.Top)
                        {
                            SetWindowPos(hWnd, IntPtr.Zero,
                                         releasedRect.Left, landingTop, 0, 0,
                                         0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                        }
                    }
                    UpdateGeometry();''')

patch("SettingsForm.cs",
'''        Note("Smooth live drag: move to top edge to maximize, pull title bar down to restore.");
        Note("With one-display confinement OFF, smooth drag can cross displays while staying on-screen.");''',
'''        Note("Smooth live drag: pull partly above the screen; release to return to its top edge.");
        Note("Dragging to the top does NOT maximize. Use the maximize button if wanted.");
        Note("With one-display confinement OFF, smooth drag can cross displays.");''')

print("Smooth live drag now permits partial top overshoot and snaps back at mouse release, with no auto-maximize")
