# UxPlay Quality Launcher Full — v91o Build 75

Corrective feature build from the verified v91o Build 74 source.

- Moves the visible Wi-Fi renderer Pin/Unpin control off the mirrored video/client area and into the native title-bar area immediately left of Minimize.
- Keeps the real Windows Sizable frame from Build 73/74 for native drag, Minimize, Maximize/Restore, Close, snap, and edge/corner resizing.
- Uses a renderer-owned, no-taskbar, no-activation title-bar control; no DLL/code injection into UxPlay is added and the native frame is not replaced.
- Pin state still uses the existing shared ToggleRendererPin / SetRendererPinned path and remains synchronized with system-menu/tray pin state.
- Preserves Wi-Fi section-only tests, Wi-Fi FPS controls, firewall repair, runtime self-repair, Direct USB behavior, settings/data paths, AppId, and installer identity.

Final source ZIP SHA-256: `1d940dbca354f468912d8c5991d6f99a73a6599de672c4c7b11594f9b11ec917`

Validation status: source static audit PASS 36/36; ZIP integrity PASS. Windows C# compile, installer build, live iPhone/AirPlay, title-bar placement, pin click/topmost behavior, and window interaction are NOT TESTED yet.
