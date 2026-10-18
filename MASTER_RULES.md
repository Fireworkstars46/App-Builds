# Master App / Script Development Rules

This file is the canonical, full-detail rule set for all current and future app/script projects unless a project has an explicit project-specific requirement that is intentionally different.

Keep this GitHub copy detailed. Do not compress, shorten, or remove important requirements merely to fit a chat/message length limit. A shorter summary may be used for convenience in a chat, but that summary never replaces or weakens this canonical file.

Project-specific requirements add to these rules and override only the specific generic rule they intentionally conflict with. Preserve intentional project behavior. Do not force a tray, taskbar model, startup mode, multi-instance model, platform feature, UI pattern, or other generic behavior onto a project that was explicitly designed differently.

## 1. General goals
- Build stable, conflict-free, update-safe, reversible software.
- Preserve all known working features and intentional behavior during fixes, audits, rebuilds, and updates.
- Prefer minimal, targeted changes over unnecessary rewrites when a working project already exists.
- Keep unrelated projects independent unless integration is explicitly requested.
- Do not change unrelated behavior while fixing one feature.
- Respect established project-specific workflows, UI behavior, hotkeys, file formats, paths, settings, data, and user expectations.
- A confirmed regression or broken required feature changes the project/build status to NOT DONE until corrected and retested.
- Once a build is confirmed DONE, preserve that known-good build unchanged unless a legitimate new revision is required.
- Do not create a new build merely because a master rule changed. Audit the existing build first. Only create the next Build when an actual code/artifact correction or requested feature/change is required.
- Do not claim work was performed, tested, archived, or verified when it was not.

## 2. Version and build numbering
- Every downloadable revision must clearly identify both Version and Build.
- Increment Build for every revised downloadable artifact or code revision that changes the released program/script behavior or contents.
- Do not increment Build only because:
  - MASTER_RULES.md changed;
  - an audit was rerun with no required code/artifact changes;
  - an unchanged historical build is copied to permanent storage;
  - documentation or archive metadata is added without changing the released artifact.
- Use Build 1 only for a genuinely new project/version line when appropriate; do not accidentally reset established Build history.
- Preserve the project’s existing versioning scheme when one is already established.
- Never reuse a Build number for a different reconstructed or revised artifact.
- If a historical source/build is lost and a later reconstruction or correction is required, continue with the next legitimate Build number rather than pretending the reconstruction is the missing historical build.
- Include Version + Build in logs, diagnostics, reports, About/status areas, installers, source/release packages, and release filenames where practical.
- All artifacts claimed to belong to one release must identify the same Version + Build unless a project has an explicitly documented packaging exception.

## 3. Project identity, isolation, and update compatibility
- Give each project unique project-owned resources where applicable, including:
  - data/settings/log/temp folders;
  - registry locations;
  - package/bundle/application IDs;
  - mutexes and single-instance identifiers;
  - window/message IDs;
  - named pipes/sockets/ports;
  - shortcuts;
  - startup entries;
  - scheduled tasks/services;
  - filenames;
  - installer/uninstall identity;
  - update channels/keys/URLs;
  - other persistent resources.
- Do not let one project scan, modify, message, kill, hook, reuse, or share private state with another project unless explicitly requested.
- Preserve working project identity, paths, config formats, settings/data, file formats, package/bundle IDs, signing identity, release keys, and update compatibility.
- Warn before any change that could break in-place updates, overwrite user data, require uninstall/reinstall, change signing identity, invalidate existing settings, or create a second install identity.
- New settings should preserve old behavior or default OFF when enabling them could be disruptive, unless the user explicitly requested the new behavior as default.
- Upgrades should load older valid settings/data where practical rather than silently resetting them.
- Project-owned cleanup/uninstall logic must never remove unrelated files, registry values, tasks, shortcuts, services, or data belonging to another project.

## 4. Safety and least privilege
- Prefer per-user, least-permission, reversible methods.
- Avoid unnecessary administrator/root access, services, scheduled tasks, firewall changes, registry changes, hooks/injection, debugger attachment, process manipulation, broad system scanning, drivers, or unrelated file/input/clipboard access.
- Request elevated privileges only when genuinely required for the requested feature and keep the elevated scope as narrow as practical.
- Never log passwords, tokens, secrets, private messages, clipboard contents, typed text, raw keystrokes, or unrelated user data.
- Never delete, overwrite, move, rename, or modify unrelated files.
- If AV/SmartScreen flags behavior, first redesign or reduce the suspicious behavior when possible. Do not recommend disabling security products or adding broad exclusions unless the user explicitly approves a narrowly scoped exception after understanding the risk.
- Bulk/destructive operations should provide Preview/Dry Run/Test, include/exclude controls, confirmation where appropriate, and Undo/recovery when practical.
- Tests for destructive features must use isolated temporary test data rather than the user’s real files.
- Diagnostic/test features must not silently broaden permissions or collect unrelated data.

