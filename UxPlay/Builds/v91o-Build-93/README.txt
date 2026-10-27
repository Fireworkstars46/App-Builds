UxPlay Quality Launcher Full - v91o Build 93
Read-only Windows Apple/libusb0 driver-stack diagnostic

Build 92 real runtime evidence confirmed the short-lived activation-helper handoff worked, but the iPhone still reached QuickTime config 5, sent the canonical 16-byte PING, accepted the 16-byte reply, and then never sent CWPA.

The selected iPhone repeatedly reports READY_WITH_APPLE_KERNEL_FILTER_CAUTION. A closely matching upstream Windows/libusb0 report documents Handshaking/no-video failures when libusb0 is stacked with AppleLowerFilter/AppleKmdfFilter. Build 93 therefore does not make another protocol guess and does not mutate the Apple driver stack.

Targeted Build 93 change:
- Direct USB Test remains one-button.
- Before the unchanged Build 92 capture path starts, collect a privacy-safe read-only inventory for the exact selected iPhone parent.
- Log parent service/class, UpperFilters/LowerFilters names, parent driver INF/provider/version/description/matching ID, AppleLowerFilter/AppleKmdfFilter service registration, and Apple Mobile Device Service running state.
- Do not log the selected phone serial or PnP instance ID in these diagnostic lines.
- If the Apple-kernel-filter caution exists, log it and continue capture unchanged.
- Do not remove Apple filters, rebind the parent driver, uninstall Apple support, or disable Windows/AV security.

Preserved: Build 92 activation-helper handoff, Build 91 no-startup-halt-clear behavior, Build 90 claim-first/configuration-0 repair and synchronous reader, canonical PING/CWPA/CVRP/FEED protocol framing, one-button Direct USB Test, Build 86 prompt fixes, persistent USB renderer/settings, Build 80 known-good Wi-Fi behavior, stable AppId {F07F126D-812E-48F9-A296-46D459067E7C}, and per-user identity.

Static audit: 189/189 PASS.
ZIP integrity: PASS.
Windows C# compile: NOT TESTED in this Linux environment.
Real Windows driver-stack inventory: NOT TESTED.
Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
Status: NOT DONE / PENDING runtime validation.
