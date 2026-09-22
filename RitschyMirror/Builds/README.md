# RitschyMirror English builds

## Latest: 1.3.2 English — Smooth FPS 1

**[Download the Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-smoothfps1/RitschyMirror-English-Setup-1.3.2-SmoothFPS1.exe)**

- [Successful Windows build and logs](https://github.com/Fireworkstars46/App-Builds/actions/runs/35690996755)
- [GitHub Release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-smoothfps1)
- [Smooth drag and FPS patch source](../Source/smooth_drag_and_fps.py)

Changes beyond the previous Copy Mode build:

- Move the preview window by its title bar **without entering the blocking Windows modal drag loop**. The capture/render thread can continue updating during titlebar dragging. Resize behavior has not been changed.
- Optional **FPS limit**: 30, 60, 120, or unlimited; VSync is a separate setting. Actual achievable FPS is constrained by the display, capture card, preview app, and workload.
- **Low latency** setting to prefer the newest frame from Windows Graphics Capture rather than queue stale frames.
- Newly created **windowed** preview starts on the selected target monitor (HDMI capture display), avoiding initial mirror-in-mirror from previewing the primary display on itself.
- Existing English UI, 8-bit SDR Copy mode, Windows Extend mode, and fallback for DXGI_ERROR_UNSUPPORTED remain available.

Suggested starting settings for a 1920×1080 desktop into a 1280×720 preview: Capture mode = monitor; Source = DISPLAY1; Target = HDMI TO USB; Output mode = windowed; Copy mode = on; FPS limit = 60; Low latency = on; VSync = off if it helps responsiveness (turn on if tearing occurs). Restart (display) after installing or changing structural settings.

This is an **unofficial experimental build**. The installer was compiled and packaged successfully on a Windows GitHub Actions runner, but the actual capture smoothness, live dragging, and FPS were **not tested on the affected laptop**. Low latency can improve freshness without guaranteeing a particular delay. Capture-card preview software can impose its own latency/FPS limitations.

## Earlier builds

- [Copy Mode 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-copymode1/RitschyMirror-English-Setup-1.3.2-CopyMode1.exe)
- [Capture Fix 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-capturefix1/RitschyMirror-English-Setup-1.3.2-CaptureFix1.exe)
- [Initial English version](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2/RitschyMirror-English-Setup-1.3.2.exe)

Installer EXEs are published as GitHub Releases assets and Actions artifacts, rather than committed to Git history.
