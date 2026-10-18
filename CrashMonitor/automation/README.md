# Crash Monitor GitHub release automation

This folder exists so future Crash Monitor releases can be built and permanently archived by GitHub Actions without using a separate Work chat to upload EXE/ZIP binaries.

**Adding this automation does not create Build 13 and does not change the completed v4.2 Build 12 release.** `request.json` is intentionally disabled until a real future code/artifact revision is requested.

## Release flow

1. Start from the previous DONE release's archived `Crash_Monitor_*_Source.zip` in `CrashMonitor/releases/<base release>/`.
2. Prepare a normal unified text patch under `CrashMonitor/automation/patches/`. The patch represents the next build's source/documentation changes and uses paths relative to the root of the extracted source ZIP.
3. Update `request.json` **last**. Changing that one text file triggers the workflow.
4. GitHub Actions extracts the previous archived source ZIP, applies the patch, builds the freestanding Win32 x64 installer, runs that build's own `release_checks_*.py`, creates a deterministic source ZIP, hashes both exact artifacts, and refuses to continue on any compile/static failure.
5. The workflow commits the generated installer, source ZIP, CI logs, request snapshot, patch, hash manifest, and a PENDING `ARCHIVE_STATUS.md` into a brand-new `CrashMonitor/releases/vX.Y-BuildN/` folder. It refuses to reuse or overwrite an existing release folder/build number.
6. The workflow fetches the just-pushed files back from `origin/main`, recomputes both SHA-256 values, validates the source ZIP, and records the remote retrieval verification in `ARCHIVE_STATUS.md`.
7. Install and run the Windows Safe Self-Test from the **exact GitHub-built installer**. Do not rebuild it locally for release testing.
8. Add the runtime report/log evidence and update the final status only when the current rules allow it.

## Why this removes the Work-chat binary upload step

The main chat only needs to write text to GitHub: the patch, request, and later runtime evidence/status. GitHub Actions itself creates and commits the binary EXE and ZIP, so the chat never has to base64/upload those binary files through the GitHub contents connector.

## Safety / release guarantees

- `request.json` is the only automatic push trigger, so source/patch preparation can happen without starting half-finished builds.
- `enabled: false` is a no-op.
- An archived release must use a target build greater than the base build.
- Existing release folders are immutable: the builder fails rather than overwriting one.
- Compiler warnings/errors block the release.
- The target build's own static/release checker must return zero failures.
- An optional `expected_static_pass` count can lock the expected static total when known.
- The generated source ZIP is sorted and uses fixed ZIP timestamps for deterministic packaging.
- The final PE link uses a zero timestamp to reduce needless binary variation between equivalent rebuilds.
- The workflow records exact byte sizes and SHA-256 values before committing.
- Build automation never claims Windows runtime PASS, never converts environment-owned checks to PASS, and never marks the release DONE by itself.
- No passwords, signing keys, release keys, or other secrets belong in `request.json` or patch files.

## Patch format

Generate a standard unified Git patch from two extracted source trees, with file paths relative to the source ZIP root. Renames are allowed. Example:

```text
diff --git a/crash_monitor_42_build12-source.cpp b/crash_monitor_42_build13-source.cpp
similarity index 99%
rename from crash_monitor_42_build12-source.cpp
rename to crash_monitor_42_build13-source.cpp
...
```

The patch must update all Version/Build strings, filenames, release notes, manifests/scripts, and any intentionally changed source. The release checker is expected to catch stale identifiers as an additional guard.

## request.json fields

- `enabled`: must be `true` to build.
- `archive`: normally `true`. When false, the workflow only produces an Actions artifact and does not commit a permanent release folder.
- `base_release_folder`: previous archived release folder, for example `v4.2-Build12`.
- `target_version`: version string, for example `4.2`.
- `target_build`: next legitimate Build number.
- `patch_file`: repository-relative unified patch file. A blank patch is only useful for non-archival verification.
- `expected_static_pass`: integer when the expected total is known, otherwise `null`.

## Build environment

The workflow uses Ubuntu 24.04, Python 3.12, pinned Pillow 11.3.0, Clang/lld, and the project's established freestanding `x86_64-pc-windows-msvc` build/link flags. It logs tool versions in every generated release folder.
