# DisneyNOW Fire TV Hybrid TV Shell

Unofficial personal-use Fire TV compatibility project for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, Disney credentials, provider tokens, DRM keys, or DRM-bypass logic. It preserves Disney's normal authentication/entitlement path and only attempts native playback when legitimate media/DRM request information has been observed from the authenticated session.

## Current build

- Version: **0.1**
- Build: **9**
- Android versionCode: **9**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **NOT DONE - COMPATIBILITY TEST** until Build 9 is physically verified on the user's Fire TV Stick.
- Permanent signer certificate SHA-256: `2f4b3c694fc2865668d604fe5542f6cb183f1a1487908e873c98fca34c0fd838`

Downloader/raw APK:
`https://raw.githubusercontent.com/Fireworkstars46/App-Builds/main/DisneyNOWFireTV/Releases/v0.1-Build9-Compatibility-Test/DisneyNOW-Fire-TV-v0.1-Build9-Permanent-Signed.apk`

Install Build 9 directly over the prior permanent-signed build. Do not uninstall first if existing cookies/settings/login state should be preserved.

## Current architecture

Build 8 changed the app from a cursor-first WebView experiment toward a hybrid TV shell after real Fire TV testing showed persistent lag, playback errors, and incomplete CSS-only page zoom. The default is low-overhead Native TV Navigation, with Cursor Navigation and Legacy JS Focus Navigation retained as compatibility modes. Performance Mode is available, Page Zoom supports the established custom 0-500 range using WebView-level scaling, and Silk remains available as a playback fallback.

Build 8 also added an experimental AndroidX Media3 1.8.1 HLS/DASH player path. It may use legitimate media-manifest and probable DRM-license request information observed from the authenticated DisneyNOW session. It does not extract DRM keys, bypass DRM, fabricate entitlement/license responses, or copy Disney proprietary player/authentication code.

## Build 9 Debug Mode

Build 9 adds optional privacy-safe diagnostics while preserving the Build 8 architecture. Debug Mode defaults **OFF** so normal use does not incur its extra instrumentation work.

When enabled, Debug Mode can collect bounded app-owned diagnostic information useful for the Fire TV lag/playback problem, including:

- page/load timing;
- WebView/main-frame error counts;
- Media3 player errors/state;
- media-manifest and probable DRM candidate counts;
- D-pad dispatch timing samples/average/maximum;
- active navigation mode, Performance Mode, Page Zoom, and fullscreen state;
- Java heap usage;
- current main-frame host only, not the full URL.

The app menu includes **Debug Snapshot**, **Export Debug Report**, and **Reset Debug Counters**. Export Debug Report writes the snapshot plus up to the last 200 privacy-safe app log lines to the app-owned debug folder.

The debug report is intentionally designed not to export passwords, cookies, Authorization headers, provider tokens, full protected media/license URLs, query strings, device serials, or typed text. WebView remote debugging remains disabled.

## Fire TV controls

- D-pad: native TV/WebView focus by default; compatibility cursor mode remains selectable.
- Center/Select: activate the currently focused control or compatibility cursor target.
- Back: web back; exits fullscreen/native player first when applicable.
- Menu (three-lines button): opens app controls/settings/debug tools.

## Verification and release status

Build 9 source is reconstructed from the permanent historical chain and SHA-256-verified Build 9 patch inputs. CI passed static/release audit **179 PASS / 0 FAIL**, Java/Android compilation, unit tests, lint (**0 errors / 13 warnings**), package/version checks, and permanent signer checks. The signed APK uses the established long-lived signing identity and passed APK v2/v3 verification.

Physical Fire TV behavior remains environment-dependent and is not claimed by CI. Required real-device checks include responsiveness/lag, provider login, whole-page zoom appearance, Disney playback error behavior, Media3/Widevine behavior when applicable, Debug Mode usefulness/export, and Silk fallback.
