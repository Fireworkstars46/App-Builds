# RitschyMirror English builds

## Latest: English 1.3.2 — OBS Projector 1

**[Download the Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-obsprojector1/RitschyMirror-English-Setup-1.3.2-OBSProjector1.exe)**

- [Windows compilation, packaging, and release: successful](https://github.com/Fireworkstars46/App-Builds/actions/runs/35815828824)
- [OBS-style presentation source patch](../Source/obs_style_native_video_surface.py)

The preview is one ordinary **top-level Windows window**, hosting an **embedded video-only child surface** (not a second on-screen preview window). A dedicated GUI thread handles Windows native titlebar drag/edge resize, Snap, maximize/restore and cross-monitor movement; the existing capture/render thread separately owns the video child swapchain. During native window resizing, the video child follows the client rectangle and the worker keeps submitting new frames to its swapchain, using the last captured texture at the selected FPS when capture does not produce a newer frame yet. DXGI backbuffer reallocations and preview-geometry configuration writes are deferred until release. Other window modes keep their previous implementation. This aims to avoid both main-thread drag freezes and repeated swapchain reallocations, without using OBS or network streaming.

**Test on the actual laptop:** Close the application and its tray icon. Install OBS Projector 1 over the prior release; choose Capture mode Monitor, source Main / DISPLAY1, target HDMI TO USB, Output mode Windowed, Preview style Recursive projector (OBS-style), Borderless projector OFF, Preview window movement Normal Windows (browser-like), FPS limit 60. Restart the preview. Move the titlebar and hold a window edge while resizing; verify that content visibly changes before releasing the mouse, and that the child video image fills the new size after release. If the image remains blank or pauses, enable debug logging, perform a five-second drag while your desktop content changes, and share the latest mirror.log. The Windows CI compile/package result **does not prove** perfect OBS parity or physical HDMI capture-card behavior on your laptop.

## Previous: Native Live 2

[Native Live 2 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-nativelive2)

## Native Live 2 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-nativelive2/RitschyMirror-English-Setup-1.3.2-NativeLive2.exe)**

- [Windows compilation, installer, and release succeeded](https://github.com/Fireworkstars46/App-Builds/actions/runs/35814725992)
- [Source patch](../Source/native_live_drag_resize_v2.py)

Native Live 2 retains one standard Win32 preview on its own UI thread, with the capture/render thread separate. A second live-resize issue was the rendering thread calling DXGI ResizeBuffers repeatedly while a native titlebar move or border resize was in progress, plus continuously writing window geometry to the config on each resize event. During native move/resize this build continues presenting new frames using the current buffers while Windows scales the image to the changing window size; buffer reallocation and geometry save happen after release. This specifically targets preview pauses/blanking during a regular Windows drag or resize. It does not change which monitor is captured or duplicate the Windows display.

**Test:** Close RitschyMirror and its tray icon, install Native Live 2 over the previous installer, select Capture mode Monitor and your main-display source; Output mode Windowed; Preview style Recursive projector (OBS-style); Borderless projector OFF; Preview window movement Normal Windows (browser-like); FPS limit 60. Keep Windows set to Extend. Restart the preview. While holding the title bar or a resize border, verify that the source video visibly changes *before* releasing the mouse. The compiled installer alone cannot verify the native DWM/capture performance on the actual laptop. If frames still visibly pause, reproduce one 5-second drag with the debug log enabled and share the latest mirror.log so the capture FPS and rendering/present stalls during the gesture can be compared.

## Previous: Native Live 1

[Native Live 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-nativelive1)

## Native Live 1 details

**[Download Windows installer](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-nativelive1/RitschyMirror-English-Setup-1.3.2-NativeLive1.exe)**

- [Successful Windows compile, installer package and release](https://github.com/Fireworkstars46/App-Builds/actions/runs/35812233981)
- [Native UI thread source patch](../Source/native_live_ui_thread.py)

### Native Windows window with live rendering

This release changes how **Normal Windows (browser-like)** works for windowed, framed previews. The existing preview HWND and Windows message loop now belong to a dedicated UI thread, while the existing Direct3D capture/render pipeline continues on the independent engine thread. Windows' modal titlebar drag and border resize loop therefore no longer blocks the main rendering loop. The regular Windows frame, minimize/maximize/restore buttons, native window snapping and normal cross-monitor movement are preserved without forcing the custom smooth-drag movement restrictions. It uses a **single real preview HWND**; native UI-thread creation does not open a second preview.

**Test settings:** Close RitschyMirror and its tray icon, install Native Live 1 over the previous build, set **Output mode → Windowed**, **Borderless projector → OFF**, **Preview window movement → Normal Windows (browser-like)**, leave your chosen projector/Lightshot/FPS options unchanged, then restart the preview. Drag its titlebar and resize from each edge; expect Windows' normal movement with frames continuing during the gesture. The native Windows window may still let you move portions of its frame off-screen, just as other Windows apps do. Windows snapping is controlled by normal Windows Snap settings.

This build has compiled and was packaged successfully on GitHub Actions. **The behavior and achieved FPS during a live Windows drag must still be tested on the actual main laptop and HDMI capture card**. Windows' window compositor, capture mode, or system load can still affect the perceived frame rate; if a capture freeze or crash occurs, share the newest `mirror.log` from Settings → About → Open debug log folder.

## Previous: Resize Bounds 1

[Resize Bounds 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-resizebounds1)

## Resize Bounds 1 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-resizebounds1/RitschyMirror-English-Setup-1.3.2-ResizeBounds1.exe)**

- [Successful Windows build and release](https://github.com/Fireworkstars46/App-Builds/actions/runs/35811688818)
- [Source patch](../Source/resize_screen_bounds_only.py)

This version separates whole-window **movement** from edge **resizing** in Smooth live drag. Moving a window preserves the previous partial-offscreen movement and cross-display behavior, with the existing top bounce. Resizing via an edge or corner now stays inside the working area of the monitor where resizing began, independent of the **Keep preview inside one display** movement setting. If the window was partially offscreen from moving it, the resize first brings it fully into the selected monitor; the same preview window and live renderer remain in use.

To test: fully close RitschyMirror and its tray icon, install Resize Bounds 1 over Vertical Drag 1, select Windowed output, Borderless projector OFF, Smooth live drag, and Keep preview inside one display OFF. Restart the preview. Drag the whole window partially above the top and pull it back down, then resize from a side or corner. The edge resize must stop before it extends beyond that monitor's visible work area. Moving the whole window should retain its previous behavior. The Windows installer compiled successfully; actual live resize behavior on the user's monitor setup still requires testing.

## Previous: Vertical Drag 1

[Vertical Drag 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-verticaldrag1)

## Vertical Drag 1 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-verticaldrag1/RitschyMirror-English-Setup-1.3.2-VerticalDrag1.exe)**

- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35810956261)
- [Source patch](../Source/fix_tall_window_vertical_drag.py)

Corrects a vertical dragging lock after top-edge bounce for very tall restored preview windows. The previous smooth-drag code capped the window top at the screen top when its saved height exceeded the monitor usable height: horizontal movement worked, but downward movement was mathematically prevented. This release changes the lower vertical bound for an oversized window to allow pulling the title bar downward and keep it accessible near the monitor bottom. It retains dragging partly above the screen and returning to the top on release, the normal title bar, live preview resizing, cross-screen movement with confinement OFF, and the existing projector/Lightshot/FPS controls.

To test: close app and tray icon, install Vertical Drag 1 over Live Bounce 1; choose Windowed output, Borderless projector OFF, Smooth live drag, and Keep preview inside one display OFF. Restart preview; drag the window upward partly off-screen, release so it bounces to the top, then grab the title bar and drag it downward. The Windows build passed; runtime drag behavior on the user's actual monitor setup still requires testing.

## Previous: Live Bounce 1

[Live Bounce 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-livebounce1)

## Live Bounce 1 details

**[Download Windows installer EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-livebounce1/RitschyMirror-English-Setup-1.3.2-LiveBounce1.exe)**

- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35810293808)
- [Top-edge bounce source patch](../Source/live_top_edge_bounce.py)

This revision changes **Smooth live drag**: you can pull the normal-sized preview about halfway above the physical screen top while holding the mouse button. On release it repositions the same normal-sized preview to the working area's top edge instead of maximising it or sticking to the top during the drag. Dragging across the boundary between two extended Windows monitors remains available with **Keep preview inside one display = OFF**. The existing manual maximize/restore button still works; dragging from a deliberately maximized preview still restores its prior dimensions. Video remains rendered by the existing preview render loop; actual FPS during resizing depends on hardware.

To test: close RitschyMirror including its tray icon, install Live Bounce 1 over the previous version, set **Output mode: Windowed**, **Borderless projector: OFF**, **Preview window movement: Smooth live drag**, and **Keep preview inside one display: OFF**. Stop and restart preview after changes. Drag the title bar so its upper half extends above the screen, and release it; the outer top edge should land flush with the visible screen/work area without maximizing. If the window starts maximized from a previously saved preference, click its Restore Down button once to return to the normal window size.

### Previous: Live Snap 1

[Live Snap 1 release](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-livesnap1)

## Live Snap 1 details

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
