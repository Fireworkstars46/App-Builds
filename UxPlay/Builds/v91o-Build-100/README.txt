UxPlay Quality Launcher Full - v91o Build 100
Stable QuickTime activation handoff + PING->CWPA diagnostics

Baseline: exact released Build 99 ZIP SHA-256 a591719fe2403cb02be32357c2e5d7914a79334a4f7f688f533e4c08ed3a208d.

Real Build 99 validation disproved the guarded AppleLowerFilter-detach hypothesis on this iPhone: the exact-parent guard reached READY, but QuickTime configuration 5 / subclass 0x2A no longer appeared after activation; restoration was VERIFIED.

Build 100 disables AppleLowerFilter mutation in the one-button path and keeps the normal Apple/libusb0 stack intact. The activate-only libusb0 helper now requires the exact selected parent's QuickTime descriptor to remain continuously visible for at least 750 ms before helper exit. The observation is bounded to 5 seconds and does not mutate filters, configuration, alternate settings, endpoint halt state, or protocol packets.

The backend also logs the exact first bulk-OUT payload and PING dispatch completion timing. PING/CWPA/CVRP/FEED framing is unchanged.

Preserved: Build 95 fail-fast behavior, Build 92 helper isolation, Build 91 no-startup-halt-clear, Build 90 claim-first/config-0 repair, one-click Direct USB Test, persistent USB renderer, Build 80 known-good Wi-Fi behavior, stable AppId {F07F126D-812E-48F9-A296-46D459067E7C}, per-user install identity, and security protections.

Driver safety: Build 100 does NOT detach AppleLowerFilter, remove AppleKmdfFilter, uninstall/rebind Apple software, replace usbccgp, or disable Defender/Bitdefender/SmartScreen/Firewall.

Validation: static/source audit 233/233 PASS; Python backend syntax PASS; ZIP integrity PASS. Windows C# compile, real Windows stable handoff, and real iPhone PING->CWPA->CVRP->FEED->H.264 are NOT TESTED.

Status: NOT DONE / pending Windows build + real iPhone validation.
