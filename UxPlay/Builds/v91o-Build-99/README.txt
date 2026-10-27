UxPlay Quality Launcher Full - v91o Build 99
Build 98 libusb0 filter-helper C# local-scope compile fix

Baseline: exact released Build 98 ZIP UxPlay_V91O_Build_98_Filter_Helper_Compile_Fix.zip
Baseline SHA-256: dc732584b11c054ac3f688ca84f12a6bea9dbed0dd0c81df88c82c741d21bfa3
Baseline ZIP integrity: PASS

Real Build 98 Windows build evidence: usb_direct_backend.exe and usb_mi01_activation_helper_build98.exe built successfully, but usb_libusb0_filter_helper_build98.exe failed C# compilation with CS0136 at source lines 1038 and 1053. The generic install/remove locals backupPath and verifyReadable conflicted with same-named locals inside earlier child scopes.

Build 99 targeted change:
- backupPath -> operationBackupPath in the ordinary install/remove path.
- verifyReadable -> finalVerifyReadable in the ordinary final libusb0 verification path.
- All references updated consistently.
- Required Build 99 release/runtime identity updates.

Guarded exact-selected-iPhone AppleLowerFilter test behavior is otherwise unchanged from Build 98/97. Build 95 fail-fast behavior, persistent USB renderer, and Build 80 known-good Wi-Fi behavior remain preserved. No Apple software uninstall, global Apple filter removal, AppleKmdfFilter removal, libusb0 removal, Zadig, or security-product disabling.

Validation:
Static/source audit: 235/235 PASS.
ZIP integrity: PASS.
Windows C# compile: NOT TESTED in Linux environment.
Real guarded AppleLowerFilter detach/restart/restore: NOT TESTED.
Real PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
Status: NOT DONE / pending Windows build + real iPhone validation.
