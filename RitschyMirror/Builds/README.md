# RitschyMirror English builds

## Latest: English 1.3.2 — Native Window 1

**[Download the Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-nativewindow1/RitschyMirror-English-Setup-1.3.2-NativeWindow1.exe)**

- [GitHub Release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-nativewindow1)
- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35802668373)
- [Source patch](../Source/native_window_main_preview.py)

### Changes

- Preview opens on **Main display** respects the setting; it is no longer forcibly relocated to HDMI. Choose **Extended display** to make the HDMI-to-USB capture card see the RitschyMirror preview. With only the preview window on Main, the alt laptop's HDMI capture stream cannot also see that window (the HDMI output is a different monitor).
- **Preview window movement** setting: **Normal Windows (browser-like)** (new default) uses the real system titlebar and window border mechanics, including dragging across displays and Windows Snap. **Smooth live drag** uses the earlier non-blocking custom movement logic instead.
- The previous **Keep preview inside one display** setting affects **Smooth live drag** only and does not stop cross-display movement in Normal Windows mode; default is now off for new configurations.
- On Windows versions supporting `WDA_EXCLUDEFROMCAPTURE`, RitschyMirror requests exclusion of its own preview window from Windows Graphics Capture, to prevent mirror-in-mirror loops when that window is on the captured source screen. If Windows refuses exclusion, the log warns. Other capture tools may not honor the Windows exclusion.
- Native OS drag/resize can momentarily pause the preview while a mouse button is held because the renderer and native window's message loop use the same thread. Release the mouse button to resume; use Smooth live drag if uninterrupted preview rendering during movement matters more than native window snapping.
- Keeps the 80-byte Direct3D constant-buffer alignment fix, optional SDR auto clarity, debug logs and Open log folder button, remembered window dimensions and positions, and Extend mode support.

### Test

1. Close RitschyMirror fully (including system tray icon), install Native Window 1 over the old English build (no manual uninstall).
2. Open Settings → **Preview opens on: Main display**, set **Preview window movement: Normal Windows (browser-like)**, and leave **Keep preview inside one display** off if using Smooth live drag later. Restart the preview.
3. Drag the preview's titlebar or use a window edge as in a normal browser, including across Windows displays. The setting changes how preview moves, not Windows display topology.
4. For the physical HDMI capture card on the alt laptop to show the preview, place the preview onto **HDMI TO USB** (or select Extended display at startup).
5. If the app freezes or repeats itself, open Settings → About → Open debug log folder and share the latest `mirror.log` section. The Windows build compiled successfully but the end-to-end behavior on this specific laptop and capture card still requires testing.

## Previous builds

- [Debug Fix 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debugfix1)
- [Debug 1 (contains the pre-fix shader buffer size bug)](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debug1)
- [Preview Select 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-previewselect1)
