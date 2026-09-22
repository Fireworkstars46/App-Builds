# RitschyMirror English builds

## Latest: 1.3.2 English — Copy Mode 1

**[Download the ready-to-install Windows setup EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-copymode1/RitschyMirror-English-Setup-1.3.2-CopyMode1.exe)**

- [Release details](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-copymode1)
- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35690097779)
- [Copy-mode source changes](../Source/add_copy_mode.py)

In Settings > Image / Tone mapping, enable **Copy mode (SDR colors, no image adjustments; restart required)**, set Capture mode to **monitor**, and keep Output mode on **windowed**. Click **Restart (display)**. In copy mode the program requests 8-bit SDR BGRA capture from Windows Graphics Capture, uses an 8-bit output swapchain, and bypasses tone mapping, exposure, gamma, saturation and contrast. The alternative DXGI capture fallback remains available outside copy mode.

**Limitations:** This is an unofficial build tested only by automated Windows compilation and installer packaging. Copy mode aims to preserve SDR colors but cannot guarantee pixel-identical capture through HDMI, the capture card, its preview app and Windows display color management. A 1280x720 preview of a 1920x1080 desktop will still be downscaled, affecting text sharpness. Moving the preview window onto the extended HDMI display prevents the mirror-in-mirror effect.

## Previous builds

- [English capture fix 1](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-capturefix1/RitschyMirror-English-Setup-1.3.2-CaptureFix1.exe)
- [Initial English version](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2/RitschyMirror-English-Setup-1.3.2.exe)

Build executables are published in GitHub Releases and Actions artifacts, rather than being committed to this repository.
