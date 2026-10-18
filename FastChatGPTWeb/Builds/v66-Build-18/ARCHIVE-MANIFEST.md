# Fast ChatGPT Web v66 Build 18 — Archive Manifest

> Archival metadata created on 2026-10-18 and updated after the exact Build 18 source ZIP, installer EXE, standalone app EXE, and runtime logs were recovered. This file is **not** a new app Build and is **not** an original Build 18 release artifact. Version remains **v66** and Build remains **18**.

## Exact artifacts archived in this repository

The following files are byte-for-byte copies of existing Build 18 files that were available at archival time:

| File | SHA-256 |
| --- | --- |
| `README.txt` | `cb8e5aac2804a562e03e2ba9724755a841862f10bca4e6403d52fec76584d182` |
| `AUDIT-v66-Build-18.txt` | `86c81e53c408c0ffcc72bd162e10b10140eb104faf4f6b79563573c0b390f752` |
| `STATIC-CHECKS-v66-Build-18.txt` | `769ca5fc32cba99a4fa86ea872b53f36ebf05607e3e3bc67721082a8b098678c` |
| `FastChatGPT_WebView_v66_Build_18_Source.sha256.txt` | `acc4cb65fd58abf48635d6fcd622c24019c5a4617b61a5953e2f62bf4c52d102` |
| `BUILD-STAGE.txt` | `5d91cf56c4cd67d078a8831f649deb24e3c552d2e222f42bf058a671edf26d7e` |

`README.txt` is the exact Build 18 README extracted byte-for-byte from the existing source ZIP, so the original Build 18 change notes/history remain preserved without rewriting them.

## Exact recovered Build 18 binaries/source

The following exact files were recovered from the Build 18 release and verified locally during archival:

| File | Size | SHA-256 | Identity/integrity verification |
| --- | ---: | --- | --- |
| `FastChatGPT_WebView_v66_Build_18_Source.zip` | 214,748 bytes | `6aedf0b0327bd50e7ac22c22c45fe51696773332bc7030925ca67d9c2174eb95` | Matches the previously archived Build 18 source checksum exactly; ZIP integrity test passed with no bad entries. |
| `FastChatGPT_WebView_v66_Build_18_Setup.exe` | 234,102,403 bytes | `bb2fe8db82508b353f0b7bbeece1a004d4202b00aaa1aac76e291c4dc5776988` | Valid x64 PE; embedded version strings include `66.0.0.18`, `66 Build 18`, and `Fast ChatGPT Web Setup`. |
| `FastChatGPTWebFinal.exe` | 72,213,017 bytes | `b3dff53c33a6d9b2e8b47462f73bc2367e1db86280a7799d129f325ea84f8848` | Valid x64 PE; embedded version strings include `66.0.0.18` and `66 Build 18`. |

