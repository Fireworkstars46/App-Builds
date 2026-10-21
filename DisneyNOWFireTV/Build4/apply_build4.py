#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_build4.py <extracted Build 2 source root>")

root = Path(sys.argv[1]).resolve()
main = root / "DisneyNOWFireTV" / "Source" / "app" / "src" / "main" / "java" / "com" / "fireworkstars46" / "disneynowfiretv" / "MainActivity.java"
gradle = root / "DisneyNOWFireTV" / "Source" / "app" / "build.gradle"

if not main.is_file() or not gradle.is_file():
    raise SystemExit("expected DisneyNOW Build 2 source layout not found")

text = main.read_text(encoding="utf-8")
if "cursorEnabled" not in text:
    raise SystemExit("cursorEnabled state not found; refusing unsafe patch")
if "KEYCODE_DPAD_UP" not in text or "KEYCODE_DPAD_CENTER" not in text:
    raise SystemExit("existing cursor key handler not found; refusing unsafe patch")
if "boolean dispatchKeyEvent(KeyEvent event)" in text:
    raise SystemExit("dispatchKeyEvent already exists; refusing duplicate patch")

# WebView can consume DPAD events before Activity.onKeyDown receives them. Intercept
# cursor-navigation keys at Activity.dispatchKeyEvent while cursor mode is enabled,
# invoke the existing production onKeyDown/onKeyUp cursor path, and consume the
# event so WebView/site focus navigation cannot also move.
method = r'''

    private boolean isCursorNavigationKey(int keyCode) {
        return keyCode == KeyEvent.KEYCODE_DPAD_UP
                || keyCode == KeyEvent.KEYCODE_DPAD_DOWN
                || keyCode == KeyEvent.KEYCODE_DPAD_LEFT
                || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT
                || keyCode == KeyEvent.KEYCODE_DPAD_CENTER
                || keyCode == KeyEvent.KEYCODE_ENTER
                || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER;
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        if (cursorEnabled && isCursorNavigationKey(event.getKeyCode())) {
            if (event.getAction() == KeyEvent.ACTION_DOWN) {
                onKeyDown(event.getKeyCode(), event);
            } else if (event.getAction() == KeyEvent.ACTION_UP) {
                onKeyUp(event.getKeyCode(), event);
            }
            return true;
        }
        return super.dispatchKeyEvent(event);
    }
'''

last = text.rfind("\n}")
if last < 0:
    raise SystemExit("MainActivity class closing brace not found")
text = text[:last] + method + text[last:]
main.write_text(text, encoding="utf-8")

# Build 4 is a corrective build. Keep versionName/package identity unchanged and
# advance Android versionCode so it can update Build 3 in place.
g = gradle.read_text(encoding="utf-8")
if "versionCode 2" not in g:
    raise SystemExit("expected Build 2 versionCode not found")
g = g.replace("versionCode 2", "versionCode 4", 1)
gradle.write_text(g, encoding="utf-8")

# Update release/build labels in the exact source package without changing the
# established version line or unrelated behavior.
for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in {".java", ".gradle", ".md", ".txt", ".py", ".xml"}:
        continue
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    n = s.replace("Build 2", "Build 4").replace("BUILD 2", "BUILD 4").replace("Build2", "Build4")
    if n != s:
        p.write_text(n, encoding="utf-8")

# Targeted regression assertions for the reported Fire TV/iPhone-remote bug.
patched = main.read_text(encoding="utf-8")
required = [
    "boolean dispatchKeyEvent(KeyEvent event)",
    "cursorEnabled && isCursorNavigationKey(event.getKeyCode())",
    "onKeyDown(event.getKeyCode(), event)",
    "onKeyUp(event.getKeyCode(), event)",
    "return true;",
    "return super.dispatchKeyEvent(event);",
]
missing = [x for x in required if x not in patched]
if missing:
    raise SystemExit("Build 4 regression patch incomplete: " + repr(missing))

print("Build 4 cursor-input corrective patch applied successfully")
