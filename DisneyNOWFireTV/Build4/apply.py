#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib

BUILD3_HASHES = {
    "app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java": "7956eac66ca4442f380262ed96f7045e95505ce1aa86cade12dd344a9c7b8f3a",
    "app/build.gradle": "0de300eded35e2683618868fd969545db3245616e2dd041a9540c94d7b30c7f9",
    "README.md": "cdda1149ac90dfd6cc13520c31115773e5f8b7b99f294a71bf465d07a1f922f8",
    "BUILD_INFO.md": "1d1f5e0f0d39148e95431fd758565221b7d19cf1bab966ad5e8be067ce378cb3",
    "tools/static_audit.py": "324a1b09fff596d5986349e9a8e505a16dc6c05848276ef42e6db7d93621433a",
}

BUILD4_HASHES = {
    "app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java": "a8e293210fd266e3a703106f039a073f71a7aebc286a88ec63bd1cdeb4af1866",
    "app/build.gradle": "8e6cba92c1ee74745f6e06d4db90b61c8ead106dce4de56ff2cab4bdac3d378b",
    "README.md": "2dc4f9d53215231fbc1f468c41139334a9aeb55c73d5bc74440ec2cf4b1d62eb",
    "BUILD_INFO.md": "3f90e9c70049898cc888da31271d3e22da4b0961af64c7741507bb7e8702e13f",
    "tools/static_audit.py": "5bd3718e4255cb8f3e96e0d0eaa3f059fe7c38a00bb2e07f6848cf819c4def8d",
}

README4 = '''# Source — DisneyNOW Fire TV Web Wrapper v0.1 Build 4

This is an Android/Fire TV WebView wrapper intended to use the normal DisneyNOW website on a Fire TV Stick.

## Build 4 cursor-input correction

Real Fire TV testing of Build 3 found a reproducible regression: Cursor Navigation could be ON, but D-pad input still used the WebView's normal non-cursor focus/navigation behavior. Build 4 fixes this at the input-dispatch layer.

- With **Cursor Navigation ON**, Activity-level `dispatchKeyEvent()` consumes D-pad directions before WebView and moves the native cursor.
- Center/Select/Enter is consumed and clicks the WebView at the cursor position.
- Both key-down and key-up events are consumed while cursor mode is active so WebView cannot also perform native focus navigation.
- With **Cursor Navigation OFF**, the app does not intercept those cursor keys and normal WebView navigation is preserved.
- Fullscreen custom-video input is not intercepted by cursor mode.
- The existing `onKeyDown()` cursor handling remains as a fallback path.
- Safe Self-Test now exercises the Activity pre-WebView dispatch interception through the real production method and restores cursor position after the test.

## Preserved behavior

Build 4 preserves the Build 3 permanent signing identity and all unrelated working behavior, including package ID `com.fireworkstars46.disneynowfiretv`, Version 0.1, app settings/web data, 75% default Page Zoom, native cursor overlay, edge scrolling, legacy focus navigation fallback, user-agent choices, diagnostics, Safe Self-Test, fullscreen callbacks, hardware acceleration, and normal DisneyNOW authentication/DRM paths.

## Signing / installation note

Build 4 must be signed with the exact permanent private release key established for Build 3. That private key is intentionally not committed to the public repository. Because Build 3 is already on that permanent identity, Build 4 should install directly over Build 3 as an in-place update when its signing certificate is verified to match.

## Runtime status

The source/build/static checks can verify that the pre-WebView key interception exists and is wired through production code, but actual Fire TV/iPhone Fire TV remote behavior and Disney protected playback remain physical runtime checks. Therefore this compatibility build remains **NOT DONE** until those checks are performed on the target Fire TV.
'''

