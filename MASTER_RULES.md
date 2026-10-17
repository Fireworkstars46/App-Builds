# Master App / Script Development Rules

These rules apply to all current and future app/script projects unless a project has an explicit project-specific requirement that is intentionally different. Preserve intentional project behavior. Do not force a tray, taskbar model, startup mode, platform feature, or UI pattern onto a project that was explicitly designed differently. Project-specific requirements add to these rules and override only the conflicting generic rule.

## 1. General goals
- Build stable, conflict-free, update-safe, reversible software.
- Keep unrelated projects independent unless integration is explicitly requested.
- Preserve all known working features and intentional behavior during fixes and updates.
- Prefer minimal, targeted changes over rewrites when a working project already exists.
- A confirmed regression or broken required feature changes project status to NOT DONE until corrected and retested.
- Once a build is confirmed DONE, preserve that known-good build unchanged unless a new revision is requested.

## 2. Version and build numbering
- Every downloadable revision must show both Version and Build.
- Increment Build for every revised downloadable artifact, including corrective builds.
- Use Build 1 only for a new project/new version line as appropriate; do not reset Build accidentally.
- Preserve the project’s existing versioning scheme when already established.
- Include Version + Build in logs, diagnostics, reports, About/status areas when applicable, and release filenames where practical.

## 3. Project identity, isolation, and update compatibility
- Give each project unique project-owned resources: data/settings/log/temp folders, registry locations, package/bundle IDs, mutexes, window/message IDs, named pipes, ports, shortcuts, tasks/services, filenames, uninstall identity, and other persistent identifiers.
- Do not let one project scan, modify, message, kill, hook, or share private state with another project unless explicitly requested.
- Preserve working project identity, paths, config formats, settings/data, file formats, package/bundle IDs, signing identity, release keys, and update compatibility.
- Warn before any change that could break in-place updates, overwrite user data, require uninstall/reinstall, change signing identity, or invalidate existing settings.
- New settings should preserve old behavior or default OFF when enabling them could be disruptive, unless the user explicitly requested the new behavior as default.

## 4. Safety and least privilege
- Prefer per-user, least-permission, reversible methods.
- Avoid unnecessary admin/root, services, scheduled tasks, firewall changes, registry changes, hooks/injection, debugger attachment, process manipulation, broad system scanning, drivers, or unrelated file/input/clipboard access.
- Never log passwords, tokens, secrets, private messages, clipboard contents, keystrokes, or unrelated user data.
- Never delete/overwrite unrelated files.
- If AV/SmartScreen flags something, first redesign the behavior causing the warning; do not recommend disabling security or broad exclusions unless specifically approved.
- Bulk/destructive operations should provide Preview/Dry Run/Test, include/exclude controls, confirmation where appropriate, and Undo/recovery when practical.

## 5. Preserve existing UX and project-specific behavior
- Existing intentional UX is binding. Examples: a project intentionally using no tray, a taskbar-visible app, a tray-only worker, a specific startup mode, a custom hotkey model, or a project-specific workflow.
- Do not add generic features that contradict an established project design.
- Preserve existing working controls, hotkeys, menu items, file formats, settings, state behavior, and update paths unless the requested change requires modification.
- Project-specific features must be included in release testing, not just generic framework features.

## 6. Settings architecture and persistence
- Use one source of truth for each setting/state.
- Any state shown in more than one place must stay synchronized both ways: Settings controls, tray checks/labels, status text, overlays, hotkeys, window styles, and saved state.
- Duplicate controls must use the same production setter/update path instead of separate logic.
- Important save/load/persistence operations must verify success. try/catch alone is not proof.
- Persistence tests must perform write -> reload/read -> compare.
- Use atomic settings writes where practical.
- Handle missing/corrupt settings safely and recover to valid defaults without destroying unrelated data.
- Provide Restore Defaults confirmation when destructive.
- Provide Export/Import Settings when appropriate and validate import content before applying.
- Preserve settings through updates.
- For apps that can run multiple instances against shared settings/state, prevent stale instances from overwriting newer committed changes on exit or save. Use synchronization, versioning, reload-before-write, or another deterministic conflict policy appropriate to the project.
- Settings intended to take effect immediately should apply through the normal production state path and persist without requiring an undocumented Save or restart step. If a restart/relaunch is required, make that explicit in the UI/status and preserve the pending value safely.

