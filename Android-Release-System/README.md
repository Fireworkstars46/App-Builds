# Android Release System for Future Apps

This directory is the reusable permanent-release standard for new Android apps in `Fireworkstars46/App-Builds`.

It does **not** weaken or replace `MASTER_RULES.md`. The master rules remain authoritative. This system exists to make the normal Android release process repeatable and much less manual after each app's one-time signing identity is established.

## What this solves

For each future Android app, the one-time setup is:

1. Choose the permanent package ID before the first long-lived installable release.
2. Create one permanent release keystore for that app. Do not reuse a debug/CI key as the permanent identity.
3. Keep at least two durable recovery copies outside GitHub, ChatGPT attachments, `/mnt/data`, temporary CI artifacts, and other ephemeral storage.
4. Perform one real recovery test from a backup copy and record only the safe public SHA-256 certificate fingerprint.
5. Create a GitHub Environment for that app containing the standardized private signing secrets.
6. Copy the template release metadata into the app source tree.
7. Add a tiny caller workflow that points to the app source folder and its GitHub Environment.

After that, normal future Builds reuse the same package ID and signer. The shared workflow builds the APK, checks the package/version/signer, generates a checksum, and can create a permanent GitHub Release automatically.

## Standard GitHub Environment secrets

Each app gets its own GitHub Environment, for example `android-example-app`, with these same secret names:

- `ANDROID_RELEASE_KEYSTORE_B64`
- `ANDROID_RELEASE_STORE_PASSWORD`
- `ANDROID_RELEASE_KEY_ALIAS`
- `ANDROID_RELEASE_KEY_PASSWORD`

The values are app-specific even though the secret names are standardized.

The GitHub copy is for automated signing only. It does **not** replace the required durable recovery backups.

## Standard project files

Copy these template files into every new Android app source tree:

- `release/RELEASE_CONFIG.env`
- `release/RELEASE_NOTES.md`
- `signing/EXPECTED_SIGNER_SHA256.txt`
- `signing/BACKUP_RECOVERY_STATUS.txt`

The project build script must read these environment variables for its `release` signing config:

- `ANDROID_RELEASE_KEYSTORE`
- `ANDROID_RELEASE_STORE_PASSWORD`
- `ANDROID_RELEASE_KEY_ALIAS`
- `ANDROID_RELEASE_KEY_PASSWORD`

The release build must fail closed if those values are unavailable. Never generate a replacement key automatically.

## Shared workflow

The reusable workflow is:

`.github/workflows/android-release-reusable.yml`

It performs these release gates:

- validates the release contract and required metadata;
- refuses release while backup/recovery status is not `PASS`;
- reconstructs the app-specific signing keystore only in the temporary GitHub runner from an Environment secret;
- builds `assembleRelease`;
- verifies package ID;
- verifies `versionName`;
- verifies `versionCode`;
- verifies the APK signing certificate SHA-256 fingerprint;
- generates SHA-256 for the APK;
- uploads a short-lived verification artifact;
- optionally creates the permanent GitHub Release;
- refuses to overwrite an existing tag/release;
- removes the temporary runner keystore at the end.

## Build history

Every changed installable revision must use the next legitimate Build/versionCode. Never reuse a Build number for changed APK bytes. Existing historical release tags/assets must remain immutable.

## Permanent APK location

The intended permanent downloadable APK lives as a GitHub Release asset. Chat files and Actions artifacts are convenience/testing copies only.

## Important limitation

This system deliberately cannot make the first permanent signing identity fully hands-off. The private key must have durable user-controlled recovery backups and a real recovery test before the first permanent release. That one-time safety gate protects future in-place Android updates.
