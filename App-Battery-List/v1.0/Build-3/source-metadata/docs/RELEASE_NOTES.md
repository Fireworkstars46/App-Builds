# Release Notes — App Battery List v1.0 Build 3

Requested Guided Review workflow improvement from Build 2.

Added:
- Auto Review mode.
- When Android Settings returns from the current app's App Info page, Auto Review advances the saved queue and opens the next app automatically.
- Auto Next ON/OFF state stored with the Guided Review session.
- Auto Next toggle in the active review controls.
- Start dialog now offers Auto Review or Manual Review.
- Diagnostics shows Auto Next state.
- Safe Self-Test coverage for Auto Next persistence, toggle write -> reload/read -> compare, return-decision logic, and Build 2-compatible manual default behavior.

Preserved:
- Package ID `com.fireworkstars46.appbatterylist`.
- VersionName 1.0.
- Permanent signing certificate identity.
- Build 2 review persistence namespace and existing saved queue compatibility.
- Manual Previous / Done & Next / Skip & Next / End Review controls.
- Existing list/search/filter/copy/TXT/CSV/share/diagnostics/logging features.
- No Internet/storage/Accessibility/root/device-admin/background-service permissions.
- Secure Folder remains a separate profile and separate review.

Intentionally not added:
- No undocumented Samsung Settings component/deep link. Android's supported public battery intents do not provide Samsung's arbitrary per-app Optimized/Unrestricted/Restricted page.
- No automatic battery-mode selection.

Changed:
- Build 2 -> Build 3.
- versionCode 2 -> 3.

Release status before physical S22 validation: NOT DONE / pre-release candidate. Compiler/static/signing checks must pass, and the Auto Review Settings return loop plus Safe Self-Test must be tested on the physical Galaxy S22 before DONE.