## 7. UI and window rules
- No clipped, truncated, overlapping, hidden, or off-screen controls/text at supported sizes.
- Use tabs, scrolling, wrapping, compact layouts, or responsive reflow when needed instead of shrinking text until unreadable.
- Keep critical actions such as Close/Exit/Save accessible.
- Resizable windows need safe minimum dimensions.
- Support DPI scaling, resolution changes, and multi-monitor configurations.
- Use native DPI-aware layout where practical.
- Default/reset placement must use the OS-defined PRIMARY monitor, not assume monitor #1.
- Remember useful window X/Y/W/H and applicable window state, last tab/page, or panel selection.
- Never restore remembered windows off-screen; clamp/recover to a visible usable area.
- Include Reset Window Layout when window position/size is remembered.
- Hidden test windows should use direct GUI/object APIs for geometry/state checks when discovery APIs may ignore hidden windows.

## 8. Always on Top / Pin Window
- For projects with normal windows/settings where appropriate, provide remembered configurable Always on Top / Pin Window when requested or already established.
- If exposed in Settings and tray, both controls must use one shared state path and remain synchronized both ways.
- Test the actual topmost window style/state, not only the stored checkbox value.
- Persist and restore the setting correctly when it is designed to persist.

## 9. Tray behavior
- Apply this section only to projects that use a tray icon; do not force a tray onto apps intentionally designed without one.
- Tray apps should provide working Open/Show/Settings and Exit App controls.
- When applicable, include Start Minimized, Minimize-to-Tray, Close/X-to-Tray vs Exit, Pause/Resume, notifications, Debug, Safe Self-Test, Logs, Diagnostics, and Export Report.
- Start Minimized, Open Settings at startup, Start Paused, Minimize-to-Tray, and Close/X behavior are separate settings unless the project intentionally combines them.
- Tray labels/checkmarks/tooltips must reflect actual current state.
- Dynamic labels such as Pause/Resume must update immediately and stay synchronized with Settings/status.
- Tray icon/menu must recover after Explorer/taskbar restart using the appropriate TaskbarCreated/rebuild path.
- Do not allow single-click and double-click tray actions to both trigger accidentally.

## 10. Close, Minimize, and Exit behavior
- Close/X-to-Tray, Minimize-to-Tray, normal Close, and Exit App are distinct behaviors and must not call each other accidentally.
- Exit App must actually terminate the app/process through one shared production exit path.
- Every Exit control/menu item must use that same path.
- If Close/X-to-Tray is enabled, X must hide/close to tray without terminating.
- If the project intentionally uses “X exits” and no tray, preserve that design.
- Test each applicable behavior independently.
- A callback existing is not proof that Exit/Close/Minimize works.
- Test actual process termination via an isolated child/subprocess/test harness when practical. If real termination cannot be automated safely, report SKIPPED/NOT TESTED rather than PASS.

## 11. Single-instance and startup ordering
- Normally use single-instance behavior unless the project intentionally supports multiple instances.
- Relaunch should show/focus the existing app when that is the intended UX.
- If a project intentionally supports switching between multi-instance and single-instance modes at runtime, define the transition behavior explicitly. When consolidating existing instances, choose the survivor deterministically and request graceful shutdown of the others through the normal exit path rather than force-killing them. Re-enabling multi-instance should permit future launches and should not recreate previously closed instances unless the project explicitly requires that behavior.
- Verify startup initialization order.
- External messages/callbacks must not access Settings/UI/state before required initialization has completed.
- Safely defer early requests/messages until state is ready.
- Test startup decisions such as Start Minimized, Start Paused, Open Settings, and autostart registration where applicable.

