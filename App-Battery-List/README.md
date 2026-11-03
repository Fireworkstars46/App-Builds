# App Battery List

Android utility for reviewing installed apps and guiding battery/background-setting review.

## Current project
- Version: 1.0
- Build: 2
- Package ID: `com.fireworkstars46.appbatterylist`
- Target device: Samsung Galaxy S22 / Android 16
- Status: **NOT DONE / release pending**
- Release blocker: permanent Android signing identity durable-backup + real recovery-test gate has not passed yet.
- No permanent release APK is archived/released yet.

## Build history
- Build 1: initial installed-app listing/export/App Info utility.
- Build 2: adds Guided Battery Review with saved progress, Previous, Done & Next, Skip & Next, and automatic opening of the next app's App Info page.

Build 2 source is archived under `v1.0/Build-2/source/`. Build 1 remains preserved unchanged under `v1.0/Build-1/source/`.

The app does **not** silently change Samsung's Optimized / Unrestricted / Restricted setting. It opens standard Android App Info one app at a time; the user makes the battery choice.

Samsung Secure Folder is a separate Android/Knox profile, so a copy installed inside Secure Folder is required to enumerate/review that profile separately.

Private signing keys/passwords are intentionally not stored in this repository.
