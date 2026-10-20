# DisneyNOW Fire TV Web Wrapper

Unofficial personal-use Fire TV compatibility wrapper for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, credentials, provider tokens, DRM keys, or any DRM-bypass logic. It loads DisneyNOW's own website in the device WebView and relies on Disney's normal authentication, playback, and DRM paths.

## Current build

- Version: **0.1**
- Build: **2**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **Corrective compatibility test / NOT DONE** until Build 2 is physically verified on the user's Fire TV Stick.

Build 1 established that the DisneyNOW site could load on the user's Fire TV Stick, but real hardware testing found three defects: D-pad navigation was very laggy, there was no visible cursor, and the page was too zoomed in. Build 2 corrects those issues while preserving the same package ID and Disney authentication/DRM path.

## Fire TV controls

- D-pad: move the visible native cursor by default.
- Center/Select: click the web control under the cursor.
- Moving beyond the top/bottom edge: scroll the page.
- Back: web back; exits fullscreen video first when applicable.
- Menu (three-lines button): opens app controls.

The app menu provides Home, Reload, Page Zoom, Cursor Navigation, optional Legacy Focus Navigation, user-agent profiles, clear app web data, diagnostics, diagnostic export, Safe Self-Test, About, and Exit.

Page Zoom defaults to **75%** and can be changed from 50% through 100% presets.

## Build 2 performance/navigation change

The old DOM focus-scanning navigation remains only as an optional fallback. The default D-pad path now moves a native overlay cursor and injects only the click event into the WebView, avoiding a full `querySelectorAll`/focus scan on every directional button press. Hardware acceleration remains enabled for the application and is explicitly requested on the WebView.

## Signing warning

Builds 1 and 2 are **experimental CI debug-signed APKs**. The CI debug signing key is intentionally not archived in this public repository. Because hosted runners can use different debug keys, Android may require Build 1 to be uninstalled before Build 2 can be installed. A final update-compatible release requires a preserved private signing key.

## Source seed

Build 2 preserves the original Build 1 `SourceSeed/` unchanged. The workflow deterministically reconstructs that known Build 1 source and then applies the SHA-256-verified `Build2/apply.py` corrective replacement set. The permanent Build 1 source/binaries remain preserved under its historical release archive, and the Build 2 release archive contains the fully patched human-readable source plus the reconstruction/patch inputs.
