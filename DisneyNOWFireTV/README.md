# DisneyNOW Fire TV Hybrid TV Shell

Unofficial personal-use Fire TV compatibility project for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, Disney credentials, provider tokens, DRM keys, or DRM-bypass logic. It preserves Disney's normal authentication/entitlement path and only attempts native playback when legitimate media/DRM request information has been observed from the authenticated session.

## Current build

- Version: **0.1**
- Build: **10**
- Android versionCode: **10**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **NOT DONE - COMPATIBILITY TEST** until Build 10 is physically verified on the user's Fire TV Stick.
- Permanent signer certificate SHA-256: `2f4b3c694fc2865668d604fe5542f6cb183f1a1487908e873c98fca34c0fd838`

Downloader/raw APK:
`https://raw.githubusercontent.com/Fireworkstars46/App-Builds/main/DisneyNOWFireTV/Releases/v0.1-Build10-Compatibility-Test/DisneyNOW-Fire-TV-v0.1-Build10-Permanent-Signed.apk`

Install Build 10 directly over Build 9. **Do not uninstall first** if existing cookies/settings/login state should be preserved.

## Current architecture

Build 8 changed the app from a cursor-first WebView experiment toward a hybrid TV shell after real Fire TV testing showed persistent lag, playback errors, and incomplete CSS-only page zoom. The default is low-overhead Native TV Navigation, with Cursor Navigation and Legacy JS Focus Navigation retained as compatibility modes. Performance Mode is available, Page Zoom supports the established custom 0-500 range using WebView-level scaling, and Silk remains available as a playback fallback.

Build 8 also added an experimental AndroidX Media3 1.8.1 HLS/DASH player path. It may use legitimate media-manifest and probable DRM-license request information observed from the authenticated DisneyNOW session. It does not extract DRM keys, bypass DRM, fabricate entitlement/license responses, or copy Disney proprietary player/authentication code.

## Build 9 Debug Mode

Build 9 added optional privacy-safe diagnostics while preserving the Build 8 architecture. Debug Mode defaults **OFF** so normal use does not incur its extra instrumentation work.

When enabled, Debug Mode can collect bounded app-owned diagnostic information useful for the Fire TV lag/playback problem, including page/load timing, WebView/main-frame errors, Media3 state/errors, media/DRM candidate counts, D-pad dispatch timing, active navigation/performance/zoom/fullscreen state, Java heap use, and current main-frame host only.

The app menu includes **Debug Snapshot**, **Export Debug Report**, and **Reset Debug Counters**. Export Debug Report writes the snapshot plus up to the last 200 privacy-safe app log lines to the app-owned debug folder.

The debug report is intentionally designed not to export passwords, cookies, Authorization headers, provider tokens, full protected media/license URLs, query strings, device serials, or typed text. WebView remote debugging remains disabled.

## Build 10 native handoff diagnostics

Build 10 is a targeted response to the first real Build 9 debug report. That report confirmed that DisneyNOW HLS manifests were being observed during the failed WebView playback attempt, while no native-player attempt had yet been captured.

Build 10 preserves the user-triggered Media3 design and adds visibility into the HLS/DASH -> native-player handoff:

- the **Try Native Player** menu item reports whether it is waiting for a stream or ready with detected HLS/DASH;
- the first HLS/DASH detection per page can show a one-time hint directing the user to **Menu > Try Native Player** after the WebView playback failure;
- debug counters track handoff-ready events, native-player attempts, player creation, and prepare calls;
- a handoff-stage state tracks the path from manifest detection through player creation/configuration/prepare/play/state/error;
- safe session-context indicators record only header counts/presence and cookie availability, never values;
- post-manifest non-GET traffic is classified by safe host/method/content-type category to help identify a license/DRM handoff without recording request bodies or full protected URLs;
- Media3 failures record error codes and exception class chains only, not sensitive exception messages.

Native playback remains explicitly user-triggered; Build 10 does not automatically hijack playback. No DRM keys, DRM bypass, fabricated entitlement/license/token responses, or proprietary Disney code are used.

## Fire TV controls

- D-pad: native TV/WebView focus by default; compatibility cursor mode remains selectable.
- Center/Select: activate the currently focused control or compatibility cursor target.
- Back: web back; exits fullscreen/native player first when applicable.
- Menu (three-lines button): opens app controls/settings/debug tools.

## Verification and release status

Build 10 source is reconstructed from the permanent historical chain and hash-verified Build 10 patch inputs. Public and private CI both independently reconstructed the exact source. Verification passed:

- static/release audit: **194 PASS / 0 FAIL**;
- Android compile + unit tests: **PASS**;
- lint: **0 errors / 13 warnings**;
- package/version identity: `com.fireworkstars46.disneynowfiretv`, versionCode **10**, versionName **0.1**;
- permanent signer fingerprint: exact established identity;
- APK signing verification: **v1/v2/v3 PASS**;
- public permanent release archive: verified present.

Signed APK SHA-256:
`247b15f776104b5113aa3a26ffdcfad34f37f2d57fc3470895403d5c2c2e7d3c`

Physical Fire TV behavior remains environment-dependent and is not claimed by CI. Required real-device checks include installing over Build 9, reproducing the WebView playback failure, confirming the detected-stream hint/menu readiness, invoking **Try Native Player**, observing playback/error behavior, exporting the Build 10 debug report, and checking responsiveness/provider auth/zoom/fallback behavior.