## 5. Preserve existing UX and project-specific behavior
- Existing intentional UX is binding unless the user asks to change it.
- Examples include a project intentionally using:
  - no tray icon;
  - a taskbar-visible main window;
  - tray-only operation;
  - X-to-exit behavior;
  - Close/X-to-tray behavior;
  - a specific startup mode;
  - single-instance or multi-instance behavior;
  - a custom hotkey model;
  - a project-specific workflow.
- Do not add generic features that contradict an established project design merely because another project has them.
- Preserve existing working controls, hotkeys, menu items, file formats, settings, state behavior, paths, and update flows unless the requested change requires modification.
- When a project intentionally differs from a generic master rule, document that difference rather than silently forcing the generic behavior.
- Project-specific features must be included in release testing, not just generic framework features.

## 6. Settings architecture and persistence
- Use one source of truth for each setting/state.
- Any state shown in more than one place must stay synchronized both ways, including Settings controls, tray checks/labels, status text, overlays, hotkeys, window styles, and saved state.
- Duplicate controls must call the same production setter/update path rather than maintaining separate copies of the logic.
- Important save/load/persistence operations must verify success. A try/catch that suppresses errors is not proof of a successful write/read.
- Persistence tests must perform write -> reload/read -> compare.
- Use atomic settings writes where practical so a crash/interruption cannot leave a partially written configuration.
- Handle missing, invalid, or corrupt settings safely and recover to valid defaults without destroying unrelated valid data.
- Preserve unknown/forward-compatible values where practical rather than rewriting the entire settings file unnecessarily.
- Provide Restore Defaults confirmation when restoring defaults would discard meaningful customized state.
- Provide Export/Import Settings when appropriate for the project.
- Validate imported content before applying it and reject malformed/incompatible values safely.
- Import/Restore Defaults should intentionally replace only the settings they are designed to replace.
- Preserve settings through updates unless an intentional migration is required.
- Settings intended to take effect immediately must:
  - use the normal production state path;
  - visibly/runtime apply immediately;
  - persist without an undocumented Save button or restart;
  - keep duplicated UI/tray/status representations synchronized.
- Settings that require restart/relaunch must:
  - clearly say so in the UI/status;
  - save the pending value safely;
  - preserve it across the required relaunch;
  - avoid pretending the runtime state already changed when it did not.
- Startup-only settings such as Start Minimized/Open Settings at startup may naturally take effect on the next launch, but they must still save immediately and clearly represent that next-launch behavior.
- For apps that can run multiple instances against shared settings/state:
  - prevent stale instances from overwriting newer committed changes on exit or save;
  - use synchronization, versioning, reload-before-write, merge-by-changed-value, locking, or another deterministic conflict policy appropriate to the project;
  - do not let an old in-memory settings snapshot silently rewrite newer values;
  - keep Import Settings/Restore Defaults semantics explicit if those operations intentionally replace the full configuration.

## 7. UI and window rules
- No clipped, truncated, overlapping, hidden, or off-screen controls/text at supported sizes.
- Do not solve clipping by shrinking text until it becomes unreadable.
- Use tabs, scrolling, wrapping, compact layouts, grouping, responsive reflow, or larger windows when needed.
- Keep critical actions such as Save, Close Settings, Exit App, Apply, Restore Defaults, and Test accessible.
- Resizable windows need safe minimum dimensions that prevent controls from becoming unusable.
- Support DPI scaling, resolution changes, and multi-monitor configurations where applicable.
- Use native DPI-aware layout where practical.
- Default/reset placement must use the OS-defined PRIMARY monitor rather than assuming monitor #1.
- Remember useful window X/Y/W/H and applicable window state, last tab/page, or panel selection when the project is designed to remember them.
- Never restore a remembered window completely off-screen or to an unusable size; clamp/recover it to a visible usable work area.
- Include Reset Window Layout when window position/size is remembered and the user could otherwise become stuck with a bad saved layout.
- Hidden test windows should use direct GUI/object APIs for geometry/state checks when normal window-discovery APIs may ignore hidden windows.
- Window-state tests should verify the actual window behavior/state, not only the saved setting value.
- Startup window placement should not flash on an unintended monitor/window state before moving to the final intended state when that can reasonably be avoided.

