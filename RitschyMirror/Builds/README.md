# RitschyMirror English builds

## Latest: 1.3.2 English — Preview Select 1

**[Download the Windows setup EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-previewselect1/RitschyMirror-English-Setup-1.3.2-PreviewSelect1.exe)**

- [Successful Windows build and packaging log](https://github.com/Fireworkstars46/App-Builds/actions/runs/35695801233)
- [Release page](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-previewselect1)
- [Preview startup display source patch](../Source/preview_start_display.py)

### New preview startup location setting

In **Settings → Source / Target & Mode → Preview opens on**, select one of:

- **Main display**: opens the windowed preview on the Windows primary screen.
- **Extended display**: opens the preview on the selected Target monitor (e.g., HDMI TO USB).
- **Remember last position** (default): opens at the last saved location, falling back to the selected Target if no valid saved position exists.

The option changes *window placement only*, not Windows Extend mode, capture source, or target selection. The custom preview size and maximize/restore state continue to be saved. Changes take effect the next time you click **Restart (display)** or relaunch the preview. Opening the whole-desktop preview on the screen being captured can produce a mirror-in-mirror recursion until the window is moved off that screen.

Earlier changes remain available: SDR Copy mode, Windows Graphics Capture fallback, adjustable FPS, lower-latency newest-frame capture, custom window sizing, persistent geometry, and nonblocking drag/resizing.

**Testing:** The code compiled and the setup EXE was packaged successfully on a GitHub Actions Windows runner. Actual placement, window behavior, live FPS and capture-card output have not yet been tested on the user's Windows laptop. This is an unofficial experimental build.

## Earlier builds

- [Resize Save 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-resizesave1/RitschyMirror-English-Setup-1.3.2-ResizeSave1.exe)
- [Smooth FPS 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-smoothfps1/RitschyMirror-English-Setup-1.3.2-SmoothFPS1.exe)
- [Copy Mode 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-copymode1/RitschyMirror-English-Setup-1.3.2-CopyMode1.exe)

Installer EXEs live in GitHub Releases and Actions artifacts and are linked from this folder; they are not committed to Git source history.
