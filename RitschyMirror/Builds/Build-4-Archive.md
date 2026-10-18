# RitschyMirror 1.3.2 Build 4 — Archive Manifest

This is archival metadata for the already-existing **RitschyMirror 1.3.2 Build 4** release. It does **not** create a new Build and does not alter the application binaries, source archive, settings, IDs, install path, updater identity, signing state, or release tag.

## Canonical release

- Version: **1.3.2**
- Build: **4**
- Tag: `ritschymirror-english-1.3.2-build4-masterrules`
- Release: https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-build4-masterrules
- Release target commit: `2b0913b78552fc3c956b4efb38a6031de34ce707`
- Successful producing workflow: https://github.com/Fireworkstars46/App-Builds/actions/runs/39024854359
- Published: 2026-10-17T10:28:15Z

## Exact archived release assets

All of the following are the exact Build 4 release assets already published on GitHub. SHA-256 values are the digests reported by GitHub for the release assets and were independently matched against the exact local copies retained from the successful Build 4 workflow.

| Artifact | SHA-256 |
| --- | --- |
| [RitschyMirror-English-Setup-1.3.2-Build4-MasterRules.exe](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-English-Setup-1.3.2-Build4-MasterRules.exe) | `e968c207e07dba018d5dd285ded5142c3016a831725454536afd985f0445ae67` |
| [RitschyMirror-1.3.2-Build4-MasterRules-Source.zip](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-MasterRules-Source.zip) | `abd1fa99b8e823277534fa7a57fca94eeba6ec2e531e6b77fb70d73717c006e7` |
| [RitschyMirror-1.3.2-Build4-MasterRules-Audit.txt](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-MasterRules-Audit.txt) | `d0b8940913bda74a6eca3db9b11340b60450f466fe0bee90d9973c1fdd2f4123` |
| [RitschyMirror-1.3.2-Build4-Safe-Self-Test-CI.txt](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-Safe-Self-Test-CI.txt) | `8ba4d45f7816b0039bb36dca02b2350d8756488ac3cd5499eda24453bb82497b` |
| [RitschyMirror-1.3.2-Build4-AV-Safety-Audit.txt](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-AV-Safety-Audit.txt) | `6e740a595c3d74e49e9ecf059330e0bedec65eaae8d54c1ce36c37e467a91644` |
| [RitschyMirror-1.3.2-Build4-Verification-Summary.txt](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-Verification-Summary.txt) | `993fc9cced0ef8b82ee6e6338d448dd9229676ac7fa71d850f73304d1897fbcb` |
| [RitschyMirror-1.3.2-Build4-SHA256.txt](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-build4-masterrules/RitschyMirror-1.3.2-Build4-SHA256.txt) | `700390260df48a65df5115fc410325998acb21f886d451c35f17b4f294339ee5` |

There was no separate portable EXE/package in this Build 4 release; the installer EXE above is the applicable executable release artifact.

## Release notes / history

Build 4 was the corrective release required by the then-current `MASTER_RULES.md` audit. It intentionally preserved the existing mirroring/rendering behavior, AppId, install path, single-instance design, `app_settings.json`, `mirror_config.json`, logs/data, shortcuts, startup identity, tray/taskbar behavior, and Build 3 update compatibility.

The release corrected audit/test gaps around atomic settings writes, early single-instance restore signaling, single-vs-double tray-click arbitration, shared duplicate-setting production setters, Settings window geometry/off-screen recovery/reset, close-decision behavior, and broader production-path Safe Self-Test coverage with individual PASS/FAIL/SKIPPED reporting. Multi-instance stale-writer/runtime-mode requirements remained not applicable because RitschyMirror intentionally stayed single-instance.

The producing Windows workflow compiled with warnings treated as errors, tested a real Build 3 -> Build 4 in-place update with byte-exact config preservation, ran the installed Safe Self-Test, verified shortcut/startup choices, and verified data-preserving uninstall. No AV exclusions were added. Real GPU/capture hardware, physical Explorer tray behavior, and SmartScreen/Bitdefender reputation remained manual/interactive checks.

## Archive verification

- GitHub release ID: `415738619`
- Every listed release asset currently reports GitHub state `uploaded` and exposes its release download URL.
- The successful GitHub Actions workflow run `39024854359` completed with conclusion `success` at commit `2b0913b78552fc3c956b4efb38a6031de34ce707`.
- GitHub Actions artifact `RitschyMirror-1.3.2-Build4-MasterRules` (artifact ID `12097918272`) was successfully retrieved during archive verification and had GitHub-reported digest `sha256:fc6c9d9880d06277ba880b3c15fab06715eb52e6f02b87d3ca3604ad08b0c495`.
- SHA-256 of each exact Build 4 file matched the corresponding GitHub release-asset digest listed above.
- The archived `RitschyMirror-1.3.2-Build4-SHA256.txt` file also contains the expected hashes for the installer, source ZIP, AV audit, MASTER_RULES audit, Safe Self-Test report, and verification summary.
- Release notes are retained on the GitHub Release itself and summarized here so the release history remains discoverable from the repository tree.

## Archive status

**COMPLETE / verified**
