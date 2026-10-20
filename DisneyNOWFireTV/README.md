# DisneyNOW Fire TV Web Wrapper

Unofficial personal-use Fire TV compatibility wrapper for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, credentials, provider tokens, DRM keys, or any DRM-bypass logic. It loads DisneyNOW's own website in the device WebView and relies on Disney's normal authentication, playback, and DRM paths.

## Current build

- Version: **0.1**
- Build: **1**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **Compatibility test / NOT DONE** until runtime testing is completed on the user's Fire TV Stick.

Build 1 exists to answer one question first: can DisneyNOW web playback work through the Fire TV's Android WebView/DRM stack when iOS WebKit playback does not?

## Fire TV controls

- D-pad: TV-friendly focus navigation when enabled.
- Center/Select: activate the focused web control.
- Back: web back; exits fullscreen video first when applicable.
- Menu (three-lines button): opens the app menu.

The app menu provides Home, Reload, user-agent profiles, TV Focus Navigation, clear app web data, diagnostics, diagnostic export, Safe Self-Test, About, and Exit.

## Signing warning for Build 1

Build 1 is an **experimental CI debug-signed APK**. The CI debug signing key is intentionally not archived in this public repository. A later stable release signed with a preserved private release key may therefore require uninstalling this compatibility-test APK first. This is intentional for the test build and is one reason Build 1 remains NOT DONE.

## Source seed

The repository stores the exact Build 1 source as a SHA-256-verified split seed under `SourceSeed/` so it can be reconstructed deterministically by the build workflow. The permanent Build 1 archive contains a normal human-readable source ZIP after a successful compile.
