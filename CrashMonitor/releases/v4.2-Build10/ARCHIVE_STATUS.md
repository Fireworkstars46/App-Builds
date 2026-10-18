# Crash Monitor v4.2 Build 10 — Archive Status

**Release:** v4.2 Build 10  
**Archive repository:** `Fireworkstars46/App-Builds`  
**Target folder:** `CrashMonitor/releases/v4.2-Build10/`  
**Build increment for archival:** No — archival/metadata does not change the released Build 10 program.

## Verified release evidence

- Static/release audit: **163 PASS / 0 FAIL**.
- Actual Windows Safe Self-Test: **36 PASS / 0 FAIL / 0 SKIPPED / 6 NOT TESTED**.
- Actual Windows Safe Self-Test report is archived in this folder as `CrashMonitor-SafeSelfTest-v4.2-Build10.txt`.
- Release/audit/history text artifacts in this folder were compared by Git blob identity with the local Build 10 files and match exactly.

## Exact release hashes that must be satisfied

- `Crash_Monitor_v4.2_Build_10_Setup.exe`
  - Size: **154624 bytes**
  - SHA-256: `602eb882926073000006baa3a9c2b15f3ad0e514cb4f53d3261b59d6894337a1`
  - Local Git blob SHA: `0969bf410694f5070a6aeb224ac2d39684b2dedf`
- `Crash_Monitor_v4.2_Build_10_Source.zip`
  - Size: **104273 bytes**
  - SHA-256: `7e887d88e6a52d3ff443ec0ef7c15776f97a23a0d942ad0dca95c3213b21333c`
  - Local Git blob SHA: `9bd0e1fbbfe9dca7c725cb0e971ad9c40b339627`
- `CrashMonitor-SafeSelfTest-v4.2-Build10.txt`
  - Size: **6163 bytes**
  - SHA-256: `11cc5c27048d9ef5fde8ff3fb7abe13ce017dfc3e4f3c3a988b316fd2b25a302`
  - Git blob SHA: `1c869800120543cc5e47c57b0afe1c33c67735df`

## Current Section 27 status

**INCOMPLETE — exact installer and source ZIP are still required.**

The available GitHub connector can create UTF-8 files and Git blobs, but it does not expose a direct local-file/binary-upload parameter. A binary transport attempt produced objects whose sizes/blob identities did not match the exact local Build 10 artifacts. Those incorrect copies were removed from the current `main` archive folder rather than being misrepresented as valid release artifacts.

Section 27 must remain incomplete until the exact 154624-byte installer and 104273-byte source ZIP are uploaded under the filenames above and verified against the recorded SHA-256/Git-blob identities. **Do not create Build 11 solely for this archive blocker.**

## Remaining manual/environment checks

1. Actual Update/Repair over an installed older build and user-data preservation.
2. Actual Windows sign-out/reboot proving Start with Windows launches at sign-in.
3. Actual Windows Search indexing/discovery and user-visible shortcut launch.
4. Real HKLM WER enable/disable UAC elevation flow.
5. Physical Explorer.exe/taskbar termination/restart.
6. Bitdefender/SmartScreen reputation result.

**Project status:** Build 10 has no automated Safe Self-Test failures, but permanent Section 27 archival is not yet complete because the two exact binary release artifacts are not yet present on `main`.