## 12. Logging, diagnostics, and privacy
- Log startup/shutdown, major actions, state/settings changes, warnings, errors, recovery, timestamps, and Version+Build.
- Keep logs project-local and bounded. A typical target is up to 5 rotating logs around 5 MB each unless the project has a better established limit.
- Keep crash dumps separate from normal logs when applicable.
- Provide easy access to Logs, Diagnostics, and Export Diagnostic Report for diagnostic-capable projects.
- Diagnostics must be targeted to the project and avoid unrelated system/user content.

## 13. Static/release checks
Before release, check at minimum:
- syntax/parser errors;
- undefined or duplicate functions;
- callback/event/hotkey wiring;
- startup order and initialization;
- settings defaults/load/save paths;
- project paths/IDs/resources;
- tray/menu/control callbacks;
- window creation and state restoration;
- version/build/signing/update behavior;
- import/export format handling;
- conflicts with other projects/resources;
- missing referenced files/resources;
- obvious dead controls or unreachable code.

## 14. AutoHotkey/case-insensitive-language checks
- In case-insensitive languages such as AutoHotkey, statically check locals, parameters, globals, controls/properties, labels, and helper names for case-insensitive collisions/shadowing.
- Pay special attention to short helpers such as R(), W(), logging, settings, state, and utility functions.
- Do not allow a local/parameter name to silently shadow a function/helper.
- Parser errors, #Warn issues, startup warnings, uncaught runtime exceptions, or important failures hidden by broad try/catch block DONE status.
- In AutoHotkey, an OnExit callback must explicitly return 0/blank unless exit cancellation is intentionally required; do not let a logging/helper return value accidentally cancel process termination.
- For AutoHotkey projects with ExitApp/OnExit behavior, add an isolated child-process/test-harness regression test for actual termination when practical so accidental OnExit cancellation is detected before DONE.
- Static checks must verify that built-in variables, built-in functions, directives, and other runtime-specific language features are valid for the project’s targeted AutoHotkey/runtime version.
- Be especially strict when code is migrated, reused, or adapted between AutoHotkey v1 and v2 or between other incompatible runtime versions.
- Invalid version-specific references are release-blocking issues, even when the surrounding logic is otherwise correct.
- When practical, add a targeted regression check for known runtime-version mismatch mistakes so the same incompatibility cannot silently return in a later build.

## 15. Safe Self-Test requirements
- Provide a Safe Self-Test for projects where meaningful automated testing is possible.
- Test every safely testable feature, not just a token subset.
- Use REAL production code paths whenever practical. Do not duplicate logic in a fake test-only implementation and call that proof.
- A callback/function existing is not a functional PASS; exercise the action and verify the resulting behavior.
- Test isolated temporary settings/data so real user settings/data are never damaged.
- Persistence: write -> reload/read -> compare.
- Test Settings <-> tray/UI synchronization and the actual underlying state.
- Test startup decisions/order, single-instance guard behavior, early message deferral, and applicable autostart logic.
- For multi-instance projects that share settings/state, when safely automatable, test stale-writer/conflict behavior so an older instance closing or saving cannot overwrite a newer committed setting.
- For projects with a runtime multi-instance/single-instance toggle, test the transition through production paths: multiple instances are allowed when enabled; disabling keeps the documented deterministic survivor and gracefully closes/consolidates the others; re-enabling allows future launches without resurrecting closed instances.
- For settings documented as immediate, verify both runtime effect and persistence without a separate Save/restart. For settings documented as restart-required, verify the UI/status clearly says so and the value survives the required restart/relaunch when safely testable.
- Test window X/Y/W/H, primary-monitor placement, remembered position/size/tab/state, Reset Window Layout, and topmost state where applicable.
- Test import/export round-trip where applicable.
- Test Manual Check vs automatic/watcher paths where both exist.
- Test project-specific rules/engines through their production path.
- File-moving/destructive tests must use isolated temporary files/folders only.
- Test Undo/recovery with isolated data where applicable.
- Report expected vs actual on failures.
- Every individual test reports PASS, FAIL, or SKIPPED/NOT TESTED.
- Never count an unavailable or unexecuted test as PASS.
- SKIPPED must be limited to genuinely disruptive/unautomatable actions such as an actual reboot/logoff or forced Explorer termination when a safe equivalent cannot be used.

