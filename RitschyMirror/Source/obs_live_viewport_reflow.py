"""OBS Projector 2: update the letterbox/canvas aspect DURING native resizing.

OBS Projector 1 gave a framed UI thread and a distinct child video HWND. But
Native Live 2 intentionally keeps an OLD swapchain buffer size for the duration
of the gesture. Renderer.ComputeLayout still used that old width and height,
so a new client shape stretched the old viewport, causing visibly delayed,
stuck or incorrectly positioned black letterboxing while resizing.

On EVERY render iteration: read the video's CURRENT client width and height.
Compute the actual FIT (or stretch/top-strip) content viewport in current
client coordinates, then transform the viewport to the unchanged physical
swapchain buffer coordinates. When DWM stretches those existing buffers to
the child window's live client size, the content and black bars both already
have the correct current geometry. Continue to defer ResizeBuffers and
geometry/config writes until mouse release to avoid D3D stalls.

In particular do not force stretch: preserve the source's aspect ratio
and leave the expected black letterbox only when the window is not 16:9.
"""
import os
from pathlib import Path

root = Path(os.environ["RITSCHY_SOURCE"])
def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected 1 anchor, found {n}: {old[:130]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched", path)

patch("Renderer.cs",
'''    public int Width { get; private set; }
    public int Height { get; private set; }

    public Renderer(''',
'''    public int Width { get; private set; }
    public int Height { get; private set; }

    // Logical size of the visible embedded projector video area, independent
    // of the physical DXGI backbuffer size while its native parent resizes.
    // Only the capture/render thread reads or writes these fields.
    private int _livePresentationWidth;
    private int _livePresentationHeight;

    public void SetLivePresentationSize(int clientWidth, int clientHeight, bool nativeGesture)
    {
        if (nativeGesture && clientWidth > 0 && clientHeight > 0)
        {
            _livePresentationWidth = clientWidth;
            _livePresentationHeight = clientHeight;
        }
        else
        {
            _livePresentationWidth = 0;
            _livePresentationHeight = 0;
        }
    }

    public Renderer(''')

patch("Renderer.cs",
'''        float W = Width, H = Height;
        string mode = (cfg.LayoutMode ?? "top_strip").Trim().ToLowerInvariant();''',
'''        // Compute layout in LIVE client coordinates rather than the old
        // backbuffer dimensions. This prevents Fit's black bars from staying
        // at the old aspect/position until the native mouse drag ends.
        float W = _livePresentationWidth > 0 ? _livePresentationWidth : Width;
        float H = _livePresentationHeight > 0 ? _livePresentationHeight : Height;
        string mode = (cfg.LayoutMode ?? "top_strip").Trim().ToLowerInvariant();''')

patch("Renderer.cs",
'''        return (vp, cMinX, cMinY, cMaxX, cMaxY);
    }

    /// <summary>
    /// Aus dem Zustand der Quelle''',
'''        if (_livePresentationWidth > 0 && _livePresentationHeight > 0)
        {
            // The swapchain buffers are deliberately fixed while dragging.
            // DWM stretches the presented buffer into the live child HWND.
            // Inverse-map the logical rectangle into buffer coordinates so
            // the final on-screen black area and video viewport BOTH match
            // the CURRENT window aspect instead of the old buffer aspect.
            float scaleX = Width / W, scaleY = Height / H;
            vp = new Viewport(vp.X * scaleX, vp.Y * scaleY,
                              vp.Width * scaleX, vp.Height * scaleY, 0f, 1f);
        }
        return (vp, cMinX, cMinY, cMaxX, cMaxY);
    }

    /// <summary>
    /// Aus dem Zustand der Quelle''')

patch("MirrorEngine.cs",
'''                if (cfg.DebugLogging) DebugPulse("renderer.Render");
                renderer.Render(capture, cfg);''',
'''                if (cfg.DebugLogging) DebugPulse("renderer.Render");
                // An embedded child video surface is resized by the UI
                // thread's WM_SIZE handler *during* a native window gesture.
                // Reflow the Fit viewport and its black bars on each frame.
                // Do not change D3D backbuffer dimensions until gesture end.
                renderer.SetLivePresentationSize(
                    window.ClientWidth, window.ClientHeight,
                    liveNativeWindow && window.NativeInteractiveMoveSize);
                renderer.Render(capture, cfg);''')

patch("SettingsForm.cs",
'''        Note("The normal Windows frame, buttons, snapping, and one visible preview remain unchanged.");''',
'''        Note("The normal Windows frame, buttons, snapping, and one visible preview remain unchanged.");
        Note("Fit layout's picture and black padding update continuously to match live window size.");''')

print("OBS Projector 2: live viewport reflow of video and black bars without DXGI buffer reallocations")
