# Fast ChatGPT Web — No-Work Release Automation

This is repository/release infrastructure for **future legitimate Fast ChatGPT Web builds**. Adding or changing this automation does **not** create a new app Build and does not change the current released app.

Current app baseline at the time this automation was added: **v66 Build 18 — DONE**.

## Goal

Future Fast ChatGPT Web builds can be built and archived without using ChatGPT Work or manually uploading large GitHub Release assets.

The ordinary ChatGPT GitHub connection can update source/release metadata and create release-gate branches. GitHub Actions then performs the Windows build and GitHub Release asset upload inside GitHub.

## Canonical future source location

Before a future legitimate build is staged, its complete release source tree is placed at:

`FastChatGPTWeb/Source/Current/`

That source must already contain the intended Version + Build in the app project, setup project, builder, filenames, reports, and release notes.

Do not update `Source/Current` merely to create a cosmetic/reconstructed Build. MASTER_RULES.md and the project's established build-number rules remain mandatory.

## Stage a future build

After the source and static/release reports for a legitimate future Build are ready and committed, create a branch with this exact format:

`fastchatgptweb-stage-v<VERSION>-build<BUILD>`

Example for a legitimate future v66 Build 19:

`fastchatgptweb-stage-v66-build19`

Creating that branch triggers `.github/workflows/fastchatgptweb-release.yml`.

The staging job:

1. verifies the branch Version + Build against both project files and the established builder;
2. refuses to overwrite/reuse an existing release tag;
3. makes the source ZIP before build outputs exist;
4. runs the project's established `BUILD-REAL-SETUP-EXE.bat` on a Windows GitHub runner;
5. verifies the build-success marker and required app/setup artifacts;
6. computes SHA-256 for the exact source ZIP, installer, and app EXE;
7. creates a **draft** GitHub Release containing those exact files plus applicable reports/notes;
8. stores the staged release directory as a GitHub Actions artifact for retrieval/testing.

The draft-release gate is intentional: compilation alone is not enough to call a build DONE.

## Validate before publishing

Run/review the required real Windows Safe Self-Test and any justified manual/interactive checks according to the current `MASTER_RULES.md`.

Archive privacy-safe validation evidence under:

`FastChatGPTWeb/Builds/v<VERSION>-Build-<BUILD>/SAFE-SELF-TEST-ARCHIVE-EVIDENCE.md`

Also archive the matching static-check report in that Build directory.

The evidence must explicitly show Safe Self-Test PASS and **0 FAIL**. Do not fabricate an unrun test or convert a missing result into PASS.

## Publish the exact already-staged release

After validation evidence is committed, create:

`fastchatgptweb-publish-v<VERSION>-build<BUILD>`

Example:

`fastchatgptweb-publish-v66-build19`

The publish job:

1. requires the archived Safe Self-Test evidence and static report;
2. requires zero FAIL;
3. downloads the existing **draft** GitHub Release assets;
4. verifies the exact asset SHA-256 values against the staged SHA-256 file;
5. verifies the source ZIP, setup EXE, and `FastChatGPTWebFinal.exe` are all present;
6. publishes that same draft release without rebuilding or replacing its binaries;
7. verifies the release no longer reports `draft=true`.

This means the binaries that were staged/tested are the exact binaries that become the permanent release.

## Normal-chat workflow

For future legitimate builds, the intended path is:

**regular chat → GitHub source commit → stage branch → GitHub Actions builds/uploads draft → Windows validation → evidence commit → publish branch → GitHub Actions verifies/publishes → regular chat verifies/archive manifest**

ChatGPT Work is not required for the binary upload step.

## Safety / identity rules

- Preserve established Fast ChatGPT Web project identity, paths, settings/data, IDs, installer/uninstall identity, login/WebView profile behavior, update compatibility, version history, and intentional multi-instance behavior.
- Never reuse an existing Build number for modified/reconstructed binaries.
- Never publish a staged release merely because it compiled.
- Never replace a draft release asset after it has been used as validation evidence; make the next legitimate Build instead if code/artifacts must change.
- Private runtime/navigation logs should not be published verbatim to this public repository.
- The repository `MASTER_RULES.md` remains the canonical mandatory rule set at release time.
