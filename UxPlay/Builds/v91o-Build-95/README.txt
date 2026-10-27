UxPlay Quality Launcher Full - v91o Build 95
Rollback Build 94 hybrid + fail-fast Direct USB test

WHY THIS BUILD EXISTS
Build 94 introduced an Auto-only hybrid path: exact-parent libusb0 activation followed by UsbDk live QuickTime streaming. Real runtime evidence showed the UsbDk Valeria protocol handler failed almost immediately with an Input/Output Error and stopped, but the outer backend process stayed alive. The section test therefore waited its full 300-second no-popup safety window and made the whole app look frozen.

TARGETED BUILD 95 CHANGE
1. Roll back the Build 94 hybrid path completely by basing Build 95 on the exact Build 93 source.
2. Auto returns to Build 93's exact-parent libusb0 reference capture behavior.
3. Preserve the Build 93 read-only driver-stack diagnostic. Do NOT remove AppleLowerFilter/AppleKmdfFilter, do NOT rebind a driver, do NOT uninstall Apple software, and do NOT disable security software.
4. Add a fail-fast guard in Direct USB Test. If the backend tail reports USB_ERROR, USB_ERROR_CODE, a Valeria USB read error, a stopped Valeria protocol handler, or a traceback before H.264 reaches the renderer, the test stops immediately instead of sitting in the silent safety window.
5. Reduce the no-popup safety window from 300 seconds to a maximum of 60 seconds. No project-owned Keep-Waiting prompt is reintroduced.

PRESERVED
- Build 93 read-only Apple/libusb0 driver-stack inventory.
- Build 92 activation-helper handoff.
- Build 91 no-startup CLEAR_FEATURE behavior for libusb0.
- Build 90 claim-first/configuration-0 repair and synchronous large reads.
- Canonical PING/CWPA/CVRP/FEED protocol bytes and handlers. The PING bytes already match exactly, so Build 95 does not change protocol framing.
- One-click Direct USB Test flow. No new project-owned OK/Yes/No/Keep-Waiting prompt is added. Windows UAC and iOS-owned Trust/Allow/passcode prompts remain outside our app and cannot be bypassed.
- Automatic exact-iPhone libusb0 prerequisite install/restart only when the existing narrow prerequisite states require it.
- Build 86 prompt responsiveness fix for non-test/manual paths.
- Persistent black Direct USB renderer and saved geometry.
- Build 80 known-good Wi-Fi renderer behavior unchanged.
- Stable AppId {F07F126D-812E-48F9-A296-46D459067E7C}.
- Per-user installation identity/settings paths.
- Windows Firewall, Bitdefender/Defender/SmartScreen remain enabled.

REMOVED FROM BUILD 94
- No Auto caution-stack hybrid capture.
- No libusb0-activation-only -> UsbDk-stream handoff.
- No five-minute silent wait after a dead Valeria protocol thread.

VALIDATION STATUS
- Static/source regression audit: 198/198 PASS.
- Python backend syntax: PASS.
- ZIP integrity: PASS.
- Windows C# compile: NOT TESTED in this Linux environment.
- Real fail-fast behavior on Windows: NOT TESTED.
- Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
- Real H.264 arrival: NOT TESTED.

Status: NOT DONE / pending Windows + real iPhone validation.
