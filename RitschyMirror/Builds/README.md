# RitschyMirror English builds

## Latest: English 1.3.2 — Live Snap 1

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-livesnap1/RitschyMirror-English-Setup-1.3.2-LiveSnap1.exe)**

- [Successful Windows build and installer publication](https://github.com/Fireworkstars46/App-Builds/actions/runs/35809793131)
- [Live snap/restore source patch](../Source/live_browser_snap_restore.py)

This build adds browser-style **drag to top edge to maximize** and **drag a maximized title bar down to restore its last small size** to the existing **Smooth live drag** mode. It also constrains window movement to the combined desktop edges without locking the window to one monitor (when Keep preview inside one display is OFF). This is custom nonblocking snapping, not full Windows Aero Snap parity. It preserves the live recursive projector, selectable FPS, Lightshot screenshot visibility and standard title bar when Borderless projector is OFF.

### Test

1. Close RitschyMirror and its tray icon. Install Live Snap 1 over Projector FPS 1. No uninstall is needed.
2. Settings → Output mode: Windowed; Preview style: Recursive projector (OBS-style); Borderless projector: OFF; Preview window movement: Smooth live drag; Keep preview inside one display: OFF. Restart preview.
3. Drag the title bar to the upper physical screen edge and release to maximize, then drag the maximized title bar downward to restore the prior size. Drag to the edge of the combined desktop; it should remain reachable on-screen and still allow crossing to an adjacent display.
4. The continuous preview and this specific monitor layout have not been tested on the user's own laptop; send a screenshot or newest mirror.log section if the movement or capture is incorrect.

## Previous: Projector FPS 1

[Previous installer release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-projectorfps1)

## Projector FPS 1 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-projectorfps1/RitschyMirror-English-Setup-1.3.2-ProjectorFPS1.exe)**

[Successful Windows build and release](https://github.com/Fireworkstars46/App-Builds/actions/runs/35808097520).

This revision removes the projector-only 30 FPS cap. Projector mode now respects Settings → FPS limit: **30, 60, 120, or unlimited**, exactly as normal preview does. It retains the single-window recursive tunnel, optional borderless projector, Lightshot screenshot visibility, smooth live drag, and Windows Extend support. The FPS selection is a target/upper cap, not a guarantee of achieved FPS. Unlimited can increase GPU load and worsen lag during continuous live resizing.

### Installation and test

Close RitschyMirror completely including its tray icon, install Projector FPS 1 over the previous build, and choose Settings → FPS limit → **60** first. Keep **Preview style → Recursive projector (OBS-style)** and **Preview window movement → Smooth live drag** for the same visual effect with live resizing. If 60 FPS is fluid, test 120 FPS or unlimited; if it gets worse, lower the limit. No Windows display duplication is needed. The Windows build completed successfully, but live performance on the user's own laptop and capture card remains unverified.

## Previous build: Projector 1 (forced 30 FPS cap)

[Projector 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-projector1)

## Projector 1 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-projector1/RitschyMirror-English-Setup-1.3.2-Projector1.exe)**

- [GitHub release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-projector1)
- [Successful Windows compile and installer packaging](https://github.com/Fireworkstars46/App-Builds/actions/runs/35805309888)
- [Projector feature source](../Source/recursive_projector_mode.py)

### Projector 1 features

A new **Preview style** setting offers *Normal preview* or *Recursive projector (OBS-style)*. Projector mode uses the same existing Win32 preview window, not additional preview HWNDs. When the preview is on its captured monitor and Windows capture exclusion is off, screen feedback repeatedly depicts that same window, producing an image tunnel. The exact feedback pattern depends on placement, scaling, and frame pacing and cannot be promised to have a particular spiral geometry.

**Borderless projector (no repeating title bars)** is an independent setting enabled by default. When projector mode is on, the preview has a borderless window surface so the nested captured images do not show a repeated title bar. Move the window by dragging the interior; resize near the first nine physical pixels of an edge or corner, or turn the borderless option off to get the normal Windows window controls. Press Alt+F4 or Escape to close the borderless preview. The app tray/settings remain available. Normal preview preserves the previous native browser-like window behavior.

Projector mode is visible to Lightshot because it disables preview capture exclusion while active, regardless of the normal *Hide preview from screenshots* setting; toggling screenshot hiding has no effect until returning to Normal preview. Recursive feedback can consume substantial GPU/CPU; projector mode caps its software frame limiter at 30 FPS. Normal mode respects the existing FPS selector. Windows remains on **Extend**, not Duplicate.

### Test on the main laptop

1. Fully close RitschyMirror including its tray icon, then install Projector 1 over your previous English build. No manual uninstall is needed; existing config should remain.
2. Settings: Capture mode = **monitor**, Source = **Main** internal display, Target = **HDMI TO USB**; Output mode = **windowed**; Preview opens on = **Main display**.
3. Choose Preview style = **Recursive projector (OBS-style)** and select **Borderless projector** to remove title bars. Apply via the existing **Restart (structural)** button or stop/start mirroring.
4. Make the preview smaller than the physical screen and position it off-center to see a clear recursive tunnel. A fullscreen window covering the same captured display can eliminate the visible inset/tunnel effect. Press Lightshot's capture key to test screenshot visibility.
5. If you need the *alt* laptop's camera app to show the mirrored output instead, move the preview onto the **HDMI TO USB** target/extended display. The window on main by itself does not generate video content on the extended output; Windows Extend keeps the screens distinct. Feedback may stop after you move the preview off the captured Main display.
6. If any frame stalls or unexpectedly multiple OS windows appear, open Settings → About → Open debug log folder and share the latest `mirror.log` section. Build/publish passed on GitHub Actions, but the actual screen feedback/dragging has not yet been validated on the user's laptop.

### Prior builds

- [Lightshot 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-lightshot1)
- [Native Window 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-nativewindow1)
- [Debug Fix 1](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-debugfix1)
