# Permanent APK release — App Battery List v1.0 Build 5

## Verified artifact identity
- Package: `com.fireworkstars46.appbatterylist`.
- versionName: `1.0`; versionCode/Build: `5`.
- Permanent certificate SHA-256: `BB:7F:D5:23:C7:67:32:70:28:07:5F:F7:8B:1D:50:D2:B5:5B:79:57:1A:3E:46:51:C2:BF:23:F2:BB:4F:43:93`.
- Signed APK SHA-256: `2f248417e655d6f249ff7415c3940212f838beebd80b18e5254e8a83aa24b63a`.
- Source ZIP SHA-256: `d5a422e118ad25d7a5b15101df155f985cc3887de02bb7b724514aa335eeeef2`.

## Execution evidence
- PASS — Local Java 17 compilation of actual AllSettingsReviewStore, AllSettingsAutoAdvance and AllSettingsAdvice sources against isolated Android stubs; 18 local harness assertions. This is NOT an Android UI runtime pass.
- PASS — Exact Build 3 source was SHA-256 verified, corrected Build 5 source patch SHA-256 verified, all 33 source manifest hashes checked.
- PASS — Real Android Gradle release compile (private run `41793167094`, job `126451008800`).
- PASS — Permanent signer recovery and expected fingerprint comparison before compiling.
- PASS — aapt package/versionCode/versionName checks and apksigner signature/fingerprint checks.
- PASS — GitHub Release asset publication and independent download-back SHA-256 verification (public run `41793546957`).
- PASS — Build 5 permanent source ZIP and signed APK archived in GitHub Release: https://github.com/Fireworkstars46/App-Builds/releases/tag/app-battery-list-v1.0-build5.
- NOT TESTED — Physical S22 All Settings Review App Info/Notifications Settings launches and auto-advance return callbacks.
- NOT TESTED — Safe Self-Test run on physical S22 and actual Android settings page behavior.
- NOT TESTED — Secure Folder and interactive OS export/share.

## No hidden privileges or settings changes
This app only navigates to supported Android Settings screens, then waits for the user to return. It cannot detect or change arbitrary other apps' settings and never claims to. The review state records visits, not applied setting changes. No new Android permission was introduced.

## Build 4 history
Build 4 Java compilation failed due a local-variable shadowing collision in the new Safe Self-Test and produced no released APK. The corrected artifact was assigned Build 5, leaving the Build 4 source patch untouched. Build 3 remains the previous permanent installable baseline.

**Final state: PRE-RELEASE / NOT DONE pending real-device testing.** Source, binary, signing and GitHub archive steps all passed.
