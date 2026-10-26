# DisneyNOW Fire TV Hybrid TV Shell

Unofficial personal-use Fire TV compatibility project for `https://disneynow.com/`.

This project does **not** bundle Disney video, Disney artwork, Disney credentials, provider tokens, DRM keys, or DRM-bypass logic. It preserves Disney's normal authentication/entitlement path and only uses legitimate media/session information observed from the authenticated DisneyNOW session.

## Current build

- Version: **0.1**
- Build: **12**
- Android versionCode: **12**
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Status: **NOT DONE - COMPATIBILITY TEST** until Build 12 is physically verified on the user's Fire TV Stick.
- Permanent signer certificate SHA-256: `2f4b3c694fc2865668d604fe5542f6cb183f1a1487908e873c98fca34c0fd838`

Downloader/raw APK:
`https://raw.githubusercontent.com/Fireworkstars46/App-Builds/main/DisneyNOWFireTV/Releases/v0.1-Build12-Compatibility-Test/DisneyNOW-Fire-TV-v0.1-Build12-Permanent-Signed.apk`

Install Build 12 directly over Build 11. **Do not uninstall first** if existing cookies/settings/login state should be preserved.

## Current architecture

Build 8 changed the app from a cursor-first WebView experiment toward a hybrid TV shell after real Fire TV testing showed persistent lag, playback errors, and incomplete CSS-only page zoom. Native TV Navigation, Cursor Navigation, and Legacy JS Focus Navigation remain available; Performance Mode, the established 0-500 Page Zoom range, and Silk fallback are preserved.

Build 8 also introduced an experimental AndroidX Media3 1.8.1 HLS/DASH player path using only legitimate media/session information observed from the authenticated DisneyNOW WebView session. It does not extract DRM keys, bypass DRM, fabricate entitlement/license responses, or copy proprietary Disney player/authentication code.

## Debug/diagnostic history

Build 9 added optional privacy-safe diagnostics. Build 10 added detailed HLS/DASH -> native-player handoff diagnostics after physical testing showed DisneyNOW HLS manifests even when WebView playback failed.

Physical Build 10 testing showed the app could observe the DisneyNOW HLS stream but the manual **Try Native Player** workflow was confusing and still required user intervention.

Build 11 therefore tried automatic native Media3 handoff/fallback. The Build 11 physical debug report proved that Media3 could progress through player creation, HLS configuration, buffering, `READY`, and `isPlaying=true`. However, the user also observed glitchy/finicky behavior followed by an app/process restart. The report did not contain a Java/Media3 error immediately before that restart, so Build 11's automatic native path is treated as a regression and remains NOT DONE.

## Build 12 corrective stability behavior

Build 12 removes the Build 11 automatic native-player takeover from normal use.

- Automatic native Media3 launch is disabled.
- The Build 10 manual **Try Native Player** menu control remains omitted.
- DisneyNOW media-manifest observation remains available for diagnostics without automatically starting Media3.
- Existing package identity, app data, settings, cookies/login state, navigation modes, Performance Mode, zoom, diagnostics, Media3 dependency, and Silk fallback are preserved.

Build 12 also adds persistent privacy-safe crash/restart breadcrumbs:

- a project-owned session-active marker survives process death/restart;
- the next launch can report whether the previous session ended without a clean `onDestroy`;
- a bounded privacy-safe stage/breadcrumb is persisted so the next report can show what app/player stage was active before the restart;
- a privacy-safe uncaught-exception handler records exception class/cause-chain information only, then forwards to Android's prior/default handler;
- no exception message, cookie, Authorization header, provider token, full protected media/license URL, request body, typed text, or DRM key is intentionally stored.

The unclean-session marker is diagnostic evidence, **not proof of a Java crash**, because Android/Fire OS can terminate a process without delivering a Java exception or `onDestroy` callback.

## Fire TV controls

- D-pad: native TV/WebView focus or compatibility cursor mode according to the saved navigation setting.
- Center/Select: activate the focused control or compatibility cursor target.
- Back: web back; exits fullscreen/native player first when applicable.
- Menu (three-lines button): opens app controls/settings/debug tools.

## Verification and release status

Build 12 source is reconstructed from the permanent historical chain and hash-verified patch inputs. Public and private CI independently reconstructed the exact source. Verification passed:

- static/release audit: **217 PASS / 0 FAIL**;
- Android compile + unit tests: **PASS**;
- lint: **0 errors / 13 warnings**;
- package/version identity: `com.fireworkstars46.disneynowfiretv`, versionCode **12**, versionName **0.1**;
- permanent signer fingerprint: exact established identity;
- APK signing verification: **v1/v2/v3 PASS**;
- public permanent release archive: verified present and retrievable.

Signed APK SHA-256:
`bf65901db9d28018ff21b21f6ad0b2bb62519a503dd08a6adeebf7f9cf67bf75`

Physical Fire TV behavior remains environment-dependent and is not claimed by CI. Required Build 12 real-device checks are stability/responsiveness, provider/login state preservation, normal DisneyNOW playback behavior without automatic Media3 takeover, persistent previous-session crash/restart breadcrumb reporting if another restart occurs, zoom, and Silk fallback.
