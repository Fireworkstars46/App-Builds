# UxPlay Quality Launcher Full — v91o Build 80

Corrective build for the Build 79 title-bar Pin regression.

## User-reported Build 79 regression
- The Pin still did not visually match the supplied MirrorTo reference closely enough.
- The Pin could be missing on the renderer's first visible frame and appear only after the title bar was clicked/activated.

## Build 80 corrective change
- Keeps the native Windows draggable/resizable renderer frame.
- Keeps native Minimize / Maximize / Close.
- Keeps the one-click Pin in the native small title-bar icon slot.
- Uses a normalized alpha silhouette derived from the user-provided MirrorTo pushpin reference.
- Same silhouette in both states: gray = unpinned, bright blue = pinned.
- Primes the Pin icon before the renderer HWND is created/shown.
- Re-applies it once the HWND exists and requests a bounded frame redraw.
- Removes the path that could let the launcher's normal icon own the initial caption paint.
- No floating overlay, custom caption paint loop, or DLL injection/hooking.
- Wi-Fi regression gate now requires Pin priming before first Show() and a completed first visible Show().

Static/source audit: 58/58 PASS.

Windows C# compile, Inno build, live AirPlay, first-frame visibility, exact appearance, color-state behavior, and drag/minimize/maximize/resize remain NOT TESTED until run on the user's Windows PC.