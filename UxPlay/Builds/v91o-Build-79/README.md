# UxPlay Quality Launcher Full — v91o Build 79

Requested change: keep Build 78's gray/blue Pin state behavior, but change the visible title-bar Pin artwork to the same tilted pushpin-style silhouette shown in the user's MirrorTo reference.

Build 79 keeps the real native Windows frame. The renderer's native small title-bar icon slot remains the one-click Pin/Unpin target. The exact same tilted pushpin geometry is used in both states; only the color changes: gray when unpinned and bright blue when pinned.

Preserved behavior includes native title-bar dragging, Minimize, Maximize/Restore, Close, edge/corner resize, persistent AirPlay renderer attachment, Wi-Fi section-only tests, FPS controls, firewall repair, runtime self-repair, Direct USB behavior, shared Always-on-Top state, and the system-menu Pin fallback.

No floating title-bar overlay, custom non-client caption repaint loop, or native-titlebar DLL injection is used.

Static/source audit: 50/50 PASS. ZIP integrity: PASS. Windows C# compile, Inno Setup build, live AirPlay, real title-bar icon appearance/color/click behavior, and drag/minimize/maximize/resize regression behavior remain NOT TESTED until run on the user's Windows PC.