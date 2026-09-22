# RitschyMirror English builds

## Latest: 1.3.2 English — Capture Fix 1

**[Download the ready-to-install Windows EXE](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2-capturefix1/RitschyMirror-English-Setup-1.3.2-CaptureFix1.exe)**

- [Release details](https://github.com/Fireworkstars46/App-Builds/releases/tag/ritschymirror-english-1.3.2-capturefix1)
- [Successful Windows build](https://github.com/Fireworkstars46/App-Builds/actions/runs/35689314339)
- [Capture workaround source](../Source/enable_monitor_fallback.py)

This unofficial English build adds a whole-monitor Windows Graphics Capture fallback when the original DXGI Desktop Duplication API reports `DXGI_ERROR_UNSUPPORTED (0x887A0004)`. The existing UI, Windows Extend mode and windowed output remain available. The Windows build and installer packaging succeeded; the workaround still needs to be tested on the affected laptop.

## Previous version

- [English 1.3.2 original installer (without capture fallback)](https://github.com/Fireworkstars46/App-Builds/releases/download/ritschymirror-english-1.3.2/RitschyMirror-English-Setup-1.3.2.exe)

Build executables live in GitHub Releases and Actions artifacts, linked from this folder, rather than being committed to the Git source tree.
