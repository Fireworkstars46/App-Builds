# UxPlay Quality Launcher Full — v91o Build 81

## Direct USB persistent renderer + once-per-build prompt acknowledgement

Build 81 returns focus to Direct USB while preserving the user-confirmed Build 80 Wi-Fi renderer/title-bar pin behavior.

### Direct USB changes

1. **Persistent black USB renderer**
   - Start USB Mirroring / Direct USB Test opens a native-framed black renderer immediately.
   - The renderer exists before H.264 arrives, like the Wi-Fi persistent renderer.
   - The temporary GStreamer Direct3D11 window is hidden quickly, converted to a child window, and embedded into the persistent host.
   - Disconnect/renderer loss returns the persistent host to black while the session remains active.
   - Stop/Back/page close hides the persistent USB renderer cleanly.

2. **Once-per-build launcher reminder**
   - The launcher's "handle Trust / Allow / passcode / USB prompt" reminder is shown once for each Build number.
   - Clicking OK writes `DirectUsbPhonePromptAcknowledgedBuild=<current build>` to project settings.
   - The write is reloaded and compared before it is treated as saved.
   - Stop USB, unplug/replug, page close, app close/relaunch do not reset that acknowledgement.
   - A newer Build number automatically causes the reminder to appear once again.
   - iOS-owned Trust/Allow/passcode prompts remain controlled by iOS; this launcher acknowledgement does not suppress or control them.

3. **Direct USB settings persistence**
   - USB access, topmost, borderless, aspect lock, fullscreen, monitor, and renderer X/Y/width/height are saved.
   - Save is performed on Start, Stop, Back/page close, and app close.
   - Settings use write → reload → compare verification.
   - Renderer placement is clamped to a visible Windows work area on restore.
   - Private iPhone/UDID values are not saved.

4. **Better USB failure evidence**
   - Important backend lines (Valeria, libusb0, USBMux, PING/CWPA/CVRP/FEED, QuickTime, USB_ERROR_CODE/USB_HINT, timeouts/errors) are copied into the bounded project `UxPlay.log`.
   - Backend exit code, elapsed runtime, and a bounded stderr tail are recorded.
   - The backend emits a final Build 81 exit-code line.

5. **Direct USB test gate**
   - Section-only Direct USB Test remains scoped to Direct USB.
   - It now checks that the native black persistent renderer host is initialized before the live mirror test.

### Preserved

- Build 80 Wi-Fi native renderer window and MirrorTo-style gray/blue pin behavior.
- Wi-Fi section-only test, FPS control, stable-mode FPS opt-in, anti-flash attach, firewall repair, and runtime self-repair.
- Direct USB exact-parent/libusb0, UsbDk, and Normal libusb paths.
- Stable AppId and per-user installer identity.
- No Bitdefender/Defender disabling or broad exclusions.
- No DLL injection/hooking is added.

## Build status

**SOURCE PACKAGE ONLY / NOT DONE / PENDING WINDOWS TEST.**

Windows compile, Inno installer build, live iPhone USB behavior, renderer attach, prompt persistence, and H.264 success still require the user's Windows test.
