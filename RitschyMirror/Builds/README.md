# RitschyMirror English builds

## Latest: English 1.3.2 — Auto Clarity & Edges 1

**[Download the Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-clarityedges1/RitschyMirror-English-Setup-1.3.2-ClarityEdges1.exe)**

- [Release page](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-clarityedges1)
- [Successful Windows build and installer packaging](https://github.com/Fireworkstars46/App-Builds/actions/runs/35786982630)
- [Auto clarity and screen edge patch](../Source/auto_clarity_and_window_edges.py)

### Changes

- **Auto clarity (mild SDR text sharpening):** An optional GPU preview filter in RitschyMirror's **Copy mode** that mildly sharpens text and scales its strength up when the source is reduced to a smaller preview. It is an adjustable on/off switch under **Image / Tone mapping**. This *does not* change Camera HD's own Sharpness setting, correct the capture card's hardware compression, or recreate detail lost in the capture feed. Stronger sharpening may cause halos or slightly reduce performance; disable Auto clarity if that occurs.
- **Keep preview inside its current display:** An optional checkbox under **Source / Target & Mode**. When enabled, dragging the titlebar or resizing the preview using a border/corner is constrained to the display on which the move/resize began. The app also gently snaps the preview to the screen edge (~12 pixels). The feature prevents an accidental drag onto the other laptop's HDMI output display. Turn it off to move the preview freely between displays.
- Preserves the existing preview location selector (Main / Extended / Remember last position), custom sizing, maximize/restore, saved geometry, copy mode, monitor capture fallback, and FPS/low-latency controls.

**Important:** Normal Windows windows *can* cross between monitors; the stop-at-edge behavior is a custom optional restriction. The preview app's hand-implemented drag/resize path is *not* identical to native Windows Aero Snap or OBS's UI. The limiter applies to mouse drag/edge resize, not every OS window-placement shortcut or programmatic repositioning.

### Installation and initial settings

Close the previous RitschyMirror process completely, install the EXE, open Settings and enable **Copy mode**, **Auto clarity**, and **Keep preview inside its current display**. Under **Preview opens on**, choose **Extended display** if the preview should drive your HDMI capture card, or **Main display** if you want to see the preview on your own screen (which may produce mirror-in-mirror if it also captures the main screen). Restart (display) to apply structural changes. Windows should remain in **Extend** mode.

**Test status:** GitHub Actions on Windows compiled and packaged the application and published the installer successfully. Real-world text sharpness, screen-edge confinement, resizing and capture-card latency have **not been tested on the target laptop**. Auto clarity is image enhancement, not an automatic objective sharpness or capture feed diagnosis algorithm.

## Previous builds

- [Preview Select 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-previewselect1/RitschyMirror-English-Setup-1.3.2-PreviewSelect1.exe)
- [Resize Save 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-resizesave1/RitschyMirror-English-Setup-1.3.2-ResizeSave1.exe)
- [Smooth FPS 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-smoothfps1/RitschyMirror-English-Setup-1.3.2-SmoothFPS1.exe)

Installer EXEs are GitHub release assets and Actions artifacts, linked here instead of checked into source Git history.
