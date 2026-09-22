"""Add a separate 8-bit SDR 'Copy mode' to the English RitschyMirror build.

Copy mode uses WGC's SDR BGRA8 capture and outputs sampled RGB without
the existing HDR/SDR tone mapping, gamma, saturation, or contrast shader.
This is a color-neutral preview path, not a guarantee of pixel-perfect
end-to-end HDMI/capture-card/display reproduction.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def replace_one(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {old[:110]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print(f"Updated {path}")

replace_one("MirrorConfig.cs",
'    [JsonPropertyName("tonemap_enabled")]  public bool TonemapEnabled { get; set; } = true;',
'    [JsonPropertyName("copy_mode")]        public bool CopyMode { get; set; } = false;\n'
'    [JsonPropertyName("tonemap_enabled")]  public bool TonemapEnabled { get; set; } = true;')
replace_one("MirrorConfig.cs",
'        "output_bit_depth", "source_display", "target_display",',
'        "copy_mode", "output_bit_depth", "source_display", "target_display",')

replace_one("SettingsForm.cs",
'        Header("Image / Tone mapping");',
'        Header("Image / Tone mapping");\n'
'        CheckRow("Copy mode (SDR colors, no image adjustments; restart required)",\n'
'                 _cfg.CopyMode, v => _cfg.CopyMode = v);')

replace_one("WindowCapture.cs",
'    private bool _showCursor;',
'    private bool _showCursor;\n'
'    private readonly DirectXPixelFormat _captureFormat;')
replace_one("WindowCapture.cs",
"""    public WindowCapture(ID3D11Device device, IntPtr hwnd, bool inputIsHdr, bool showCursor)
        : this(device, hwnd, inputIsHdr, showCursor, captureMonitor: false)
    {
    }
""",
"""    public WindowCapture(ID3D11Device device, IntPtr hwnd, bool inputIsHdr,
                         bool showCursor, bool copySdr = false)
        : this(device, hwnd, inputIsHdr, showCursor, captureMonitor: false, copySdr: copySdr)
    {
    }
""")
replace_one("WindowCapture.cs",
"""    public WindowCapture(ID3D11Device device, IntPtr captureHandle, bool inputIsHdr,
                         bool showCursor, bool captureMonitor)
    {
        _device = device;
        InputIsHdr = inputIsHdr;
        _showCursor = showCursor;
""",
"""    public WindowCapture(ID3D11Device device, IntPtr captureHandle, bool inputIsHdr,
                         bool showCursor, bool captureMonitor, bool copySdr = false)
    {
        _device = device;
        InputIsHdr = inputIsHdr && !copySdr;
        _showCursor = showCursor;
        _captureFormat = copySdr ? DirectXPixelFormat.B8G8R8A8UIntNormalized
                                 : DirectXPixelFormat.R16G16B16A16Float;
""")
replace_one("WindowCapture.cs",
'            _d3dDevice, DirectXPixelFormat.R16G16B16A16Float, 2, new SizeInt32 { Width = _poolW, Height = _poolH });',
'            _d3dDevice, _captureFormat, 2, new SizeInt32 { Width = _poolW, Height = _poolH });')
replace_one("WindowCapture.cs",
'            try { pool.Recreate(_d3dDevice, DirectXPixelFormat.R16G16B16A16Float, 2, content); } catch { /* nächster Versuch */ }',
'            try { pool.Recreate(_d3dDevice, _captureFormat, 2, content); } catch { /* nächster Versuch */ }')

replace_one("MirrorEngine.cs",
'capture = new WindowCapture(device, hwnd, winHdr, cfg.ShowCursor);',
'capture = new WindowCapture(device, hwnd, winHdr, cfg.ShowCursor, copySdr: cfg.CopyMode);')
replace_one("MirrorEngine.cs",
"""            try
            {
                capture = new DuplicationCapture(device, src.Output);
            }
            catch (SharpGen.Runtime.SharpGenException ex)
                when (ex.HResult == unchecked((int)0x887A0004))
            {
                // User's RTX laptop reports DXGI_ERROR_UNSUPPORTED from DuplicateOutput1.
                // WGC can capture the entire selected monitor from the DWM compositor.
                Log("DXGI DuplicateOutput1 is unsupported on this system; switching to Windows Graphics Capture (monitor fallback).");
                context.Dispose();
                device.Dispose();
                D3D11CreateDevice(dst.Adapter, DriverType.Unknown, DeviceCreationFlags.BgraSupport, featureLevels,
                    out device, out context).CheckError();
                var hmonitor = src.Output.Description1.Monitor;
                capture = new WindowCapture(device, hmonitor, src.Hdr, cfg.ShowCursor, captureMonitor: true);
                Log("Windows Graphics Capture monitor fallback started.");
            }
""",
"""            if (cfg.CopyMode)
            {
                // Copy mode needs the 8-bit Windows Graphics Capture path, not the
                // FP16 desktop-duplication/tone-mapping pipeline.
                context.Dispose();
                device.Dispose();
                D3D11CreateDevice(dst.Adapter, DriverType.Unknown, DeviceCreationFlags.BgraSupport, featureLevels,
                    out device, out context).CheckError();
                var hmonitor = src.Output.Description1.Monitor;
                capture = new WindowCapture(device, hmonitor, src.Hdr, cfg.ShowCursor,
                                            captureMonitor: true, copySdr: true);
                Log("Copy mode: whole-monitor SDR BGRA8 capture with image adjustments bypassed.");
            }
            else
            {
                try
                {
                    capture = new DuplicationCapture(device, src.Output);
                }
                catch (SharpGen.Runtime.SharpGenException ex)
                    when (ex.HResult == unchecked((int)0x887A0004))
                {
                    Log("DXGI DuplicateOutput1 unsupported; switching to Windows Graphics Capture monitor fallback.");
                    context.Dispose();
                    device.Dispose();
                    D3D11CreateDevice(dst.Adapter, DriverType.Unknown, DeviceCreationFlags.BgraSupport, featureLevels,
                        out device, out context).CheckError();
                    var hmonitor = src.Output.Description1.Monitor;
                    capture = new WindowCapture(device, hmonitor, src.Hdr, cfg.ShowCursor, captureMonitor: true);
                    Log("Windows Graphics Capture monitor fallback started.");
                }
            }
""")
replace_one("MirrorEngine.cs",
'var renderer = new Renderer(factory, device, context, window.Hwnd, outW, outH, cfg.OutputBitDepth);',
'var renderer = new Renderer(factory, device, context, window.Hwnd, outW, outH, cfg.CopyMode ? 8 : cfg.OutputBitDepth);')

replace_one("Renderer.cs",
'        public float SrcScale, Pad0;',
'        public float SrcScale;\n        public int CopyMode;')
replace_one("Renderer.cs",
'            SrcScale = srcScale,',
'            SrcScale = srcScale,\n            CopyMode = cfg.CopyMode ? 1 : 0,')
replace_one("Shaders.cs",
'    float _pad;',
'    int CopyMode;           // 8-bit SDR raw color preview: skip all image corrections')
replace_one("Shaders.cs",
'    float3 col = Src.Sample(Smp, suv).rgb;',
'    float3 col = Src.Sample(Smp, suv).rgb;\n'
'    // Copy mode samples the WGC SDR BGRA8 texture and writes the RGB values unchanged.\n'
'    // It bypasses tone mapping, sRGB transfer, exposure, saturation, contrast, and gamma.\n'
'    if (CopyMode != 0) return float4(saturate(col), 1);')

print("8-bit SDR copy-mode patch applied")
