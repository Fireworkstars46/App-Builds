# App Battery List — v1.0 Build 3

Purpose: create a clean list of installed Android apps and guide the user through reviewing battery/background settings app-by-app with fewer repeated taps.

## Project identity
- App name: App Battery List
- Package ID: `com.fireworkstars46.appbatterylist`
- Version: 1.0
- Build: 3
- Android versionCode: 3
- Release target: Galaxy S22 / Android 16 / Samsung One UI 8
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
  - **Auto Review mode:** when Android Settings returns control to App Battery List, the current app is marked done and the next app's App Info page opens automatically;
  - **Manual Review mode:** preserves the Build 2 Previous / Done & Next / Skip & Next workflow;
  - Auto Next can be toggled on/off for the active review and persists with review state;
  - remembers current position and skipped apps across app restarts;
  - excludes system apps, disabled apps, and App Battery List itself.
- Copy current filtered list.
- Export TXT and CSV to `Downloads/App Battery List` with no storage permission.
- Share TXT using Android's chooser.
- Diagnostics page including Guided Review state and Auto Next mode.
- Safe Self-Test using production query/filter/export/logging/review-state code paths where practical.
- Bounded project-local activity log.

## Guided Review safety / Android limitation
Build 3 still uses the standard public Android `Settings.ACTION_APPLICATION_DETAILS_SETTINGS` page for each package. Android does not expose a supported public intent for third-party apps to jump directly to Samsung's per-app **Optimized / Unrestricted / Restricted** three-choice screen for arbitrary other apps.

The app therefore does **not** use Accessibility, root, ADB, hidden Samsung components/APIs, or device-admin privileges to press Battery or change another app's battery mode. The user remains in control of the actual battery setting.

Auto Review uses Android's normal activity-result return path: App Battery List launches App Info for the current package, waits for Settings to return control, advances through the same persisted Guided Review production path, then opens the next package. If an OEM Settings build does not return the activity result as expected, the existing manual controls remain available as a fallback.

## Privacy / permissions
The only declared permission is `android.permission.QUERY_ALL_PACKAGES`, needed to enumerate packages visible to the current profile. The app declares no Internet permission and no storage permission. It has no background service.

## Secure Folder limitation
Samsung Secure Folder is a separate Android/Knox profile. Android profile isolation means an app running outside Secure Folder should not be expected to enumerate the Secure Folder profile. To list/review Secure Folder apps, install/open the same utility inside Secure Folder and run a separate review there.

## Release signing gate
The established permanent signing identity is preserved from Builds 1-2.

- Durable backup copies: PASS.
- Real recovery test from a durable backup: PASS.
- Expected permanent certificate SHA-256 is recorded under `signing/`.
- Release builds fail closed if signing environment variables, expected signer metadata, or backup/recovery PASS status are missing.
- No private keystore/password is stored in this public source package.

## Build environment variables
- `APP_BATTERY_LIST_KEYSTORE`
- `APP_BATTERY_LIST_STORE_PASSWORD`
- `APP_BATTERY_LIST_KEY_ALIAS`
- `APP_BATTERY_LIST_KEY_PASSWORD`

Never commit the keystore or passwords to a public repository.