## 16. Testing buttons, menus, hotkeys, and controls
- Every safely testable Settings button, tray item, toggle, hotkey, menu command, and duplicate control must have a valid callback AND verified behavior.
- Exercise production handlers/setters directly or through the real UI path where safe.
- Verify expected vs actual state/value/result after each action.
- Examples of valid evidence: real state value, UI value, tray checkmark/label, window visibility/topmost state, saved/reloaded setting, moved file, Undo result, process termination, output file, or actual project-specific operation.
- “The callback exists” or “the function is referenced” is a static check only, not a functional PASS.

## 17. Watcher / mover / background-worker apps
- Show clear real state such as Running, Paused, Busy, Waiting, Error when applicable.
- Provide Manual Check Now/Refresh when useful.
- Manual and automatic paths should use the same underlying engine where practical.
- Test watcher vs Manual Check equivalence where both should behave the same.
- For file movers: use isolated test trees, test selection/order/threshold/limits, staging, actual move/copy engine, and real Undo/recovery without touching real user files.
- Validate nesting protection and prevent source/destination recursion or self-move conditions.

## 18. Overlay / hotkey / input tools
- Preserve per-game/per-app profiles and isolation when applicable.
- Do not capture/log unrelated keys, clipboard, or input.
- Test hotkey enable/disable, conflicts, typing-mode exclusions, profile load/save, overlay visibility, movement/size, pin/topmost state, and startup state where applicable.
- Avoid hooks/injection when a safer API/input method is sufficient.
- Confirm overlays do not unintentionally interfere with unrelated apps/windows.

## 19. Windows-specific rules
- Use unique per-project storage/registry/resources.
- Prefer least-invasive diagnostics and per-user configuration.
- Handle Explorer/taskbar restarts for tray-dependent apps.
- Respect taskbar-visible vs tray-only vs no-tray design chosen for the project.
- Preserve update/install/uninstall identity for compiled apps.
- Unsigned Windows builds may still trigger SmartScreen/AV; do not claim a clean local static test guarantees reputation-based warnings will not occur.

## 20. Android rules
- When requested, deliver a ready APK rather than only source/build instructions.
- Preserve package ID and release signing key so new builds update over installed versions.
- Increment versionCode for each installable update and preserve the chosen versionName scheme.
- Use unique project resources and launcher identity/icon.
- Preserve existing data/update compatibility where platform rules permit.
- Keep/backup signing-key information safely; never expose private keys in chat or logs.
- Unless the project says otherwise, target the user’s intended Galaxy S22 / current supported Android environment.

## 21. iOS rules
- Preserve bundle ID, signing identity/profile strategy, supported iOS version, and update compatibility.
- Do not change bundle ID casually because it creates a separate app/install identity.
- Preserve sideload/update behavior when that is part of the project.
- Keep platform/version compatibility explicit, especially for older supported iPhones/iOS versions.

## 22. Release artifacts
- Provide the requested final artifact type: script, EXE/build package, APK, IPA/project/source ZIP, etc., according to project needs and tool availability.
- Use clear filenames containing project/version/build where practical.
- Include source/static-check reports/hash reports when useful or established for that project.
- Preserve existing release layout and update flow unless change is required.