## 8. Always on Top / Pin Window
- For projects with normal windows/settings where appropriate, provide remembered configurable Always on Top / Pin Window when requested or already established.
- Do not force this feature onto projects where it is intentionally absent or meaningless.
- If exposed in both Settings and tray, both controls must use one shared production setter/state path and remain synchronized both ways.
- The displayed Settings value, tray checkmark, runtime window style, and persisted value must agree.
- Test the actual topmost window style/state, not only the stored checkbox value.
- Persist and restore the setting correctly when it is designed to persist.
- Changing the setting should affect the correct project windows and must not accidentally force unrelated windows topmost.

## 9. Tray behavior
- Apply this section only to projects that use a tray icon; do not force a tray onto apps intentionally designed without one.
- Tray apps should provide working Open/Show/Settings and Exit App controls when appropriate.
- When applicable, include established project features such as:
  - Start Minimized to Tray;
  - Minimize to Tray;
  - Close/X to Tray vs Exit;
  - Pause/Resume;
  - notifications;
  - Debug Mode;
  - Safe Self-Test;
  - Logs;
  - Diagnostics;
  - Export Diagnostic Report;
  - Always on Top/Pin Window.
- Start Minimized, Open Settings at startup, Start Paused, Minimize-to-Tray, and Close/X behavior are separate concepts/settings unless the project intentionally combines them.
- Tray labels, checkmarks, tooltips, enabled/disabled state, and dynamic text must reflect the actual current state.
- Dynamic labels such as Pause/Resume must update immediately after the state changes.
- If the same option exists in Settings and tray, changing either one must update the other through the same production state path.
- Tray icon/menu must recover after Explorer/taskbar restart using the appropriate TaskbarCreated/rebuild path when applicable.
- Configurable tray single-click/double-click actions must not both trigger from one double-click accidentally.
- Tray-only/minimized startup must still provide a reliable way to open the app/settings and exit cleanly.
- A visible tray item existing is not proof that its action works; applicable tray actions belong in functional testing.

## 10. Close, Minimize, and Exit behavior
- Close/X-to-Tray, Minimize-to-Tray, normal Close, and Exit App are distinct behaviors and must not accidentally call or imitate each other.
- Exit App must actually terminate the app/process through one shared production exit path.
- Every Exit control/menu item must use that same intended production exit path unless a documented project-specific reason requires otherwise.
- If Close/X-to-Tray is enabled, X must hide/close to tray without terminating.
- If Minimize-to-Tray is enabled, minimizing must not accidentally perform a full exit.
- If the project intentionally uses X to exit and has no tray, preserve that design.
- Test each applicable behavior independently.
- A callback/function existing is not proof that Exit/Close/Minimize works.
- Test actual process termination via an isolated child/subprocess/test harness when practical.
- Exit handlers must not accidentally cancel termination because of a helper return value, exception, event handler, or logging call.
- If real termination cannot be automated safely, report it as SKIPPED/NOT TESTED rather than PASS.
- Shutdown/exit should flush required state/logs safely without hanging indefinitely.

## 11. Single-instance and startup ordering
- Normally use single-instance behavior unless the project intentionally supports multiple instances.
- Intentionally single-instance projects do not need to add multi-instance support merely to satisfy these rules.
- Relaunch should show/focus the existing app when that is the intended UX rather than silently doing nothing or creating conflicting duplicates.
- Use a project-unique mutex/guard/identity when needed so unrelated programs cannot collide with the single-instance mechanism.
- Verify startup initialization order.
- External messages/callbacks must not access Settings/UI/state before required initialization has completed.
- Safely defer early requests/messages until state is ready.
- Test startup decisions such as Start Minimized, Start Paused, Open Settings, and autostart registration where applicable.
- If a project intentionally supports multiple instances, define clearly what is shared and what is per-instance.
- If a project intentionally supports switching between multi-instance and single-instance modes at runtime:
  - define the transition behavior explicitly;
  - when consolidating existing instances, choose the survivor deterministically;
  - request graceful shutdown of the other instances through the normal exit path rather than force-killing them;
  - re-enabling multi-instance should permit future launches;
  - re-enabling must not resurrect previously closed instances unless the project explicitly requires that behavior.
- Any project-specific survivor policy (for example, keep oldest instance) remains project-specific unless separately approved as a general rule.

