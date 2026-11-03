# App Battery List — v1.0 Build 1

Purpose: create a clean list of installed Android apps so battery/background settings can be reviewed app-by-app.

## Project identity
- App name: App Battery List
- Package ID: `com.fireworkstars46.appbatterylist`
- Version: 1.0
- Build: 1
- Android versionCode: 1
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
- Copy current filtered list.
- Export TXT and CSV to `Downloads/App Battery List` with no storage permission.
- Share TXT using Android's chooser.
- Diagnostics page.
- Safe Self-Test using production query/filter/export/logging code paths where practical.
- Bounded project-local activity log.

## Privacy / permissions
The only declared permission is `android.permission.QUERY_ALL_PACKAGES`, needed to enumerate packages visible to the current profile. The app declares no Internet permission and no storage permission. It has no background service.

## Secure Folder limitation
Samsung Secure Folder is a separate Android/Knox profile. Android profile isolation means an app running outside Secure Folder should not be expected to enumerate the Secure Folder profile. To list Secure Folder apps, install/open the same utility inside Secure Folder and export that profile separately.

## Release signing gate
Build 1 source is prepared and its permanent signing key/certificate identity has been created. The public certificate SHA-256 is recorded under `signing/`, but the release gate remains pending. A release APK must not be produced with a debug/temporary replacement key. Before the first permanent installable release:
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
