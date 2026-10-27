UxPlay Quality Launcher Full - v91o Build 92
Windows libusb0 activation-helper handoff correction

Build 91 reached exact QuickTime config 5, repaired libusb0 configuration 0, claimed interface 2, received the iPhone's canonical 16-byte PING, and wrote the canonical 16-byte PING reply, but CWPA never followed.

Build 92 fixes one remaining lifecycle mismatch with the current Windows libusb0 reference: activation now runs through the existing exact-parent QuickTime helper in a short-lived --activate-only mode. The helper owns the invalidated activation handle through the config-5 transition, confirms the exact QuickTime node, then exits without restoring normal mode. Its process exit releases the stale activation handle before the capture backend opens a fresh QuickTime handle for claim/PING/CWPA.

Protocol framing is unchanged. The canonical PING bytes and existing CWPA/CVRP/FEED handlers are preserved. Build 91's no-startup-halt-clear behavior, Build 90's claim-first/configuration-0 repair and synchronous large reads, one-button Direct USB Test, Build 86 prompt behavior, persistent Direct USB renderer, and Build 80 Wi-Fi behavior are preserved.

Stable AppId: {F07F126D-812E-48F9-A296-46D459067E7C}
Static audit: 179/179 PASS.
ZIP integrity: PASS.
Windows C# compile: NOT TESTED in Linux environment.
Real helper activation handoff: NOT TESTED.
Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
Status: NOT DONE / PENDING runtime validation.
