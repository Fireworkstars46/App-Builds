UxPlay Quality Launcher Full - v91o Build 94
Hybrid libusb0 Activation-Only -> UsbDk Streaming

WHY THIS BUILD EXISTS
Build 93 read-only diagnostics confirmed the selected iPhone parent is using:
- Windows usbccgp composite parent
- libusb0 UpperFilter
- AppleLowerFilter lower filter
- Apple USB driver 552.0.0.0
- Apple kernel-filter services present

Build 93 still reached QuickTime config 5, received canonical PING and sent the canonical PING reply, but CWPA never arrived.

Build 94 does NOT remove, replace, rebind, disable or uninstall Apple drivers or filters.
Instead, Auto mode uses a hybrid transport only when BOTH are true:
1. the exact selected iPhone passes the verified libusb0 readiness probe with READY_WITH_APPLE_KERNEL_FILTER_CAUTION; and
2. UsbDk is already installed.

HYBRID FLOW
1. Exact-parent libusb0 activate-only helper sends the existing scoped QuickTime 0x40/0x52 activation request.
2. The helper owns the invalidated legacy handle only through activation and exits.
3. UsbDk/libusb1 then opens the freshly exposed QuickTime configuration and owns live bulk IN/OUT for PING/CWPA/CVRP/FEED/H.264.
4. The normal backend cleanup/restore path runs when capture ends.

This avoids carrying live QuickTime bulk traffic through the caution-stack libusb0 path while preserving the proven exact-parent activation path.

ONE-BUTTON BEHAVIOR
Direct USB Test remains the only project button needed for the automatic test path.
No new project-owned OK/Yes/No/Keep-Waiting prompt is added.
Windows UAC and iOS-owned Trust/Allow/passcode prompts, when genuinely required by the OS/device, cannot be bypassed.

PRESERVED
- Build 92/93 exact-parent activation helper behavior
- Build 90 synchronous Windows-style reader for explicit libusb0 reference mode
- Build 91 no unconditional startup halt-clear for libusb0
- Build 86 instant prompt dismissal implementation (prompt remains skipped by Direct USB Test)
- Persistent black Direct USB renderer and USB renderer settings
- Frozen Build 80 Wi-Fi behavior and title-bar pin behavior
- Stable AppId/update identity
- No Bitdefender/Defender/SmartScreen weakening

SAFETY
- Build 94 does not mutate the Apple parent driver binding.
- Build 94 does not remove AppleLowerFilter or AppleKmdfFilter.
- Build 94 does not remove libusb0 from the selected phone.
- Build 94 does not install UsbDk automatically from the live capture path; hybrid is selected only when UsbDk is already present.
- Exact selected-device checks remain required for the libusb0 activation helper.

TEST STATUS
Static/source audit: see STATIC_AUDIT_V91O_BUILD_94_RESULTS.txt
Python backend syntax: tested in build environment.
Windows C# compile: NOT TESTED in this Linux environment.
Real Windows hybrid handoff: NOT TESTED.
Real iPhone PING -> CWPA -> CVRP -> FEED -> H.264: NOT TESTED.

Status: NOT DONE / pending Windows + real iPhone validation.

PROTOCOL PRESERVATION
The canonical PING bytes and Valeria protocol framing are unchanged in Build 94. This build changes transport ownership only; it does not change PING/CWPA/CVRP/FEED packet framing.
The upstream GPL reference source is not bundled or copied into the active project source; it is used only as an external behavioral reference.
