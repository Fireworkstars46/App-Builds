# RitschyMirror English builds

## Latest: English 1.3.2 — Debug Fix 1

**[Download the fixed Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-debugfix1/RitschyMirror-English-Setup-1.3.2-DebugFix1.exe)**

- [Build / release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debugfix1)
- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35801578377)
- [Source of the two startup corrections](../Source/fix_debug_startup.py)

### Why the prior Auto Clarity and Debug builds failed on startup

The new auto-clarity parameter made the Direct3D constant-buffer C# struct 72 bytes long. D3D11 constant buffer byte sizes must be divisible by 16; the driver rejected 72 with E_INVALIDARG at CreateBuffer. Debug Fix 1 adds 8 bytes of padding to make the buffer 80 bytes. Merely disabling Auto Clarity does *not* change the original broken buffer size; install this fixed build to test.

The user's diagnostics also revealed preview_open_on=main even though the main display was the captured SOURCE. Debug Fix 1 moves the preview to the selected HDMI target automatically when its startup rectangle would overlap the captured source display, preventing the common recursive mirror-at-startup feedback. The selectable Preview opens on setting is preserved for non-overlapping window placement.

### Test

1. Fully close RitschyMirror (including tray), install Debug Fix 1 **over** the previous English build. Existing settings should be preserved.
2. Open Settings. Keep Windows on **Extend**, Capture mode **monitor**, Source = main internal display, Target = HDMI TO USB, Preview opens on = **Extended display**. Keep **Debug logging** enabled. You may first test with Auto Clarity OFF for minimal variables.
3. Start mirroring once. The preview should open on HDMI rather than the captured source. If the preview is black, frozen or recursively repeats, close the application, open Settings → About → Open debug log folder, and send the newest `mirror.log` section.
4. This build has passed compilation and installer packaging on Windows, but physical monitor, capture-card and preview behavior remain unverified on the target machine.

## Previous builds

- [Debug 1 (contains the 72-byte startup bug)](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debug1)
- [Auto Clarity & Edges 1 (contains the same bug)](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-clarityedges1)
- [Preview Select 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-previewselect1)