## 12. Logging, diagnostics, Debug Mode, and privacy
- Log useful project events such as startup/shutdown, Version+Build, major actions, settings/state changes, warnings, errors, recovery, and important test outcomes.
- Keep logs project-local and bounded. A typical target is up to 5 rotating logs around 5 MB each unless the project has a better established limit.
- Do not allow debug/activity logs to grow without bound.
- Keep crash dumps separate from normal activity/debug logs when applicable.
- Provide easy access to Logs, Diagnostics, and Export Diagnostic Report for diagnostic-capable projects.
- Diagnostics must be targeted to the project and avoid collecting unrelated system/user content.
- Debug Mode, when the project has one, should:
  - be clearly identifiable as enabled/disabled;
  - add useful diagnostic detail without changing normal functional behavior more than necessary;
  - remain synchronized between Settings/tray/status if shown in more than one place;
  - persist only if the project intentionally makes it persistent;
  - never capture passwords, tokens, private messages, clipboard contents, typed text, raw keystrokes, or unrelated user activity;
  - avoid high-frequency polling or excessive logging that causes noticeable lag when a safer event-driven method is available.
- Safe Debug Mode for input/hotkey/overlay tools must remain privacy-safe and must not record the actual user text or raw private input.
- Production behavior must work correctly with Debug Mode OFF. A feature is not acceptable if it only works while debug/test instrumentation is enabled.
- Opening logs/diagnostics should not require disabling AV/SmartScreen or broadening permissions.
- Exported diagnostic reports should identify Version+Build and enough relevant state to troubleshoot the project without exposing secrets.

## 13. Static/release checks
Before release, perform applicable static/release checks and report real PASS/FAIL results. At minimum check:
- syntax/parser/compiler errors;
- unresolved build errors;
- undefined or duplicate functions/methods/classes;
- case-sensitive/case-insensitive name collisions as appropriate to the language;
- callback/event/hotkey/menu wiring;
- startup order and initialization;
- settings defaults/load/save/migration paths;
- immediate-setting/restart-required behavior declarations;
- project paths/IDs/resources;
- single-instance/multi-instance declarations and guards;
- tray/menu/control callbacks;
- window creation and state restoration;
- version/build/signing/update behavior;
- package/bundle/installer identity;
- import/export format handling;
- conflicts with other project resources;
- missing referenced files/resources/dependencies;
- obvious dead controls or unreachable code;
- stale version/build strings;
- release artifact filenames and metadata;
- project-specific invariants and known regression areas.

Static checks do not replace runtime/Safe Self-Test verification for behavior that can be safely exercised.

## 14. AutoHotkey/case-insensitive-language checks
- In case-insensitive languages such as AutoHotkey, statically check locals, parameters, globals, controls/properties, labels, class members, and helper names for case-insensitive collisions/shadowing.
- Pay special attention to short helpers such as R(), W(), H(), X(), Y(), logging, settings, state, and utility functions.
- Do not allow a local/parameter name to silently shadow a function/helper because capitalization differs.
- Parser errors, #Warn issues, startup warnings, uncaught runtime exceptions, or important failures hidden by broad try/catch block DONE status.
- In AutoHotkey, an OnExit callback must explicitly return 0/blank unless exit cancellation is intentionally required; do not let a logging/helper return value accidentally cancel process termination.
- For AutoHotkey projects with ExitApp/OnExit behavior, add an isolated child-process/test-harness regression test for actual termination when practical so accidental OnExit cancellation is detected before DONE.
- Static checks must verify that built-in variables, built-in functions, directives, object APIs, and other runtime-specific language features are valid for the project’s targeted AutoHotkey/runtime version.
- Be especially strict when code is migrated, reused, or adapted between AutoHotkey v1 and v2 or between other incompatible runtime versions.
- Invalid version-specific references are release-blocking issues even when surrounding logic appears correct.
- When practical, add a targeted regression check for known runtime-version mismatch mistakes so the same incompatibility cannot silently return in a later build.
- Do not suppress #Warn/parser/startup errors merely to make a build appear clean; correct the underlying issue.

