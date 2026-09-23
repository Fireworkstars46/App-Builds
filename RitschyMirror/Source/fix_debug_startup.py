"""Fix the two concrete startup faults shown in mirror.log.

1. The previous auto_clarity script expanded the Direct3D shader parameter
   C# struct from 64 to 72 bytes; Direct3D 11 constant buffers require the
   buffer byte size to be a multiple of 16. Add 8 bytes of explicit padding
   to make the managed struct and HLSL declaration 80 bytes.
2. Prevent startup recursive previews by relocating a windowed monitor
   preview onto the target display if it overlaps its captured source.
Runs after debug_capture_freezes.py.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, before, after):
    p = root / path
    s = p.read_text(encoding="utf-8")
    hits = s.count(before)
    if hits != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {hits}: {before[:120]!r}")
    p.write_text(s.replace(before, after, 1), encoding="utf-8")
    print("Patched " + path)

patch("Renderer.cs",
'        public float AutoClarity, _padSharp;',
'''        // D3D11 CONSTANT_BUFFER ByteWidth must be a multiple of 16.
        // Original parameters: 64 bytes. AutoClarity and _padSharp: +8.
        // Add 8 more bytes so Marshal.SizeOf<ShaderParams>() is 80, not 72.
        public float AutoClarity, _padSharp, _padSharp2, _padSharp3;''')

patch("Shaders.cs",
'''    float _padSharp;
};''',
'''    float _padSharp;
    float2 _padSharpExtra;  // explicit padding to 80 bytes, matches C# ShaderParams
};''')

patch("MirrorEngine.cs",
'''        Log("Step: Creating window...");
        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,
        };''',
'''        // A captured screen must NOT contain its own preview. Merely warning
        // is insufficient: the GPU will recursively paint the same screen.
        // When Source and Target differ, move the preview to Target regardless
        // of saved geometry or the older 'Preview opens on: Main' preference.
        // Leave Windows in Extend; do not modify display topology.
        if (windowed && captureMode == "monitor" && debugSourceDisplay >= 0)
        {
            var sourceBounds = displays[debugSourceDisplay];
            bool overlapsCapturedDisplay =
                x < sourceBounds.R && x + outW > sourceBounds.L &&
                y < sourceBounds.B && y + outH > sourceBounds.T;
            if (overlapsCapturedDisplay && debugSourceDisplay != dstIdx)
            {
                x = dst.L + Math.Max(0, (dst.R - dst.L - outW) / 2);
                y = dst.T + Math.Max(0, (dst.B - dst.T - outH) / 2);
                Log("[SAFETY] Preview placement overlapped captured source; opening on HDMI target instead to prevent recursive mirroring.");
            }
        }

        Log("Step: Creating window...");
        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,
        };''')

print("Fixed shader constant buffer alignment and unsafe preview startup position")
