# Release Notes — App Battery List v1.0 Build 2

Requested feature revision from Build 1.

Added:
- Guided Battery Review for enabled user-installed apps.
- Saved review progress with resume support.
- Open Current, Previous, Done & Next, Skip & Next, and End Review controls.
- Automatic opening of the next app's App Info page after Done & Next / Skip & Next.
- Skipped-app tracking and completion summary.
- Diagnostics visibility for Guided Review state.
- Safe Self-Test coverage for review queue planning plus isolated write -> reload/read -> compare persistence/advance/previous/completion/clear paths.

Preserved:
- Package ID `com.fireworkstars46.appbatterylist`.
- VersionName 1.0.
- Permanent signing certificate identity metadata.
- Existing list/search/filter/copy/TXT/CSV/share/diagnostics/logging features.
- No Internet/storage/background-service permissions.

Changed:
- Build 1 -> Build 2.
- versionCode 1 -> 2.

Status: NOT DONE / release pending.
Blockers: permanent signer durable-backup + real recovery-test gate is still pending; physical Galaxy S22/Samsung Settings round-trip and Secure Folder behavior remain NOT TESTED until run on-device; no final release APK is permitted until the signing gate passes.
