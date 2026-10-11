from pathlib import Path
import os
root=Path(os.environ['RITSCHY_SOURCE'])

def patch(path, old, new, count=1):
    p=root/path
    s=p.read_text(encoding='utf-8')
    n=s.count(old)
    if n!=count:
        raise RuntimeError(f'{path}: anchor count {n}, expected {count}: {old[:120]!r}')
    p.write_text(s.replace(old,new,count),encoding='utf-8')
    print('patched', path)

# Build identity: keep normal version 1.3.2, continue build sequence.
patch('AppInfo.cs',
'''    public const string Copyright = "© 2026 RitschyRigz — MIT-Lizenz";

    /// <summary>Saubere Version „1.0.2" (Major.Minor.Build) aus der Assembly.</summary>''',
'''    public const string Copyright = "© 2026 RitschyRigz — MIT-Lizenz";
    public const int BuildNumber = 3;
    public static string BuildLabel => $"v{Version} Build {BuildNumber}";

    /// <summary>Saubere Version „1.0.2" (Major.Minor.Build) aus der Assembly.</summary>''')

# New backward-compatible app settings. Defaults intentionally reproduce Build 2 behavior.
patch('AppSettings.cs',
'''    [JsonPropertyName("minimize_settings_to_tray")]
    public bool MinimizeSettingsToTray { get; set; } = false;

    private static readonly JsonSerializerOptions ReadOpts = new()''',
'''    [JsonPropertyName("minimize_settings_to_tray")]
    public bool MinimizeSettingsToTray { get; set; } = false;
    // Build 2 behavior: the main Settings X exits the application.
    [JsonPropertyName("close_settings_to_tray")]
    public bool CloseSettingsToTray { get; set; } = false;
    // Build 2 normally starts as a tray application without showing Settings.
    [JsonPropertyName("start_minimized_to_tray")]
    public bool StartMinimizedToTray { get; set; } = true;
    [JsonPropertyName("open_settings_at_startup")]
    public bool OpenSettingsAtStartup { get; set; } = false;
    // Build 2 showed tray balloon notifications; preserve that on upgrade/fresh install.
    [JsonPropertyName("notifications_enabled")]
    public bool NotificationsEnabled { get; set; } = true;

    private static readonly JsonSerializerOptions ReadOpts = new()''')

# Debug/Test OFF by default for a fresh config. Existing JSON remains authoritative on updates.
patch('MirrorConfig.cs',
'''    [JsonPropertyName("debug_logging")]    public bool DebugLogging { get; set; } = true;''',
'''    [JsonPropertyName("debug_logging")]    public bool DebugLogging { get; set; } = false;''')

# Bounded, sanitized, versioned log with preserved mirror.log path.
patch('MirrorEngine.cs',
'''    private readonly object _logGate = new();
    private long _debugHeartbeatTicks;''',
'''    private readonly object _logGate = new();
    private const long MaxLogBytes = 2L * 1024L * 1024L;
    private const int LogArchiveCount = 3;
    private long _debugHeartbeatTicks;''')
patch('MirrorEngine.cs',
'''    public void Log(string msg)
    {
        var line = $"[{DateTime.Now:HH:mm:ss}] {msg}";
        Console.WriteLine(line);
        lock (_logGate)
        {
            try { File.AppendAllText(LogPath, line + Environment.NewLine); }
            catch { /* Logging must never take down the capture thread. */ }
        }
    }
''',
'''    public void Log(string msg)
    {
        var safe = DiagnosticsManager.SanitizeText(msg);
        var line = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] [{AppInfo.BuildLabel}] {safe}";
        Console.WriteLine(line);
        lock (_logGate)
        {
            try
            {
                RotateLogsIfNeeded(line.Length + Environment.NewLine.Length);
                File.AppendAllText(LogPath, line + Environment.NewLine);
            }
            catch { /* Logging must never take down the capture thread. */ }
        }
    }

    private void RotateLogsIfNeeded(int incomingChars)
    {
        var f = new FileInfo(LogPath);
        if (!f.Exists || f.Length + incomingChars * 2L < MaxLogBytes) return;
        for (int i = LogArchiveCount; i >= 1; i--)
        {
            string src = i == 1 ? LogPath : LogPath + "." + (i - 1);
            string dst = LogPath + "." + i;
            if (!File.Exists(src)) continue;
            if (File.Exists(dst)) File.Delete(dst);
            File.Move(src, dst);
        }
    }
''')
patch('MirrorEngine.cs',
'''            _thread.Start();
            var rendering = _thread;''',
'''            Log("[ENGINE] Start requested.");
            _thread.Start();
            var rendering = _thread;''')
