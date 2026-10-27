UxPlay Quality Launcher Full - v91o Build 97
Guarded exact-iPhone AppleLowerFilter compatibility test

BASELINE / SOURCE INTEGRITY
Build 97 is based on the user-returned exact Build 95 ZIP whose SHA-256 is:
a41b1d6d2fc16efc342cbf05df08685e17d8b9ea8485ecd05054d3a30e0d9f62
The uploaded Build 95 ZIP passed ZIP integrity before modification.

WHY THIS BUILD EXISTS
Build 95 fixed the Build 94 freeze regression and is the stable baseline. Real iPhone runtime still reaches QuickTime configuration 5, claims interface 2, receives the canonical 16-byte PING and sends the canonical PING reply, but the phone never sends CWPA.

Build 93/95 read-only diagnostics identified the selected physical iPhone parent as usbccgp with libusb0 UpperFilter plus AppleLowerFilter on the lower-filter side. Current Windows iPhone-mirroring reference code classifies legacy libusb0 stacked with AppleLowerFilter/AppleKmdfFilter as an unsafe/caution stack and uses conservative lifecycle handling. That warning alone is not proof of causation, so Build 97 performs a reversible exact-device compatibility test rather than globally uninstalling or replacing Apple drivers.

TARGETED BUILD 97 CHANGE
1. Direct USB Test remains the only project-owned action needed.
2. When Auto is selected and the exact selected iPhone reports READY_WITH_APPLE_KERNEL_FILTER_CAUTION, Build 97 starts the existing elevated exact-parent filter helper in a new guarded mode.
3. The helper verifies the exact physical Apple parent, verifies its parent service remains usbccgp and verifies libusb0 is already present as the UpperFilter.
4. The helper creates a durable ProgramData backup containing the exact original UpperFilters and LowerFilters lists plus a privacy-preserving hashed filename.
5. The helper removes ONLY the AppleLowerFilter entry from that exact selected parent's LowerFilters list. Every other LowerFilters entry is preserved in original order. UpperFilters are not changed.
6. The helper applies the LowerFilters property through Windows SetupAPI, verifies the exact resulting list, and restarts ONLY the exact selected Apple parent through pnputil /restart-device.
7. The elevated helper stays alive as a guard while capture runs. It restores the exact original LowerFilters list and restarts the exact selected Apple parent when any of these happens:
   - the launcher signals normal USB stop/failure;
   - the launcher exits/crashes;
   - the guard safety timeout is reached.
8. If guard restoration is not confirmed after the helper exits, the launcher can invoke an emergency exact-parent restore from the durable backup. This second UAC path is used only as a recovery fallback.
9. The unchanged Build 95 capture path remains the normal libusb0 QuickTime capture/protocol path after the guarded detach. The PING bytes already match exactly. Build 97 does not change protocol framing and does not change PING/CWPA/CVRP/FEED framing.
10. Build 97 does NOT remove Apple software, does NOT replace usbccgp, does NOT uninstall AppleLowerFilter globally, does NOT remove AppleKmdfFilter, does NOT remove libusb0, does NOT use Zadig, and does NOT disable Defender/Bitdefender/SmartScreen/Firewall.

ONE-BUTTON / PROMPT BEHAVIOR
Direct USB Test is still the only project button required. The guarded driver test may cause one Windows UAC prompt because modifying one exact device's filter property requires elevation. No new project-owned OK/Yes/No/Keep-Waiting prompt is added. Windows UAC and iOS-owned Trust/Allow/passcode prompts remain outside our app and cannot be bypassed.

FAILURE / RESTORE BEHAVIOR
- If temporary detach cannot be written and verified, capture does not start.
- If exact-device restart after detach fails, the helper restores the original list before it exits.
- If capture fails, StopUsbMirror signals the guard to restore before normal UI cleanup finishes.
- If capture succeeds and is left running for visual verification, the guard remains active; pressing Stop/closing the USB session restores the original filter list.
- If the launcher process disappears unexpectedly, the independent elevated guard notices parent-process exit and restores automatically.
- A durable backup remains under ProgramData for recovery evidence.

PRESERVED
- Build 95 rollback/fail-fast behavior and max 60-second silent safety window.
- Build 93 privacy-safe driver-stack diagnostics.
- Build 92 activation-helper handoff.
- Build 91 no unconditional startup endpoint halt-clear behavior for libusb0.
- Build 90 claim-first/configuration-0 repair, synchronous large reads and device-originated PING ordering.
- Build 86 prompt responsiveness fix for non-test/manual paths.
- Persistent black Direct USB renderer and saved geometry.
- Build 80 known-good Wi-Fi renderer/native frame/MirrorTo-style pin behavior unchanged.
- Stable AppId {F07F126D-812E-48F9-A296-46D459067E7C} and per-user install identity.

REFERENCE / LICENSING NOTE
External open-source Windows iPhone-mirroring code was used only as behavioral reference for the caution-stack diagnosis. No external project source file is vendored or copied into the active launcher source tree. Build 97 implements its guarded exact-device test independently in this project's existing helper/launcher code.

VALIDATION STATUS
- Exact Build 95 input checksum: VERIFIED.
- Static/source preservation and guard audit: 223/223 PASS.
- Python backend syntax: PASS in build environment.
- ZIP integrity: PASS.
- Windows C# compile: NOT TESTED in this Linux environment.
- Real SetupAPI exact-parent LowerFilters mutation: NOT TESTED.
- Real guard restore on normal stop: NOT TESTED.
- Real guard restore on launcher crash: NOT TESTED.
- Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
- Real H.264 arrival: NOT TESTED.

Status: NOT DONE / pending Windows + real iPhone validation.
