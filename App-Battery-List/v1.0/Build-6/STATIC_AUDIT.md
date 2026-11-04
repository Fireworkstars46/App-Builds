# Static / Release Audit — App Battery List v1.0 Build 6

- PASS (source): unchanged applicationId com.fireworkstars46.appbatterylist, versionName 1.0, versionCode 6, projectBuild 6.
- PASS (source): Build 5 complete archived source matches SHA-256 d5a422e118ad25d7a5b15101df155f985cc3887de02bb7b724514aa335eeeef2.
- PASS (source): isolated All Settings Review prefs retain name all_settings_review_v1, older saved sessions default to App Info first.
- PASS (source): new sessions use supported Notification Settings intent first, and App Info second where applicable.
- PASS (source): Important Only uses advisory package categories, not actual/current system settings; Review All remains available.
- PASS (source): no changes to Guided Review, filter, TXT/CSV, share, settings/data paths, signing gate or permissions.
- PASS (source): matching app/package/step return gate; manual previous/next/skip fallback preserved.
- PASS (isolated): 18 legacy harness assertions + 43 new notification-first/important-only plan, persistence, regression assertions.
- NOT TESTED: real Android Gradle compile until CI runs.
- NOT TESTED: physical Samsung S22 Settings return callbacks and supported Notifications action.
- NOT TESTED: S22 Safe Self-Test, Secure Folder and export/share OS operations.
- NOT TESTED: final signer APK identity verification until CI runs.
- NOT TESTED: final source/APK archival checksum retrieval until publication.

**Status:** PRE-RELEASE / NOT DONE pending applicable tests; do not claim UI passes from source review alone.
