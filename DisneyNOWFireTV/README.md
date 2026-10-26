# DisneyNOW Fire TV Hybrid TV Shell

Unofficial personal-use Fire TV compatibility project for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, Disney credentials, provider tokens, DRM keys, or DRM-bypass logic. It preserves Disney's normal authentication/entitlement path and only attempts native playback when legitimate media/DRM request information has been observed from the authenticated session.

## Current build

- Version: **0.1**
- Build: **11**
- Android versionCode: **11**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **NOT DONE - COMPATIBILITY TEST** until Build 11 is physically verified on the user's Fire TV Stick.
- Permanent signer certificate SHA-256: `2f4b3c694fc2865668d604fe5542f6cb183f1a1487908e873c98fca34c0fd838`

Downloader/raw APK:
`https://raw.githubusercontent.com/Fireworkstars46/App-Builds/main/DisneyNOWFireTV/Releases/v0.1-Build11-Compatibility-Test/DisneyNOW-Fire-TV-v0.1-Build11-Permanent-Signed.apk`

Install Build 11 directly over Build 10. **Do not uninstall first** if existing cookies/settings/login state should be preserved.

## Current architecture

Build 8 changed the app from a cursor-first WebView experiment toward a hybrid TV shell after real Fire TV testing showed persistent lag, playback errors, and incomplete CSS-only page zoom. Native TV Navigation, Cursor Navigation, and Legacy JS Focus Navigation remain available; Performance Mode, the established 0-500 Page Zoom range, and Silk fallback are preserved.

Build 8 also introduced an experimental AndroidX Media3 1.8.1 HLS/DASH player path using only legitimate media/session information observed from the authenticated DisneyNOW WebView session. It does not extract DRM keys, bypass DRM, fabricate entitlement/license responses, or copy proprietary Disney player/authentication code.

## Build 9 Debug Mode

Build 9 added optional privacy-safe diagnostics. Debug Mode defaults **OFF** and production behavior is designed to work without it.

When enabled, Debug Mode records bounded app-owned diagnostics for page/load timing, WebView/main-frame errors, Media3 state/errors, media/DRM candidate counts, D-pad dispatch timing, navigation/performance/zoom/fullscreen state, Java heap use, and safe host/type/state information. The menu provides **Debug Snapshot**, **Export Debug Report**, and **Reset Debug Counters**.

The diagnostic path is intentionally designed not to export passwords, cookies, Authorization headers, provider tokens, full protected media/license URLs, query strings, device serials, request bodies, or typed text. WebView remote debugging remains disabled.

## Build 10 handoff findings

Build 10 added targeted handoff diagnostics after the first physical Build 9 report showed DisneyNOW HLS manifests during the failed WebView playback attempt. Physical Build 10 testing confirmed repeated HLS-ready events but showed **0 native-player attempts**, because the native player still depended on a manual **Try Native Player** menu step. The user reported that this was not better and made the app more confusing.

## Build 11 automatic native handoff/fallback

Build 11 removes that normal-use manual handoff step.

- When a legitimate HLS media manifest is observed, the app automatically schedules one native Media3 attempt for that page after the manifest burst settles.
- Repeated manifest observations are debounced so the attempt waits briefly for the stream candidate to stabilize instead of firing for every request.
- The normal app menu no longer contains the Build 10 **Try Native Player** control.
- If Media3 reports a setup/player error, the app automatically stops the native attempt and restores the WebView path.
- If native playback does not begin within the bounded startup watchdog, the app automatically falls back to the WebView path.
- The automatic production behavior does not depend on Debug Mode; Debug Mode only adds safe scheduling/attempt/start/fallback evidence.
- Existing settings, cookies/login state, package identity, navigation modes, Performance Mode, zoom behavior, diagnostics, and Silk fallback are preserved.

No DRM keys, DRM bypass, fabricated entitlement/license/token responses, or proprietary Disney code are used.

## Fire TV controls

- D-pad: native TV/WebView focus or compatibility cursor mode according to the saved navigation setting.
- Center/Select: activate the focused control or compatibility cursor target.
- Back: web back; exits fullscreen/native player first when applicable.
- Menu (three-lines button): opens app controls/settings/debug tools.

## Verification and release status

Build 11 source is reconstructed from the permanent historical chain and hash-verified Build 11 patch inputs. Public and private CI independently reconstructed the exact source. Verification passed:

- static/release audit: **207 PASS / 0 FAIL**;
- Android compile + unit tests: **PASS**;
- lint: **0 errors / 13 warnings**;
- package/version identity: `com.fireworkstars46.disneynowfiretv`, versionCode **11**, versionName **0.1**;
- permanent signer fingerprint: exact established identity;
- APK signing verification: **v1/v2/v3 PASS**;
- public permanent release archive: verified present.

Signed APK SHA-256:
`279a6d1d4a2aaab3c7fbf32cfa44c8f384c82524d93669064768d6f7a8f2c29f`

Physical Fire TV behavior remains environment-dependent and is not claimed by CI. Required real-device checks include installing Build 11 over Build 10, starting a DisneyNOW video normally, observing whether automatic native playback succeeds or automatically falls back, exporting a Build 11 debug report, and checking provider login, responsiveness, zoom, and Silk fallback behavior.
