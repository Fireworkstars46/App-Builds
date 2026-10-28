# DisneyNOW Fire TV Hybrid TV Shell

Unofficial personal-use Fire TV compatibility project for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, Disney credentials, provider tokens, DRM keys, or DRM-bypass logic. It preserves Disney's normal authentication/entitlement path and only uses legitimate media/session information observed from the authenticated DisneyNOW session.

## Current build

- Version: **0.1**
- Build: **14**
- Android versionCode: **14**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **NOT DONE - COMPATIBILITY TEST** until Build 14 is physically verified on the user's Fire TV Stick.
- Permanent signer certificate SHA-256: `2f4b3c694fc2865668d604fe5542f6cb183f1a1487908e873c98fca34c0fd838`

Downloader/raw APK:
`https://raw.githubusercontent.com/Fireworkstars46/App-Builds/main/DisneyNOWFireTV/Releases/v0.1-Build14-Compatibility-Test/DisneyNOW-Fire-TV-v0.1-Build14-Permanent-Signed.apk`

Install Build 14 directly over the currently installed build. **Do not uninstall first** if existing cookies/settings/login state should be preserved.

## Current architecture

Build 8 changed the app from a cursor-first WebView experiment toward a hybrid TV shell after real Fire TV testing showed persistent lag, playback errors, and incomplete CSS-only page zoom. Native TV Navigation, Cursor Navigation, and Legacy JS Focus Navigation remain available; Performance Mode, the established 0-500 Page Zoom range, and Silk fallback are preserved.

Build 8 also introduced an experimental AndroidX Media3 1.8.1 HLS/DASH player path using only legitimate media/session information observed from the authenticated DisneyNOW WebView session. It does not extract DRM keys, bypass DRM, fabricate entitlement/license responses, or copy proprietary Disney player/authentication code.

## Playback/debug history

Build 9 added optional privacy-safe diagnostics. Build 10 added detailed HLS/DASH -> native-player handoff diagnostics after physical testing showed DisneyNOW HLS manifests even when WebView playback failed.

Physical Build 10 testing showed the app could observe the DisneyNOW HLS stream but the manual **Try Native Player** workflow was confusing and still required user intervention.

Build 11 tried automatic native Media3 handoff/fallback. Physical testing proved Media3 could reach `READY` and `isPlaying=true`, but the user also observed glitchy/finicky behavior followed by an app/process restart. The automatic native path is therefore treated as a regression.

Build 12 returned to the safer behavior: automatic native Media3 launch is disabled, the manual **Try Native Player** menu action is omitted, and persistent privacy-safe crash/restart breadcrumbs were added. Physical Build 12 testing was substantially more stable, but its debug report recorded a rare D-pad dispatch maximum of about 2.5 seconds.

## Build 14 lag/stability correction

Build 14 preserves Build 12's safer no-auto-native playback behavior and targets the remote/input backlog seen in the Build 12 physical report.

- In **Native TV Navigation** mode only, rapid repeated directional `ACTION_DOWN` events inside an **85 ms** guard window are suppressed.
- The first directional press and `ACTION_UP` are still forwarded normally.
- Select, Menu, Back, Cursor Navigation, Legacy Focus Navigation, Performance Mode, zoom, Silk fallback, and crash/restart breadcrumbs remain preserved.
- Debug Mode now reports how many directional repeats were suppressed.
- Debug Mode also counts D-pad dispatches taking **100 ms or longer**, while retaining average/max timing.
- Automatic native Media3 launch remains disabled.
- The normal menu still does not expose **Try Native Player**.

These input changes are intended to reduce key-repeat queue buildup without changing normal single-tap navigation. CI does **not** claim the physical lag is fixed; Build 14 requires real Fire TV comparison.

## Crash/restart diagnostics

The persistent privacy-safe crash/restart system from Build 12 remains enabled:

- a project-owned session-active marker can survive process death/restart;
- the next launch can report whether the previous session ended without a clean `onDestroy`;
- a bounded privacy-safe stage/breadcrumb can show what app/player stage was last active;
- a privacy-safe uncaught-exception handler records exception class/cause-chain information only and forwards to Android's prior/default handler;
- no exception message, cookie, Authorization header, provider token, full protected media/license URL, request body, typed text, or DRM key is intentionally stored.

The unclean-session marker is diagnostic evidence, **not proof of a Java crash**, because Android/Fire OS can terminate a process without delivering a Java exception or `onDestroy` callback.

## Fire TV controls

- D-pad: native TV/WebView focus or compatibility cursor mode according to the saved navigation setting.
- Center/Select: activate the focused control or compatibility cursor target.
- Back: web back; exits fullscreen/native player first when applicable.
- Menu (three-lines button): opens app controls/settings/debug tools.

## Verification and release status

Build 14 source is reconstructed from the permanent historical chain and hash-verified patch inputs. Public and private CI independently reconstructed the exact source. Verification passed:

- static/release audit: **227 PASS / 0 FAIL**;
- Android compile + unit tests: **PASS**;
- lint: **0 errors / 14 warnings**;
- package/version identity: `com.fireworkstars46.disneynowfiretv`, versionCode **14**, versionName **0.1**;
- permanent signer fingerprint: exact established identity;
- APK signing verification: **v1/v2/v3 PASS**;
- public permanent release archive: verified and published.

Signed APK SHA-256:
`7c85da481cf2db1c0f375bfa79ba3e505b4247bc59d5444666f2b1c627382e00`

Physical Fire TV behavior remains environment-dependent and is not claimed by CI. Required Build 14 real-device checks are D-pad responsiveness (single taps and held/repeated directions), the new suppressed-repeat and >=100 ms timing counters, provider/login state preservation, normal DisneyNOW playback behavior without automatic Media3 takeover, crash/restart breadcrumb behavior if another restart occurs, zoom, and Silk fallback.