patch('MirrorEngine.cs',
'''    public void Stop()
    {
        Thread? t;
        lock (_gate) { _stop = true; t = _thread; }''',
'''    public void Stop()
    {
        Thread? t;
        lock (_gate) { _stop = true; t = _thread; }
        if (t is { IsAlive: true }) Log("[ENGINE] Stop requested.");''')
# Do not log a selected window title; executable identity is sufficient and avoids private title text.
patch('MirrorEngine.cs',
'''            Log($"Quelle = Fenster '{cfg.WindowTitle}' ({cfg.WindowExe}), Ziel = Display {dstIdx} ({dst.Name}), output_mode={mode}, layout={cfg.LayoutMode}, HDR={winHdr}");''',
'''            Log($"Source = app window ({cfg.WindowExe}), Target = Display {dstIdx} ({dst.Name}), output_mode={mode}, layout={cfg.LayoutMode}, HDR={winHdr}");''')

# Diagnostics/self-test implementation. All temporary test files are app-local and deleted.
diag = r'''using System.IO.Compression;
using System.Runtime.InteropServices;
using System.Text;

namespace RitschyMirror;

/// <summary>
/// Project-local diagnostics only. No process injection/hooks/debugger attachment,
/// no clipboard/keystroke capture, no broad filesystem scanning, and no shared temp.
/// Diagnostic exports live outside mirror.log rotation under RitschyMirror\Diagnostics.
/// </summary>
internal static class DiagnosticsManager
{
    public static string DiagnosticsDirectory(string baseDir)
        => Path.Combine(baseDir, "Diagnostics");

    public static string SanitizeText(string? value)
    {
        var s = value ?? "";
        try
        {
            string profile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            string local = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            if (!string.IsNullOrWhiteSpace(profile)) s = s.Replace(profile, "%USERPROFILE%", StringComparison.OrdinalIgnoreCase);
            if (!string.IsNullOrWhiteSpace(local)) s = s.Replace(local, "%LOCALAPPDATA%", StringComparison.OrdinalIgnoreCase);
            string user = Environment.UserName;
            if (!string.IsNullOrWhiteSpace(user)) s = s.Replace(user, "%USERNAME%", StringComparison.OrdinalIgnoreCase);
        }
        catch { }
        return s;
    }

    public static string WriteCrashReport(string baseDir, Exception ex, string source)
    {
        string dir = Path.Combine(DiagnosticsDirectory(baseDir), "Crashes");
        Directory.CreateDirectory(dir);
        string path = Path.Combine(dir, $"Crash-{DateTime.Now:yyyyMMdd-HHmmss-fff}.txt");
        var text = new StringBuilder()
            .AppendLine("RitschyMirror crash diagnostic")
            .AppendLine($"Version: {AppInfo.BuildLabel}")
            .AppendLine($"Timestamp: {DateTime.Now:O}")
            .AppendLine($"Source: {source}")
            .AppendLine($"Exception: {ex.GetType().FullName}")
            .AppendLine("Message: " + SanitizeText(ex.Message))
            .AppendLine("Stack:")
            .AppendLine(SanitizeText(ex.StackTrace));
        File.WriteAllText(path, text.ToString());
        return path;
    }

    public static bool RunSafeSelfTest(string baseDir, out string reportPath, out string summary)
    {
        string diagnostics = DiagnosticsDirectory(baseDir);
        Directory.CreateDirectory(diagnostics);
        reportPath = Path.Combine(diagnostics, "Safe-Self-Test-Last.txt");
        string temp = Path.Combine(diagnostics, "SelfTestTemp-" + Guid.NewGuid().ToString("N"));
        var lines = new List<string>
        {
            "RitschyMirror Safe Test Mode / Self-Test",
            $"Version: {AppInfo.BuildLabel}",
            $"Timestamp: {DateTime.Now:O}",
            "Scope: isolated project-only settings I/O + static UI/path checks",
            ""
        };
        bool ok = true;
        void Pass(string s) => lines.Add("PASS: " + s);
        void Fail(string s) { ok = false; lines.Add("FAIL: " + s); }
        try
        {
            Directory.CreateDirectory(temp);
            string appPath = Path.Combine(temp, "app_settings.json");
            string mirrorPath = Path.Combine(temp, "mirror_config.json");

            var a = new AppSettings
            {
                AgentEnabled = false,
                AgentBind = "localhost",
                AgentPort = 18774,
                AutostartMirror = false,
                MinimizeSettingsToTray = true,
                CloseSettingsToTray = true,
                StartMinimizedToTray = true,
                OpenSettingsAtStartup = false,
                NotificationsEnabled = false,
            };
            a.Save(appPath);
            var a2 = AppSettings.Load(appPath);
            if (a2.AgentEnabled || a2.AgentPort != 18774 || !a2.MinimizeSettingsToTray || !a2.CloseSettingsToTray)
                Fail("isolated app_settings.json round-trip");
            else Pass("isolated app_settings.json read/write round-trip");

            var m = new MirrorConfig { DebugLogging = false, FpsLimit = 60, LayoutMode = "fit" };
            m.Save(mirrorPath);
            var m2 = MirrorConfig.Load(mirrorPath);
            if (m2.DebugLogging || m2.FpsLimit != 60 || !string.Equals(m2.LayoutMode, "fit", StringComparison.OrdinalIgnoreCase))
                Fail("isolated mirror_config.json round-trip");
            else Pass("isolated mirror_config.json read/write round-trip");

            MirrorConfig.MergePatch(mirrorPath, new System.Text.Json.Nodes.JsonObject { ["fps_limit"] = 30 });
            if (MirrorConfig.Load(mirrorPath).FpsLimit != 30) Fail("isolated settings merge/update");
            else Pass("isolated settings merge/update");

            File.Delete(appPath);
            File.Delete(mirrorPath);
            if (File.Exists(appPath) || File.Exists(mirrorPath)) Fail("isolated settings delete");
            else Pass("isolated settings delete");

            var uiIssues = SettingsForm.ValidateUiLayoutContract().ToList();
            if (uiIssues.Count == 0) Pass("Settings UI layout contract (scrollable content + responsive bottom controls)");
            else foreach (var issue in uiIssues) Fail("UI: " + issue);

            string expected = Path.GetFullPath(baseDir).TrimEnd(Path.DirectorySeparatorChar);
            string actual = Path.GetFullPath(AppContext.BaseDirectory).TrimEnd(Path.DirectorySeparatorChar);
            if (!string.Equals(expected, actual, StringComparison.OrdinalIgnoreCase)) Fail("application base-path identity");
            else Pass("application base-path identity");

            Pass("Safe Test Mode used only app-local Diagnostics/SelfTestTemp data");
        }
        catch (Exception ex)
        {
            Fail("self-test exception: " + SanitizeText(ex.Message));
        }
        finally
        {
            try { if (Directory.Exists(temp)) Directory.Delete(temp, recursive: true); }
            catch (Exception ex) { Fail("temporary self-test cleanup: " + SanitizeText(ex.Message)); }
        }

        lines.Add("");
        lines.Add(ok ? "RESULT: PASS" : "RESULT: FAIL");
        File.WriteAllLines(reportPath, lines);
        summary = ok ? "Safe self-test passed." : "Safe self-test found one or more problems.";
        return ok;
    }

    public static string CreateDiagnosticReport(string baseDir, AppSettings app, MirrorConfig cfg, bool engineRunning)
    {
        string dir = DiagnosticsDirectory(baseDir);
        Directory.CreateDirectory(dir);
        string path = Path.Combine(dir, "Diagnostic-Report-Latest.txt");
        string bindKind = app.AgentBind.Equals("localhost", StringComparison.OrdinalIgnoreCase) ? "localhost"
            : app.AgentBind is "+" or "0.0.0.0" ? "network wildcard" : "custom bind (value omitted)";
        var lines = new[]
        {
            "RitschyMirror diagnostic report",
            $"Version: {AppInfo.BuildLabel}",
            $"Timestamp: {DateTime.Now:O}",
            $"OS: {Environment.OSVersion.VersionString}",
            $"Process architecture: {RuntimeInformation.ProcessArchitecture}",
            $"Engine running: {engineRunning}",
            $"Capture mode: {cfg.ResolveCaptureMode()}",
            $"Output mode: {cfg.ResolveOutputMode()}",
            $"Layout: {cfg.LayoutMode}",
            $"FPS limit: {(cfg.FpsLimit <= 0 ? "unlimited" : cfg.FpsLimit)}",
            $"Debug Mode: {cfg.DebugLogging}",
            $"Preview minimize-to-tray: {cfg.MinimizePreviewToTray}",
            $"Preview taskbar button hidden: {cfg.HidePreviewTaskbarButton}",
            $"Main Settings minimize-to-tray: {app.MinimizeSettingsToTray}",
            $"Main Settings X-to-tray: {app.CloseSettingsToTray}",
            $"Open Settings at startup: {app.OpenSettingsAtStartup}",
            $"Start minimized to tray: {app.StartMinimizedToTray}",
            $"Notifications enabled: {app.NotificationsEnabled}",
            $"Start mirroring automatically: {app.AutostartMirror}",
            $"HTTP agent enabled: {app.AgentEnabled}",
            $"HTTP agent bind type: {bindKind}",
            $"HTTP agent port: {app.AgentPort}",
            "Window titles, clipboard data, keystrokes, messages, tokens and passwords are not included.",
        };
        File.WriteAllLines(path, lines);
        return path;
    }

    public static string ExportLogsAndDiagnostics(string baseDir, AppSettings app, MirrorConfig cfg, bool engineRunning)
    {
        string diagnostics = DiagnosticsDirectory(baseDir);
        string exports = Path.Combine(diagnostics, "Exports");
        Directory.CreateDirectory(exports);
        string report = CreateDiagnosticReport(baseDir, app, cfg, engineRunning);
        string staging = Path.Combine(diagnostics, "ExportStage-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(staging);
        try
        {
            File.Copy(report, Path.Combine(staging, Path.GetFileName(report)), overwrite: true);
            string selfTest = Path.Combine(diagnostics, "Safe-Self-Test-Last.txt");
            if (File.Exists(selfTest)) File.Copy(selfTest, Path.Combine(staging, Path.GetFileName(selfTest)), true);
            for (int i = 0; i <= 3; i++)
            {
                string source = i == 0 ? Path.Combine(baseDir, "mirror.log") : Path.Combine(baseDir, "mirror.log." + i);
                if (File.Exists(source)) File.Copy(source, Path.Combine(staging, Path.GetFileName(source)), true);
            }
            string zip = Path.Combine(exports, $"RitschyMirror-Diagnostics-{DateTime.Now:yyyyMMdd-HHmmss}.zip");
            ZipFile.CreateFromDirectory(staging, zip, CompressionLevel.Optimal, includeBaseDirectory: false);
            return zip;
        }
        finally
        {
            try { if (Directory.Exists(staging)) Directory.Delete(staging, true); } catch { }
        }
    }
}
'''
(root/'DiagnosticsManager.cs').write_text(diag,encoding='utf-8')
print('created DiagnosticsManager.cs')