## 15. Safe Self-Test requirements
- Provide a Safe Self-Test for projects where meaningful automated testing is possible.
- Test every safely testable required feature, not just a token subset.
- Use REAL production code paths whenever practical. Do not duplicate the application logic in a fake test-only implementation and call that proof.
- A callback/function existing is not a functional PASS; exercise the action and verify the resulting behavior/state.
- Test isolated temporary settings/data so real user settings/data are never damaged.
- File-moving/destructive tests must use isolated temporary files/folders only.
- Clean up temporary test data when practical, while preserving the report/log evidence needed to diagnose a failure.
- Persistence tests must perform write -> reload/read -> compare.
- Test Settings <-> tray/UI synchronization and verify the actual underlying runtime state.
- Test startup decisions/order, single-instance guard behavior, early message deferral, and applicable autostart logic.
- For multi-instance projects that share settings/state, when safely automatable, test stale-writer/conflict behavior so an older instance closing or saving cannot overwrite a newer committed setting.
- For projects with a runtime multi-instance/single-instance toggle, test the transition through production paths:
  - multiple instances are allowed when enabled;
  - disabling keeps the documented deterministic survivor;
  - other instances close/consolidate gracefully through normal exit behavior;
  - re-enabling allows future launches;
  - closed instances are not resurrected unless explicitly intended.
- For settings documented as immediate, verify both runtime effect and persistence without a separate Save/restart.
- For settings documented as restart/relaunch-required, verify the UI/status clearly says so and the value survives the required restart/relaunch when safely testable.
- Test window X/Y/W/H, primary-monitor placement, remembered position/size/tab/state, Reset Window Layout, and actual topmost state where applicable.
- Test import/export round-trip where applicable.
- Test Manual Check vs automatic/watcher paths where both exist and should behave equivalently.
- Test project-specific rules/engines through their production path.
- Test Undo/recovery using isolated data where applicable.
- Test applicable Debug Mode/Safe Debug Mode controls and state synchronization without capturing private input.
- Report expected vs actual on failures.
- Every individual test must report PASS, FAIL, or SKIPPED/NOT TESTED.
- Never count an unavailable, unexecuted, timed-out, or skipped test as PASS.
- SKIPPED/NOT TESTED must be limited to genuinely disruptive, unsafe, environment-dependent, or unautomatable actions and must state why.
- Examples of justified skips can include an actual reboot/logoff, forced Explorer termination, a real destructive user-file action, or a live external interaction that cannot be safely isolated.
- Safe Self-Test output must identify the tested Version + Build so evidence cannot be confused with another release.
- Keep useful incremental test evidence so a crash/hang does not erase all information about what completed.

### Safe Self-Test progress and hang visibility
- Long-running Safe Self-Tests must provide visible progress/status when practical instead of appearing frozen or idle.
- A user should be able to tell that the test is still running.
- Show useful status such as:
  - `Running`;
  - current test name or number;
  - completed/total count when the total is known;
  - current phase for multi-stage tests;
  - final PASS/FAIL/SKIPPED totals;
  - clear completion/failure/cancelled state.
- Progress/status must reflect the real test sequence and must never claim completion before all required tests have actually finished.
- Write/flush the Safe Self-Test report incrementally as tests complete when practical so the last recorded test identifies where a crash or hang occurred.
- For potentially slow subprocess, dump, ZIP/archive, network, external-tool, or file-operation tests, use a reasonable timeout/hang-detection strategy when practical rather than waiting forever.
- A timeout must be reported accurately as a failure/timeout or justified SKIPPED/NOT TESTED result; never silently convert it to PASS.
- If a test intentionally runs synchronously, provide status updates between stages/tests whenever the UI/framework permits.
- Completion dialogs/status must appear only after the actual test sequence has finished and the final report/totals have been written.
- A Safe Self-Test that is visibly stuck or never reaches final totals must not be treated as PASS/DONE.

## 16. Testing buttons, menus, hotkeys, and controls
- Every safely testable Settings button, tray item, toggle, hotkey, menu command, duplicate control, and important action must have a valid callback AND verified behavior.
- Exercise production handlers/setters directly or through the real UI path where safe.
- Verify expected vs actual state/value/result after each action.
- Examples of valid behavioral evidence include:
  - real state value;
  - UI value;
  - tray checkmark/label;
  - window visibility/topmost state;
  - saved/reloaded setting;
  - moved/copied file;
  - Undo result;
  - process termination;
  - output file/report;
  - actual project-specific operation.
- “The callback exists”, “the function is referenced”, or “the menu item is present” is a static check only, not a functional PASS.
- Duplicate controls for the same setting/action should be tested for two-way synchronization where safely possible.
- Test disabled/enabled states and dynamic labels when they are part of the behavior.

