# Fast ChatGPT Web v66 Build 18 — Archive Manifest

> Archival metadata created on 2026-10-18. This file is **not** a new app Build and is **not** an original Build 18 release artifact. Version remains **v66** and Build remains **18**.

## Exact artifacts archived in this repository

The following files are byte-for-byte copies of existing Build 18 files that were still available at archival time:

| File | SHA-256 |
| --- | --- |
| `README.txt` | `cb8e5aac2804a562e03e2ba9724755a841862f10bca4e6403d52fec76584d182` |
| `AUDIT-v66-Build-18.txt` | `86c81e53c408c0ffcc72bd162e10b10140eb104faf4f6b79563573c0b390f752` |
| `STATIC-CHECKS-v66-Build-18.txt` | `769ca5fc32cba99a4fa86ea872b53f36ebf05607e3e3bc67721082a8b098678c` |
| `FastChatGPT_WebView_v66_Build_18_Source.sha256.txt` | `acc4cb65fd58abf48635d6fcd622c24019c5a4617b61a5953e2f62bf4c52d102` |
| `BUILD-STAGE.txt` | `5d91cf56c4cd67d078a8831f649deb24e3c552d2e222f42bf058a671edf26d7e` |

`README.txt` is the exact Build 18 README extracted byte-for-byte from the existing source ZIP, so the original Build 18 change notes/history remain preserved without rewriting them.

## Exact artifacts known locally but not committed

These files were still available locally during archival, but were **not** substituted, rebuilt, redacted, or relabeled as exact GitHub artifacts:

| File | SHA-256 | Reason not committed |
| --- | --- | --- |
| `FastChatGPT_WebView_v66_Build_18_Source.zip` | `6aedf0b0327bd50e7ac22c22c45fe51696773332bc7030925ca67d9c2174eb95` | Exact binary ZIP was available, but the current GitHub connector did not provide a reliable direct local-file binary upload path. No reconstructed/repacked ZIP was substituted. |
| `APP-BUILD-LOG.txt` | `bf0605019ccebf79594d72e249d660ed747b947e087f1f4f6821c995f0dcc116` | Contains a local Windows user path; not published to the public repository as an exact log without redaction. Redaction would no longer be exact. |
| `SETUP-BUILD-LOG.txt` | `28ea42af841bd0e0e86c9b0f2ed8146d1c40c5bad36c017bd9844c68b81a0334` | Contains a local Windows user path; not published to the public repository as an exact log without redaction. Redaction would no longer be exact. |
| `app.log` | `561f9668ccc7f0e6132165347c9d2f356aa2f2729d9fd8f94e24dcd9af9d1b0e` | Contains historical ChatGPT conversation/branch URLs and other private runtime navigation history. Not published to the public repository. |
| `debug.log` | `e65fab46536e1fb7680c17f3316e6b6cd24f150fdb3deb9c6492fb2f9335d1cf` | Contains historical ChatGPT conversation/branch URLs and other private runtime navigation history. Not published to the public repository. |

The local runtime logs contained the Build 18 Safe Self-Test result `46 PASS / 0 FAIL / 7 SKIPPED`, but there was no separate standalone exact Safe Self-Test report file available. I did not manufacture one from the logs and label it as historical evidence.

## Missing exact historical release artifacts

The following applicable release artifacts were not available in the current conversation/container and therefore were not reconstructed:

- compiled app EXE/package;
- finished installer `FastChatGPT_WebView_v66_Build_18_Setup.exe`;
- separate standalone Safe Self-Test report/evidence file, apart from the private runtime logs noted above.

## Build identity and status

- Project: **Fast ChatGPT Web**
- Version: **v66**
- Build: **18**
- Build number was **not** incremented for this archive operation.
- Build 18 remains the current known-good DONE build established in the project chat.
- Existing project identity, settings/data paths, IDs, oldest-instance survivor behavior, update compatibility, and Build 18 code/artifacts were not changed by this archival operation.

## Archive status

**INCOMPLETE**

Reason: exact source ZIP and compiled installer/app artifacts are not all present as retrievable GitHub files, and the exact runtime logs were intentionally not published to this public repository because they contain private navigation identifiers. The files listed under “Exact artifacts archived” are preserved byte-for-byte and should be hash-verified after commit.