BUILD_INFO4 = '''# Build information

- Project: DisneyNOW Fire TV Web Wrapper
- Version: 0.1
- Build: 4
- Android versionCode: 4
- Package ID: `com.fireworkstars46.disneynowfiretv`
- Minimum SDK: 22 (Android 5.1 / Fire OS 5-era compatibility target)
- Target SDK: 35
- Distribution: personal sideload compatibility test
- Release state: NOT DONE pending real Fire TV runtime verification of the Build 4 cursor-input interception correction and DisneyNOW protected playback.

Build 4 is a corrective build for the reproducible Build 3 issue where Cursor Navigation could be visibly enabled but Fire TV/iPhone Fire TV remote D-pad input still followed the WebView's native non-cursor focus navigation.

The correction intercepts D-pad direction and Select/Enter key events in `Activity.dispatchKeyEvent()` before the focused WebView can consume them. When Cursor Navigation is ON, direction keys move the native cursor and Select/Enter clicks at the cursor. When Cursor Navigation is OFF, normal WebView navigation remains available. Fullscreen custom-video input is left to the fullscreen view.

Build 4 preserves the package ID, settings/web-data paths, Version 0.1 line, Build 3 permanent release-signing identity, Disney authentication path, DRM behavior, 75% default page zoom, native cursor overlay, and legacy focus fallback. Android `versionCode` increments from 3 to 4.

This build follows the repository's current `MASTER_RULES.md` as of source creation. The release workflow records the exact master-rules SHA-256 used at build time.
'''

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def expect_hashes(root: Path, expected: dict[str, str], label: str) -> None:
    bad = []
    for rel, wanted in expected.items():
        p = root / rel
        got = sha(p) if p.is_file() else "missing"
        if got != wanted:
            bad.append(f"{rel}: expected {wanted}, got {got}")
    if bad:
        raise SystemExit(label + " hash verification failed:\n" + "\n".join(bad))

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    root = Path(args.source).resolve()
    expect_hashes(root, BUILD3_HASHES, "Build 3 baseline")

    mainp = root / "app/src/main/java/com/fireworkstars46/disneynowfiretv/MainActivity.java"
    s = mainp.read_text(encoding="utf-8")
    anchor = "    @Override\n    public boolean onKeyDown(int keyCode, KeyEvent event) {\n"
    dispatch = '''    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        if (event != null) {
            int keyCode = event.getKeyCode();
            int action = event.getAction();

            if (keyCode == KeyEvent.KEYCODE_MENU) {
                if (action == KeyEvent.ACTION_DOWN && event.getRepeatCount() == 0) {
                    showAppMenu();
                }
                return true;
            }

            if (customView == null && isCursorEnabled() && isCursorNavigationKey(keyCode)) {
                if (action == KeyEvent.ACTION_DOWN) {
                    if (isCursorDirectionKey(keyCode)) {
                        moveCursor(keyCode, event.getRepeatCount());
                    } else if (event.getRepeatCount() == 0) {
                        performCursorClick();
                    }
                }
                // Consume both DOWN and UP before WebView can perform its native focus navigation.
                return true;
            }
        }
        return super.dispatchKeyEvent(event);
    }

    private static boolean isCursorDirectionKey(int keyCode) {
        return keyCode == KeyEvent.KEYCODE_DPAD_LEFT
                || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT
                || keyCode == KeyEvent.KEYCODE_DPAD_UP
                || keyCode == KeyEvent.KEYCODE_DPAD_DOWN;
    }

    private static boolean isCursorNavigationKey(int keyCode) {
        return isCursorDirectionKey(keyCode)
                || keyCode == KeyEvent.KEYCODE_DPAD_CENTER
                || keyCode == KeyEvent.KEYCODE_ENTER
                || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER;
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
'''
    s = replace_once(s, anchor, dispatch, "dispatchKeyEvent insertion")
    s = replace_once(s,
        "if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER) {\n                performCursorClick();",
        "if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER) {\n                performCursorClick();",
        "cursor click fallback")
    s = replace_once(s,
        "if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER) {\n                sendEnterToWebView();",
        "if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER) {\n                sendEnterToWebView();",
        "legacy enter fallback")
    s = replace_once(s, "BuildConfig.APP_BUILD == 3 && BuildConfig.VERSION_CODE == 3", "BuildConfig.APP_BUILD == 4 && BuildConfig.VERSION_CODE == 4", "version self-test")
    s = replace_once(s, "SafeSelfTest-v0.1-Build3.txt", "SafeSelfTest-v0.1-Build4.txt", "self-test filename")
    self_anchor = '''        } else {
            results.add(TestResult.skipped("Native cursor production movement path",
                    "Cursor mode is disabled or WebView geometry is not ready; no page click is performed by Safe Self-Test."));
        }

        int originalZoom = currentPageZoom();
'''
    self_repl = '''        } else {
            results.add(TestResult.skipped("Native cursor production movement path",
                    "Cursor mode is disabled or WebView geometry is not ready; no page click is performed by Safe Self-Test."));
        }

        if (isCursorEnabled() && webView.getWidth() > dp(160)) {
            ensureCursorPosition();
            float dispatchBeforeX = cursorX;
            float dispatchBeforeY = cursorY;
            long now = android.os.SystemClock.uptimeMillis();
            boolean dispatchConsumed = dispatchKeyEvent(new KeyEvent(now, now, KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DPAD_RIGHT, 0));
            boolean dispatchMoved = cursorX > dispatchBeforeX || (dispatchBeforeX >= webView.getWidth() - cursorView.cursorRadius());
            boolean upConsumed = dispatchKeyEvent(new KeyEvent(now, now + 1L, KeyEvent.ACTION_UP, KeyEvent.KEYCODE_DPAD_RIGHT, 0));
            cursorX = dispatchBeforeX;
            cursorY = dispatchBeforeY;
            cursorView.setCursorPosition(cursorX, cursorY);
            addResult(results, "Activity pre-WebView D-pad dispatch interception",
                    dispatchConsumed && dispatchMoved && upConsumed,
                    "downConsumed=" + dispatchConsumed + " moved=" + dispatchMoved + " upConsumed=" + upConsumed);
        } else {
            results.add(TestResult.skipped("Activity pre-WebView D-pad dispatch interception",
                    "Cursor mode is disabled or WebView geometry is not ready; no page click is performed by Safe Self-Test."));
        }

        int originalZoom = currentPageZoom();
'''
    s = replace_once(s, self_anchor, self_repl, "dispatch regression self-test")
    s = replace_once(s,
        "Build 3 preserves the Build 2 Fire TV cursor, zoom, and performance corrections and establishes the permanent release-signing identity for future in-place updates. It remains NOT DONE until this signed build is tested on the actual Fire TV Stick.",
        "Build 4 fixes the Fire TV cursor regression reported on Build 3 by intercepting D-pad/Select events at the Activity dispatch layer before WebView native focus navigation can consume them. Cursor OFF still leaves normal WebView navigation available. Build 4 preserves the Build 3 permanent release-signing identity for in-place updates and remains NOT DONE until tested on the actual Fire TV Stick.",
        "about text")
    mainp.write_text(s, encoding="utf-8")

    gradle = root / "app/build.gradle"
    g = gradle.read_text(encoding="utf-8")
    g = replace_once(g, "versionCode 3", "versionCode 4", "versionCode")
    g = replace_once(g, "buildConfigField 'int', 'APP_BUILD', '3'", "buildConfigField 'int', 'APP_BUILD', '4'", "APP_BUILD")
    gradle.write_text(g, encoding="utf-8")

    (root / "README.md").write_text(README4, encoding="utf-8")
    (root / "BUILD_INFO.md").write_text(BUILD_INFO4, encoding="utf-8")

    audit = root / "tools/static_audit.py"
    t = audit.read_text(encoding="utf-8")
    replacements = [
        ("STATIC-AUDIT-v0.1-Build3.txt", "STATIC-AUDIT-v0.1-Build4.txt"),
        ('EXPECTED_BUILD = "3"', 'EXPECTED_BUILD = "4"'),
        ('EXPECTED_VERSION_CODE = "3"', 'EXPECTED_VERSION_CODE = "4"'),
        (r'versionCode\s+3\b', r'versionCode\s+4\b'),
        ("buildConfigField 'int', 'APP_BUILD', '3'", "buildConfigField 'int', 'APP_BUILD', '4'"),
        ("BuildConfig.APP_BUILD == 3", "BuildConfig.APP_BUILD == 4"),
        ('("Fire TV Menu key app controls", "KEYCODE_MENU"),', '("Fire TV Menu key app controls", "KEYCODE_MENU"),\n    ("Activity pre-WebView key dispatch override", "public boolean dispatchKeyEvent(KeyEvent event)"),\n    ("Cursor keys consumed before WebView", "Consume both DOWN and UP before WebView"),\n    ("Cursor dispatch directional helper", "isCursorDirectionKey"),\n    ("Cursor dispatch Select/Enter helper", "isCursorNavigationKey"),'),
        ('("Cursor movement self-test through production method", "Native cursor production movement path"),', '("Cursor movement self-test through production method", "Native cursor production movement path"),\n    ("Pre-WebView dispatch regression self-test", "Activity pre-WebView D-pad dispatch interception"),'),
        ('add("Corrective issues documented", all(term in readme.lower() for term in ["laggy", "no cursor", "zoomed in"]), "Build 1 regression list")', 'add("Build 4 cursor regression documented", all(term in readme.lower() for term in ["cursor navigation", "non-cursor", "dispatchkeyevent"]), "Build 3 cursor-input regression and Build 4 interception fix")'),
        ('add("Build info matches Version + Build", "Version: 0.1" in build_info and "Build: 3" in build_info, "BUILD_INFO.md")', 'add("Build info matches Version + Build", "Version: 0.1" in build_info and "Build: 4" in build_info, "BUILD_INFO.md")'),
        ('add("Build 3 self-test report filename", "SafeSelfTest-v0.1-Build3.txt" in main, "current build report path")', 'add("Build 4 self-test report filename", "SafeSelfTest-v0.1-Build4.txt" in main, "current build report path")'),
        ('"Version: 0.1 Build 3",', '"Version: 0.1 Build 4",'),
        ('"Runtime Fire TV smoothness, real provider sign-in, DRM license negotiation, physical cursor/click behavior, Page Zoom appearance, and fullscreen protected video are not claimed by this static audit.",', '"Runtime Fire TV/iPhone remote cursor behavior, real provider sign-in, DRM license negotiation, Page Zoom appearance, and fullscreen protected video are not claimed by this static audit.",'),
    ]
    for i, (old, new) in enumerate(replacements, 1):
        t = replace_once(t, old, new, f"audit replacement {i}")
    audit.write_text(t, encoding="utf-8")

    expect_hashes(root, BUILD4_HASHES, "Build 4 result")
    print("Build 4 corrective source applied and verified.")

if __name__ == "__main__":
    main()
