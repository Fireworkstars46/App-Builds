# UxPlay Quality Launcher Full — v91o Build 77

Corrective build for the missing Build 76 title-bar pin control.

## What changed
- Preserves the real native Windows `FormBorderStyle.Sizable` renderer frame.
- Preserves native drag, Minimize, Maximize/Restore, Close, and edge/corner resizing.
- Removes Build 76 custom non-client pin painting, which was not visible on the user's Windows system because the native/DWM caption repainted over it.
- Uses a leading clickable pin glyph in the native window title text instead: `📌  Direct3D11 renderer`.
- Pinned state adds a check mark after the pin.
- Only the pin-glyph rectangle is intercepted; the rest of the caption remains ordinary native draggable title-bar area.
- Keeps the system-menu `Pin on top` fallback and the shared renderer topmost state.
- No floating title-bar overlay, DLL injection, or custom non-client painting.

## Validation
- Static/source audit: 42/42 PASS.
- ZIP integrity: PASS.
- Windows C# compile: NOT TESTED here.
- Inno Setup installer build: NOT TESTED here.
- Live AirPlay/iPhone renderer: NOT TESTED here.
- Actual pin glyph visibility/click, native drag, caption buttons, resize, and topmost interaction: NOT TESTED here.

Build 77 remains NOT DONE / PENDING until Windows runtime validation.
