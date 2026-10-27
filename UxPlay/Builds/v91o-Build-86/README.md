# UxPlay Quality Launcher Full — v91o Build 86

Corrective USB prompt-latency build.

## Confirmed Build 85 state
- The previous stuck/glitching Direct USB OK box is fixed.
- User reported a remaining brief (~1 second) visible lag on OK dismissal.
- Build 85 log showed the dedicated STA prompt thread started at 05:33:37.589 and OK was accepted at 05:33:38.944.

## Build 86 targeted change
- Preserve Build 85's dedicated STA prompt UI thread.
- OK/Cancel now disable controls and `Hide()` the prompt before any project logging or cleanup.
- `Close()` is requested immediately after `Hide()`.
- Removed the launcher-side `promptThread.Join(1200)` wait entirely.
- The USB test path returns the winning outcome immediately instead of appearing frozen while the prompt thread winds down.

## Preserved
- Build 84 USB transport / queued-handshake work.
- Persistent black Direct USB renderer and USB settings persistence.
- Once-per-Build phone-confirmation acknowledgement semantics.
- Build 80 known-good Wi-Fi renderer/title-bar pin/FPS behavior.
- Stable AppId and per-user install identity.

## Validation
- Static/source audit: 108/108 PASS.
- ZIP integrity: PASS.
- Windows compile: NOT TESTED.
- Installer build: NOT TESTED.
- Live Direct USB/iPhone test: NOT TESTED.
- Actual OK/Cancel visual latency on Windows: NOT TESTED.

Status: **NOT DONE / PENDING Windows validation**.
