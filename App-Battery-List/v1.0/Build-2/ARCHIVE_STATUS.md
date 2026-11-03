# Archive Status — App Battery List v1.0 Build 2

- Source tree: ARCHIVED on GitHub.
- Build 1: preserved unchanged.
- Source hashes: archived.
- Compiler verification: **PASS** — GitHub Actions run `41650507654` compiled the `.dev` debug identity successfully with Android 17/API 37 preview SDK, JDK 17, AGP 9.5.0, and Gradle 9.6.0.
- Verification-only debug APK SHA-256: `390914158159874337de1b885f13bfd729835f2fb453a232ebd4f4749a0c320e`.
- Verification artifact ZIP SHA-256: `7b925237f57d653d1f77a2ff164b959051d27db0358c5445fe332d11e814bd05`.
- Verification artifact: GitHub Actions artifact ID `13236773811`; independently downloaded and hashes rechecked after the successful run.
- Physical Galaxy S22 / Samsung Settings runtime test: NOT TESTED.
- Guided Review real App Info -> Battery -> Back -> Next round-trip: NOT TESTED on-device.
- Secure Folder profile test: NOT TESTED.
- Safe Self-Test runtime execution on the Galaxy S22: NOT TESTED.
- Permanent signing durable-backup + real recovery-test gate: **PASS** — two durable recovery copies exist and private recovery test run `41659723022`, job `125999413354` verified the exact permanent certificate identity.
- Permanent release APK: PENDING permanent release build/sign/archive.

Overall project/release status: **NOT DONE / pending permanent APK + remaining on-device checks**.

This source archive does not contain private signing keys or passwords. The debug APK above exists only as compiler-verification evidence and must not be treated as the permanent release/update identity.
