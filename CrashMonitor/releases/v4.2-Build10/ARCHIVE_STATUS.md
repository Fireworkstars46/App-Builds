# Crash Monitor v4.2 Build 10 — Archive Status

**Section 27: COMPLETE — exact release artifacts uploaded and retrieved successfully.**  
**Verification date:** 2026-10-18  
**Release:** v4.2 Build 10  
**Archive repository:** `Fireworkstars46/App-Builds`  
**Target folder:** `CrashMonitor/releases/v4.2-Build10/`  
**Build increment:** None. The released program, installer, and source ZIP are unchanged.

## Exact binary verification

Both original attachments were checked locally before upload, uploaded as binary Git blobs, retrieved from GitHub using the binary-preserving base64 file route, decoded, and compared byte for byte with the attachments. SHA-256 was calculated again from the retrieved bytes. Both sizes, SHA-256 hashes, and Git blob identities match the originals.

| Artifact | Verified bytes | Verified SHA-256 | Git blob SHA |
| --- | ---: | --- | --- |
| `Crash_Monitor_v4.2_Build_10_Setup.exe` | 154624 | `602eb882926073000006baa3a9c2b15f3ad0e514cb4f53d3261b59d6894337a1` | `0969bf410694f5070a6aeb224ac2d39684b2dedf` |
| `Crash_Monitor_v4.2_Build_10_Source.zip` | 104273 | `7e887d88e6a52d3ff443ec0ef7c15776f97a23a0d942ad0dca95c3213b21333c` | `9bd0e1fbbfe9dca7c725cb0e971ad9c40b339627` |

The source ZIP passed an integrity check after retrieval. Its 24 entries were preserved without extraction/repackaging or modification.

The binary verification commit is [`f9b3106ebc9af02cffa29ad9b4a09bee37b98966`](https://github.com/Fireworkstars46/App-Builds/commit/f9b3106ebc9af02cffa29ad9b4a09bee37b98966). Both binaries are part of that commit and its descendant archive-status commit on `main`.

## Existing release evidence preserved

All 13 pre-existing files other than this intentionally updated status document were retrieved successfully and retain their original sizes and Git blob identities. The only release-folder changes are the addition of the two exact binaries and this archive-status update.

Existing reports record:

- Static/release audit: **163 PASS / 0 FAIL**; compiler **0 warnings / 0 errors**.
- Actual Windows Safe Self-Test: **36 PASS / 0 FAIL / 0 SKIPPED / 6 NOT TESTED**, reaching **SAFE SELF-TEST FINISHED**.
- These are previously archived test results, not new application tests executed during this archival task.
- Actual Windows report: `CrashMonitor-SafeSelfTest-v4.2-Build10.txt`; 6163 bytes; SHA-256 `11cc5c27048d9ef5fde8ff3fb7abe13ce017dfc3e4f3c3a988b316fd2b25a302`; Git blob `1c869800120543cc5e47c57b0afe1c33c67735df`.

The current authoritative `MASTER_RULES.md` was checked: Git blob `8dfded979df65ded2f84757cf8a678c664225186`. Archiving unchanged finished bytes and updating archive metadata do not require Build 11.

## Resolved archive blocker

Earlier attempts lacked access to the original binaries or produced truncated historical objects. Those rejected objects were not restored. The original installer and source ZIP were subsequently attached to this Work task and matched the recorded expected sizes and hashes. The current archive contains the exact originals, so the earlier BLOCKED / INCOMPLETE archive status is resolved.

## Separately documented manual/environment checks

These six items remain **NOT TESTED**, are not counted as PASS, and were not performed by this archive task:

| Check | Reason it remains NOT TESTED |
| --- | --- |
| Actual Update/Repair over an installed older build and user-data preservation | Requires the installed Windows environment and an older installation. |
| Actual Windows sign-out/reboot proving Start with Windows launches at sign-in | Requires a real interactive sign-out/reboot. |
| Windows Search indexing/discovery and user-visible shortcut launch | Requires the actual installed Windows shell/indexing environment. |
| Real HKLM WER enable/disable UAC elevation flow | Requires the real privileged registry/UAC interaction; the isolated registry engine was tested separately. |
| Physical Explorer.exe/taskbar termination/restart | Disrupts the user's desktop; the production TaskbarCreated recovery path was tested without terminating Explorer. |
| Bitdefender/SmartScreen reputation result | Depends on the real security product and external reputation state; static checks do not prove this outcome. |

**Archive status: COMPLETE. No remaining Section 27 blocker.**  
**Version/build: v4.2 Build 10; no rebuild or corrective build required for this task.**  
**Overall release status: pending / NOT DONE for the separately documented manual/environment evidence.** The automated-test and permanent-archive evidence is complete; no claim is made that the six Windows checks were performed.