## 17. Watcher / mover / background-worker apps
- Show clear real state such as Running, Paused, Busy, Waiting, Stopped, or Error when applicable.
- Provide Manual Check Now/Refresh when useful to the project.
- Manual and automatic/watcher paths should use the same underlying engine where practical to avoid divergent behavior.
- Test watcher vs Manual Check equivalence where both should behave the same.
- Do not let overlapping worker runs corrupt shared state; serialize/debounce/reject overlap appropriately for the project.
- For file movers/copy tools:
  - use isolated test trees;
  - test selection/order/threshold/limits;
  - test staging when used;
  - exercise the actual move/copy engine;
  - verify final source/destination results;
  - test Undo/recovery without touching real user files;
  - validate nesting protection;
  - prevent source/destination recursion, self-move, and reprocessing of staging/output folders.
- Paused/stopped state must actually stop or defer new work according to the documented behavior.
- Status text/tray state must match the actual worker state.

## 18. Overlay / hotkey / input tools
- Preserve per-game/per-app profiles and isolation when applicable.
- Do not capture/log unrelated keys, clipboard content, typed text, or private input.
- Test hotkey enable/disable, conflicts, typing-mode exclusions, profile load/save, overlay visibility, movement/size, pin/topmost state, and startup state where applicable.
- Avoid hooks/injection when a safer API/input method is sufficient.
- Confirm overlays do not unintentionally interfere with unrelated apps/windows.
- Learned per-game/per-window state must not leak into another profile.
- Hotkey/profile changes should take effect and persist according to their documented immediate/restart behavior.
- Safe Debug Mode must remain event-focused and privacy-safe.
- Live gameplay/input automation that cannot be safely automated may be SKIPPED, but all surrounding safely testable configuration/state logic should still be tested.

## 19. Windows-specific rules
- Use unique per-project storage/registry/resources.
- Prefer least-invasive diagnostics and per-user configuration.
- Handle Explorer/taskbar restarts for tray-dependent apps.
- Respect the taskbar-visible vs tray-only vs no-tray design chosen for the project.
- Preserve update/install/uninstall identity for compiled apps.
- Keep installer and portable/standalone behavior consistent with the project’s established design.
- Do not require administrative rights unless the feature actually requires them.
- Unsigned Windows builds may still trigger SmartScreen/AV reputation warnings; do not claim a clean local static test guarantees no reputation-based warning.
- Do not instruct the user to disable Bitdefender/Defender/SmartScreen or create broad exclusions merely to make a build work.
- When crash dumps are part of a project, keep dumps bounded/separate and test dump creation only with safe isolated methods when possible.
- Explorer/taskbar forced termination is disruptive and may be a justified SKIPPED test if there is no safe equivalent.
- Preserve Windows startup/autostart behavior and registration compatibility when applicable.

## 20. Android rules
- When requested and tool availability allows, deliver a ready APK rather than only source/build instructions.
- Preserve package ID and release signing key so new builds update over installed versions.
- Increment versionCode for each installable update and preserve the chosen versionName scheme.
- Use unique project resources and launcher identity/icon.
- Preserve existing app data/update compatibility where platform rules permit.
- Keep/backup signing-key information safely; never expose private keys in chat, logs, repositories, or diagnostics.
- Do not change package ID casually because it creates a separate app identity/install.
- Request only permissions actually required by the app’s features.
- Unless the project says otherwise, target the user’s intended Galaxy S22/current supported Android environment.

## 21. iOS rules
- Preserve bundle ID, signing identity/profile strategy, supported iOS version, and update compatibility.
- Do not change bundle ID casually because it creates a separate app/install identity.
- Preserve sideload/update behavior when that is part of the project.
- Keep platform/version compatibility explicit, especially for older supported iPhones/iOS versions.
- Preserve the project’s established signing/re-signing workflow where possible.
- Do not expose signing secrets/private keys/profiles unnecessarily in logs or repositories.
- When older iOS support is an established requirement, do not silently adopt APIs/deployment targets that break that support.

## 22. Release artifacts
- Provide the requested final artifact type according to project needs and tool availability, such as script, standalone EXE, installer/setup, build package, APK, IPA/project/source ZIP, or other established package.
- Use clear filenames containing project/version/build where practical.
- Include source, static-check reports, Safe Self-Test reports, release notes, and hash reports when useful or established for that project.
- Preserve existing release layout and update flow unless a change is required.
- Artifacts for one release must correspond to the same source/revision and Version + Build.
- Do not silently replace an older release artifact with different bytes under the same historical filename/path.
- Generate SHA-256 or another established strong checksum for important release artifacts when practical.
- If a release artifact cannot be produced with the available tools, say so clearly rather than substituting a different artifact without explanation.
- Archive only exact completed artifacts; a reconstructed/staged copy with different bytes must not be claimed as the original artifact.

