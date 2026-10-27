# UxPlay Quality Launcher Full — v91o Build 76

Corrective build from the exact verified v91o Build 75 source.

## Confirmed Build 75 regression
The user's Windows video/log showed that the Build 75 floating owned title-bar pin overlay caused unreliable title-bar dragging, visible pin flicker/glitching, and crowding/cutoff around the native Minimize area. AirPlay itself still attached successfully.

## Build 76 correction
- Removes the Build 75 floating/owned title-bar overlay window completely.
- Keeps the real Windows Sizable renderer frame.
- Paints a compact Pin/Unpin control directly into the app-owned renderer window's non-client title bar.
- Only the compact pin rectangle intercepts a click; the rest of the caption remains Windows-owned for native drag and double-click maximize.
- Minimize, Maximize/Restore, and Close remain untouched native Windows caption buttons.
- Adds a safe caption minimum width based on Windows caption-button metrics so native controls and a useful drag area cannot be squeezed off-screen.
- Pins the persistent renderer host first rather than changing z-order on the temporary UxPlay/GStreamer window while it is waiting to be embedded.
- Preserves Wi-Fi section-only tests, Wi-Fi FPS controls, firewall repair, runtime self-repair, Direct USB behavior, paths/settings/AppId/installer identity, tray behavior, and diagnostics.
- No title-bar DLL injection/hooking is used in the Build 76 main build path.

## Validation
Static/source audit: 38/38 PASS.
ZIP integrity: PASS.
Windows C# compile, installer build, live AirPlay, real native-caption painting, drag, caption-button visibility, and pin/topmost behavior are NOT TESTED here and require the user's Windows PC.

Final source ZIP SHA-256: `6558a7661fc22ba058bd358de8a2c34a0319e9285085a089f21a65ab357dce84`
