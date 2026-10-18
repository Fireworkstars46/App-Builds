# Crash Monitor v4.2 Build 12 — Archive Status

## Section 27: COMPLETE

Verified 2026-10-18 against the current authoritative MASTER_RULES.md, Git blob `8dfded979df65ded2f84757cf8a678c664225186`.

Destination: `Fireworkstars46/App-Builds/CrashMonitor/releases/v4.2-Build12/` on `main`.

The exact original installer, source ZIP, actual Windows runtime report, and original release evidence are permanently archived. All 39 artifact/evidence paths were retrieved from immutable artifact commit `2bded51901702ad8c4791cff24fc6539ad916dd9`, decoded, compared byte for byte with the originals, and independently checked for byte size, SHA-256, and Git blob identity.

## Exact artifacts verified after retrieval

| File | Verified bytes | Verified SHA-256 |
| --- | ---: | --- |
| `Crash_Monitor_v4.2_Build_12_Setup.exe` | 162,304 | `50b4f02cb7340bd938d9261966f27b1d4f2e48311a98428a466b7f96469ad8c7` |
| `Crash_Monitor_v4.2_Build_12_Source.zip` | 106,334 | `70105e60904373c2725ed7a820195ea103a6182f1e8e59cc60a404572b68a5ed` |
| `CrashMonitor-SafeSelfTest-v4.2-Build12.txt` | 6,911 | `6a2447fd995fdc1c6991ed419b8370816cde11270ad7e04a2803645486b38b45` |

The installer SHA-256 matches the expected original Build 12 release hash. The source ZIP passed its CRC/integrity test; every file under `source/` matches the corresponding ZIP member exactly. The ZIP was not repackaged, and no program, source, or original release-document bytes were changed.

Detailed retrieval results for all 39 paths are in [ARCHIVAL_VERIFICATION_v4.2_Build_12.json](ARCHIVAL_VERIFICATION_v4.2_Build_12.json). [SHA256SUMS_v4.2_Build_12.txt](SHA256SUMS_v4.2_Build_12.txt) records hashes for the released artifacts and original evidence; the checksum file and newly added archive metadata are excluded from that manifest.

## Original evidence preserved

- Full original source ZIP and browsable exact source/build resources in `source/`.
- Build instructions, static/release summary, and all individual static results.
- Actual Windows Safe Self-Test report, separate from the preserved pre-runtime Safe Self-Test note.
- Release notes, regression evidence, master-rules audit, AV/safety audit, warnings, and safe recovery metadata.
- Existing historical archives: all 24 older Crash Monitor files remain unchanged. All 97 previously existing repository files were unchanged in the artifact commit; this completion step updates only the Build 12 archive status and adds its verification record.

Some original release documents state that runtime execution was pending when they were written. Those historical documents remain byte-for-byte intact; the later actual Windows report and this archive status supersede those pending-runtime statements.

## Validation evidence

- Project/version: **Crash Monitor v4.2 Build 12**.
- Original static/release evidence: **174 PASS / 0 FAIL**.
- Original compiler evidence: **0 warnings / 0 errors**.
- Actual supplied Windows Safe Self-Test: **39 PASS / 0 FAIL / 0 SKIPPED / 4 NOT TESTED**, ending with `SAFE SELF-TEST FINISHED`.
- Runtime coverage includes physical Explorer/taskbar restart and tray recovery, a real temporary Start Menu shortcut launch, and staged Update/Repair image replacement with isolated user-data preservation.
- The staged Update/Repair check is not relabeled as a full installed upgrade test.
- No recompilation, new Windows test run, rebuild, or artifact revision was performed during archival. No independent monitor.log file was supplied in this archival session; no additional log or process-exit claim is made.

## Four environment-owned checks remain NOT TESTED

1. **Real Windows sign-out/reboot startup:** requires an actual session transition; isolated startup-registration checks cannot prove the next sign-in behavior.
2. **Windows Search indexing/discovery timing:** depends on the asynchronous indexer; the successful actual shortcut launch does not prove indexing.
3. **Actual HKLM WER UAC approval/elevation:** requires real Windows consent and the applicable elevated environment; isolated registry-engine checks do not prove consent interaction.
4. **Bitdefender/SmartScreen reputation:** depends on external security products and reputation services; static/local tests cannot establish it. The established unsigned executable state is unchanged.

None is converted to PASS. These justified environment-owned exclusions are documented under MASTER_RULES sections 15 and 23. No further user-run tests are requested to complete this archival task.

## Final release status

**Section 27: COMPLETE.**

**Release: DONE for the applicable static, safely testable runtime, and permanent-archive requirements, with the four justified environment-owned checks above remaining NOT TESTED.** This is not a claim that those four checks passed.

Version remains **v4.2 Build 12**. No Build 13 was needed or created. There are no remaining archive blockers or user GitHub upload steps. A subsequently confirmed regression would reopen the release under the normal corrective-build rule.
