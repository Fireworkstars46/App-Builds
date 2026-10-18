# Crash Monitor v4.2 Build 12

Build 12 is a corrective release for the Build 11 Safe Self-Test startup regression.

## Fixed

- Fixes the reproducible Windows Safe Self-Test child exit `0xC0000005` seen in Build 11 before its persistent report was created.
- Moves the large 39-check self-test body onto a dedicated worker thread with an explicit 262,144-byte committed stack, while keeping the process-entry wrapper tiny.
- Corrects the launcher-side initial Safe Self-Test progress total from the stale value 36 to 39.

## Preserved

- Build 11 automated checks for staged Update/Repair preservation, actual temporary Start Menu shortcut launch, and guarded physical Explorer/taskbar restart/recovery.
- Build 10 boundary-safe archive splitting and deterministic reassembly regression coverage.
- Existing project identity, settings/data paths, installer/update identity, mutex/window classes, tray/taskbar behavior, WER integration, OBS PSS/VA-clone dump path, lossless compression, and unsigned signing state.

## Validation status

Static/release checker: 174 PASS / 0 FAIL.
Compiler: 0 warnings / 0 errors.
Compiler stack-usage evidence: `RunSafeSelfTest` wrapper 72 bytes; execution worker 40 bytes; 39-check body 41,016 bytes, executed with a 262,144-byte committed worker stack.

Windows runtime Safe Self-Test is still required before Build 12 can be considered DONE. Expected automated structure remains 39 numbered checks with 4 environment-owned NOT TESTED items.
