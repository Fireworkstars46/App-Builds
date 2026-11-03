# App Battery List

Android utility for reviewing installed apps and preparing battery/background-setting recommendations.

## Current project
- Version: 1.0
- Build: 1
- Package ID: `com.fireworkstars46.appbatterylist`
- Target device: Samsung Galaxy S22 / Android 16
- Status: **NOT DONE / release pending**
- Release blocker: permanent Android signing identity durable-backup + real recovery-test gate has not passed yet.
- No APK is archived/released yet.

## Build 1
Full Build 1 source is archived under `v1.0/Build-1/source/`.

The app currently:
- lists apps visible to the current Android profile;
- supports search and User/System filtering;
- exports/copies TXT/CSV lists;
- opens Android App Info when an app is tapped;
- does **not** silently change another app's battery mode;
- does **not** automatically cycle through all app settings in Build 1.

Samsung Secure Folder is a separate Android/Knox profile, so a copy installed inside Secure Folder is required to enumerate that profile separately.

Private signing keys/passwords are intentionally not stored in this repository.
