UxPlay Quality Launcher Full - v91o Build 96
Temporary AppleLowerFilter exact-device capture test

Reason:
Build 95 is responsive and reaches QuickTime config 5, receives the canonical 16-byte PING, and sends the canonical PING reply, but CWPA never arrives. Runtime driver inventory showed usbccgp + libusb0 UpperFilter + AppleLowerFilter on the selected iPhone parent (Apple driver 552.0.0.0).

Targeted Build 96 change:
- Auto/Direct USB Test only, when READY_WITH_APPLE_KERNEL_FILTER_CAUTION is detected.
- Back up the exact selected parent's original LowerFilters before mutation.
- Temporarily remove only AppleLowerFilter from that exact parent.
- Preserve usbccgp parent service and libusb0 UpperFilter.
- Restart only the exact selected Apple parent.
- Re-probe for a clean exact-parent libusb0 path.
- Run the Build 95 QuickTime/Valeria protocol path unchanged.
- Restore the exact original LowerFilters automatically when USB stops or launcher exits.
- Elevated helper monitors launcher PID and stop signal.
- A ProgramData pending backup plus user marker supports stale-session recovery on the next one-button test if restore cannot be confirmed.

Not changed:
- No parent driver rebind/replacement.
- No Apple Devices/iTunes/Apple Mobile Device Support package uninstall.
- No AppleKmdfFilter service removal.
- No libusb0 removal.
- No Zadig.
- No unrelated USB-device changes.
- No Bitdefender/Defender/SmartScreen/Firewall disabling.
- Build 95 fail-fast/no-five-minute-freeze behavior preserved.
- Build 80 known-good Wi-Fi behavior preserved.

Validation:
Static audit: 223/223 PASS.
ZIP integrity: PASS.
Windows C# compile: NOT TESTED in Linux environment.
Real temporary AppleLowerFilter detach/restart/restore: NOT TESTED.
Real PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
Status: NOT DONE / pending Windows + real iPhone validation.
