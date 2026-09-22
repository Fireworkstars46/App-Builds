"""Use Windows Graphics Capture for a monitor if DXGI desktop duplication is unsupported.

The initial capture implementation and all existing rendering/UI behavior remain intact.
Only the unsupported DXGI capture path falls back to WGC's monitor capture.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])

def replace_once(path, old, new):
    p = root / path
    content = p.read_text(encoding="utf-8")
    occurrences = content.count(old)
    if occurrences != 1:
        raise RuntimeError(f"Expected exactly one code anchor in {path}, found {occurrences}")
    p.write_text(content.replace(old, new, 1), encoding="utf-8")
    print(f"Patched {path}")

replace_once("WindowCapture.cs",
"""    public WindowCapture(ID3D11Device device, IntPtr hwnd, bool inputIsHdr, bool showCursor)
    {
        _device = device;
        InputIsHdr = inputIsHdr;
        _showCursor = showCursor;
        _d3dDevice = CreateDirect3DDevice(device);
        _item = CreateItemForWindow(hwnd);
        _item.Closed += (_, _) => _sourceLost = true;
        StartSession();
    }
""",
"""    public WindowCapture(ID3D11Device device, IntPtr hwnd, bool inputIsHdr, bool showCursor)
        : this(device, hwnd, inputIsHdr, showCursor, captureMonitor: false)
    {
    }

    // Windows Graphics Capture can capture a whole monitor as well as a single window.
    // When DXGI DuplicateOutput1 fails with DXGI_ERROR_UNSUPPORTED (0x887A0004),
    // the engine uses this monitor path instead of retrying the unsupported API.
    public WindowCapture(ID3D11Device device, IntPtr captureHandle, bool inputIsHdr,
                         bool showCursor, bool captureMonitor)
    {
        _device = device;
        InputIsHdr = inputIsHdr;
        _showCursor = showCursor;
        _d3dDevice = CreateDirect3DDevice(device);
        _item = captureMonitor ? CreateItemForMonitor(captureHandle)
                               : CreateItemForWindow(captureHandle);
        _item.Closed += (_, _) => _sourceLost = true;
        StartSession();
    }
""")

replace_once("WindowCapture.cs",
"""    [DllImport("d3d11.dll", EntryPoint = "CreateDirect3D11DeviceFromDXGIDevice", SetLastError = true)]
""",
"""    private static GraphicsCaptureItem CreateItemForMonitor(IntPtr hmonitor)
    {
        if (hmonitor == IntPtr.Zero)
            throw new InvalidOperationException("The source monitor does not have a valid handle.");

        var factory = ActivationFactory.Get("Windows.Graphics.Capture.GraphicsCaptureItem");
        var interop = factory.AsInterface<IGraphicsCaptureItemInterop>();
        Guid iid = GraphicsCaptureItemIid;
        IntPtr abi = interop.CreateForMonitor(hmonitor, ref iid);
        var item = GraphicsCaptureItem.FromAbi(abi);
        Marshal.Release(abi);
        return item;
    }

    [DllImport("d3d11.dll", EntryPoint = "CreateDirect3D11DeviceFromDXGIDevice", SetLastError = true)]
""")

replace_once("MirrorEngine.cs",
"""            Log($"Quelle = Display {srcIdx} ({src.Name}), Ziel = Display {dstIdx} ({dst.Name}), output_mode={mode}, layout={cfg.LayoutMode}");
            capture = new DuplicationCapture(device, src.Output);
""",
"""            Log($"Quelle = Display {srcIdx} ({src.Name}), Ziel = Display {dstIdx} ({dst.Name}), output_mode={mode}, layout={cfg.LayoutMode}");
            try
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
""")

print("WGC monitor fallback patch applied")
