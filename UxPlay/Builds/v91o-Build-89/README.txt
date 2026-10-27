UxPlay Quality Launcher Full - v91o Build 89

Corrective target
- Build 88 successfully advanced into the QuickTime/PING timeout-recovery stage, but the Direct USB section test interrupted the still-running backend after each 60-second wait with a project-owned "Keep Waiting?" Yes/No dialog.
- The user requires Direct USB Test itself to be the only application control needed for the test workflow.

Build 89 change
- Direct USB Test no longer shows the project-owned once-per-build phone-confirmation reminder.
- Direct USB Test no longer shows the 60-second "Keep Waiting?" Yes/No dialog.
- The obsolete section-test wait for USBMUX_PREFLIGHT_RESULT was removed because the Build 84+ live libusb0 path intentionally skips that blocking preflight.
- After automatic prerequisite setup and backend start, the section test watches the renderer and backend continuously with no application confirmation prompts.
- The backend can succeed or fail first. A bounded 300-second maximum automatic safety window remains for the normal 60-second section-test request; if nothing resolves by then, the launcher stops/restores USB automatically and reports FAIL without asking the user another question.
- Windows UAC and iOS-owned Trust/Allow/passcode prompts are not project-owned and cannot be bypassed; they may still require normal user approval if the OS/phone presents them.

Preserved
- Build 88 one-button exact-iPhone libusb0 prerequisite repair and exact-device PnP restart.
- Build 87 airplaya-derived activation lifecycle: release pre-transition handle, fresh enumerate/inspect/dispose polling, dynamic subclass 0x2A discovery, clear ENDPOINT_HALT on both QuickTime endpoints.
- Build 86 dedicated STA prompt implementation remains in source but is not invoked by Direct USB Test.
- Build 84 queued 5x4096 USB IN reader, canonical protocol ordering, timeout recovery, and protocol diagnostics.
- Persistent black Direct USB renderer and settings persistence.
- Build 80 known-good Wi-Fi native renderer/title-bar pin/FPS behavior.
- Stable installer AppId and per-user install identity.

Safety
- No Defender/Bitdefender/SmartScreen disabling or exclusions.
- No broad driver replacement.
- Exact selected iPhone parent only for automatic filter repair/restart.
- Existing libusb0 system files/service must already be healthy; unsafe/unverified states fail closed.
- The automatic wait is bounded; it does not wait forever.

Validation status
- Static/source audit only in this environment.
- Windows C# compile / installer build: NOT TESTED.
- UAC/helper execution on the user's Windows PC: NOT TESTED for Build 89 package.
- Real one-click UI behavior with the user's iPhone: NOT TESTED.
- Real H.264 arrival: NOT TESTED.

Status: NOT DONE / pending Windows + real iPhone validation.

Reference implementation note
- Build 89 preserves the independently implemented protocol behavior informed by the previously supplied open-source reference; it does not vendor, copy, or redistribute airplaya source files.
