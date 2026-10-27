# UxPlay Quality Launcher Full — v91o Build 84

USB queued-handshake corrective source package.

## Status

- **NOT DONE / PENDING** real Windows + iPhone validation.
- Build 80 Wi-Fi renderer/pin behavior is intentionally preserved.
- Build 83 phone-confirmation single-outcome fix is preserved.

## Why Build 84 exists

The latest supplied Direct USB evidence showed the UsbDk fallback remaining on the normal four-configuration profile and failing before QuickTime configuration 5. Historical evidence from this same PC showed the exact-parent libusb0 reference path reaching configuration 5, claiming the QuickTime interface, receiving the canonical Valeria PING, and replying to it, but then stalling before CWPA/H.264.

## Targeted changes

1. Auto still prefers the exact selected-iPhone libusb0 reference transport when its existing filter/interface is verified ready.
2. Auto now gives transient libusb0 PnP/interface registration up to about 3 seconds of read-only settle/re-probe time before falling back.
3. The chosen Auto transport and fallback reason are mirrored to UxPlay.log.
4. The live libusb0 capture path no longer blocks for the old 90-second USBMux/Lockdown preflight before servicing QuickTime bulk traffic.
5. The Windows-reference five-request bulk-IN reader (5 × 4096 bytes) is armed before the first Valeria PING. Builds 62–83 deferred this until CWPA; the observed failure was PING → reply → no CWPA.
6. Canonical PING-only handshake ordering remains unchanged. HPD1 remains in the bundled Valeria CWPA handler; no blind early HPD1 retry was added.
7. Existing bounded Windows timeout recovery remains.

## Preserved

- Persistent black Direct USB renderer and saved placement.
- Once-per-build launcher reminder semantics.
- iOS-owned Trust/Allow/passcode prompts remain controlled by iOS; this app only controls its own reminder.
- Build 83 non-modal single-outcome OK/Cancel/backend-exit prompt path.
- Explicit UsbDk and Normal libusb advanced selections.
- Exact-parent identity checks and guarded libusb0 restore.
- Build 80 Wi-Fi native title bar, MirrorTo-style pin, FPS controls, anti-flash path, firewall repair, and runtime self-repair.
- Stable installer AppId and per-user install identity.

## Testing status

- Static/source audit: **98/98 PASS**.
- ZIP integrity: PASS.
- Python syntax: PASS.
- Windows C# compile: NOT TESTED in the Linux build environment.
- Inno Setup installer build: NOT TESTED here.
- Real iPhone config-5/CWPA/H.264: NOT TESTED here.

Do not call Build 84 DONE until the Windows build and real Direct USB test pass.
