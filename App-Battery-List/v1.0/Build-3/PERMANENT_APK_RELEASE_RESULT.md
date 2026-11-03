# Permanent APK Release Result — App Battery List v1.0 Build 3

Status: **PASS for build/sign/archive; PRE-RELEASE / NOT DONE pending physical-device validation**.

Permanent release identity:
- Package ID: `com.fireworkstars46.appbatterylist`
- versionName: `1.0`
- versionCode / Build: `3`
- Permanent signer SHA-256: `BB:7F:D5:23:C7:67:32:70:28:07:5F:F7:8B:1D:50:D2:B5:5B:79:57:1A:3E:46:51:C2:BF:23:F2:BB:4F:43:93`
- APK SHA-256: `7ff2ef388d2394be8b902ddebbe27c64bb36ab8476200e713c07f3266cd1b12f`
- APK size: 2,160,956 bytes
- Reconstructed source ZIP SHA-256: `d9b3a9cce515a4b9919305417526f5b70e005c1b299fb5f654a2f80a9846492d`

Release build/sign verification:
- Private permanent build/sign run: `41672628058`
- Job: `126044737399`
- Exact source reconstruction/hash verification: **PASS**
- Permanent signing recovery/fingerprint verification: **PASS**
- Android release compilation: **PASS**
- Package/version verification: **PASS**
- APK signature verification: **PASS**

Permanent archive:
- GitHub tag: `app-battery-list-v1.0-build3`
- GitHub Release name: `App Battery List v1.0 Build 3 — Permanent Signed Pre-release`
- Release state: **Pre-release**
- Public release publication/retrieval run: `41673220070`
- Published APK and source ZIP were downloaded back from the GitHub Release and their exact SHA-256 values were rechecked: **PASS**
- The one-use transfer workflow was removed after successful publication; the release assets remain permanent under the tag.

Feature status:
- Build 3 adds Guided Review **Auto Review / Auto Next** while preserving Manual Review and the existing Done & Next / Skip & Next fallback controls.
- No hidden Samsung API/component, Accessibility auto-clicking, root, or ADB behavior was added.

Remaining validation:
- Physical Galaxy S22 Auto Review App Info -> Battery -> Back -> automatic next-App-Info loop: **NOT TESTED**
- Safe Self-Test on physical Galaxy S22: **NOT TESTED**
- Secure Folder runtime/profile behavior: **NOT TESTED**

Therefore Build 3 is archived and update-compatible, but remains **NOT DONE** until the applicable physical-device checks pass. The Build 3 APK bytes must not be replaced under this tag; any future code/artifact correction must use the next legitimate Build number.