## 23. DONE criteria
A project/build is DONE only when all of the following are true:
- required static/release checks PASS;
- Safe Self-Test has 0 FAIL for all safely testable required features;
- there are no unresolved parser/#Warn/startup/runtime errors;
- there are no known broken controls, tray actions, window behaviors, persistence paths, Exit/Close behaviors, or project-specific required features;
- any SKIPPED/NOT TESTED items are clearly listed and limited to genuinely disruptive/unautomatable actions;
- update compatibility and existing working behavior have been preserved unless an intentional change was requested.

Do not mark DONE just because code parses, callbacks exist, or a partial test passes.

## 24. Corrective-build rule
- If a user reports a reproducible bug after a build was called DONE, immediately treat the project as NOT DONE until the bug is fixed and the relevant regression tests are added/run.
- Preserve all unrelated working behavior while correcting the bug.
- Increment Build for the correction.
- Re-run static checks and all relevant Safe Self-Tests before restoring DONE status.

## 25. Evidence and reporting
- When reporting completion, state Version + Build, static-check result, Safe Self-Test result, and any SKIPPED/NOT TESTED items.
- Distinguish static validation from real runtime testing.
- Do not claim an OS-level behavior was physically tested if it was only simulated/validated by logic.
- For failures, report the exact failing feature and expected vs actual result when available.

## 26. Future rules and lessons
- When a new general development requirement, safety rule, testing rule, or recurring lesson is discovered, add it to this master rules file so future projects use it automatically.
- When a new general rule, recurring lesson, or regression-prevention rule is discovered in a chat, tell the user it appears useful for the master rules and ask: “Want me to add this to MASTER_RULES.md?” Do not modify the master file automatically without the user’s approval.
- If the new rule comes from a bug or regression, also add or strengthen a Safe Self-Test/regression test that would detect that problem in future builds.
- Project-specific features stay with that project unless they are useful as a general rule for other projects.
- Do not remove or weaken existing master rules when adding new ones unless the user explicitly requests it.

## 27. Permanent build archive
- When GitHub access is available, use `https://github.com/Fireworkstars46/App-Builds` as the authoritative long-term archive for completed app/script builds and their release history.
- Chat attachments, `/mnt/data`, temporary download links, conversation file cards, and file-library copies must not be the only copy of a completed build. They may be provided as convenience copies, but they do not replace the permanent archive.
- Preserve every applicable completed-release artifact, including the full source/source ZIP, standalone EXE or other runnable/package artifact, installer/setup package, static/audit report, Safe Self-Test report or evidence, checksums/hashes, release notes/history, and project recovery metadata that is safe to store.
- Never archive passwords, tokens, private signing keys, secrets, or other sensitive recovery material. Preserve only recovery metadata that is safe for the repository.
- Preserve historical completed builds unchanged. Do not silently overwrite, replace, or repurpose an older Version/Build path or artifact with a later reconstruction or revision.
- Use clear project/version/Build folders and filenames so old releases remain independently identifiable and recoverable.
- Verify that the intended permanent GitHub copies actually exist and are retrievable after archival. A commit attempt, upload attempt, chat attachment, or generated file is not proof of successful permanent archival.
- If archival fails or GitHub is unavailable, report that clearly and do not claim the permanent archive succeeded. Keep any available convenience copy, but retry permanent archival when GitHub access becomes available.
- Archiving an unchanged existing build does not increment its Version or Build number. Increment Build only when a revised downloadable artifact/code revision is actually produced under the normal version/build rules.
- Never fabricate or relabel a missing historical source/build to fill an archive gap. Record the historical artifact/source as unavailable or lost, preserve all trustworthy remaining evidence, and continue with the next legitimate Build number if reconstruction or code changes are required.
- When GitHub is available for the project, permanent archival verification is part of release completion: do not call the release fully archived/DONE until the required permanent release artifacts have been verified in `Fireworkstars46/App-Builds`.
