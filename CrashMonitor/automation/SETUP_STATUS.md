# Crash Monitor release automation setup status

Status: **READY**

The GitHub-based Crash Monitor release builder is installed and leaves v4.2 Build 12 unchanged.

Validation completed on 2026-10-18:

- Workflow registration/push trigger verified successfully.
- Disabled-request probe run `39107851477` completed successfully.
- Non-archival Build 12 verification run `39107920819` completed successfully.
- The GitHub runner successfully prepared dependencies, extracted the archived Build 12 source ZIP, rebuilt the installer, ran the Build 12 release checker at **174 PASS / 0 FAIL**, packaged the source ZIP, and uploaded the generated verification artifact.
- Permanent archive commit/retrieval steps were intentionally skipped during the Build 12 verification because `archive` was false.
- Final ready-state probe run `39107986555` completed successfully after `request.json` was returned to `enabled: false`.
- `request.json` is now disabled and pre-positioned for a future v4.2 Build 13 request, but **Build 13 has not been created**.

Future normal release flow:

1. Add the next build's unified text patch under `CrashMonitor/automation/patches/`.
2. Update `CrashMonitor/automation/request.json` last and set `enabled: true` / `archive: true`.
3. GitHub Actions builds and statically validates the release, commits the exact EXE and source ZIP into a new immutable release folder, retrieves both files back from `origin/main`, verifies SHA-256, and records archive verification.
4. Run the Windows Safe Self-Test on that exact GitHub-built installer and add the runtime evidence/status as text.

No separate Work chat should be required for normal future Crash Monitor binary archival unless a future release introduces binary source inputs that cannot be generated from the text-based source/patch workflow.
