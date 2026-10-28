UxPlay Quality Launcher v91o Build 104

Purpose
- Fix first-open/main/settings windows appearing behind other windows when Pin is OFF.
- Use one-shot foreground presentation only: restore/show -> BringToFront -> Activate -> SetForegroundWindow.
- Do NOT set TopMost or change the remembered Pin state.
- Preserve Build 103 USB behavior; Build 104 is not claimed to fix Direct USB mirroring.

Baseline
Exact Build 103 package:
UxPlay_V91O_Build_103_Unsafe_Stack_UsbDk_First.zip
SHA-256:
aee681be857246d8542dc6620bf7a1362f94133e2a610767496392c790d3d15b

Build 103 real USB result
- Auto correctly selected same-backend UsbDk on the Apple-kernel-filter caution stack.
- The 0x40/0x52/index2 activation request returned normally.
- QuickTime subclass 0x2A never appeared during the bounded 45-second fresh-handle wait.
- Build 103 failed before PING/CWPA/video.

Build 104 source package SHA-256
2a8e2bc91d95646c55af37b4525bd57232138338dd31a58710b962e818450607

Build 103 -> Build 104 source patch
Raw patch SHA-256:
cfc0bc1ebb4890e7b3faf4e1fae2b4b649eb0c16711690859b2269429c8aae48
Raw patch size: 195387 bytes

Archive encoding
The raw patch was compressed with xz -9e and base64 encoded, then split into:
source-patch-parts/part00.b64
source-patch-parts/part01.b64
source-patch-parts/part02.b64

Concatenated xz/base64 SHA-256:
6cf5b7d8d4ac9390efdd972bce58385c988826afb0c37b8467a0afa270d0af38
Concatenated size: 43496 bytes

Part SHA-256 values
part00.b64  7ab458e67322c5631c6627d4718d0b5960892901634af22fafec547fb880021a  16000 bytes
part01.b64  dcad2e3781469a61cf651b1aaeb2b11ce4f6a78e949c3028af3ef99b11c467d6  16000 bytes
part02.b64  4ebd4aa0ac04dc45d52832eb8b3d9e23d6f6746507471f88a8dd2768709b12c3  11496 bytes

Reconstruction
1. Start from the exact Build 103 ZIP hash above and extract it.
2. Concatenate part00.b64 + part01.b64 + part02.b64 in lexical order with no separators.
3. Verify the concatenated file SHA-256 is 6cf5b7d8d4ac9390efdd972bce58385c988826afb0c37b8467a0afa270d0af38.
4. Base64-decode the concatenated data to an .xz stream.
5. XZ-decompress to UxPlay_Build103_to_Build104_SOURCE.patch.
6. Verify raw patch SHA-256 cfc0bc1ebb4890e7b3faf4e1fae2b4b649eb0c16711690859b2269429c8aae48.
7. Apply the patch to the exact Build 103 source tree.

Validation status
- Static audit: 94/94 PASS.
- Python backend syntax: PASS.
- ZIP integrity: PASS.
- Windows C# compile: NOT TESTED for Build 104 in the current environment.
- Real Windows foreground/z-order behavior: NOT TESTED until user validation.
- Real iPhone Direct USB capture: intentionally unchanged from Build 103 and NOT claimed fixed.
