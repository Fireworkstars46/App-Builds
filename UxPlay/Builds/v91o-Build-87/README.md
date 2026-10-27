# UxPlay Quality Launcher Full — v91o Build 87

Corrective Direct USB build based on the user's Build 86 runtime evidence plus behavior independently reimplemented after reviewing the user-provided open-source airplaya USB reference.

## Targeted Direct USB changes

- Release the pre-transition USB handle immediately after the `0x40/0x52`, `wIndex=2` QuickTime activation request.
- Treat the activation request's I/O error as compatible with the expected device disconnect/re-enumeration.
- Fresh-enumerate/inspect/dispose USB handles every 500 ms while waiting for vendor subclass `0x2A` instead of holding a persistent stale/fresh handle.
- No automatic second activation request while waiting for the AV personality.
- Discover the QuickTime configuration dynamically from the subclass `0x2A` descriptor in the active activation path.
- Send `CLEAR_FEATURE(ENDPOINT_HALT)` to both QuickTime bulk endpoints before the first live read on the exact-parent libusb0 path.

## Preserved

- Build 86 dedicated-STA instant-dismiss confirmation prompt.
- Build 84 queued 5×4096 bulk-IN reader and PING-only handshake ordering.
- Persistent black Direct USB renderer/settings persistence.
- Build 80 known-good Wi-Fi renderer/title-bar pin/FPS behavior.
- Stable AppId and per-user install identity.

## Validation

- Static/source audit: 123/123 PASS.
- ZIP integrity: PASS.
- Windows compile: NOT TESTED.
- Installer build: NOT TESTED.
- Real iPhone QuickTime re-enumeration / H.264: NOT TESTED.

Status: **NOT DONE / PENDING runtime validation**.
