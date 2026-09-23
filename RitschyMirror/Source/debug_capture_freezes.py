"""Add actionable, low-frequency diagnostics for freeze and recursive mirroring.

Applied after auto_clarity_and_window_edges.py. Does not change image, monitor
selection, output placement or frame timing. A separate watchdog thread can
still append an alert if the renderer gets stuck inside Present/capture.
"""
import os
from pathlib import Path
root = Path(os.environ["RITSCHY_SOURCE"])

def patch(path, old, new):
    p = root / path
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{path}: expected exactly one code anchor, found {n}: {old[:100]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("Patched " + path)

# Toggle is on by default for this diagnostic build, but disabling it removes
# periodic per-frame instrumentation and watchdog alerts.
patch("MirrorConfig.cs",
'    [JsonPropertyName("auto_clarity")]     public bool AutoClarity { get; set; } = true;',
'    [JsonPropertyName("auto_clarity")]     public bool AutoClarity { get; set; } = true;\n'
'    [JsonPropertyName("debug_logging")]    public bool DebugLogging { get; set; } = true;')

patch("MirrorConfig.cs",
'        "layout_mode", "crop_x", "crop_y", "crop_w", "crop_h", "show_cursor", "keep_awake", "auto_clarity",',
'        "layout_mode", "crop_x", "crop_y", "crop_w", "crop_h", "show_cursor", "keep_awake", "auto_clarity", "debug_logging",')

patch("SettingsForm.cs",
'        CheckRow("Low latency (prefer newest captured frame)",\n'
'                 _cfg.LowLatency, v => _cfg.LowLatency = v);',
'        CheckRow("Low latency (prefer newest captured frame)",\n'
'                 _cfg.LowLatency, v => _cfg.LowLatency = v);\n'
'        CheckRow("Debug logging (FPS, stalls and repeated-screen detection)",\n'
'                 _cfg.DebugLogging, v => _cfg.DebugLogging = v);')

patch("SettingsForm.cs",
'        Header("About");',
'''        Header("About");
        var logButton = new Button
        {
            Text = "Open debug log folder",
            Location = new Point(LX, _y),
            Width = 190, Height = 30
        };
        logButton.Click += (_, _) =>
        {
            try
            {
                var folder = Path.GetDirectoryName(_engine.LogPath);
                if (string.IsNullOrWhiteSpace(folder))
                    throw new InvalidOperationException("Log folder unavailable.");
                System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = "\\\"" + folder + "\\\"",
                    UseShellExecute = true
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show(this, "Cannot open log folder: " + ex.Message,
                    "RitschyMirror diagnostics", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        };
        _panel.Controls.Add(logButton);
        _y += 37;
        Note("After a freeze, open mirror.log here and share the latest lines.");''')

# Serialize writes because both the render and watchdog threads write log.
patch("MirrorEngine.cs",
'    private readonly object _gate = new();',
'''    private readonly object _gate = new();
    private readonly object _logGate = new();
    private long _debugHeartbeatTicks;
    private string _debugStage = "not started";
    private int _debugActive;

    private void DebugPulse(string stage)
    {
        Volatile.Write(ref _debugStage, stage);
        Interlocked.Exchange(ref _debugHeartbeatTicks, DateTime.UtcNow.Ticks);
    }

    private void RunDebugWatchdog(Thread renderThread)
    {
        long previousWarningTicks = 0;
        while (!_stop && renderThread.IsAlive)
        {
            Thread.Sleep(1000);
            if (_stop || !renderThread.IsAlive || Volatile.Read(ref _debugActive) == 0)
                continue;
            long last = Interlocked.Read(ref _debugHeartbeatTicks);
            if (last <= 0) continue;
            long now = DateTime.UtcNow.Ticks;
            double unresponsiveSeconds = (now - last) / (double)TimeSpan.TicksPerSecond;
            if (unresponsiveSeconds >= 4 &&
                (previousWarningTicks == 0 || (now - previousWarningTicks) >= TimeSpan.FromSeconds(5).Ticks))
            {
                previousWarningTicks = now;
                Log($"[DEBUG] RENDER STALL: no progress for {unresponsiveSeconds:F1}s; last stage={Volatile.Read(ref _debugStage)}. This may be a blocking capture, resize, GPU call or Present.");
            }
        }
    }''')

patch("MirrorEngine.cs",
'''        Console.WriteLine(line);
        try { File.AppendAllText(LogPath, line + Environment.NewLine); } catch { }''',
'''        Console.WriteLine(line);
        lock (_logGate)
        {
            try { File.AppendAllText(LogPath, line + Environment.NewLine); }
            catch { /* Logging must never take down the capture thread. */ }
        }''')

patch("MirrorEngine.cs",
'''            _thread.Start();
        }
    }

    public void Stop()''',
'''            Interlocked.Exchange(ref _debugActive, 0);
            Interlocked.Exchange(ref _debugHeartbeatTicks, 0);
            _thread.Start();
            var rendering = _thread;
            new Thread(() => RunDebugWatchdog(rendering))
            {
                IsBackground = true,
                Name = "MirrorDebugWatchdog"
            }.Start();
        }
    }

    public void Stop()''')

patch("MirrorEngine.cs",
'''        var cfg = MirrorConfig.Load(ConfigPath);
        Log("RitschyMirror Render-Start.");''',
'''        var cfg = MirrorConfig.Load(ConfigPath);
        Interlocked.Exchange(ref _debugActive, cfg.DebugLogging ? 1 : 0);
        if (cfg.DebugLogging) DebugPulse("initializing capture and displays");
        Log("RitschyMirror Render-Start.");
        if (cfg.DebugLogging)
            Log($"[DEBUG] Session start: capture_mode={cfg.ResolveCaptureMode()}, output_mode={cfg.ResolveOutputMode()}, " +
                $"preview_open_on={cfg.PreviewOpenOn}, copy_mode={cfg.CopyMode}, auto_clarity={cfg.AutoClarity}, " +
                $"fps_limit={cfg.FpsLimit}, vsync={cfg.Vsync}, low_latency={cfg.LowLatency}, " +
                $"keep_preview_on_display={cfg.KeepPreviewOnDisplay}.");''')

patch("MirrorEngine.cs",
'''        ICaptureSource capture;

        if (captureMode == "window")''',
'''        ICaptureSource capture;
        int debugSourceDisplay = -1;

        if (captureMode == "window")''')

patch("MirrorEngine.cs",
'''            var src = displays[srcIdx];
            D3D11CreateDevice(src.Adapter, DriverType.Unknown, DeviceCreationFlags.BgraSupport, featureLevels,''',
'''            var src = displays[srcIdx];
            debugSourceDisplay = srcIdx;
            if (cfg.DebugLogging && srcIdx == dstIdx)
                Log("[DEBUG] WARNING: Source and Target are the same monitor; capturing the preview itself may produce an endless mirror.");
            D3D11CreateDevice(src.Adapter, DriverType.Unknown, DeviceCreationFlags.BgraSupport, featureLevels,''')

patch("MirrorEngine.cs",
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,
        };
        if (windowed && cfg.PreviewMaximized) window.Maximize();''',
'''        var window = new Win32Window("RitschyMirror", x, y, outW, outH, borderless)
        {
            KeepOnDisplay = windowed && cfg.KeepPreviewOnDisplay,
        };
        if (windowed && cfg.PreviewMaximized) window.Maximize();
        if (cfg.DebugLogging && GetWindowRect(window.Hwnd, out RECT previewRect))
        {
            Log($"[DEBUG] Preview window bounds=({previewRect.Left},{previewRect.Top})-({previewRect.Right},{previewRect.Bottom}); " +
                $"target screen=({dst.L},{dst.T})-({dst.R},{dst.B}); source display index={debugSourceDisplay}.");
            if (debugSourceDisplay >= 0)
            {
                var source = displays[debugSourceDisplay];
                bool overlap = previewRect.Left < source.R && previewRect.Right > source.L &&
                               previewRect.Top < source.B && previewRect.Bottom > source.T;
                if (overlap)
                    Log("[DEBUG] RECURSIVE MIRROR WARNING: RitschyMirror preview overlaps the captured SOURCE screen. Move preview to the HDMI target or choose Extended display in Preview opens on.");
            }
        }''')

patch("MirrorEngine.cs",
'''        long framesRendered = 0;
        long nextFrameAt = 0;''',
'''        long framesRendered = 0;
        long debugNewFrames = 0;
        long debugIntervalFrames = 0;
        long debugIntervalStart = System.Diagnostics.Stopwatch.GetTimestamp();
        long nextFrameAt = 0;''')

patch("MirrorEngine.cs",
'''            window.PumpMessages();
            if (!window.Running || _stop) break;''',
'''            if (cfg.DebugLogging) DebugPulse("window message pump");
            window.PumpMessages();
            if (!window.Running || _stop) break;''')

patch("MirrorEngine.cs",
'''                    cfg.LowLatency = nc.LowLatency;''',
'''                    cfg.LowLatency = nc.LowLatency;
                    cfg.DebugLogging = nc.DebugLogging;
                    Interlocked.Exchange(ref _debugActive, cfg.DebugLogging ? 1 : 0);''')

patch("MirrorEngine.cs",
'''            bool hasNewFrame;
            try { hasNewFrame = capture.TryAcquire(context); }''',
'''            bool hasNewFrame;
            if (cfg.DebugLogging) DebugPulse("capture.TryAcquire");
            try { hasNewFrame = capture.TryAcquire(context); }''')

patch("MirrorEngine.cs",
'''            if (capture.Srv != null && (hasNewFrame || resized))
            {
                renderer.Render(capture, cfg);
                renderer.Present(cfg.Vsync);
                framesRendered++;''',
'''            if (hasNewFrame) debugNewFrames++;
            if (capture.Srv != null && (hasNewFrame || resized))
            {
                if (cfg.DebugLogging) DebugPulse("renderer.Render");
                renderer.Render(capture, cfg);
                if (cfg.DebugLogging) DebugPulse("renderer.Present");
                renderer.Present(cfg.Vsync);
                if (cfg.DebugLogging) DebugPulse("frame presented");
                framesRendered++;
                debugIntervalFrames++;''')

patch("MirrorEngine.cs",
'''            else
            {
                // WGC often has no new frame for an unchanged desktop. Do not
                // re-present the same texture in a tight CPU/GPU spin loop.
                Thread.Sleep(1);
            }
        }

        Log(sessionResult''',
'''            else
            {
                // WGC often has no new frame for an unchanged desktop. Do not
                // re-present the same texture in a tight CPU/GPU spin loop.
                Thread.Sleep(1);
            }

            // Low-rate frame diagnostics; no per-frame disk writes.
            if (cfg.DebugLogging)
            {
                DebugPulse("render loop running");
                long now = System.Diagnostics.Stopwatch.GetTimestamp();
                double secs = (now - debugIntervalStart) /
                    (double)System.Diagnostics.Stopwatch.Frequency;
                if (secs >= 2.0)
                {
                    Log($"[DEBUG] FPS={debugIntervalFrames / secs:F1}, " +
                        $"new capture frames={debugNewFrames / secs:F1}/s, " +
                        $"capture_size={capture.Width}x{capture.Height}, " +
                        $"preview_client={window.ClientWidth}x{window.ClientHeight}, " +
                        $"preview_maximized={window.IsMaximized}, " +
                        $"preview_minimized={window.IsMinimized}.");
                    debugIntervalStart = now;
                    debugIntervalFrames = 0;
                    debugNewFrames = 0;
                }
            }
        }
        Interlocked.Exchange(ref _debugActive, 0);

        Log(sessionResult''')

print("Added low-rate diagnostic metrics, source/preview recursion warning, independent stall watchdog and open-log control")
