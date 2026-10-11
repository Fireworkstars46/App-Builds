"""Resolve compiler/analyzer warnings exposed by Build 3 warnings-as-errors.

These are correctness/static-cleanliness fixes only. They preserve runtime behavior:
- assert the capture SRV is present at the draw point already required by the renderer,
- make UI-contract checks runtime local-variable checks rather than compile-time constants,
- remove obsolete preview-full-exit bookkeeping left unused after preview X became
  preview-only in the previous completed build,
- remove duplicate manifest DPI declarations because Program already requests
  PerMonitorV2 with SetProcessDpiAwarenessContext before WinForms starts.
"""
import os, re
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def replace(path, old, new, count=1):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != count:
        raise RuntimeError(f"{path}: expected {count} anchor(s), found {n}: {old[:140]!r}")
    p.write_text(s.replace(old, new, count), encoding="utf-8")
    print("patched", path)

# The active frame must have an SRV to reach the render pass. Tell nullable analysis
# that this existing invariant is intentional; do not add a new branch or behavior.
replace("Renderer.cs", "_ctx.PSSetShaderResource(0, cap.Srv);", "_ctx.PSSetShaderResource(0, cap.Srv!);")

# Preserve the self-test checks without creating compile-time unreachable branches.
replace("SettingsForm.cs",
'''    public static IEnumerable<string> ValidateUiLayoutContract()
    {
        if (LX < 0 || CX <= LX || ROW < 24) yield return "UI layout constants are invalid.";
        const int minimumContentWidth = 360;
        const int minimumContentHeight = 320;
        if (minimumContentWidth < 320 || minimumContentHeight < 280)
            yield return "UI minimum-size contract is invalid.";
    }
''',
'''    public static IEnumerable<string> ValidateUiLayoutContract()
    {
        int lx = LX, cx = CX, row = ROW;
        if (lx < 0 || cx <= lx || row < 24) yield return "UI layout constants are invalid.";
        int minimumContentWidth = 360;
        int minimumContentHeight = 320;
        if (minimumContentWidth < 320 || minimumContentHeight < 280)
            yield return "UI minimum-size contract is invalid.";
    }
''')

# Build 2 ultimately made preview X stop mirroring only, so the earlier interim
# full-app-close callback/flag are dead code and should not survive Build 3.
replace("Win32Window.cs", '''    private volatile bool _engineInitiatedClose;
    // The tray host owns the process lifetime. On a genuine user close,
    // request an app exit on the WinForms UI thread; native preview UI
    // MUST NOT directly join the render thread or call Application.Exit.
    public static event Action? PreviewUserClosed;
''', "")
replace("Win32Window.cs", '''        // Engine.Stop / Restart / device-loss cleanup uses WM_CLOSE to wake
        // the dedicated native UI thread. Suppress the user-X callback for
        // that INTERNAL WM_CLOSE, even if it is delivered asynchronously.
        _engineInitiatedClose = true;
''', "")

# .NET WinForms analyzer WFO0003 rejects manifest DPI settings when the app also
# configures DPI programmatically. Program.cs already calls PerMonitorV2 before
# Application.EnableVisualStyles, so retain that single documented mechanism.
manifest = root / "app.manifest"
m = manifest.read_text(encoding="utf-8")
m2, n = re.subn(r'''\s*<windowsSettings>.*?</windowsSettings>''', "", m, count=1, flags=re.S)
if n != 1:
    raise RuntimeError(f"app.manifest: expected one windowsSettings DPI block, found {n}")
manifest.write_text(m2, encoding="utf-8")
print("removed duplicate manifest DPI declaration; Program PerMonitorV2 path retained")

print("Build 3 warnings-as-errors cleanup applied")
