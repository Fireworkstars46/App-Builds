"""Fix smooth live drag being vertically locked at the top after bounce.

Applies AFTER live_top_edge_bounce.py. The previous code calculates
maxY = max(work.Top, work.Bottom - window.Height). For an unusually tall
normal window, maxY is always the top edge, so dragging downward cannot
change Y. Keep enough of the titlebar visible when moving an oversized
window, instead of trying to keep all of its height inside the work area.
Retains the partial top overshoot and release-time bounce behavior.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(before)
    if n != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {n}: {before[:100]!r}")
    p.write_text(s.replace(before, after, 1), encoding="utf-8")
    print("Patched", path)

# With KeepOnDisplay ON, its earlier maxY was work.Top for a too-tall
# window. Permit the top/titlebar to move down into the display anyway.
patch("Win32Window.cs",
'''                        int maxY = Math.Max(_gestureBounds.Top, _gestureBounds.Bottom - h);
                        moveX = Math.Clamp(moveX, _gestureBounds.Left, maxX);''',
'''                        int maxY = h > _gestureBounds.Height
                            ? Math.Max(_gestureBounds.Top, _gestureBounds.Bottom - 48)
                            : Math.Max(_gestureBounds.Top, _gestureBounds.Bottom - h);
                        moveX = Math.Clamp(moveX, _gestureBounds.Left, maxX);''')

# With KeepOnDisplay OFF, preserve cross-monitor dragging and the
# half-height upward overshoot. If the window exceeds the current monitor
# height, cap Y so at least its top 48 pixels remain visible near the
# bottom instead of pinning it to onCursor.Top (the original bug).
patch("Win32Window.cs",
'''                            moveY = Math.Clamp(moveY, onCursor.Top - topOvershoot,
                                               Math.Max(onCursor.Top, onCursor.Bottom - h));''',
'''                            int maxMoveY = h > onCursor.Height
                                ? Math.Max(onCursor.Top, onCursor.Bottom - 48)
                                : Math.Max(onCursor.Top, onCursor.Bottom - h);
                            moveY = Math.Clamp(moveY, onCursor.Top - topOvershoot,
                                               maxMoveY);''')

print("Fixed vertical lock of oversized smooth-drag preview while retaining top bounce")
