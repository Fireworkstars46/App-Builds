# App Battery List v1.0 Build 6

Canonical source reconstruction: start with archived Build 5 source ZIP from GitHub release, verify its SHA-256 `d5a422e118ad25d7a5b15101df155f985cc3887de02bb7b724514aa335eeeef2`, concatenate `source-patch/app.patch.gz.b64.part*` in numeric order, base64-decode, verify SHA-256 `7adc63967d2ab46ea71f1b552f6d142a30a28dd4401d4c681d5e1dc2957852a9`, gunzip and apply with `patch -p1 --fuzz=0`, then validate every file hash against `SOURCE_SHA256SUMS.txt`.

User-facing behavior: new All Settings Review starts with Notifications, then App Info for relevant Battery, Permissions, Mobile Data checks. Important Only defaults to relevant pages/apps; Review All retains full two-page mode. Old Build 5 review state maintains its App Info-first behavior until restart. No automatic protected settings changes.

Private signing keys/credentials are NEVER stored in this public archive. Release artifacts, source ZIP and verification evidence must be published only after the permanent signing identity is verified.
