# RitschyMirror English builds

## Latest: 1.3.2 English — Resize Save 1

**[Download the ready-to-install Windows setup EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-resizesave1/RitschyMirror-English-Setup-1.3.2-ResizeSave1.exe)**

- [GitHub Release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-resizesave1)
- [Successful Windows compile, installer packaging and workflow log](https://github.com/Fireworkstars46/App-Builds/actions/runs/35695295849)
- [New custom preview resizing patch](../Source/persistent_resizable_preview.py)

### Changes

- Drag any preview window edge or corner to adjust its size. The app processes the movement and resize without entering the default blocking Windows modal move/size loop; on-screen output is intended to keep updating during the gesture.
- Preview renderer resizes its D3D11 swap-chain buffer to the **actual client area** when the window is resized, maximized or restored. Maximized output no longer stretches the old 1280x720 back buffer; this can improve text clarity.
- Clicking **maximize** fills the monitor; clicking **restore** returns to the precise previous *normal window* size and location.
- Save the custom non-maximized size, location and maximized state in the existing mirror_config.json. Reopen/restart and the preview returns to its previous dimensions and maximized/restored state when the selected output is windowed. If the saved preview is offscreen after changing monitor topology, it starts on the selected target monitor instead.
- Existing monitor capture fallback, English interface, Copy mode, target-display placement, adjustable FPS and low-latency controls remain.

### How to use

1. Close RitschyMirror completely; install the latest EXE; open Settings.
2. Keep Capture mode = monitor, Source = DISPLAY1, Target = HDMI TO USB, Output mode = windowed, Copy mode = on, and FPS limit = 60 for a first test.
3. Click Start / Stop; the preview should appear on the extended HDMI target screen. Drag a border/corner to any size you like. Click maximize and restore, then restart RitschyMirror to test remembering the size.
4. VSync off may reduce latency but can create tearing; turn it on if you notice that. Actual smoothness/FPS is still constrained by your HDMI capture card and the Camera/Camera HD preview app on the other laptop.

**Testing status:** The patched application **compiled** and the installer was **packaged successfully on Windows GitHub Actions**. The resizing, custom size persistence and end-to-end video smoothness have **not been tested on your laptop**; this is an unofficial experimental build, not guaranteed to match OBS frame timing, presentation latency, Windows snap behavior or capture-card preview performance.

## Earlier builds

- [Smooth FPS 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-smoothfps1/RitschyMirror-English-Setup-1.3.2-SmoothFPS1.exe)
- [Copy Mode 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-copymode1/RitschyMirror-English-Setup-1.3.2-CopyMode1.exe)
- [Capture Fix 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-capturefix1/RitschyMirror-English-Setup-1.3.2-CaptureFix1.exe)

Installer EXEs are published as GitHub Releases assets and Actions artifacts, rather than committed to source Git history.
