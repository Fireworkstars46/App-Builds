UxPlay Quality Launcher Full - v91o Build 98
Build 97 libusb0 filter-helper C# compile fix

BASELINE / SOURCE INTEGRITY
Build 98 is based on the exact released Build 97 ZIP:
UxPlay_V91O_Build_97_Guarded_AppleLowerFilter_Test.zip
SHA-256:
7fbad19ea2ebbf7845c343473324ecc6f0c35a0382af7fb1b7ccdba42cbdeb9f
The Build 97 ZIP passed ZIP integrity before modification.

WHY THIS BUILD EXISTS
A real Windows Build 97 build log showed that the Python Direct USB backend and the MI_01 activation helper built successfully, but the new exact-parent libusb0 filter helper failed C# compilation at UsbLibUsb0FilterHelper.cs lines 571-572 with CS1010 (newline in constant) and CS1012 (too many characters in character literal).

ROOT CAUSE
The Build 97 source accidentally emitted malformed Windows-backslash literals in IsSafeRestoreSignalPath().

TARGETED BUILD 98 CHANGE
Build 98 changes only the release/build identity plus those malformed C# literals. The LocalApplicationData and Temp root trimming code now uses valid escaped Windows backslashes in C# source. No guarded-driver-test behavior, capture protocol, filter semantics, restoration semantics, UI workflow, renderer behavior, Wi-Fi behavior, or installer identity is intentionally changed.

PRESERVED FROM BUILD 97
- Direct USB Test remains the only project-owned action needed.
- Exact selected Apple physical parent validation.
- usbccgp parent requirement and libusb0 UpperFilter requirement.
- Full original UpperFilters/LowerFilters backup before any mutation.
- Temporary removal of ONLY AppleLowerFilter from the exact selected parent's LowerFilters.
- SetupAPI write + read-back verification.
- Exact selected device restart only.
- Independent elevated guard process.
- Automatic original-LowerFilters restoration on normal USB stop/failure, launcher exit/crash, or guard timeout.
- Emergency exact-parent backup restore fallback.
- Build 95 fail-fast/no-five-minute-freeze behavior.
- Build 80 known-good Wi-Fi behavior.
- Stable AppId {F07F126D-812E-48F9-A296-46D459067E7C} and per-user install identity.
- No Apple software uninstall, no global Apple filter removal, no AppleKmdfFilter removal, no libusb0 removal, no Zadig, and no security-product disabling.

ADDITIONAL PRESERVATION / SAFETY GUARANTEES
- The PING bytes already match exactly; Build 98 does not change protocol framing.
- No new project-owned OK/Yes/No/Keep-Waiting prompt is added.
- Windows UAC and iOS-owned Trust/Allow/passcode prompts remain outside our app and cannot be bypassed.
- The independent guard still restores the original LowerFilters when the launcher exits/crashes or the guard safety timeout is reached.
- Build 98 does NOT remove Apple software, does NOT replace usbccgp, and does NOT disable Defender/Bitdefender/SmartScreen/Firewall.

VALIDATION STATUS
- Exact Build 97 input checksum: VERIFIED.
- Build 97 real Windows compiler error: VERIFIED from user BUILD_LOG.txt.
- Corrected helper backslash literals: SOURCE-VERIFIED.
- Static/source preservation + C# lexical audit: 230/230 PASS.
- Python backend syntax: PASS.
- ZIP integrity: PASS.
- Windows C# compile: NOT TESTED in this Linux environment.
- Real guarded AppleLowerFilter detach/restart/restore: NOT TESTED for Build 98.
- Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED for Build 98.

Status: NOT DONE / pending Windows build + real iPhone validation.
