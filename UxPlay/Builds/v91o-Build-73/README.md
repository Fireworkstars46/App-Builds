# UxPlay Quality Launcher Full — v91o Build 73

Corrective Build 73 from verified Build 72 source.

- Wi-Fi persistent renderer now uses a real native Windows resizable frame instead of a borderless fake title bar.
- Restores normal Windows title-bar dragging, Minimize, Maximize/Restore, Close, and native edge/corner resizing.
- GStreamer Direct3D11 remains embedded as a borderless child.
- First-connect renderer polling reduced from 100 ms to 25 ms to reduce the temporary standalone-window flash before stable attach.
- Preserves Build 72 section-only tests, Wi-Fi FPS controls, firewall repair, runtime self-repair, Direct USB behavior, settings/data paths, AppId, and update identity.

Final source ZIP SHA-256: `3611d8c6ae2359cb479d07131e3e6db04b588bc29faf76d1cffe788b013bed36`

Status: source static audit PASS 28/28. Windows compile, installer build, live iPhone/Wi-Fi test, and real window interaction are NOT TESTED yet. Permanent GitHub binary/source-ZIP archive is INCOMPLETE because the available GitHub connector does not expose a direct binary/release-asset upload from the local build file.
