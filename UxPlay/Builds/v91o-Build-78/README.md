# UxPlay Quality Launcher Full — v91o Build 78

Requested UI change:
- Make the renderer title-bar Pin control visibly change color, similar to MirrorTo.
- Gray = unpinned.
- Bright blue = pinned.

Implementation:
- The renderer keeps the real native Windows sizable frame.
- The native small title-bar icon slot is used as the one-click Pin/Unpin control.
- Windows draws the title-bar pin icon; there is no floating overlay or custom non-client repaint loop.
- Left-clicking the native title-bar pin icon toggles Always-on-Top.
- Right-click / Alt+Space keeps the system-menu `Pin on top` fallback.
- Native caption dragging, Minimize, Maximize/Restore, Close, and edge/corner resizing are preserved.
- No DLL injection/hooking is used.

Static/source audit: 48/48 PASS.

Build 78 remains NOT DONE / PENDING until Windows compile, installer build, and live Wi-Fi/AirPlay GUI validation are completed.
