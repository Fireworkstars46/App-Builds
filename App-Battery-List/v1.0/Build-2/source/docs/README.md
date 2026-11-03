# App Battery List — v1.0 Build 2

Purpose: create a clean list of installed Android apps and guide the user through reviewing battery/background settings app-by-app.

## Project identity
- App name: App Battery List
- Package ID: `com.fireworkstars46.appbatterylist`
- Version: 1.0
- Build: 2
- Android versionCode: 2
- Release target: Galaxy S22 / Android 16
- targetSdk: 36
- compileSdk: 37
- AGP: 9.5.0
- Java: 17

## Features
- Lists packages visible to the current Android profile.
- Shows app icon, label, package name, User/System classification, and enabled state.
- Search by app name or package.
- Filter All / User / System.
- Tap an app to open Android App Info.
- Guided Battery Review for enabled user-installed apps:
  - starts/resumes a saved review queue;
  - opens the current app's App Info page;
  - after the user returns, provides Open Current / Previous / Done & Next / Skip & Next / End Review;
  - automatically opens the next app when Done & Next or Skip & Next is chosen;
  - remembers current position and skipped apps across app restarts;
  - excludes system apps, disabled apps, and App Battery List itself.
- Copy current filtered list.
- Export TXT and CSV to `Downloads/App Battery List` with no storage permission.
- Share TXT using Android's chooser.
- Diagnostics page including Guided Review state.
- Safe Self-Test using production query/filter/export/logging/review-state code paths where practical.
- Bounded project-local activity log.

## Guided Review safety / Android limitation
The app only opens the standard Android App Info page for each package. It does not use Accessibility, root, ADB, hidden Samsung APIs, or device-admin privileges to press or change Optimized / Unrestricted / Restricted automatically. The user remains in control of the battery choice. This is intentional least-privilege behavior.

## Privacy / permissions
The only declared permission is `android.permission.QUERY_ALL_PACKAGES`, needed to enumerate packages visible to the current profile. The app declares no Internet permission and no storage permission. It has no background service.

## Secure Folder limitation
Samsung Secure Folder is a separate Android/Knox profile. Android profile isolation means an app running outside Secure Folder should not be expected to enumerate the Secure Folder profile. To list/review Secure Folder apps, install/open the same utility inside Secure Folder and run a separate review there.

## Release signing gate
Build 2 preserves the established package ID and permanent signing identity metadata from Build 1. The public certificate SHA-256 remains recorded under `signing/`, but the release gate is still pending. A release APK must not be produced with a debug/temporary replacement key. Before the first permanent installable release:
1. Save at least two durable user-controlled backup copies of the permanent keystore outside ChatGPT/temp/CI storage.
2. Perform a real recovery test using one backup copy.
3. Verify the recovered signer SHA-256 matches the recorded expected fingerprint.
4. Mark the backup/recovery gate PASS only after that verification.
5. Only then build/sign the release APK and archive the exact finished artifacts.

The Gradle `preReleaseBuild` path depends on `verifyReleaseSigning` and fails when signing environment variables or expected signer metadata are missing.

## Build environment variables (after signing gate passes)
- `APP_BATTERY_LIST_KEYSTORE`
- `APP_BATTERY_LIST_STORE_PASSWORD`
- `APP_BATTERY_LIST_KEY_ALIAS`
- `APP_BATTERY_LIST_KEY_PASSWORD`

Never commit the keystore or passwords to a public repository.
