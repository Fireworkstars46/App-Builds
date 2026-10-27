# UxPlay Quality Launcher Full — v91o Build 85

Corrective scope:
- Fixes the Build 84 Direct USB phone-confirmation OK-button delay/glitch shown in the user's recording.
- The reminder now runs on a dedicated STA Windows UI thread with its own `Application.Run()` message loop.
- The launcher/test thread no longer uses `Application.DoEvents()` to keep the reminder responsive.
- OK/Cancel use the existing single atomic outcome and close from the prompt UI thread.
- Backend exit still auto-closes the reminder and is not saved as an acknowledgement.
- Only a real OK click saves the once-per-Build acknowledgement.

Preserved:
- Build 84 USB transport changes, including Auto transport selection and queued handshake work.
- Persistent black Direct USB renderer and saved USB renderer placement/settings.
- Known-good Build 80 Wi-Fi native renderer/title-bar pin/FPS behavior.
- Stable installer AppId and per-user install identity.

Validation status:
- Static/source audit: 105/105 PASS.
- ZIP integrity: PASS.
- Windows compile: NOT TESTED.
- Installer build: NOT TESTED.
- Real OK-click responsiveness: NOT TESTED until run on the user's Windows PC.
- Live iPhone Direct USB CWPA/H.264: NOT TESTED.
- Build status: NOT DONE / PENDING.
