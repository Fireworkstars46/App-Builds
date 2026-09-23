# RitschyMirror English builds

## Latest: RitschyMirror English 1.3.2 — Debug 1

**[Download the Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-debug1/RitschyMirror-English-Setup-1.3.2-Debug1.exe)**

- [Successful Windows build and installer packaging](https://github.com/Fireworkstars46/App-Builds/actions/runs/35800732553)
- [Release page](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debug1)
- [Diagnostic patch source](../Source/debug_capture_freezes.py)

### New debugging tools

- **Debug logging (FPS, stalls and repeated-screen detection)**: Enabled by default for the debug build, with an on/off checkbox in the image settings.
- **Open debug log folder**: A button under Settings → About opens the folder containing `mirror.log`. After reproducing a freeze, close mirroring if possible, then open the log and share its most recent lines.
- **Recursive mirror warning**: When the preview window overlaps the captured source display at startup, the log prints `RECURSIVE MIRROR WARNING`. Another warning identifies source and target being the same display.
- **Render stall watchdog**: A separate background thread records `RENDER STALL` if the rendering loop makes no progress for at least four seconds, including the last recorded stage (window pump, capture acquire, GPU render, present, etc.). Warning repeats at most once per five seconds.
- **Low-frequency diagnostics**: Approximate presented FPS, new captured frames per second, source and preview dimensions, window state and startup capture/preview display selections. No screenshots or videos are recorded by these diagnostics.
- Existing features remain: SDR Copy mode, optional automatic clarity, optional screen-edge confinement, preview opens on Main/Extended/Remember, custom window sizing and maximize/restore, FPS limit and low latency.

### Steps for the freeze / mirror-in-mirror issue

1. Quit RitschyMirror completely from its tray icon; install Debug 1 over the previous English build. Your existing `mirror_config.json` should remain in place.
2. Open Settings; ensure **Debug logging** is checked. Keep Windows set to **Extend**. For the test set Capture mode = monitor, Source monitor = the MAIN desktop, Target monitor = HDMI TO USB, and Preview opens on = Extended display. Keep the preview on the HDMI target, **not** on the captured main screen.
3. Start mirroring and briefly reproduce the glitch once. If it freezes, wait about five seconds so the independent watchdog can attempt to record the blocked stage, then end RitschyMirror using Task Manager if necessary.
4. Open Settings → About → **Open debug log folder**. Open `mirror.log` and send the lines from the latest Render-Start through the failure. The older lines from prior versions will still be in the log. Review the log before sharing since earlier versions can log app/window titles and local paths.

**Limitations:** Debug 1 adds diagnostics, not an automatic fix for freezes, recursive mirroring or capture-card image quality. Windows GitHub Actions compiled and packaged the EXE successfully, but the debugger's runtime behavior on the user's laptop has not been tested.

## Previous builds

- [Auto Clarity & Edges 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-clarityedges1/RitschyMirror-English-Setup-1.3.2-ClarityEdges1.exe)
- [Preview Select 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-previewselect1/RitschyMirror-English-Setup-1.3.2-PreviewSelect1.exe)

Installers are published as GitHub Release assets and Actions artifacts, not committed to the source history.
