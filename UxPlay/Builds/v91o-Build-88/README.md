# UxPlay Quality Launcher Full — v91o Build 88

Corrective target: make Direct USB Test a one-button workflow for the current failure where Auto reports `FILTER_NOT_INSTALLED_ON_SELECTED_PARENT` and falls back before the previously proven exact-parent libusb0 path can run.

Build 88 automatically probes the exact selected iPhone parent, installs/repairs the existing scoped libusb0 UpperFilter only when the safe precheck permits it, requests an exact-device Windows PnP restart, waits for the reference transport to become ready, then continues the live mirror test. No separate Install / Probe / QuickTime Test clicks are required. Windows UAC approval may still appear when elevation is required; UAC is not bypassed.

Preserved: Build 87 re-enumeration + endpoint-halt-clear behavior, Build 86 prompt responsiveness fix, Build 84 queued-handshake changes, persistent black USB renderer, and Build 80 known-good Wi-Fi behavior.

Static audit: 144/144 PASS. ZIP integrity: PASS.

Windows compile / installer build / elevated helper / automatic PnP restart / real iPhone QuickTime transition / H.264 remain NOT TESTED. Status: NOT DONE / pending Windows + real iPhone validation.
