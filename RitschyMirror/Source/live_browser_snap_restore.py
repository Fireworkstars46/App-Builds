"""Browser-like top maximize and drag-down restore with nonblocking live preview.

Runs after recursive_projector_mode.py. Only changes Smooth live drag on a
windowed preview. Regular/native Win32 movement retains its own Aero Snap.

A custom WM_NCLBUTTONDOWN handler previously refused to drag a maximized
window, and smooth mouse moves were not clamped when KeepOnDisplay was OFF.
This patch restores a maximized preview into its remembered size under the
cursor, maximizes it on release at the screen's top edge, and keeps dragging
inside the combined desktop work area without locking it to one monitor.
The same preview HWND and renderer continue running during the drag.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    p = root / path
    text = p.read_text(encoding="utf-8")
    hits = text.count(before)
    if hits != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {hits}: {before[:115]!r}")
    p.write_text(text.replace(before, after, 1), encoding="utf-8")
    print("Patched", path)

patch("Win32Window.cs",
'''                if (!IsZoomed(hWnd) && GetCursorPos(out POINT origin)
                    && GetWindowRect(hWnd, out RECT rect))
                {
                    _gestureBounds = System.Windows.Forms.Screen.FromHandle(hWnd).WorkingArea;
                    if (hit == 2 /*HTCAPTION*/)''',
'''                if (GetCursorPos(out POINT origin)
                    && GetWindowRect(hWnd, out RECT rect))
                {
                    _gestureBounds = System.Windows.Forms.Screen.FromHandle(hWnd).WorkingArea;
                    // Standard browser gesture: pull a maximized title bar
                    // down and restore the saved normal size, without entering
                    // DefWindowProc's modal move/resize loop.
                    if (hit == 2 /*HTCAPTION*/ && IsZoomed(hWnd))
                    {
                        int maximizedWidth = Math.Max(1, rect.Right - rect.Left);
                        double titlebarFraction = Math.Clamp(
                            (double)(origin.X - rect.Left) / maximizedWidth, 0.08, 0.92);
                        _manualDrag = true;
                        ShowWindow(hWnd, 9 /*SW_RESTORE*/);
                        if (!GetWindowRect(hWnd, out RECT restored))
                        {
                            _manualDrag = false;
                            return IntPtr.Zero;
                        }
                        int restoredWidth = Math.Max(320, restored.Right - restored.Left);
                        _dragOffsetX = (int)(restoredWidth * titlebarFraction);
                        _dragOffsetY = Math.Min(18, Math.Max(8, restored.Bottom - restored.Top));
                        SetWindowPos(hWnd, IntPtr.Zero,
                                     origin.X - _dragOffsetX, origin.Y - _dragOffsetY,
                                     0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                        SetCapture(hWnd);
                        return IntPtr.Zero;
                    }
                    if (hit == 2 /*HTCAPTION*/)''')

patch("Win32Window.cs",
'''                    SetWindowPos(hWnd, IntPtr.Zero, moveX, moveY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;''',
'''                    if (!KeepOnDisplay && GetWindowRect(hWnd, out RECT moveRect))
                    {
                        // Allow a window to pass naturally over the seam
                        // between displays, but do not let its normal-sized
                        // rectangle disappear beyond the OUTER desktop edges.
                        // For the taskbar/top edge use the cursor's monitor
                        // so the title bar always remains reachable.
                        var screens = System.Windows.Forms.Screen.AllScreens;
                        if (screens.Length != 0)
                        {
                            int virtualLeft = screens.Min(s => s.WorkingArea.Left);
                            int virtualRight = screens.Max(s => s.WorkingArea.Right);
                            int w = Math.Max(1, moveRect.Right - moveRect.Left);
                            moveX = Math.Clamp(moveX, virtualLeft,
                                               Math.Max(virtualLeft, virtualRight - w));
                            var onCursor = System.Windows.Forms.Screen.FromPoint(
                                new System.Drawing.Point(cursor.X, cursor.Y)).WorkingArea;
                            int h = Math.Max(1, moveRect.Bottom - moveRect.Top);
                            moveY = Math.Clamp(moveY, onCursor.Top,
                                               Math.Max(onCursor.Top, onCursor.Bottom - h));
                        }
                    }
                    SetWindowPos(hWnd, IntPtr.Zero, moveX, moveY,
                                 0, 0, 0x0015 /*NOZORDER | NOSIZE | NOACTIVATE*/);
                    return IntPtr.Zero;''')

patch("Win32Window.cs",
'''                if (_manualDrag || _manualResize)
                {
                    _manualDrag = false;
                    _manualResize = false;
                    UpdateGeometry();
                    GeometryDirty = true;
                    ReleaseCapture();
                    return IntPtr.Zero;
                }
                break;
            case 0x0215: // WM_CAPTURECHANGED: cancelled by Windows''',
'''                if (_manualDrag || _manualResize)
                {
                    bool finishingTitlebarDrag = _manualDrag;
                    _manualDrag = false;
                    _manualResize = false;
                    ReleaseCapture();
                    // The native WM_SIZE event still updates backbuffer size
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
                    UpdateGeometry();
                    GeometryDirty = true;
                    return IntPtr.Zero;
                }
                break;
            case 0x0215: // WM_CAPTURECHANGED: cancelled by Windows''')

patch("SettingsForm.cs",
'''        Note("Preview image may pause during a native drag until mouse release.");''',
'''        Note("Preview image may pause during a native drag until mouse release.");
        Note("Smooth live drag: move to top edge to maximize, pull title bar down to restore.");
        Note("With one-display confinement OFF, smooth drag can cross displays while staying on-screen.");''')

print("Live browser-style maximize, drag-to-restore and on-screen movement patch applied")
