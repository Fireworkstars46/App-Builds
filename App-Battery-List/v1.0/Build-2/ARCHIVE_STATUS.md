# Archive Status — App Battery List v1.0 Build 2

- Source tree: **ARCHIVED** on GitHub.
- Build 1: preserved unchanged.
- Source hashes: archived.
- Compiler verification: **PASS** — GitHub Actions run `41650507654` compiled the `.dev` debug identity successfully with Android 17/API 37 preview SDK, JDK 17, AGP 9.5.0, and Gradle 9.6.0.
- Verification-only debug APK SHA-256: `390914158159874337de1b885f13bfd729835f2fb453a232ebd4f4749a0c320e`.
- Verification artifact ZIP SHA-256: `7b925237f57d653d1f77a2ff164b959051d27db0358c5445fe332d11e814bd05`.
- Verification artifact: GitHub Actions artifact ID `13236773811`; independently downloaded and hashes rechecked after the successful run.
- Permanent signing durable-backup + real recovery-test gate: **PASS** — two durable recovery copies exist and private recovery test run `41659723022`, job `125999413354` verified the exact permanent certificate identity.
- Permanent release compile/sign/identity verification: **PASS** — private run `41660227035`, job `126001152843` completed successfully.
- Permanent package ID: `com.fireworkstars46.appbatterylist`.
- Permanent versionName: `1.0`.
- Permanent versionCode / Build: `2`.
- Permanent signer SHA-256: `BB:7F:D5:23:C7:67:32:70:28:07:5F:F7:8B:1D:50:D2:B5:5B:79:57:1A:3E:46:51:C2:BF:23:F2:BB:4F:43:93`.
- Permanent APK SHA-256: `cc3e5a4ec1c01151e567a649584d76b67026e0e5450ba22bb9468fdd58d77a85`.
- Permanent GitHub Release asset: **ARCHIVED and retrieval-verified** at tag `app-battery-list-v1.0-build2`.
- Public publish/re-download verification: **PASS** — GitHub Actions run `41661089066`, job `126004158122` successfully published the asset and re-downloaded it with the expected SHA-256.
- Release state: **Pre-release** intentionally, because remaining physical-device checks are not yet complete.
- Physical Galaxy S22 / Samsung Settings runtime test: **NOT TESTED**.
- Guided Review real App Info -> Battery -> Back -> Next round-trip: **NOT TESTED** on-device.
- Secure Folder profile test: **NOT TESTED**.
- Safe Self-Test runtime execution on the Galaxy S22: **NOT TESTED**.

Overall project/release status: **NOT DONE / permanent APK archived, pending on-device validation**.

The public source archive contains no private signing keys or passwords. The permanent signing recovery material remains only in private recovery storage. The historical debug APK is compiler-verification evidence only; the GitHub Release APK is the permanent update identity for Build 2.