## 23. DONE criteria
A project/build is DONE only when all applicable requirements are satisfied:
- required static/release checks PASS;
- Safe Self-Test has 0 FAIL for all safely testable required features;
- there are no unresolved parser/#Warn/compiler/startup/runtime errors that block the release;
- there are no known broken controls, tray actions, window behaviors, persistence paths, Exit/Close behaviors, project-specific required features, or regression blockers;
- any SKIPPED/NOT TESTED items are clearly listed, justified, and limited to genuinely disruptive/unsafe/environment-dependent/unautomatable actions;
- update compatibility and existing working behavior have been preserved unless an intentional change was requested;
- applicable release artifacts correspond to the tested build;
- permanent archive requirements in Section 27 are satisfied for releases to which the archive rule applies.

Do not mark DONE merely because code parses, callbacks exist, a partial test passes, or a test report never reached final totals.

A real reproducible bug discovered after DONE immediately reopens the project/build as NOT DONE until corrected and retested.

## 24. Corrective-build rule
- If the user reports a reproducible bug after a build was called DONE, immediately treat the project as NOT DONE until the bug is fixed and the relevant regression tests are added/run.
- Preserve all unrelated working behavior while correcting the bug.
- Increment Build for the actual correction.
- Do not reuse the previous Build number for changed code/artifacts.
- Add or strengthen a regression test that would catch the same issue again when safely possible.
- Re-run static checks and all relevant Safe Self-Tests before restoring DONE status.
- If the issue is only incomplete verification/archival of unchanged bytes and no code/artifact correction is made, do not create a meaningless extra Build solely for that verification step.

## 25. Evidence and reporting
When reporting a build/audit/release result, clearly state applicable evidence rather than only saying “good” or “done.” Include:
- project name;
- current Version + Build;
- whether a new Build was actually required and why;
- static/release audit totals (PASS/FAIL) when available;
- Safe Self-Test totals (PASS/FAIL/SKIPPED/NOT TESTED) when available;
- the exact SKIPPED/NOT TESTED items and why they were not run;
- remaining manual/interactive checks;
- known warnings and whether they are release-blocking;
- runtime/log findings when real runtime evidence was supplied;
- permanent GitHub archive status when Section 27 applies;
- hashes/checksums when they are part of the release evidence;
- final DONE/NOT DONE/pending status and remaining blockers.

Additional reporting rules:
- Distinguish static validation from real runtime testing.
- Distinguish simulated/isolated behavior from a physically performed OS-level action.
- Do not claim an OS-level behavior was physically tested if it was only simulated or validated by logic.
- For failures, report the exact failing feature and expected vs actual result when available.
- Do not hide warnings/errors just because later tests passed unless they are clearly understood and proven non-blocking.
- Historical log errors from older Builds must not be incorrectly attributed to the current Build.
- A completion report should make it possible to tell what remains before DONE without rereading the entire development history.

## 26. Future rules and lessons
- When a new general development requirement, safety rule, testing rule, or recurring lesson is discovered, add it to this master rules file so future projects can use it automatically after user approval.
- When a new general rule, recurring lesson, or regression-prevention rule is discovered in a chat, tell the user it appears useful for the master rules and ask: “Want me to add this to MASTER_RULES.md?”
- Do not modify the master file automatically without the user’s approval.
- If the user explicitly asks to add the rule, that is approval for that requested change.
- If a new rule comes from a bug/regression, also add or strengthen a Safe Self-Test/regression test requirement that would detect the problem in future builds when safely possible.
- Project-specific features stay with that project unless they are useful as a general rule for other projects.
- Do not globalize a project-specific preference (for example, a specific multi-instance survivor policy) without explicit approval.
- Do not remove or weaken existing master rules when adding new ones unless the user explicitly requests it.
- A MASTER_RULES change alone does not create a new project Build. Existing projects should be audited against the newer rule, and a corrective Build is made only if the audit exposes a real code/artifact gap.
- Keep this canonical GitHub rule file detailed. Chat-length limits are not a reason to permanently compress the stored rules.

