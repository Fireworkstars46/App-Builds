# Compiler Verification Result — App Battery List v1.0 Build 3

Status: **PASS**.

Successful permanent release pipeline:
- GitHub Actions repository: private signing/release repository.
- Workflow run: `41672628058`.
- Job: `126044737399`.
- Runner: Ubuntu 24.04.
- Java: 17.
- Gradle: 9.6.0.
- Android platform: Android 17 / API 37 preview package `platforms;android-37.0`.
- Android Build Tools: 36.0.0.
- Android Gradle Plugin: 9.5.0 from the archived project source.

Verified before compilation:
- Frozen Build 2 source + archived Build 3 text patch reconstructed the exact expected Build 3 source hashes.
- Package ID source identity remained `com.fireworkstars46.appbatterylist`.
- versionName remained `1.0`.
- versionCode / Build changed legitimately to `3`.
- Guided Review Auto Review / Auto Next source invariants were present.
- Durable signing backup/recovery gate was PASS.

Build result:
- `:app:clean :app:assembleRelease`: **PASS**.
- Permanent signer recovery and expected certificate fingerprint comparison: **PASS**.
- APK package/version verification: **PASS**.
- APK signature verification: **PASS**.
- Permanent signed APK SHA-256: `7ff2ef388d2394be8b902ddebbe27c64bb36ab8476200e713c07f3266cd1b12f`.
- Reconstructed source ZIP SHA-256: `d9b3a9cce515a4b9919305417526f5b70e005c1b299fb5f654a2f80a9846492d`.

Earlier Build 3 workflow attempts that failed during source-archive reconstruction did so before app compilation/signing. They were CI/archive setup failures and did not represent a compiler failure or changed Build 3 app artifact.

Runtime status:
- Physical Galaxy S22 Auto Review Settings-return loop: **NOT TESTED**.
- Safe Self-Test on physical Galaxy S22: **NOT TESTED**.
- Secure Folder runtime: **NOT TESTED**.