These exact files are now published as assets on [Fast ChatGPT Web v66 Build 18](https://github.com/Fireworkstars46/App-Builds/releases/tag/fastchatgptweb-v66-build18). Each public GitHub copy was independently downloaded after publication on 2026-10-18 and verified against the original file's byte count and SHA-256 above. All three match exactly. No source, executable, installer, or Build number was changed.

## Safe Self-Test evidence

The exact recovered runtime logs were inspected locally:

| File | SHA-256 | Publication status |
| --- | --- | --- |
| `app.log` | `c817234cc0933de61bef76014bad44df9fc2a32e2446ccaa4a91b42ef1f68bed` | Not published verbatim because it contains private ChatGPT navigation/conversation identifiers. |
| `debug.log` | `b6212659ce8ddde28669809c77f6e61c75e06773d0f55158985d5eeb38d2ffad` | Not published verbatim because it contains private runtime/navigation history. |

The exact Build 18 result present in the recovered `app.log` is:

`2026-10-17 05:17:21.505 [v66 Build 18] [TEST] Safe Self-Test completed: PASS; passed=46; failed=0; skipped=7.`

No Build 18 `[ERROR]` or `[WARN]` log entries were found in the supplied Build 18 runtime logs during archival verification.

`SAFE-SELF-TEST-ARCHIVE-EVIDENCE.md` in this directory records that verification. It is clearly archival metadata derived from the exact recovered logs, not a fabricated or relabeled original historical report.

## Exact historical files intentionally not published

The original runtime logs are retained as exact recovered evidence but are not suitable for this public repository because they contain private navigation/conversation identifiers. Earlier build/setup logs also contained local Windows user paths. Redacting any of those files would change their bytes, so no redacted file is presented as an exact historical artifact.

## Build identity and status

- Project: **Fast ChatGPT Web**
- Version: **v66**
- Build: **18**
- Build number was **not** incremented for this archive operation.
- Build 18 remains the current known-good DONE build established in the project chat.
- Existing project identity, settings/data paths, IDs, oldest-instance survivor behavior, update compatibility, and Build 18 code/artifacts were not changed by this archival operation.

## Archive status

**COMPLETE / verified — 2026-10-18**

- Release: [Fast ChatGPT Web v66 Build 18](https://github.com/Fireworkstars46/App-Builds/releases/tag/fastchatgptweb-v66-build18)
- Tag: `fastchatgptweb-v66-build18`
- GitHub Release ID: `416328813`
- App status: **DONE**, retained from the established historical Build 18 validation.
- Version remains **v66**; Build remains **18**. This operation only archives and verifies existing artifacts.

### Verified GitHub Release assets

| Exact artifact | GitHub asset ID | Downloaded bytes | SHA-256 | Result |
| --- | ---: | ---: | --- | --- |
| [FastChatGPT_WebView_v66_Build_18_Source.zip](https://github.com/Fireworkstars46/App-Builds/releases/download/fastchatgptweb-v66-build18/FastChatGPT_WebView_v66_Build_18_Source.zip) | 652944456 | 214,748 | `6aedf0b0327bd50e7ac22c22c45fe51696773332bc7030925ca67d9c2174eb95` | **MATCH** |
| [FastChatGPT_WebView_v66_Build_18_Setup.exe](https://github.com/Fireworkstars46/App-Builds/releases/download/fastchatgptweb-v66-build18/FastChatGPT_WebView_v66_Build_18_Setup.exe) | 652944477 | 234,102,403 | `bb2fe8db82508b353f0b7bbeece1a004d4202b00aaa1aac76e291c4dc5776988` | **MATCH** |
| [FastChatGPTWebFinal.exe](https://github.com/Fireworkstars46/App-Builds/releases/download/fastchatgptweb-v66-build18/FastChatGPTWebFinal.exe) | 652944685 | 72,213,017 | `b3dff53c33a6d9b2e8b47462f73bc2367e1db86280a7799d129f325ea84f8848` | **MATCH** |

### Verification performed

1. The three supplied original files matched the historical Build 18 checksums recorded above. The original source ZIP passed its archive integrity check.
2. GitHub confirmed that this release is published and each named asset is in the `uploaded` state. GitHub's reported SHA-256 digest for each asset matches its original.
3. Each asset was independently downloaded in full from its public GitHub Release download URL. All three returned HTTP **200**. The downloaded byte counts and independently computed SHA-256 hashes match the originals exactly.
4. The five existing historical repository files in the first table were re-fetched and their SHA-256 hashes match that table. The README, audit, and static-check report also match the corresponding entries in the exact original source ZIP byte-for-byte.
5. The existing archival metadata files were re-fetched successfully:
   - `SAFE-SELF-TEST-ARCHIVE-EVIDENCE.md`: SHA-256 `30729f78c2043b6093479c73f6746c7f95ddcd2ddee95edf9cabe5fd346dad85`.
   - `RECOVERED-ARTIFACTS-SHA256.txt`: SHA-256 `d0479d20baa4fde0651249bd1d31bbf8cf7695e6a1193d75640f934c5bbc284b`.
6. Historical validation remains **113 static PASS / 0 FAIL** and **46 Safe Self-Test PASS / 0 FAIL / 7 justified SKIPPED**. No rebuild, new static audit, or new Windows runtime test was performed or claimed for this archival operation.
7. Private runtime/navigation logs remain intentionally unpublished; the existing privacy-safe historical evidence above is preserved.

GitHub's automatically generated “Source code” downloads are repository snapshots at the archival tag. The exact original Build 18 source is the specifically named `FastChatGPT_WebView_v66_Build_18_Source.zip` release asset linked above.

No required public release artifact remains missing from this archive.