## 27. Permanent build archive
### Authoritative archive
- When GitHub access is available, use `https://github.com/Fireworkstars46/App-Builds` as the authoritative long-term archive for completed app/script builds and their release history.
- Chat attachments, `/mnt/data`, temporary download links, conversation file cards, and file-library copies may be convenience copies but must not be the only permanent copy of a release to which this rule applies.
- GitHub archival is part of the normal release process for future legitimate Builds; it is not a reason by itself to invent another Build number.

### What to preserve
Preserve every applicable completed-release artifact, including as appropriate:
- full source/source ZIP;
- standalone EXE or other runnable/package artifact;
- installer/setup package;
- APK/IPA/package where applicable;
- static/release audit report;
- Safe Self-Test report/evidence;
- checksums/hashes;
- release notes/changelog/history;
- safe project recovery metadata;
- other project-specific release evidence needed to recover or verify the build.

Do not require an artifact type that does not apply to the project, but do not omit an applicable artifact merely because another copy exists in chat.

### Exact artifact and integrity rules
- Preserve the exact finished artifact bytes whenever the artifact already exists.
- Do not reconstruct, transcode, repackage, or stage a different byte sequence and claim it is the original historical artifact.
- Record SHA-256 (or the project’s established strong checksum) for important artifacts when practical.
- After archival, verify that the intended GitHub copies actually exist and are retrievable.
- Where practical, re-download/re-fetch the archived artifact and confirm its checksum matches the finished artifact.
- A commit attempt, upload attempt, chat attachment, generated file, or metadata-only record is not proof that the actual required binary/source artifact was archived.
- If a connector/tool cannot upload binary bytes but the binary is required, use an appropriate GitHub path such as a repository binary upload mechanism or GitHub Release asset when available rather than pretending a text-only placeholder satisfies the rule.
- Large binaries may be stored as GitHub Release assets while source/history/audit metadata remains associated with the same project/release.

### Security/privacy
- Never archive passwords, tokens, private signing keys, secrets, private profiles, or other sensitive recovery material.
- Preserve only recovery metadata that is safe for the repository.
- Do not put user-private logs/data into a public repository unless they have been safely sanitized and are genuinely needed.

### History and lost-source handling
- Preserve historical completed builds unchanged.
- Do not silently overwrite, replace, or repurpose an older Version/Build path or artifact with a later reconstruction/revision.
- Use clear project/version/Build folders and filenames so old releases remain independently identifiable and recoverable.
- Never fabricate or relabel a missing historical source/build to fill an archive gap.
- Record a missing historical artifact/source accurately as unavailable/lost and preserve all trustworthy remaining evidence.
- If reconstruction or code changes are later required, continue with the next legitimate Build number rather than reusing the lost historical Build number.

### Failure/incomplete archive handling
- If archival fails or GitHub is unavailable, report that clearly and do not claim the permanent archive succeeded.
- Keep any available convenience/recovery copy, but complete permanent archival when the required capability becomes available.
- If only part of the release evidence is archived while required source/binary artifacts are still missing, report the archive as INCOMPLETE rather than YES/verified.
- Do not create a new Build solely because an unchanged current Build still needs its exact artifacts uploaded/verified.

### Build-number interaction
- Archiving an unchanged existing build does not increment its Version or Build number.
- Increment Build only when a revised downloadable artifact/code revision is actually produced under the normal version/build rules.
- Do not make Build N+1 simply because Build N needs archival verification.

### Legacy rollout for builds completed before this rule
- Builds that were already legitimately DONE before the permanent-archive rule was adopted remain DONE; do not retroactively rebuild or retest them solely because this rule was added.
- Do not create a new Build solely to make an older DONE build satisfy the new archive rule.
- If the exact older DONE artifacts are still available and can be archived safely, they may be archived under the same historical Version + Build without changing the build number.
- If an older DONE build’s exact source/artifacts are unavailable, do not fabricate them and do not downgrade that historical build solely because it predates the rule.
- For those legacy projects, permanent archival becomes mandatory with the next legitimate Build/release that is already required for a real bug fix, feature, corrective change, or other actual artifact/code change.
- From that next legitimate Build forward, the release is subject to the full archival verification requirements in this section.

### DONE interaction for releases subject to Rule 27
- For a new/future release to which this rule applies, permanent archival verification is part of release completion.
- Do not call that release fully archived/DONE until all applicable required permanent release artifacts have been verified in `Fireworkstars46/App-Builds` (or an associated GitHub Release asset when appropriate).
- An otherwise tested release may remain pending/NOT DONE because required archive artifacts are incomplete, without creating another Build solely for archival.
