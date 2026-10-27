UxPlay Quality Launcher Full - v91o Build 91
Windows libusb0 endpoint-toggle preservation correction

Build 90 real runtime evidence reached exact QuickTime config 5, repaired libusb0 configuration 0, claimed interface 2, received the iPhone's canonical 16-byte PING, and wrote the canonical 16-byte PING reply, but CWPA never followed.

Build 91 preserves the Build 90 Windows libusb0 claim-first/configuration-0-repair and synchronous large-read path while removing the unconditional startup CLEAR_FEATURE(ENDPOINT_HALT) requests on the libusb0 QuickTime IN/OUT endpoints. The current Windows libusb0 reference starts bulk I/O without that startup mutation. Read-only post-PING endpoint GET_STATUS diagnostics remain.

Preserved: one-click Direct USB Test, automatic exact-iPhone prerequisite repair, Build 86 prompt fix, persistent black Direct USB renderer/settings, Build 80 known-good Wi-Fi behavior, stable AppId {F07F126D-812E-48F9-A296-46D459067E7C}, per-user identity, security products/firewall enabled.

Static audit: 162/162 PASS.
ZIP integrity: PASS.
Windows C# compile: NOT TESTED in Linux environment.
Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.
Status: NOT DONE / PENDING runtime validation.
